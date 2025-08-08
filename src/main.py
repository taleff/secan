import sys
from PySide6 import QtWidgets
from view.main_window import Secan


def main():
    # Create QApplication instance
    app = QtWidgets.QApplication([])
    
    # Set application properties
    app.setApplicationName("Secan")
    app.setApplicationVersion('0.1')
    app.setOrganizationName('Taleff')
    
    # Create and show main window
    window = Secan()
    window.resize(1000, 600)
    window.show()
    
    # Start the event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
    
