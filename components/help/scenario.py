from dash import html


def render():
    print('rendering start')
    layout = html.Div([
        html.H1('Scenario Settings'),
        html.P(
            'To change the settings of a scenario that was loaded, click the "Data" button in the toolbar on the left. The settings window will open. Select the results you want to edit by using the dropdown menu. In the settings, you can alter the scenario name and the plots that should be produced for this scenario. Click the "Submit" button to finalize your selection. This will reload all windows with the updated scenario names and plot choices.'),

        html.Div([
            html.Center(html.Img(src='/assets/help/scenario_open.gif', style={'width': '100%'})),
            html.H3('Opening Scenario Settings', style={'font-size': '15px', 'color': 'gray', 'text-align': 'center'}),
        ]),

        html.Div([
            html.Center(html.Img(src='/assets/help/scenario_edit.gif', style={'width': '100%'})),
            html.H3('Editing Scenario Settings', style={'font-size': '15px', 'color': 'gray', 'text-align': 'center'}),
        ]),

    ])

    return layout
