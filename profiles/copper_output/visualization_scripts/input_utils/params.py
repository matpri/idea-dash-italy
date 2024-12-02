from dash import html
import dash_mantine_components as dmc


def create_widgets(df, classes, window_id):

    params_scenario = []
    params_variables = []
    if 'Technology Parameter' in classes:
        params_scenario = df[df['variable'].str.startswith('Technology Parameter')]['scenario'].unique()
        params_variables = df[df['variable'].str.startswith('Technology Parameter')]['variable'].apply(
            lambda x: x.split('|')[1]).unique()

    params_widget_layout = html.Div([
        dmc.MultiSelect(
            label='Scenario',
            data=[{'label': scenario, 'value': scenario} for scenario in params_scenario],
            value=[params_scenario[0]] if len(params_scenario) else [],
            id={
                'type': 'copper-inputs-params-scenario-select',
                'index': window_id
            },
        ),
        dmc.Select(
            label='Variable',
            data=[{'label': variable, 'value': variable} for variable in params_variables],
            value=params_variables[0] if len(params_variables) else '',
            id={
                'type': 'copper-inputs-params-variable-select',
                'index': window_id
            },
        ),
    ],
        style={'display': 'none'},
        id={
            'type': 'copper-inputs-params-widget',
            'index': window_id
        }
    )
    return params_widget_layout