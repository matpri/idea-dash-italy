import dash_mantine_components as dmc
from dash import html


def render():
    print('rendering start')
    layout = html.Div([
        dmc.Text('Add Windows', size='xl', weight=500),
        dmc.Text('To add a window click the "+" button in the toolbar on the left side of the screen.', size='md', weight=300),
        dmc.Image(src='/assets/help/load_data.png', alt='Load Data', width='100%'),
        dmc.Text('To clear the workspace click the "trash bin" in the tool bar and confirm.', size='md', weight=300),

        dmc.Text('Interact with windows', size='xl', weight=500),
        dmc.Text('To move a window, click and drag the title bar of the window.', size='md', weight=300),
        dmc.Text('To resize a window, click and drag one of the edges of the window.', size='md', weight=300),
        dmc.Text('To close a window, click the "x" in the top right corner of the title bar of the window.', size='md', weight=300),

        dmc.Image(src='/assets/help/load_data.png', alt='Load Data', width='100%'),
    ],
    )
    return layout
