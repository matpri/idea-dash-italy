import dash
import dash_mantine_components as dmc
from dash import ALL, Output, Input, State, dcc, html

from profiles.copper_output.visualization_scripts.utils import bar_over_years, bar_over_regions


def render(window_id):
    scenarios = ['BAU', 'COPPER']
    regions = ['AB', 'BC', 'MB', 'NB', 'NL', 'NS', 'NT', 'NU', 'ON', 'PE', 'QC', 'SK', 'YT']
    years = [2015, 2020, 2025, 2030, 2035, 2040, 2045, 2050]


    layout_by_year_plot = html.Div([
        dmc.Switch('Aggregate',
                   id={
                       'type': 'aggregate-switch',
                       'index': window_id,
                       'profile': 'COPPER Output',
                       'viz': 'Emissions'
                   }
                   ),
        dmc.MultiSelect(
            label='Scenarios',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=[scenarios[0]],
            id={
                'type': 'scenario-multi-select',
                'index': window_id,
                'profile': 'COPPER Output',
                'viz': 'Emissions'
            }
        ),
        dmc.Select(
            label='Region',
            data=[{'label': region, 'value': region} for region in regions],
            value=regions[0],
            id={
                'type': 'region-select',
                'index': window_id,
                'profile': 'COPPER Output',
                'viz': 'Emissions'
            }
        ),
    ], id={
        'type': 'year-plot-options',
        'index': window_id,
        'profile': 'COPPER Output',
        'viz': 'Emissions'
    },
        # style={'display': 'block'}
    )

    # layout_by_region_plot = html.Div([
    #     dmc.Switch('Aggregate'),
    #     dmc.MultiSelect(
    #         label='Scenarios',
    #         data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
    #         value=[scenarios[0]],
    #         id={
    #             'type': 'scenario-multi-select',
    #             'index': window_id,
    #             'profile': 'COPPER Output',
    #             'viz': 'Emissions 2',
    #             'plot': 'By Region'
    #         }
    #     ),
    #     dmc.Select(
    #         label='Year',
    #         data=[{'label': year, 'value': year} for year in years],
    #         value=years[0],
    #         id={
    #             'type': 'year-slider',
    #             'index': window_id,
    #             'profile': 'COPPER Output',
    #             'viz': 'Emissions 2',
    #             'plot': 'By Region'
    #         }
    #     ),
    # ], id={
    #     'type': 'region-plot-options',
    #     'index': window_id,
    #     'profile': 'COPPER Output',
    #     'viz': 'Emissions 2'
    # },
    #     # style={'display': 'none'}
    # )

    layout = html.Div([
        dmc.Select(
            label='Plot Options',
            data=[{'label': plot, 'value': plot} for plot in ['By Year', 'By Region']],
            value='By Year',
            id={
                'type': 'plot-select',
                'index': window_id,
                'profile': 'COPPER Output',
                'viz': 'Emissions 2'
            },
        ),
        layout_by_year_plot,
        # layout_by_region_plot,
    ])

    return layout
