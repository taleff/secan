from tabs.analysis_tab import AnalysisTab
from PySide6 import QtCore, QtWidgets, QtGui

class DeconvolutionTab(AnalysisTab):
    def __init__(self, parent=None):
        # Initial dialog box setup functions
        super().__init__(parent)

        self.bounds = {'Lower Bound': QtWidgets.QLineEdit(),
                       'Upper Bound': QtWidgets.QLineEdit()}

        bounds_layout = QtWidgets.QVBoxLayout()
        for bound in self.bounds.keys():
            bound_line = QtWidgets.QHBoxLayout()
            bound_line.addWidget(QtWidgets.QLabel(bound))
            bound_line.addWidget(self.bounds[bound])
            bound_line.addWidget(QtWidgets.QLabel('g/mol'))
            bounds_layout.addLayout(bound_line)

        self.peak_number = QtWidgets.QLineEdit()
        peak_number_layout = QtWidgets.QHBoxLayout()
        peak_number_layout.addWidget(
            QtWidgets.QLabel('Number of Peaks:')
        )
        peak_number_layout.addWidget(self.peak_number)

        self.peak_list = QtWidgets.QListWidget()

        self.layout.addWidget(self.selection)
        self.layout.addLayout(bounds_layout)
        self.layout.addLayout(peak_number_layout)
        self.layout.addWidget(self.show_check)
        self.layout.addWidget(self.peak_list)

        
    def update_analysis(self, sec_object):
        peaks = int(self.peak_number.text())
        lbound = float(self.bounds['Lower Bound'].text())
        rbound = float(self.bounds['Upper Bound'].text())
        
        self.results = sec_object.deconvolute(
            peaks, 0, lbound, rbound
        )
        
        # Adding the information for each of the peaks to the peak
        # list widget
        self.peak_list.clear()
        for i in range(len(self.results['mns'])):
            peak_widget = QtWidgets.QWidget()
            peak_layout = QtWidgets.QGridLayout(peak_widget)
            peak_layout.setContentsMargins(20, 0, 40, 20)
            
            peak_layout.addWidget(
                QtWidgets.QLabel('Peak {}'.format(i+1)), 0, 0
            )
            
            lab_str = 'M<sub>n</sub> (g/mol):'
            res_str = '{}'.format(float('{:.2g}'.format(self.results['mns'][i])))
            peak_layout.addWidget(QtWidgets.QLabel(lab_str), 0, 1)
            peak_layout.addWidget(QtWidgets.QLabel(res_str), 0, 2)
            
            lab_str = 'M<sub>w</sub> (g/mol):'
            res_str = '{}'.format(float('{:.2g}'.format(self.results['mws'][i])))
            peak_layout.addWidget(QtWidgets.QLabel(lab_str), 1, 1)
            peak_layout.addWidget(QtWidgets.QLabel(res_str), 1, 2)
            
            lab_str = '\u0110:'
            res_str = '{}'.format(float('{:.3g}'.format(self.results['disp'][i])))
            peak_layout.addWidget(QtWidgets.QLabel(lab_str), 2, 1)
            peak_layout.addWidget(QtWidgets.QLabel(res_str), 2, 2)
            
            lab_str = 'Area (%):'
            res_str = '{}'.format(float('{:.3g}'.format(self.results['areas'][i])))
            peak_layout.addWidget(QtWidgets.QLabel(lab_str), 3, 1)
            peak_layout.addWidget(QtWidgets.QLabel(res_str), 3, 2)
            
            list_item = QtWidgets.QListWidgetItem()
            list_item.setSizeHint(peak_widget.sizeHint())
            
            self.peak_list.addItem(list_item)
            self.peak_list.setItemWidget(list_item, peak_widget)

    def add_graph(self, ax_object, sec_object):
        for i in range(len(self.results['mns'])):
            ax_object.plot(self.results['x'], self.results['peaks'][:, i])

