from tabs.analysis_tab import AnalysisTab
from PySide6 import QtCore, QtWidgets, QtGui

class PeakTab(AnalysisTab):
    def __init__(self, parent=None):
        # Initial widget setup functions
        super().__init__(parent)

        # A form containing the bounds for the molecular weight
        # analysis
        self.bound_input_form = QtWidgets.QFormLayout()

        self.lower_mw_bound_edit = QtWidgets.QLineEdit()
        self.bound_input_form.addRow(
                self.tr('Lower Bound'), self.lower_mw_bound_edit
            )
        self.upper_mw_bound_edit = QtWidgets.QLineEdit()
        self.bound_input_form.addRow(
                self.tr('Upper Bound'), self.upper_mw_bound_edit
            )

        # A checkbox to determine whether the analysis should cut or
        # drop down to zero
        self.cut_check = QtWidgets.QCheckBox('Cut')

        # Results labels
        self.results = {
            'mn' : QtWidgets.QLabel(),
            'mw' : QtWidgets.QLabel(),
            'disp' : QtWidgets.QLabel(),
            'area' : QtWidgets.QLabel()
        }

        result_labels = {
            'mn' : QtWidgets.QLabel('M<sub>n</sub> (g/mol):'),
            'mw' : QtWidgets.QLabel('M<sub>w</sub> (g/mol):'),
            'disp' : QtWidgets.QLabel('\u0110:'),
            'area' : QtWidgets.QLabel('Area (g/mol):')
        }

        results_layout = QtWidgets.QGridLayout()
        for i, key in enumerate(self.results.keys()):
            results_layout.addWidget(
                result_labels[key], i, 0
            )
            result_labels[key].setAlignment(QtCore.Qt.AlignRight)
            results_layout.addWidget(self.results[key], i, 1)
                
        # Managing the layout
        checkmark_box = QtWidgets.QHBoxLayout()
        checkmark_box.addWidget(self.cut_check)
        checkmark_box.addWidget(self.show_check)

        self.layout.addWidget(self.selection)
        self.layout.addLayout(self.bound_input_form)
        self.layout.addLayout(checkmark_box)
        self.layout.addLayout(results_layout)
        

    def update_analysis(self, sec_object):
        try:
            self.params['lbound'] = float(self.lower_mw_bound_edit.text())
            self.params['rbound'] = float(self.upper_mw_bound_edit.text())
            self.params['cut'] = self.cut_check.isChecked()
            self.params['show'] = self.show_check.isChecked()

            self.params['trace'] = self.selection.currentRow()
            
            results = sec_object.peak_calculator(
                self.params['lbound'], self.params['rbound'],
                self.params['cut'], self.params['trace']
            )
            
            area = sec_object.area_calculator(
                self.params['lbound'], self.params['rbound'],
                self.params['cut'], self.params['trace']
            )

            results.append(area)

            for i, value in enumerate(self.results.values()):
                value.setText('{}'.format(float('{:.3g}'.format(results[i]))))
                    
        except ValueError:
            return False
        

    def add_graph(self, ax_object, sec_object):
        # Graphing the bounds of the peak to display them visually
        point1 = sec_object.edited_traces[
            sec_object.get_weight_position(self.params['rbound']),
            self.params['trace']
        ]
        point2 = sec_object.edited_traces[
            sec_object.get_weight_position(self.params['lbound']),
            self.params['trace']
        ]

        if self.cut_check.isChecked():
            ax_object.plot(
                (self.params['rbound'], self.params['lbound']),
                (point1, point2), 'k-'
            )
        else:
            ax_object.hlines(0, self.params['rbound'],
                             self.params['lbound'], 'k')
            ax_object.vlines(self.params['rbound'], 0, point1, 'k')
            ax_object.vlines(self.params['lbound'], 0, point2, 'k')
            
        ax_object.plot(
            (self.params['rbound'], self.params['lbound']),
            (point1, point2), 'k.'
        )
    
