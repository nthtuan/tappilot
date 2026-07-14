# TapPilot

TapPilot is a desktop application for managing jailbroken iOS devices, with Lua script support.

## Features

- Manage multiple iOS devices
- WebSocket communication with iOS agents
- Lua script execution
- Dark mode support
- Device reconnect and heartbeat
- Import/export devices
- And more!

## Installation

### Desktop (Windows/macOS/Linux)

1. Install Python 3.12 or later
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python main.py
   ```

### iOS Agent

1. Install Theos
2. Build the package:
   ```bash
   cd agent
   make clean package
   ```
3. Install the .deb file on your jailbroken iOS device

## License

MIT License
