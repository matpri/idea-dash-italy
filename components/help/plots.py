import dash_mantine_components as dmc
from dash import html


def render():
    print('rendering start')
    layout = html.Div([
        dmc.Text('Change plots', size='xl', weight=500),
        dmc.Text('Every window has a tab bar at the top. The tab bar is nested and contains tabs for every model type that is available in the data, and for every model type there are tabs for every plot option that is available.', size='md', weight=300),
        dmc.Text('To change the plot, click on the tab of the model type you want to change. Then click on the tab of the plot option you want to change.', size='md', weight=300),
        dmc.Text('The plot will change accordingly.', size='md', weight=300),
        dmc.Image(src='/assets/help/plots.png', alt='Change plots', width='100%'),

        dmc.Text('Edit plots', size='xl', weight=500),
        dmc.Text('Every plot has widgets to its left that allow you to change the plot, by changing predefined parameters, that include but are not limited to the scenario, the period, the region and the plot type.', size='md', weight=300),
        dmc.Text('By changing the parameters, the plot will change accordingly.', size='md', weight=300),

        dmc.Image(src='/assets/help/plots.png', alt='Edit plots', width='100%'),

        dmc.Text('Save plots', size='xl', weight=500),
        dmc.Text('To save a plot, click the "Save" button in the top right corner of the plot window.', size='md', weight=300),
        dmc.Text('The plot will be saved as a PNG file.', size='md', weight=300),

        dmc.Image(src='/assets/help/plots.png', alt='Save plots', width='100%'),

        dmc.Text('Change View', size='xl', weight=500),
        dmc.Text('To have a clean interface where only the plot is visible, hide the widgets by clicking the hamburger menu in the top left corner of the window and press the  "^" button to hide the tab bar.', size='md', weight=300),
        dmc.Text('To show the widgets or tabs again, click the hamburger menu or the "v" button accordingly.', size='md', weight=300),

        dmc.Image(src='/assets/help/plots.png', alt='Change View', width='100%'),

    ],
    )
    return layout
