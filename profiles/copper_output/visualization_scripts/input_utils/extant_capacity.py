from dash import html
import dash_mantine_components as dmc


def create_widgets(df, classes, window_id):
    e_years = []
    e_regions = []
    e_scenarios = []
    e_p_type = []
    if 'Extant Capacity' in classes:
        e_p_type = ['By Year', 'By Region', 'Trend Over Years', 'Pie Chart']
        e_years = df[df['variable'].str.startswith('Extant Capacity')]['time'].unique()
        e_scenarios = df[df['variable'].str.startswith('Extant Capacity')]['scenario'].unique()
        e_regions = df[df['variable'].str.startswith('Extant Capacity')]['region'].unique()

    extant_capacity_widget_layout = html.Div([
        dmc.Select(
            label='Representation Options',
            data=[{'label': plot, 'value': plot} for plot in e_p_type],
            value=e_p_type[0] if len(e_p_type) else '',
            id={
                'type': 'copper-inputs-extant-capacity-select',
                'index': window_id
            },
            style={'display': 'none'}
        ),
        dmc.Select(
            label='Year',
            data=[{'label': year, 'value': year} for year in e_years],
            value=e_years[0] if len(e_years) else '',
            id={
                'type': 'copper-inputs-extant-capacity-year-select',
                'index': window_id
            },
            style={'display': 'none'}
        ),
        dmc.Select(
            label='Region',
            data=[{'label': region, 'value': region} for region in e_regions],
            value=e_regions[0] if len(e_regions) else '',
            id={
                'type': 'copper-inputs-extant-capacity-region-select',
                'index': window_id
            },
            style={'display': 'none'}
        ),
        dmc.Select(
            label='Scenario',
            data=[{'label': scenario, 'value': scenario} for scenario in e_scenarios],
            value=e_scenarios[0] if len(e_scenarios) else '',
            id={
                'type': 'copper-inputs-extant-capacity-scenario-select',
                'index': window_id
            },
            style={'display': 'none'}
        ),
        dmc.MultiSelect(
            label='Select Scenarios',
            data=[{'label': scenario, 'value': scenario} for scenario in e_scenarios],
            value=e_scenarios if len(e_scenarios) else [],
            id={
                'type': 'copper-inputs-extant-capacity-scenario-multi-select',
                'index': window_id
            },
            style={'display': 'none'}
        )
    ],
        id={
            'type': 'copper-inputs-extant-capacity-widget',
            'index': window_id
        },
        style={'display': 'none'}
    )
    return extant_capacity_widget_layout