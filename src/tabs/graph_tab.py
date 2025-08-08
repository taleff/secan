from PySide6 import QtCore, QtWidgets, QtGui
from functools import partial

from dialogs.color_dialog import ColorDialog

class GraphTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        # Initial widget setup functions
        super().__init__(parent)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.parameters = {'baseline': None,
                           'normalization': None}

        # Combo for selecting the method used to adjust the baseline
        self.select_baseline_combo = QtWidgets.QComboBox()
        self.baseline_options = {'None' : 'none',
                                 'LOESS' : 'loess',
                                 'Standard Dev.' : 'stdev'}
        self.select_baseline_combo.addItems(
            self.baseline_options.keys()
        )
        
        # Combo for selecting the method by which the traces are
        # normalized
        self.select_normalization_combo = QtWidgets.QComboBox()
        self.normalization_options = {'Individual' : 'individual',
                                      'Global' : 'global',
                                      'Point' : 'point'}
        self.select_normalization_combo.addItems(
            self.normalization_options.keys()
        )
        self.normalization_edit = QtWidgets.QLineEdit()
        self.select_normalization_combo.currentIndexChanged.connect(
            self.update_point_normalization_edit
        )
        self.update_point_normalization_edit()

        # Determines whether the legend is shown and in which position
        self.legend_check = QtWidgets.QCheckBox()
        self.legend_check.stateChanged.connect(
            self.update_legend_check
        )
        self.update_legend_check()
        self.select_legend_combo = QtWidgets.QComboBox()
        self.select_legend_combo.addItems(
            ['Upper Left', 'Upper Right']
        )
        self.select_legend_combo.currentIndexChanged.connect(
            self.update_select_legend_combo
        )
        self.update_select_legend_combo()

        # Widget that lists all of the traces currently loaded
        self.trace_list = QtWidgets.QListWidget()

        baseline_box = QtWidgets.QHBoxLayout()
        baseline_box.addWidget(QtWidgets.QLabel('Baseline Correction:'))
        baseline_box.addWidget(self.select_baseline_combo)
        self.layout.addLayout(baseline_box)
        normalization_box = QtWidgets.QHBoxLayout()
        normalization_box.addWidget(QtWidgets.QLabel('Normalization:'))
        normalization_box.addWidget(self.select_normalization_combo)
        normalization_box.addWidget(self.normalization_edit)
        self.layout.addLayout(normalization_box)
        legend_box = QtWidgets.QHBoxLayout()
        legend_box.addWidget(QtWidgets.QLabel('Legend:'))
        legend_box.addWidget(self.legend_check)
        legend_box.addWidget(self.select_legend_combo)
        self.layout.addLayout(legend_box)
        self.layout.addWidget(self.trace_list)

        
    def update_chart_options(self):
        # Returns the parameters of the general dialog tab so that
        # the data can be properly graphed
        b_val = self.baseline_options[self.select_baseline_combo.currentText()]
        self.parameters['baseline'] = b_val
        if self.select_normalization_combo.currentText() == 'Point':
            n_val = self.normalization_edit.text()
        else:
            n_val = self.normalization_options[self.select_normalization_combo.currentText()]
        self.parameters['normalization'] = n_val
        traces = [self.trace_boxes[i].isChecked() for i in
                  range(len(self.trace_boxes))]
        self.parameters['traces'] = traces
        return self.parameters

    
    def add_data(self, sec):
        # Adds the sec data as a variable in order to accurately
        # display the list of traces
        self.trace_list.clear()
        self.trace_edits = []
        self.trace_buttons = []
        self.trace_boxes = []
        for i in range(len(sec)):
            trace_widget = QtWidgets.QWidget()
            trace_layout = QtWidgets.QHBoxLayout(trace_widget)
            trace_layout.setContentsMargins(20, 0, 40, 0)
            self.trace_edits.append(
                QtWidgets.QLineEdit(sec.names[i])
            )
            self.trace_edits[i].textEdited.connect(
                partial(self.update_trace_name, sec, int(i))
            )
            self.trace_buttons.append(QtWidgets.QPushButton())
            self.trace_buttons[i].setStyleSheet(
                'background-color: {}'.format(sec.colors[i])
            )
            self.trace_buttons[i].setFixedSize(20, 20)
            self.trace_buttons[i].clicked.connect(
                partial(self.open_color_dialog, sec, int(i))
            )
            self.trace_boxes.append(QtWidgets.QCheckBox())
            trace_layout.addWidget(self.trace_edits[i])

            trace_layout.addStretch()
            trace_layout.addWidget(self.trace_buttons[i])
            trace_layout.addWidget(self.trace_boxes[i])
            self.trace_boxes[i].setCheckState(QtCore.Qt.Checked)

            list_item = QtWidgets.QListWidgetItem()
            list_item.setSizeHint(trace_widget.sizeHint())
            
            self.trace_list.addItem(list_item)
            self.trace_list.setItemWidget(list_item, trace_widget)


    def update_colors(self, sec):
        for i in range(len(sec)):
            self.trace_buttons[i].setStyleSheet(
                'background-color: {}'.format(sec.colors[i])
            )
            

    @QtCore.Slot()
    def open_color_dialog(self, sec, i):
        color = ColorDialog()
        if color.exec_():
            sec.colors[i] = color.color
            self.trace_buttons[i].setStyleSheet(
                'background-color: {}'.format(sec.colors[i])
            )
            
            
    @QtCore.Slot()
    def update_point_normalization_edit(self):
        if self.select_normalization_combo.currentText() == 'Point':
            self.normalization_edit.setReadOnly(False)
        else:
            self.normalization_edit.setReadOnly(True)
            

    @QtCore.Slot()
    def update_trace_name(self, sec, i, new_name):
        sec.names[i] = new_name

        
    @QtCore.Slot()
    def update_legend_check(self):
        self.parameters['legend'] = self.legend_check.isChecked()

        
    @QtCore.Slot()
    def update_select_legend_combo(self):
        self.parameters['legend loc'] = self.select_legend_combo.currentText().lower()

