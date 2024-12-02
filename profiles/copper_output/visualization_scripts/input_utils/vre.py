from dash import html
import dash_mantine_components as dmc


def create_widgets(df, classes, window_id):
    seasons = []
    vre_variables = []
    if 'Vre Capacity Factors' in classes:
        seasons = ['Winter', 'Summer']
        vre_variables = ['Wind', 'Solar']

    vre_widget_layout = html.Div([
        dmc.Select(
            label='Season',
            data=[{'label': season, 'value': season} for season in seasons],
            value=seasons[0] if len(seasons) else '',
            id={
                'type': 'copper-inputs-season-select',
                'index': window_id
            },
        ),
        dmc.Select(
            label='VRE Variable',
            data=[{'label': vre_variable, 'value': vre_variable} for vre_variable in vre_variables],
            value=vre_variables[0] if len(vre_variables) else '',
            id={
                'type': 'copper-inputs-vre-variable-select',
                'index': window_id
            },
        )
    ],
        style={'display': 'none'},
        id={
            'type': 'copper-inputs-vre-widget',
            'index': window_id
        }
    )
    return vre_widget_layout