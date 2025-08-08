from PySide6 import QtCore, QtWidgets, QtGui
import matplotlib as mpl
import numpy as np

class TracesDialog(QtWidgets.QDialog):
    def __init__(self, current_sets=dict(), sec=None, parent=None):
        # Initial widget setup functions
        super().__init__(parent)
        self.setWindowTitle('Color')
        self.trace_options = dict()
        self.sec = sec

        self._setup_ui(current_sets)

        
    def _setup_ui(self, current_sets):
        layout = QtWidgets.QVBoxLayout(self)

        # The settings available for change in the traces dialog
        self.settings = {
            'linewidth': QtWidgets.QLineEdit(),
        }

        self.string_input = []
        self.float_input = ['linewidth']
        self.combo_input = []

        trace_layout = self._setup_trace_options()
        color_scheme_layout = self._setup_color_scheme_options()

        # Ok button
        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok
        )
        self.accepted.connect(self.update_settings)
        button_box.accepted.connect(self.accept)

        # Adding all the elements to the main layout
        layout.addLayout(trace_layout)
        layout.addLayout(color_scheme_layout)
        layout.addWidget(button_box)

        self.apply_current_settings(current_sets)


    def _setup_trace_options(self):
        trace_layout = QtWidgets.QVBoxLayout()
        trace_layout.addWidget(
            QtWidgets.QLabel('<b>Trace Options</b>')
        )
        trace_mini_layout = QtWidgets.QHBoxLayout()
        trace_mini_layout.addWidget(QtWidgets.QLabel('Linewidth:'))
        trace_mini_layout.addWidget(self.settings['linewidth'])
        trace_mini_layout.setContentsMargins(20, 5, 5, 5)
        trace_layout.addLayout(trace_mini_layout)
        
        return trace_layout


    def _setup_color_scheme_options(self):
        color_scheme_layout = QtWidgets.QVBoxLayout()
        color_scheme_layout.addWidget(
            QtWidgets.QLabel('<b>Color Scheme Options</b>')
        )
        color_scheme_mini_layout = QtWidgets.QHBoxLayout()
        color_scheme_mini_layout.addWidget(QtWidgets.QLabel('Scheme:'))
        self.scheme = QtWidgets.QComboBox()
        self.scheme.addItems(
            ('Current', 'Viridis', 'Plasma', 'Inferno', 'Magma',
             'Cividis')
        )
        color_scheme_mini_layout.addWidget(self.scheme)
        color_scheme_mini_layout.setContentsMargins(20, 5, 5, 5)
        color_scheme_layout.addLayout(color_scheme_mini_layout)
        
        return color_scheme_layout
        
        
    @QtCore.Slot()
    def reset_to_default(self):
        self.trace_options = {
            'linewidth' : 1.5,
        }
        self.apply_current_settings(self.trace_options)
        return self.trace_options
    
        
    @QtCore.Slot()
    def update_settings(self):
        for key in self.settings.keys():
            if key in self.string_input:
                temp = self.settings[key].text()
                self.trace_options[key] = temp
            if key in self.float_input:
                temp = self.settings[key].text()
                self.trace_options[key] = float(temp)
            if key in self.combo_input:
                temp = self.settings[key].currentText().lower()
                self.trace_options[key] = temp

        cmap = self.scheme.currentText().lower()
        if cmap != 'current':
            points = np.linspace(0, 1.0, len(self.sec))
            self.sec.colors = [
                mpl.colors.to_hex(mpl.colormaps[cmap](point)) for
                point in points
            ]
                

    def apply_current_settings(self, current_sets):
        for key in current_sets.keys():
            if key in self.string_input:
                self.settings[key].setText(current_sets[key])
            if key in self.float_input:
                self.settings[key].setText(str(current_sets[key]))
            if key in self.combo_input:
                self.settings[key].setCurrentText(current_sets[key].capitalize())
                
