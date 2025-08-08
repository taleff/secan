from PySide6 import QtCore, QtWidgets, QtGui

class AxesDialog(QtWidgets.QDialog):
    def __init__(self, current_sets=dict(), parent=None):
        # Initial widget setup functions
        super().__init__(parent)
        self.setWindowTitle('Axes Options')
        self.axes_options = dict()

        self._setup_ui(current_sets)


    def _setup_ui(self, current_sets):
        layout = QtWidgets.QVBoxLayout(self)

        # The settings available for change in the axes dialog
        self.settings = {
            'axes linewidth': QtWidgets.QLineEdit(),
            'x axis title' : QtWidgets.QLineEdit(),
            'x axis fontsize' : QtWidgets.QLineEdit(),
            'y axis title' : QtWidgets.QLineEdit(),
            'y axis fontsize' : QtWidgets.QLineEdit(),
            'y axis min' : QtWidgets.QLineEdit(),
            'y axis max' : QtWidgets.QLineEdit(),
            'tick width' : QtWidgets.QLineEdit(),
            'tick length' : QtWidgets.QLineEdit(),
            'tick style' : QtWidgets.QComboBox(),
            'tick labelsize' : QtWidgets.QLineEdit(),
            'minor tick width' : QtWidgets.QLineEdit(),
            'minor tick length' : QtWidgets.QLineEdit(),
            'minor tick style' : QtWidgets.QComboBox(),
        }

        self.settings['tick style'].addItems(['In', 'Out', 'Inout'])
        self.settings['minor tick style'].addItems(['In', 'Out', 'Inout'])

        self.string_input = ['x axis title', 'y axis title']
        self.float_input = ['y axis min', 'y axis max', 'tick width',
                            'tick length', 'minor tick width',
                            'minor tick length', 'x axis fontsize',
                            'y axis fontsize', 'tick labelsize',
                            'axes linewidth']
        self.combo_input = ['tick style', 'minor tick style']

        axis_layout = self._setup_axes_options()
        x_axis_layout = self._setup_x_axis_options()
        y_axis_layout = self._setup_y_axis_options()
        major_tick_layout = self._setup_major_tick_options()
        minor_tick_layout = self._setup_minor_tick_options()

        # Default button to reset to settings to default
        default_button = QtWidgets.QPushButton('Reset')
        default_button.clicked.connect(self.reset_to_default)
        default_button_layout = QtWidgets.QHBoxLayout()
        default_button_layout.addStretch()
        default_button_layout.addWidget(default_button)
        default_button_layout.addStretch()
        
        # Ok button
        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok
        )
        self.accepted.connect(self.update_settings)
        button_box.accepted.connect(self.accept)

        # Adding all the elements to the main layout
        layout.addLayout(axis_layout)
        layout.addLayout(x_axis_layout)
        layout.addLayout(y_axis_layout)
        layout.addLayout(major_tick_layout)
        layout.addLayout(minor_tick_layout)
        layout.addLayout(default_button_layout)
        layout.addWidget(button_box)

        # Inputting initial settings
        self.apply_current_settings(current_sets)


    def _setup_axes_options(self):
        # Axis Options Layout
        axis_layout = QtWidgets.QVBoxLayout()
        axis_layout.addWidget(
            QtWidgets.QLabel('<b>Axes Options</b>')
        )
        axis_mini_layout = QtWidgets.QHBoxLayout()
        axis_mini_layout.addWidget(QtWidgets.QLabel('Linewidth:'))
        axis_mini_layout.addWidget(self.settings['axes linewidth'])
        axis_mini_layout.setContentsMargins(20, 5, 5, 5)
        axis_layout.addLayout(axis_mini_layout)

        return axis_layout


    def _setup_x_axis_options(self):
        # X-Axis Options Layout
        x_axis_layout = QtWidgets.QVBoxLayout()
        x_axis_layout.addWidget(
            QtWidgets.QLabel('<b>X Axis Options</b>')
        )
        x_axis_mini_layout = QtWidgets.QHBoxLayout()
        x_axis_mini_layout.addWidget(QtWidgets.QLabel('Title:'))
        x_axis_mini_layout.addWidget(self.settings['x axis title'])
        x_axis_mini_layout.setContentsMargins(20, 5, 5, 5)
        x_axis_layout.addLayout(x_axis_mini_layout)
        
        x_axis_size_layout = QtWidgets.QHBoxLayout()
        x_axis_size_layout.addWidget(QtWidgets.QLabel('Fontsize:'))
        x_axis_size_layout.addWidget(self.settings['x axis fontsize'])
        x_axis_size_layout.setContentsMargins(20, 5, 5, 5)
        x_axis_layout.addLayout(x_axis_size_layout)
        
        return x_axis_layout


    def _setup_y_axis_options(self):
        # Y-Axis Options Layout
        y_axis_layout = QtWidgets.QVBoxLayout()
        y_axis_layout.addWidget(
            QtWidgets.QLabel('<b>Y Axis Options</b>')
        )
        y_axis_title_layout = QtWidgets.QHBoxLayout()
        y_axis_title_layout.addWidget(QtWidgets.QLabel('Title:'))
        y_axis_title_layout.addWidget(self.settings['y axis title'])
        y_axis_title_layout.setContentsMargins(20, 5, 5, 5)
        y_axis_layout.addLayout(y_axis_title_layout)
        
        y_axis_size_layout = QtWidgets.QHBoxLayout()
        y_axis_size_layout.addWidget(QtWidgets.QLabel('Fontsize:'))
        y_axis_size_layout.addWidget(self.settings['y axis fontsize'])
        y_axis_size_layout.setContentsMargins(20, 5, 5, 5)
        y_axis_layout.addLayout(y_axis_size_layout)
        
        y_axis_bounds_layout = QtWidgets.QHBoxLayout()
        y_axis_bounds_layout.addWidget(QtWidgets.QLabel('Min:'))
        y_axis_bounds_layout.addWidget(self.settings['y axis min'])
        y_axis_bounds_layout.addWidget(QtWidgets.QLabel('Max:'))
        y_axis_bounds_layout.addWidget(self.settings['y axis max'])
        y_axis_bounds_layout.setContentsMargins(20, 5, 5, 5)
        y_axis_layout.addLayout(y_axis_bounds_layout)

        return y_axis_layout


    def _setup_major_tick_options(self):
        # Major Tick Settings Layout
        major_tick_layout = QtWidgets.QVBoxLayout()
        major_tick_layout.addWidget(
            QtWidgets.QLabel('<b>Major Tick Options</b>')
        )
        major_tick_param_layout = QtWidgets.QHBoxLayout()
        major_tick_param_layout.addWidget(QtWidgets.QLabel('Width:'))
        major_tick_param_layout.addWidget(self.settings['tick width'])
        major_tick_param_layout.addWidget(QtWidgets.QLabel('Length:'))
        major_tick_param_layout.addWidget(self.settings['tick length'])
        major_tick_param_layout.setContentsMargins(20, 5, 5, 5)
        major_tick_layout.addLayout(major_tick_param_layout)
        
        major_tick_combo_layout = QtWidgets.QHBoxLayout()
        major_tick_combo_layout.addWidget(QtWidgets.QLabel('Style:'))
        major_tick_combo_layout.addWidget(self.settings['tick style'])
        major_tick_combo_layout.addStretch()
        major_tick_combo_layout.setContentsMargins(20, 5, 5, 5)
        major_tick_layout.addLayout(major_tick_combo_layout)
        
        major_tick_label_layout = QtWidgets.QHBoxLayout()
        major_tick_label_layout.addWidget(QtWidgets.QLabel('Labelsize:'))
        major_tick_label_layout.addWidget(self.settings['tick labelsize'])
        major_tick_label_layout.setContentsMargins(20, 5, 5, 5)
        major_tick_layout.addLayout(major_tick_label_layout)

        return major_tick_layout

    
    def _setup_minor_tick_options(self):
        # Minor Tick Settings Layout
        minor_tick_layout = QtWidgets.QVBoxLayout()
        minor_tick_layout.addWidget(
            QtWidgets.QLabel('<b>Minor Tick Options</b>')
        )
        minor_tick_param_layout = QtWidgets.QHBoxLayout()
        minor_tick_param_layout.addWidget(QtWidgets.QLabel('Width:'))
        minor_tick_param_layout.addWidget(self.settings['minor tick width'])
        minor_tick_param_layout.addWidget(QtWidgets.QLabel('Length:'))
        minor_tick_param_layout.addWidget(self.settings['minor tick length'])
        minor_tick_param_layout.setContentsMargins(20, 5, 5, 5)
        minor_tick_layout.addLayout(minor_tick_param_layout)
        
        minor_tick_combo_layout = QtWidgets.QHBoxLayout()
        minor_tick_combo_layout.addWidget(QtWidgets.QLabel('Style:'))
        minor_tick_combo_layout.addWidget(self.settings['minor tick style'])
        minor_tick_combo_layout.addStretch()
        minor_tick_combo_layout.setContentsMargins(20, 5, 5, 5)
        minor_tick_layout.addLayout(minor_tick_combo_layout)
        
        return minor_tick_layout
        

    @QtCore.Slot()
    def reset_to_default(self):
        self.axes_options = {
            'axes linewidth' : 1.5,
            'x axis title': 'Retention Time (min)',
            'x axis fontsize' : 16,
            'y axis title': 'Intensity',
            'y axis fontsize' : 16,
            'y axis min': -0.1,
            'y axis max': 1.1,
            'tick width': 1.5,
            'tick length': 8,
            'tick style': 'out',
            'tick labelsize': 15,
            'minor tick width': 1.0,
            'minor tick length': 6,
            'minor tick style': 'out'
        }
        self.apply_current_settings(self.axes_options)
        return self.axes_options
    
        
    @QtCore.Slot()
    def update_settings(self):
        for key in self.settings.keys():
            if key in self.string_input:
                temp = self.settings[key].text()
                self.axes_options[key] = temp
            if key in self.float_input:
                temp = self.settings[key].text()
                self.axes_options[key] = float(temp)
            if key in self.combo_input:
                temp = self.settings[key].currentText().lower()
                self.axes_options[key] = temp
                

    def apply_current_settings(self, current_sets):
        for key in current_sets.keys():
            if key in self.string_input:
                self.settings[key].setText(current_sets[key])
            if key in self.float_input:
                self.settings[key].setText(str(current_sets[key]))
            if key in self.combo_input:
                self.settings[key].setCurrentText(current_sets[key].capitalize())
        
