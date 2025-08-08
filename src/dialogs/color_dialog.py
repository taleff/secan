from PySide6 import QtCore, QtWidgets, QtGui

class ColorDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        # Initial widget setup functions
        super().__init__(parent)
        self.setWindowTitle('Color')
        layout = QtWidgets.QVBoxLayout(self)

        # Setting the colors
        self.color = '#000000'

        # Box containing the color being used
        self.colored_box = QtWidgets.QLabel()
        self.colored_box.setFixedSize(100, 100)
        self.colored_box.setStyleSheet(
            "background-color: #000000; border: 1px solid black;"
        )

        # Sliders for inputting RGB values
        rgb_code_layout = QtWidgets.QVBoxLayout()
        self.color_names = ['red', 'green', 'blue']
        self.color_sliders = dict()
        self.color_edits = dict()
        rgb_layouts = dict()
        for color_name in self.color_names:
            self.color_sliders[color_name] = QtWidgets.QSlider(
                QtCore.Qt.Orientation.Horizontal
            )
            self.color_sliders[color_name].setMinimum(0)
            self.color_sliders[color_name].setMaximum(255)
            
            self.color_edits[color_name] = QtWidgets.QLineEdit()
            self.color_edits[color_name].setText('0')
            
            rgb_layouts[color_name] = QtWidgets.QHBoxLayout()
            rgb_layouts[color_name].addWidget(
                QtWidgets.QLabel(color_name.title()), stretch=1
            )
            rgb_layouts[color_name].addWidget(
                self.color_sliders[color_name], stretch=3
            )
            rgb_layouts[color_name].addWidget(
                self.color_edits[color_name], stretch=1
            )
            rgb_code_layout.addLayout(rgb_layouts[color_name])

        for color_name in self.color_names:
            self.color_sliders[color_name].sliderMoved.connect(
                self.update_color_edit
            )
            self.color_edits[color_name].returnPressed.connect(
                self.update_color_slider
            )

        # Line edit for inputting the hex code
        hex_code_layout = QtWidgets.QHBoxLayout()
        self.hex_code_edit = QtWidgets.QLineEdit()
        self.hex_code_edit.returnPressed.connect(self.update_hex_code)
        hex_code_layout.addWidget(QtWidgets.QLabel('Hex Code:'))
        hex_code_layout.addStretch()
        hex_code_layout.addWidget(QtWidgets.QLabel('#'))
        hex_code_layout.addWidget(self.hex_code_edit)

        # Ok button
        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok
        )
        button_box.accepted.connect(self.accept)

        # Adding all the elements to the main layout
        layout.addWidget(self.colored_box)
        layout.addLayout(rgb_code_layout)
        layout.addLayout(hex_code_layout)
        layout.addWidget(button_box)
        

    @QtCore.Slot()
    def update_hex_code(self):
        self.color = '#{}'.format(self.hex_code_edit.text())
        self.update_colored_box()
        

    @QtCore.Slot()
    def update_color_edit(self):
        for color_name in self.color_names:
            self.color_edits[color_name].setText(
                '{}'.format(self.color_sliders[color_name].sliderPosition())
            )
        self.update_rgb_code()
        self.update_colored_box()
        

    @QtCore.Slot()
    def update_color_slider(self):
        for color_name in self.color_names:
            self.color_sliders[color_name].setSliderPosition(
                int(self.color_edits[color_name].text())
            )
        self.update_rgb_code()
        self.update_colored_box()
        

    @QtCore.Slot()
    def update_rgb_code(self):
        color_vals = []
        for color_name in self.color_names:
            color_vals.append(
                format(int(self.color_edits[color_name].text()), 'x').zfill(2)
            )
        self.color = '#{}{}{}'.format(*color_vals)
        

    def update_colored_box(self):
        self.colored_box.setStyleSheet(
            f'background-color: {self.color}; border: 1px solid black;'
        )
        
