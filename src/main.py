import sys
from PySide6 import QtWidgets
from view.main_window import Secan
from dialogs.error_log_dialog import UncaughtHook


def main():
    # Create QApplication instance
    app = QtWidgets.QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Secan")
    app.setApplicationVersion('0.1')
    app.setOrganizationName('Taleff')
    
    # Create and show main window
    window = Secan()
    window.resize(1000, 600)
    window.show()

    # Starting a global instance of the error message box
    qt_exception_hook = UncaughtHook()
    
    # Start the event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
    
