from dash import html
import dash_mantine_components as dmc


def create_widgets(df, classes, window_id):
    costs = []
    c_regions = []
    c_scenarios = []
    if 'Cost' in classes:
        costs = df[df['variable'].str.startswith('Cost')]['variable'].apply(lambda x: x.split('|')[1]).unique()
        c_regions = df[df['variable'].str.startswith('Cost')]['region'].unique()
        c_scenarios = df[df['variable'].str.startswith('Cost')]['scenario'].unique()

    cost_widget_layout = html.Div([
        dmc.Select(
            label='Cost Type',
            data=[{'label': cost, 'value': cost} for cost in costs],
            value=costs[0] if len(costs) else '',
            id={
                'type': 'copper-inputs-cost-select',
                'index': window_id
            },
        ),
        dmc.Select(
            label='Scenario',
            data=[{'label': scenario, 'value': scenario} for scenario in c_scenarios],
            value=c_scenarios[0] if len(c_scenarios) else '',
            id={
                'type': 'copper-inputs-cost-scenario-select',
                'index': window_id
            },
        ),
        dmc.Select(
            label='Region',
            data=[{'label': region, 'value': region} for region in c_regions],
            value=c_regions[0] if len(c_regions) else '',
            id={
                'type': 'copper-inputs-cost-region-select',
                'index': window_id
            },
        ),
    ],
        style={'display': 'none'},
        id={
            'type': 'copper-inputs-cost-widget',
            'index': window_id
        }
    )
    return cost_widget_layout