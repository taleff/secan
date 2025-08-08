from PySide6 import QtCore, QtWidgets, QtGui

class CalibrationTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        # Initial dialog box setup functions
        super().__init__(parent)
        self.setWindowTitle("Calibration")
        layout = QtWidgets.QVBoxLayout(self)
        self.calib_parameters = dict()
        self.calib_type = None
        self.line_edits = dict()
        
        # A form containing the various calibration curve inputs
        self.calib_input_form = QtWidgets.QFormLayout()

        # The possible calibration curve options along with the
        # parameters they require
        self.calib_options = {'Linear' : ['a', 'b'],
                              'Cubic' : ['a', 'b', 'c', 'd']}

        self.calib_eqns = {
            'Linear' : 'log<sub>10</sub>(MW) = at+b',
            'Cubic' : 'log<sub>10</sub>(MW) = at<sup>3</sup>+bt<sup>2</sup>+ct+d'
        }

        # Equation to display to make the parameters more sensical
        self.calib_eqn_label = QtWidgets.QLabel()

        # Button to select the type of calibration curve data that is
        # being inputted
        self.select_calib_method_combo = QtWidgets.QComboBox()
        self.select_calib_method_combo.addItems(
            self.calib_options.keys()
        )
        self.select_calib_method_combo.currentTextChanged.connect(self.combo_changed)

        # Updating the form to have the initial value
        self.combo_changed(self.select_calib_method_combo.currentText())

        # Adding all the buttons to the dialog box
        combo_box = QtWidgets.QHBoxLayout()
        combo_box.addWidget(QtWidgets.QLabel('Fitting Type:'))
        combo_box.addWidget(self.select_calib_method_combo)
        combo_box.setContentsMargins(40, 0, 40, 0)
        layout.addLayout(combo_box)
        layout.addWidget(self.calib_eqn_label)
        self.calib_eqn_label.setContentsMargins(0, 10, 0, 30)
        layout.addLayout(self.calib_input_form)
        layout.addStretch()

    @QtCore.Slot()
    def combo_changed(self, text):
        # Determine number of fields needed
        entries = self.calib_options[text]

        # Recording what the calibration type is
        self.calib_type = self.select_calib_method_combo.currentText()

        # Changing which calibration equation is displayed
        self.calib_eqn_label.setText(self.calib_eqns[text])
        self.calib_eqn_label.setAlignment(QtCore.Qt.AlignHCenter)

        # Changing the parameter dictionary to one compatible with
        # whatever calibration curve is being used
        self.calib_parameters = dict([(entry, None) for entry in
                                      entries])
        
        # Clear existing widgets
        self.clear_line_edits()
        
        # Create new widgets
        for i in range(len(entries)):
            self.line_edits[entries[i]] = QtWidgets.QLineEdit()
            # Add to layout and store reference
            self.calib_input_form.addRow(
                self.tr(entries[i]), self.line_edits[entries[i]]
            )

    @QtCore.Slot()
    def clear_line_edits(self):
        # Delete every row within the form when the type of
        # calibration curve is changed
        for i in range(self.calib_input_form.rowCount()):
            self.calib_input_form.removeRow(0)
        self.line_edits = dict()

    @QtCore.Slot()
    def update_calibration(self):
        for constant in self.calib_options[self.calib_type]:
            constant_val = float(self.line_edits[constant].text())
            self.calib_parameters[constant] = constant_val
        return self.calib_parameters, self.calib_type.lower()

    @QtCore.Slot()
    def set_calibration(self, c_type, vals):
        entries = self.calib_options[c_type.capitalize()]
        self.select_calib_method_combo.setCurrentText(c_type.capitalize())
        for i in range(len(entries)):
            self.line_edits[entries[i]].setText(str(vals[i]))
                    
