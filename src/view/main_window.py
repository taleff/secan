from PySide6 import QtCore, QtWidgets, QtGui
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure
from functools import partial

from analysis.sec import SEC
from dialogs.axes_dialog import AxesDialog
from dialogs.export_dialog import ExportDialog
from dialogs.traces_dialog import TracesDialog
from tabs.graph_tab import GraphTab
from tabs.calibration_tab import CalibrationTab
from tabs.peak_tab import PeakTab
from tabs.block_copolymer_tab import BlockCopolymerTab
from tabs.deconvolution_tab import DeconvolutionTab


class Secan(QtWidgets.QMainWindow):
    def __init__(self):
        # Creating and setting up the user interface
        super().__init__()
        self.setWindowTitle('SEC Analysis')
        self._setup_ui()
        self._create_menu_bar()
        self.sec = None

        # Restoring previous user settings
        self.read_settings()
        self.change_x_axis_title()
        

    def _setup_ui(self):
        secan_widget = QtWidgets.QWidget()
        self.setCentralWidget(secan_widget)
        layout = QtWidgets.QHBoxLayout(secan_widget)

        # Create main components
        self._create_graph_components()
        self._create_control_tabs()
        self._create_buttons()
        
        # Organize layout
        self._organize_layout(layout)

        
    def _create_graph_components(self): 
        # Chart on which the SEC traces will be displayed
        self.fig = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.fig)

        # Fields to input the upper and lower bounds to be graphed
        self.chart_bounds_edit = {
            'lower': QtWidgets.QLineEdit(),
            'upper': QtWidgets.QLineEdit()
        }

        # A checkbox to determine whether the graph should use
        # retention time or molecular weight
        self.mol_weight_check = QtWidgets.QCheckBox("MW")
        self.mol_weight_check.stateChanged.connect(
            self.change_x_axis_title
        )

    def _create_control_tabs(self):
        # Creating tabs for the user to interact with; the three
        # tabs are the basic graphs setting tab called "general",
        # a tab containing parameters for whatever anaylsis is
        # being performed called "analysis", and a tab where
        # calibration parameters can be input called "calibration"
        self.tab_widget = QtWidgets.QTabWidget()
        self.TAB_INDICES = {
            'graph': 0,
            'analysis': 1,
            'calibration': 2
        }
        self.tab_widget.addTab(GraphTab(), 'Graph')
        self.tab_widget.addTab(PeakTab(), 'Analysis')
        self.tab_widget.addTab(CalibrationTab(), 'Calibration')

        self.tab_widget.currentChanged.connect(
            lambda i: self._update_analysis_tab_selection()
        )
        
        
    def _create_buttons(self):
        # Button to import the SEC file to be analyzed. Currently this
        # must be a text or csv file with the same format as that
        # retrieved from the Tosoh EcoSEC software
        self.import_button = QtWidgets.QPushButton("Add Data")
        self.import_button.clicked.connect(self.import_sec_file)

        # Button that generates the graph
        self.generate_button = QtWidgets.QPushButton("Generate Graph")
        self.generate_button.clicked.connect(self.generate_chart)
        
        
    def _organize_layout(self, layout):
        # This subpart is the bar that will appear below the
        # graphing window
        bottom_bar_layout = QtWidgets.QHBoxLayout()
        bottom_bar_layout.addWidget(QtWidgets.QLabel('Lower Bound:'))
        bottom_bar_layout.addWidget(self.chart_bounds_edit['lower'])
        bottom_bar_layout.addWidget(QtWidgets.QLabel('Upper Bound:'))
        bottom_bar_layout.addWidget(self.chart_bounds_edit['upper'])
        bottom_bar_layout.addWidget(self.mol_weight_check)

        # This subpart is the box that will hold the graphed data
        graph_box_layout = QtWidgets.QVBoxLayout()
        graph_box_layout.addWidget(self.canvas)
        graph_box_layout.addLayout(bottom_bar_layout)

        # Generating the layout
        graph_toolbox_layout = QtWidgets.QVBoxLayout()
        graph_toolbox_layout.addWidget(self.tab_widget)
        graph_toolbox_layout.addWidget(self.import_button)
        graph_toolbox_layout.addWidget(self.generate_button)
        layout.addLayout(graph_box_layout, stretch=3)
        layout.addLayout(graph_toolbox_layout, stretch=1)
        

    def _create_menu_bar(self):
        # Creating the initial graph menu
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)
        
        self._create_graph_menu(menu_bar)
        self._create_analysis_menu(menu_bar)
        

    def _create_graph_menu(self, menu_bar):
        # Populating a menu with items related to visual settings for
        # the graph
        graph_menu = menu_bar.addMenu('Graph')
        menu_items = [
            ('Axes', 'axes'),
            ('Traces', 'traces'),
            ('Export', 'export')
        ]
        for title, key in menu_items:
            action = graph_menu.addAction(title)
            action.triggered.connect(
                partial(self.open_graph_menu_item, key)
            )

    def _create_analysis_menu(self, menu_bar):
        # Populating a menu with items related to different possible
        # analysis methods to display in the analysis tab
        analysis_menu = menu_bar.addMenu('Analysis')
        menu_items = [
            ('Peak', 'peak'),
            ('Block Copolymer', 'block'),
            ('Deconvolution', 'deconvolution')
        ]
        for title, key in menu_items:
            action = analysis_menu.addAction(title)
            action.triggered.connect(
                partial(self.change_analysis_tab, key)
            )
        
    @QtCore.Slot()
    def import_sec_file(self):
       filename, _ = QtWidgets.QFileDialog.getOpenFileName(
           self, "Open Data File", "~/", "Text Files (*.txt *.csv)"
       )

       # Does nothing if the user does not select a file
       if not filename:
           return None

       try:
           # If data has already been imported, then importing more
           # data should add to the list of traces that can be graphed
           # or analyzed
           if self.sec is None:
               self.sec = SEC(filename)
           else:
               self.sec.append(SEC(filename))
               
           self._update_ui_after_import()

       except Exception as e:
            QtWidgets.QMessageBox.critical(
                self, "Import Error", f"Failed to import file: {str(e)}"
            )

            
    def _update_ui_after_import(self):
        graph_tab = self.tab_widget.widget(
            self.TAB_INDICES['graph']
        )
        graph_tab.add_data(self.sec)
        
        self._update_analysis_tab_selection()


    @QtCore.Slot()
    def _update_analysis_tab_selection(self):
        analysis_tab = self.tab_widget.widget(
            self.TAB_INDICES['analysis']
        )
        
        analysis_tab.update_selection(self.sec)

        
    @QtCore.Slot()
    def open_graph_menu_item(self, menu_item):
        dialog_map = {
            'axes': lambda: AxesDialog(self.axes_options),
            'traces': lambda: TracesDialog(self.trace_options, self.sec),
            'export': lambda: ExportDialog(self.fig)
        }

        dialog = dialog_map[menu_item]()
        
        if dialog.exec_():
            if menu_item == 'axes':
                self.axes_options.update(dialog.axes_options)
            if menu_item == 'traces':
                self.trace_options.update(dialog.trace_options)
                graph_tab = self.tab_widget.widget(
                    self.TAB_INDICES['graph']
                )
                graph_tab.update_colors(self.sec)
                

                
    @QtCore.Slot()
    def change_analysis_tab(self, new_tab):
        # The analysis tab is located at index 1
        analysis_tab_index = self.TAB_INDICES['analysis']
        current_tab = self.tab_widget.currentIndex()

        # The options within in the analysis menu change the identity
        # of the analysis tab to whichever analysis is desired to be
        # used
        tab_type = {
            'peak': PeakTab,
            'block': BlockCopolymerTab,
            'deconvolution': DeconvolutionTab
        }
        
        self.tab_widget.insertTab(
            analysis_tab_index, tab_type[new_tab](), 'Analysis'
        )
        self.tab_widget.removeTab(analysis_tab_index+1)

        # Changing the current tab to whatever it was when the user
        # accessed the window to prevent any jarring changes
        self.tab_widget.setCurrentIndex(current_tab)
        self.tab_widget.widget(analysis_tab_index).update_selection(self.sec)
        
        
    @QtCore.Slot()
    def change_x_axis_title(self):
        if self.mol_weight_check.isChecked():
            self.axes_options['x axis title'] = 'Molecular Weight (g/mol)'
        else:
            self.axes_options['x axis title'] = 'Retention Time (min)'


    def _get_chart_bounds(self, use_mw):
        methods = {
            True : self.sec.get_weight_position,
            False : self.sec.get_time_position
        }
        
        try:
            lower_val = float(self.chart_bounds_edit['lower'].text())
            lbound = methods[use_mw](lower_val)
        except ValueError:
            lbound = -1 if use_mw else 0

        try:
            upper_val = float(self.chart_bounds_edit['upper'].text())
            rbound = methods[use_mw](upper_val)
        except ValueError:
            rbound = 0 if use_mw else -1

        if use_mw:
            lbound, rbound = rbound, lbound
            
        return lbound, rbound


    def _setup_x_axis(self):
        use_mw = self.mol_weight_check.isChecked()
        lbound, rbound = self._get_chart_bounds(use_mw)

        if use_mw:
            self._ax.set_xscale('log')
            independent_variable = self.sec.mol_weights
            self._ax.set_xlim(
                self.sec.mol_weights[rbound],
                self.sec.mol_weights[lbound]
            )
            
            return independent_variable, lbound, rbound, 'mw'
        
        else:
            independent_variable = self.sec.retention_times
            self._ax.set_xlim(
                self.sec.retention_times[lbound],
                self.sec.retention_times[rbound]
            )
            
            return independent_variable, lbound, rbound, 'rt'


    def _apply_axes_formatting(self):
        for spine in self._ax.spines.values():
            spine.set_linewidth(self.axes_options['axes linewidth'])

        self._ax.tick_params(
            which='major',
            length=self.axes_options['tick length'],
            width=self.axes_options['tick width'],
            direction=self.axes_options['tick style'],
            labelsize=self.axes_options['tick labelsize']
        )
        self._ax.tick_params(
            which='minor',
            length=self.axes_options['minor tick length'],
            width=self.axes_options['minor tick width'],
            direction=self.axes_options['minor tick style']
        )

        # Set axis labels
        self._ax.set_xlabel(
            self.axes_options['x axis title'],
            fontsize=self.axes_options['x axis fontsize']
        )
        self._ax.set_ylabel(
            self.axes_options['y axis title'],
            fontsize=self.axes_options['y axis fontsize']
        )
        
        # Set y-axis limits
        self._ax.set_ylim(
            self.axes_options['y axis min'],
            self.axes_options['y axis max']
        )


    def _plot_traces(self, independent_variable, trace_visibility):
        for i in range(len(self.sec)):
            if trace_visibility[i]:
                self._ax.plot(
                    independent_variable,
                    self.sec.edited_traces[:, i],
                    color=self.sec.colors[i],
                    label=self.sec.names[i],
                    linewidth=self.trace_options['linewidth']
                )

            
    @QtCore.Slot()
    def generate_chart(self):
        # Checking to make sure a data file has been loaded
        if self.sec is None:
            QtWidgets.QMessageBox.warning(
                self, "No Data", "Please load data before generating chart"
            )
            return None
        
        if True:
            self.sec.reset_traces()
            self.fig.clf()
            self.fig.set_canvas(self.canvas)
            self._ax = self.canvas.figure.add_subplot()

            try:
                calibration_params = self.tab_widget.widget(
                    self.TAB_INDICES['calibration']
                ).update_calibration()
                self.sec.add_calibration(*calibration_params)
            
            except Exception as e:
                pass

            graph_tab = self.tab_widget.widget(
                self.TAB_INDICES['graph']
            )
            general_parameters = graph_tab.update_chart_options()
            ind_var, lbound, rbound, x_type = self._setup_x_axis()

            self.sec.adjust_baseline(general_parameters['baseline'])
            self.sec.peak_normalize(
                general_parameters['normalization'], lbound, rbound,
                x_type
            )

            self._plot_traces(
                ind_var, general_parameters['traces']
            )
            self._apply_axes_formatting()

            analysis_tab = self.tab_widget.widget(
                self.TAB_INDICES['analysis']
            )
            analysis_tab.update_analysis(self.sec)
            if analysis_tab.show_check.isChecked():
                analysis_tab.add_graph(self._ax, self.sec)

            if general_parameters['legend']:
                leg = self._ax.legend(loc=general_parameters['legend loc'])
                leg.get_frame().set_linewidth(0.0)

            self.fig.tight_layout()
            self.canvas.draw()

        """
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self, "Chart Generation Error", f"Failed to generate chart: {str(e)}"
            )
        """

    def _get_settings_object(self):
        return QtCore.QSettings('Taleff', 'Secan')
    

    def write_settings(self):
        # Creating a settings object
        settings = self._get_settings_object()
        
        # Saving all of the axes options used to generate the graph
        settings.beginGroup('Axes')
        for key, value in self.axes_options.items():
            settings.setValue(key, value)
        settings.endGroup()

        # Saving all of the trace options used to generate the graph
        settings.beginGroup('Trace')
        for key, value in self.trace_options.items():
            settings.setValue(key, value)
        settings.endGroup()

        # Saving the current calibration values
        settings.beginGroup('Calibration')
        calibration_tab = self.tab_widget.widget(
            self.TAB_INDICES['calibration']
        )
        calib_vals = list(calibration_tab.calib_parameters.values())   
        if not None in calib_vals:
            calib_type = calibration_tab.calib_type.lower()
            settings.setValue('values', calib_vals)
            settings.setValue('type', calib_type)
        settings.endGroup()
        

    def read_settings(self, default=False):
        # Creating a settings object
        settings = self._get_settings_object()

        test = QtWidgets.QMessageBox.information(
            self, 'Settings Location', settings.fileName()
        )
        
        # Reading all of the axes options used to generate the graph
        settings.beginGroup('Axes')
        self.axes_options = AxesDialog().reset_to_default() 
        for setting in self.axes_options.keys():
            value = settings.value(setting)
            if value is not None:
                self.axes_options[setting] = value  
        settings.endGroup()

        # Reading all of the trace options used to generate the graph
        settings.beginGroup('Trace')
        self.trace_options = TracesDialog().reset_to_default() 
        for setting in self.trace_options.keys():
            value = settings.value(setting)
            if value is not None:
                self.trace_options[setting] = value
        settings.endGroup()

        # Reading the saved calibration values
        settings.beginGroup('Calibration')
        calib_style = settings.value('type')
        if calib_style is not None:
            calib_vals = settings.value('values', [], type=list)
            calibration_tab = self.tab_widget.widget(
                self.TAB_INDICES['calibration']
            )
            calibration_tab.set_calibration(calib_style, calib_vals)
        settings.endGroup()
        

    def closeEvent(self, event):
        self.write_settings()
        event.accept()

