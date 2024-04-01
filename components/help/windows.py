import dash_mantine_components as dmc
from dash import html, dcc

def render():
    layout = html.Div([
        html.H1('Add Windows'),
        html.P('To add a window click the "+" button in the toolbar on the left side of the screen.'),
        
        html.Div([
            html.Center(html.Img(src='/assets/help/windows_add.gif', style={'width':'100%'})),
            html.H3('Add Windows', style={'font-size': '15px', 'color': 'gray', 'text-align': 'center'}),
        ]),
        
        html.P('To clear the workspace click the "trash bin" in the tool bar and confirm.'),
        html.Div([
            html.Center(html.Img(src='/assets/help/windows_clear.gif', style={'width':'100%'})),
            html.H3('Clear Windows', style={'font-size': '15px', 'color': 'gray', 'text-align': 'center'}),
        ]),
        
        html.H1('Interact with windows'),
        html.P('To move a window, click and drag the title bar of the window. To resize a window, click and drag one of the edges of the window. To close a window, click the "x" in the top right corner of the title bar of the window.'),
       
        html.Div([
            html.Center(html.Img(src='/assets/help/windows_move.gif', style={'width':'100%'})),
            html.H3('Move/Resize/Close Windows', style={'font-size': '15px', 'color': 'gray', 'text-align': 'center'}),
        ]),
        
    ])
    return layout