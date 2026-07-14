import asyncio
import socket
import orjson
import threading
from typing import Optional, Callable
from models import Device, DeviceStatus
from .logger import Logger
from .config_manager import ConfigManager


class NetworkManager:
    def __init__(self, device: Device, message_callback: Optional[Callable] = None):
        self.device = device
        self.logger = Logger()
        self.config = ConfigManager()
        self.reader: Optional[asyncio.StreamReader] = None
        self.writer: Optional[asyncio.StreamWriter] = None
        self.message_callback = message_callback
        self._running = False
        self._heartbeat_task: Optional[asyncio.Task] = None
        self._reconnect_attempts = 0
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread: Optional[threading.Thread] = None

    def start(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run_event_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._loop and self._loop.is_running():
            asyncio.run_coroutine_threadsafe(self._cleanup(), self._loop)

    def _run_event_loop(self):
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self._connect_loop())

    async def _connect_loop(self):
        while self._running:
            try:
                self.device.status = DeviceStatus.CONNECTING
                self.logger.info(f"Connecting to {self.device.name} at {self.device.ip}:{self.device.port}")
                reader, writer = await asyncio.open_connection(self.device.ip, self.device.port)
                self.reader = reader
                self.writer = writer
                self.device.status = DeviceStatus.CONNECTED
                self._reconnect_attempts = 0
                self.logger.info(f"Connected to {self.device.name}")
                self._heartbeat_task = asyncio.create_task(self._heartbeat())
                await self._listen()
            except Exception as e:
                self.logger.error(f"Connection error with {self.device.name}: {e}")
                self.device.status = DeviceStatus.ERROR if self._reconnect_attempts >= self.config.settings.reconnect_attempts else DeviceStatus.RECONNECTING
                if self._running and self._reconnect_attempts < self.config.settings.reconnect_attempts:
                    self._reconnect_attempts += 1
                    self.logger.info(f"Reconnecting to {self.device.name} (attempt {self._reconnect_attempts}/{self.config.settings.reconnect_attempts}) in {self.config.settings.reconnect_delay}s")
                    await asyncio.sleep(self.config.settings.reconnect_delay)
                else:
                    self.device.status = DeviceStatus.DISCONNECTED
                    break
        await self._cleanup()

    async def _listen(self):
        try:
            while self._running:
                data = await self.reader.read(4096)
                if not data:
                    break
                try:
                    parsed_data = orjson.loads(data)
                    self.device.add_console_message(f"[RECV] {parsed_data}")
                    if self.message_callback:
                        self.message_callback(self.device, parsed_data)
                except Exception as e:
                    self.logger.error(f"Failed to parse message from {self.device.name}: {e}")
        except Exception as e:
            self.logger.error(f"Listen error from {self.device.name}: {e}")

    async def _heartbeat(self):
        while self._running and self.writer and not self.writer.is_closing():
            try:
                await self.send_message({"type": "ping"})
                await asyncio.sleep(self.config.settings.heartbeat_interval)
            except Exception as e:
                self.logger.error(f"Heartbeat error for {self.device.name}: {e}")
                break

    async def send_message(self, message: dict):
        if self.writer and not self.writer.is_closing():
            try:
                data = orjson.dumps(message)
                self.writer.write(data)
                await self.writer.drain()
                self.device.add_console_message(f"[SEND] {message}")
            except Exception as e:
                self.logger.error(f"Failed to send message to {self.device.name}: {e}")

    def send_message_sync(self, message: dict):
        if self._loop and self._loop.is_running():
            asyncio.run_coroutine_threadsafe(self.send_message(message), self._loop)

    async def _cleanup(self):
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
            try:
                await self._heartbeat_task
            except asyncio.CancelledError:
                pass
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
            self.writer = None
            self.reader = None
        self.device.status = DeviceStatus.DISCONNECTED
        self._running = False
