import dash_mantine_components as dmc
from dash import html


def render():
    print('rendering start')
    layout = html.Div([
        dmc.Text('Features', size='xl', weight=500),
        dmc.List([
            dmc.ListItem(
                'Using the Load Data option, either upload data from your local machine or select data from our results Database.'),
            dmc.ListItem(
                'Add windows to the workspace using the \'+\' button in the toolbar on the left side of the screen.'),
            dmc.ListItem(
                'Select the plots you want to see and adjust the content using their designated widgets.'),
            dmc.ListItem(
                'Resize, move, and close windows as needed. To create the dashboard view you prefer to compare and review your data'),
            dmc.ListItem('Clear your workspace using the trash bin button in the toolbar'),
            dmc.ListItem(
                'Edit Plots using the settings button in the toolbar. This allows you to edit colors for technologies and titles and axes labels.'),
            dmc.ListItem(
                'Edit your loaded data, using the last button in the toolbar. Change the scenario name to be displayed and the visualizations that should be created.'),
        ]),
    ],
    )
    return layout
