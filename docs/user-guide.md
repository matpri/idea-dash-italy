# Functionality

- **Load Data:** Use the "Load Data" option to either upload data from your local machine or select data from our
  results database.
- **Add Windows:** Add windows to the workspace using the "+" button in the toolbar on the left side of the screen.
- **Select Plots:** Choose the plots you want to see and adjust the content using their designated widgets.
- **Resize, Move, and Close Windows:** Arrange your workspace to compare and review your data.
- **Clear Workspace:** Use the trash bin button in the toolbar to clear your workspace.
- **Edit Plots:** Use the settings button in the toolbar to customize colors for technologies, titles, and axis labels.
- **Edit Loaded Data:** Use the last button in the toolbar to change the scenario name and the visualizations that
  should be created.



## Data Loading

### Preload Data
By placing model outputs csv in the `data` folder the data will be loaded automatically when the app is started.

### Load Data
To load data, click the "Load Data" button in the header. Either Load Data from your local machine or from the IDEA database.
![Opening Data Loading Window](https://gitlab.com/sesit/idea-dash/-/raw/master/assets/help/data_modal.gif)

### Local Files
To load data from your local machine, click the "Local File" button. You can either click on the field or drag your files onto the upload area. At the moment IDEA supports COPPER results in PYAM format using our pyam conversion script.
![Loading Local Data](https://gitlab.com/sesit/idea-dash/-/raw/master/assets/help/data_local.gif)

### Database
To load data from the IDEA database, click the "Database" button. Enter your API key and click "Connect". IDEA is connecting to our results Database, which might take some time to load. Once the data is loaded, you can select the runs you want to use and click "Load". You can also filter the runs by the model, scenario or author.
![Loading Data from Database](https://gitlab.com/sesit/idea-dash/-/raw/master/assets/help/data_db.gif)

### Editing Data
Once the data is loaded, you can edit the plots that should be generated and change the scenario name. Click the "Submit" button to finalize your selection. This will process the data and load them into the system.
![Editing Data](https://gitlab.com/sesit/idea-dash/-/raw/master/assets/help/data_edit.gif)
![Submitting Data](https://gitlab.com/sesit/idea-dash/-/raw/master/assets/help/data_submit.gif)

Before submitting the data, the user can edit the scenario name and select the plots that should be generated. To do so click on the filename in the list of files and a window will open where the user can change the scenario name and select the plots that should be generated.
![Editing Data](https://gitlab.com/sesit/idea-dash/-/raw/master/assets/help/data_edit.gif)

## Plot Customization

### Change Plots
Every window has a tab bar at the top. The tab bar is nested and contains tabs for every model type available in the data and for every model type, there are tabs for every plot option available. To change the plot, click on the tab of the model type you want to change, then click on the tab of the plot option you want to change. The plot will update accordingly.
![Changing Plots](https://gitlab.com/sesit/idea-dash/-/raw/master/assets/help/plot_change.gif)

### Interacting with Plots
Every plot has widgets to its left that allow you to change the plot by adjusting predefined parameters that include, but are not limited to, the scenario, period, region, and plot type. Changing these parameters will update the plot accordingly.
![Interacting with Plots](https://gitlab.com/sesit/idea-dash/-/raw/master/assets/help/plot_widgets.gif)

### Save Plots
To save a plot, click the "Save" button in the top right corner of the plot window. The plot will be saved as a PNG file.
![Saving Plots](https://gitlab.com/sesit/idea-dash/-/raw/master/assets/help/plot_save.gif)

### Change View
To have a clean interface where only the plot is visible, hide the widgets by clicking the hamburger menu in the top left corner of the window and press the "^" button to hide the tab bar. To show the widgets or tabs again, click the hamburger menu or the "v" button accordingly.
![Changing View](https://gitlab.com/sesit/idea-dash/-/raw/master/assets/help/plot_hide.gif)

## Managing Windows

### Add Windows
To add a window, click the "+" button in the toolbar on the left side of the screen.
![Adding Windows](https://gitlab.com/sesit/idea-dash/-/raw/master/assets/help/windows_add.gif)

### Clear Windows
To clear the workspace, click the "trash bin" in the toolbar and confirm.
![Clearing Windows](https://gitlab.com/sesit/idea-dash/-/raw/master/assets/help/windows_clear.gif)

### Interact with Windows
- To move a window, click and drag the title bar of the window.
- To resize a window, click and drag one of the edges of the window.
![Interacting with Windows](https://gitlab.com/sesit/idea-dash/-/raw/master/assets/help/windows_move.gif)

## Settings

### Model Settings
To change the settings of a plot, click the "Settings" button in the toolbar on the left. The settings window will open. Each model has custom settings that can be changed.
![Opening Settings](https://gitlab.com/sesit/idea-dash/-/raw/master/assets/help/open_settings.gif)

For example for COPPER the user can change the colors of the technologies.
![Changing Model Settings](https://gitlab.com/sesit/idea-dash/-/raw/master/assets/help/tech_settings.gif)
Or, change the title of the plots.
![Changing Plot Settings](https://gitlab.com/sesit/idea-dash/-/raw/master/assets/help/plot_settings.gif)

![Submitting Settings](https://gitlab.com/sesit/idea-dash/-/raw/master/assets/help/submit_settings.gif)

### Submitting Settings
To submit the settings, click the "Submit" button in the settings window. The settings will be saved and the plots will be updated accordingly.

## Generic Plots
If the data does not fit any of the predefined profiles, the platform will generate a set of generic plots. For each reporting variable a tab will be created with the following plots:
- Stacked Bar plot of the variable over time
- Stacked Bar Plot of the variable by region
- Line Plot of the variable over time by sub-variables
- Pie Chart of the variable by region

Additionally, an Overview tab will be created that colates data for each of the reporting variables and displays them in a line plot, showing either the sum over all regions, or if 'CAN' or 'National' is found in the region column the subset for that region will be shown.

These plots are only available when the data is formatted as IAMC format.


## Comparison Plots
In addition to showcasing the data per model there are 2 additional tabs available for comparison plots. First, the Power Systems tab colates data from models that are part of the Power Systems profile (\<LIST of MODELS\>), this tab has Power System specific plots showcasing the results from different models similar to scenarios. Second, a Generic Comparisson tab colates data from all models and showcases generic plots based on the naming of variables, if two or more models have the same variable name the plots will showcase the results from those models in one plot.