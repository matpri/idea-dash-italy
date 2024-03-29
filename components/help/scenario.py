import dash_mantine_components as dmc
from dash import html


def render():
    print('rendering start')
    layout = html.Div([
        dmc.Text('Scenario Settings', size='xl', weight=500),
        dmc.Text('To change the settings of a scenario that was loaded, click the "Data" button in the toolbar on the left.', size='md', weight=300),
        dmc.Image(src='/assets/help/settings.png', alt='Settings', width='100%'),
        dmc.Text('The settings window will open.', size='md', weight=300),
        dmc.Text('Select the results you want to edit by selecting it in the dropdown.', size='md', weight=300),
        dmc.Text('In the settings you can change the scenario name and the plots that should be generated for this scenario.', size='md', weight=300),
        dmc.Text('Click the "Submit" button to finalize your selection. (This will reload all windows with the updated scenario names and plot selections)', size='md', weight=300),
        dmc.Image(src='/assets/help/settings.png', alt='Settings', width='100%'),

        



    ],
    )
    return layout
