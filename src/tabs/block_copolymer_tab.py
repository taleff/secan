from PySide6 import QtCore, QtWidgets, QtGui

class BlockCopolymerTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        # Initial dialog box setup functions
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)

        self.bounds = {'Lower Bound 1:': QtWidgets.QLineEdit(),
                       'Upper Bound 1:': QtWidgets.QLineEdit(),
                       'Lower Bound 2:': QtWidgets.QLineEdit(),
                       'Upper Bound 2:': QtWidgets.QLineEdit()}

        self.indices = {'Solvent RI:': QtWidgets.QLineEdit(),
                        'Monomer 1 RI:': QtWidgets.QLineEdit(),
                        'Monomer 2 RI:': QtWidgets.QLineEdit()}

        bounds_layout = QtWidgets.QVBoxLayout()
        for bound in self.bounds.keys():
            bound_line = QtWidgets.QHBoxLayout()
            bound_line.addWidget(QtWidgets.QLabel(bound))
            bound_line.addWidget(self.bounds[bound])
            bound_line.addWidget(QtWidgets.QLabel('g/mol'))
            bounds_layout.addLayout(bound_line)

        indices_layout = QtWidgets.QVBoxLayout()
        for index in self.indices:
            index_line = QtWidgets.QHBoxLayout()
            index_line.addWidget(QtWidgets.QLabel(index))
            index_line.addWidget(self.indices[index])
            indices_layout.addLayout(index_line)
            
        layout.addLayout(bounds_layout)
        layout.addLayout(indices_layout)
        
