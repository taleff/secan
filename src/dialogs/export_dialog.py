from PySide6 import QtCore, QtWidgets, QtGui

class ExportDialog(QtWidgets.QDialog):
    def __init__(self, figure, parent=None):
        # Initial widget setup functions
        super().__init__(parent)
        self.setWindowTitle('Export Chart')
        self.figure = figure

        self._setup_ui()
        

    def _setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        # Button to choose filename
        save_button = QtWidgets.QPushButton('Choose file...')
        save_button.clicked.connect(self.get_save_name)
        button_area = QtWidgets.QHBoxLayout()
        button_area.addWidget(save_button)
        self.file_label = QtWidgets.QLabel('')
        button_area.addWidget(self.file_label)

        # Ok button
        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok
        )
        self.accepted.connect(self.save_file)
        button_box.accepted.connect(self.accept)

        # Adding all the elements to the main layout
        layout.addLayout(button_area)
        layout.addWidget(button_box)
        

    @QtCore.Slot()
    def get_save_name(self):
        file_filters = "PNG Image (*.png);;SVG Vector (*.svg);;All Files (*)"
        
        # Open file dialog
        filename, selected_filter = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Export Chart', 'sec', file_filters
        )

        self.file_label.setText(filename)
        self.filename = filename
        

    def save_file(self):
        self.figure.savefig(self.filename)
        
