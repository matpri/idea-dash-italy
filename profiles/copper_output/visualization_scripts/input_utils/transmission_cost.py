from dash import html
import dash_mantine_components as dmc


def create_widgets(df, classes, window_id):
    transmission_cost_scenario = []
    if 'Transmission Costs' in classes:
        transmission_cost_scenario = df[df['variable'].str.startswith('Transmission Costs')]['scenario'].unique()

    transmission_cost_widget_layout = html.Div([
        dmc.MultiSelect(
            label='Scenario',
            data=[{'label': scenario, 'value': scenario} for scenario in transmission_cost_scenario],
            value=[transmission_cost_scenario[0]] if len(transmission_cost_scenario) else [],
            id={
                'type': 'copper-inputs-transmission-cost-scenario-select',
                'index': window_id
            },
        )
    ],
        style={'display': 'none'},
        id={
            'type': 'copper-inputs-transmission-cost-widget',
            'index': window_id
        }
    )
    return transmission_cost_widget_layout