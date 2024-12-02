from dash import html
import dash_mantine_components as dmc


def create_widgets(df, classes, window_id):
    t_p_type = []
    t_years = []
    t_scenarios = []
    if 'Extant Transmission' in classes:
        t_p_type = ['Map Plot', 'Bar Plot']
        t_years = df[df['variable'].str.startswith('Extant Transmission')]['time'].unique()
        t_scenarios = df[df['variable'].str.startswith('Extant Transmission')]['scenario'].unique()
    transmission_widget_layout = html.Div([
        dmc.Select(
            label='Representation Options',
            data=[{'label': plot, 'value': plot} for plot in t_p_type],
            value=t_p_type[0] if len(t_p_type) else '',
            id={
                'type': 'copper-inputs-transmission-select',
                'index': window_id
            },
        ),
        dmc.Select(
            label='Year',
            data=[{'label': year, 'value': year} for year in t_years],
            value=t_years[0] if len(t_years) else '',
            id={
                'type': 'copper-inputs-year-select',
                'index': window_id
            },
        ),
        dmc.Select(
            label='Scenario',
            data=[{'label': scenario, 'value': scenario} for scenario in t_scenarios],
            value=t_scenarios[0] if len(t_scenarios) else '',
            id={
                'type': 'copper-inputs-scenario-select',
                'index': window_id
            },
            style={'display': 'none'}
        ),
        dmc.MultiSelect(
            label='Select Scenarios',
            data=[{'label': scenario, 'value': scenario} for scenario in t_scenarios],
            value=t_scenarios if t_scenarios else [],
            id={
                'type': 'copper-inputs-scenario-multi-select',
                'index': window_id
            },
            style={'display': 'none'}
        )

    ],
        style={'display': 'none'},
        id={
            'type': 'copper-inputs-transmission-widget',
            'index': window_id
        })
    return transmission_widget_layout