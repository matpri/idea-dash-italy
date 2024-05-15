import dash_mantine_components as dmc
from dash import html, dcc

from utils.generic_profile.visualization_scripts.utils import bar_over_years, bar_over_regions, trend_over_years, pie_chart

def create_generic_plots(model, name):
    def render_plot(type, df, aggregate, scenarios, region, year, scenario, pattern_active=True, text_active=False):
        from profiles.natem_output.utils import plot_settings
        print('rendering plot', type)
        unit = df['unit'].unique()[0]
        if type == 'By Year':
            return bar_over_years.plot(df, scenarios, region, aggregate, name, "Year", name, name, unit,
                                       pattern_active=pattern_active,
                                       text_active=text_active)
        elif type == 'Trend Over Years':
            return trend_over_years.plot(df, scenario, region, aggregate, name, "Year", name, name, unit)
        elif type == 'Pie Chart':
            return pie_chart.plot(df, scenario, region, year, aggregate, name, "Year", name,)
        else:
            return bar_over_regions.plot(df, scenarios, aggregate, year, name, "Region", name, name, unit, pattern_active=pattern_active,
                                         text_active=text_active)

    def plot(df, window_id):
        scenarios = df['scenario'].unique().tolist()
        regions = df['region'].unique().tolist()
        years = df['time'].unique().tolist()

        by_year_widgets = dmc.Select(
            label='Region',
            data=[{'label': region, 'value': region} for region in regions],
            value='CAN' if 'CAN' in regions else regions[0],
            id={
                'type': 'generic-region-select',
                'index': window_id
            },
            style={'display': 'block'}

        )

        by_region_widgets = dmc.Select(
            label='Year',
            data=[{'label': year, 'value': year} for year in years],
            value=years[0],
            id={
                'type': 'generic-year-select',
                'name': name,
                'model': model,
                'index': window_id
            },

            style={'display': 'none'}
        )

        pattern_toggle = dmc.Switch(
            label='Pattern',
            checked=True,
            id={
                'type': 'generic-pattern-switch',
                'name': name,
                'model': model,
                'index': window_id,
            },
            style={'display': 'block'}
        )

        text_toggle = dmc.Switch(
            label='Text',
            checked=False,
            id={
                'type': 'generic-text-switch',
                'name': name,
                'model': model,
                'index': window_id,
            },
            style={'display': 'block'}
        )

        widget_layout = html.Div([
            dmc.Select(
                label='Plot Options',
                data=[{'label': plot, 'value': plot} for plot in
                      ['By Year', 'By Region', 'Trend Over Years', 'Pie Chart']],
                value='By Year',
                id={
                    'type': 'generic-plot-select',
                'name': name,
                'model': model,
                    'index': window_id
                },
            ),
            dmc.Switch('Aggregate',
                       checked=True,
                       id={
                           'type': 'generic-aggregate-switch',
                'name': name,
                'model': model,
                           'index': window_id}),
            pattern_toggle,
            text_toggle,
            dmc.MultiSelect(
                label='Scenarios',
                data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
                value=[scenarios[0]],
                id={
                    'type': 'generic-scenario-multi-select',
                'name': name,
                'model': model,
                    'index': window_id,
                },
                style={'display': 'block'}
            ),
            dmc.Select(
                label='Scenario',
                data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
                value=scenarios[0],
                id={
                    'type': 'generic-scenario-select',
                'name': name,
                'model': model,
                    'index': window_id,
                },
                style={'display': 'none'}
            ),
            by_year_widgets,
            by_region_widgets,
            dmc.Button('Download Data', id={'type': 'generic-download-button',
                'name': name,
                'model': model,'index': window_id},
                       variant='light',
                       # center the button
                       style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
            dcc.Download(id={'type': 'generic-download',
                'name': name,
                'model': model,'index': window_id}),
        ])

        plot_layout = dcc.Graph(
            figure=render_plot('By Year', df, True, [scenarios[0]], 'CAN' if 'CAN' in regions else regions[0],
                               years[0], scenarios[0]),
            id={
                'type': 'figure',
                'index': window_id,
                'model': model,
                'name': name
            },
            style={
                'width': '100%',
                'height': '100%'
            }
        )

        return widget_layout, plot_layout

    return plot