import dash_mantine_components as dmc
from dash import html


def render():
    print('rendering start')
    layout = html.Div([
        dmc.Text('Model Settings', size='xl', weight=500),
        dmc.Text('To change the settings of a plot, click the "Settings" button in the toolbar on the left.', size='md', weight=300),
        dmc.Image(src='/assets/help/settings.png', alt='Settings', width='100%'),
        dmc.Text('The settings window will open.', size='md', weight=300),
        dmc.Text('Each model has custom settings that can be changed.', size='md', weight=300),

        dmc.Text('COPPER settings', size='xl', weight=500),
        dmc.Text('COPPER settings include the following:', size='md', weight=300),
        dmc.Text('Technology Settings', size='md', weight=300),
        dmc.Text('For each Technology you can change the color and name. in addition to the group it is aggregated to and that group`s color.', size='md', weight=300),
        dmc.Image(src='/assets/help/settings.png', alt='Settings', width='100%'),

        dmc.Text('Plot Settings', size='md', weight=300),
        dmc.Text('For each plot you can change the title, the x and y axis labels..', size='md', weight=300),
        dmc.Image(src='/assets/help/settings.png', alt='Settings', width='100%'),

        dmc.Text('When done click the "Update" button to save the changes (this will reload all windows with the update plots)', size='md', weight=300),
        dmc.Image(src='/assets/help/settings.png', alt='Settings', width='100%'),
    ],
    )
    return layout
