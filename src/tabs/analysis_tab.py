from PySide6 import QtCore, QtWidgets, QtGui

class AnalysisTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        # Initial widget setup functions
        super().__init__(parent)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.params = dict()
        self.selection = QtWidgets.QListWidget()
        self.show_check = QtWidgets.QCheckBox('Show')
        

    def update_selection_list(self, select_list, sec_object):
        select_list.clear()
        select_list.setSelectionMode(
            QtWidgets.QListWidget.SingleSelection
        )
        
        for i in range(len(sec_object)):
            item_widget = QtWidgets.QLabel(sec_object.names[i])
            list_item = QtWidgets.QListWidgetItem()
            list_item.setSizeHint(item_widget.sizeHint())
        
            select_list.addItem(list_item)
            select_list.setItemWidget(list_item, item_widget)
            
        select_list.setCurrentRow(0)
        

    def update_selection(self, sec_object):
        if sec_object is not None:
            self.update_selection_list(self.selection, sec_object)

    
    def update_analysis(self, sec_object):
        pass

    
    def add_graph(self, ax_object, sec_object):
        pass
    
