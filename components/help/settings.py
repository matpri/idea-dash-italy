from dash import html


def render():
    # print('rendering start')
    layout = html.Div([
        html.H1('Model Settings'),
        html.P(
            'To change the settings of a plot, click the "Settings" button in the toolbar on the left. The settings window will open. Each model has custom settings that can be changed.'),

        html.Div([
            html.Center(html.Img(src='/assets/help/open_settings.gif', style={'width': '100%'})),
            html.H3('Opening Settings', style={'font-size': '15px', 'color': 'gray', 'text-align': 'center'}),
        ]),

        html.H1('COPPER settings'),
        html.P(
            'COPPER settings include the following: For each Technology, you can change the color and the name. Additionally, you can adjust the group it is aggregated to and modify that group`s color. For each plot, you can change the title, the x-axis, and the y-axis labels.'),

        html.Div([
            html.Center(html.Img(src='/assets/help/tech_settings.gif', style={'width': '100%'})),
            html.H3('Technology Settings', style={'font-size': '15px', 'color': 'gray', 'text-align': 'center'}),
        ]),

        html.Div([
            html.Center(html.Img(src='/assets/help/plot_settings.gif', style={'width': '100%'})),
            html.H3('Plot Settings', style={'font-size': '15px', 'color': 'gray', 'text-align': 'center'}),
        ]),

        html.P(
            'When done, click the "Update" button to save the changes. This action will reload all windows with the updated plots.'),

        html.Div([
            html.Center(html.Img(src='/assets/help/submit_settings.gif', style={'width': '100%'})),
            html.H3('Submitting Settings', style={'font-size': '15px', 'color': 'gray', 'text-align': 'center'}),
        ]),
    ])
    return layout
