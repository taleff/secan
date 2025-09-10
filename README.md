# Secan (SEC Analysis)
Secan is a desktop program for analyzing SEC data. It is essentially a GUI wrapper for matplotlib graphing of SEC traces. It also provides a variety of analyses for SEC, including peak deconvolution and dispersity calculations.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

## Usage

### Data Input
To add data to Secan, select the 'Add Data' button located in the bottom right of the application. A file explorer dialog box will appear in order to select the desired SEC data for analysis. This data must be stored as a .txt or .csv. Currently, data exported from the following systems are supported:
* Tosoh EcoSEC
  * Header: two lines
  * Data: alternating retention time and intensity
  * Footer: none
  
In order to successfully import the data, the data file must not be modified in any way. When the data is successfully imported, a line corresponding to each trace will appear in the 'Graph' tab. Subsequent imports will append new data to the existing list of traces.

### Displaying Data
To display the data, press the 'Generate Graph' button in the bottom right. Secan does not update the graph as parameters are changed so the 'Generate Graph' button must be pressed every time a change needs to be implemented. To save the graph, select the 'Export' item in the 'Graph' dropdown menu. The bounds of the graph can be changed as well as whether the x-axis represents retention time or molecular weight.

### Tabs
The application data analysis functions are organized into three tabs: 'Graph', 'Analysis', and 'Calibration'. Each tab controls a different aspect of the SEC traces.

#### Graph
The 'Graph' tab controls high level analysis and display of the imported SEC traces. 

The baseline correction dropdown allows the user to select what baseline correction method to apply to the traces. All baseline correction methods are from the [pybaselines](https://pybaselines.readthedocs.io/en/latest/index.html) library. From my empirical experience, the provided baseline corrections work across the widest variety of SEC traces.
* None: This doesn't apply any baseline correction. It is useful for traces that don't require any baseline correction and as a control to ensure the other baseline correction methods provide sensical results.
* LOESS: This uses the locally estimated scatterplot smoothing baseline fitting routine.
* Standard Dev.: This uses the standard deviation distribution baseline fitting routine. It uses the standard deviation to identify which parts of the trace are part of the baseline.

The normalization dropdown changes the normalization method applied to the traces.
* Individual: Normalizes the highest point within the range window of each trace to one.
* Global: Normbalizes the highest point within the range window among all the traces to one. All the other traces are scaled such that the ratio of intensities between all traces matches the raw data.
* Point: Normalizes all the traces to the same value at the specified time/molecular weight. The highest global point is then normalized to one.

The legend sections provides a checkbox to determine whether a legend is shown. Additionally, a dropbox specifying the legend location is also provided.

The trace list displays all of the traces loaded into Secan. Each trace has an editable name (which is shown in the legend), a box displaying the current color, and a checkbox confirming whether the trace should be displayed. Clicking the color box opens a color dialog where the trace's color may be set.

#### Analysis
The 'Analysis' tab provides an interface through which the SEC traces may be analyzed. The analysis tab may be changed by selecting the desired analysis from the analysis dropdown menu. Each analysis variety provides a box listing the traces from which the desired trace for analysis is selected. Additionally, the analysis can be displayed by selecting the 'Show' checkbox. Any numerical results associated with the analysis are displayed within the analysis box.

#### Calibration
The 'Calibration' tab provides an input location for calibration data. To change the type of calibration curve used, select the appropriate variety from the dropdown box. Ensure that the calibration from matches the displayed equation. The calibration parameters can then be filled out. The calibration tab must be completed before any analysis functions are available or the traces can be displayed with a molecular weigh axis.

### Options
Secan provides a number of options for changing the way the graph is displayed. These may be accessed in the 'Graph' dropdown menu. These settings are saved.

## License
Licensed under the GNU GPLv3: https://www.gnu.org/licenses/gpl-3.0.html
