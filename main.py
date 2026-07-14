import sys
import traceback
from gui.main_window import MainWindow
from core import Logger


def main():
    logger = Logger()
    try:
        app = MainWindow()
        app.protocol("WM_DELETE_WINDOW", app.on_closing)
        app.mainloop()
    except Exception as e:
        logger.critical(f"Fatal error: {e}\n{traceback.format_exc()}")
        sys.exit(1)


if __name__ == "__main__":
    main()
