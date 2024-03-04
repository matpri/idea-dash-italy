import dash_mantine_components as dmc
from dash import html, dcc

from profiles.copper_output.visualization_scripts.utils import bar_over_years, bar_over_regions


def render_plot(type, df, aggregate, scenarios, region, year, title, x_axis_label, y_axis_label):
    print('rendering plot', type)
    if type == 'By Year':
        return bar_over_years.plot(df, scenarios, region, aggregate, title, x_axis_label, y_axis_label)
    else:
        return bar_over_regions.plot(df, scenarios, aggregate, year, title, x_axis_label, y_axis_label)


def plot(df, window_id):
    '''

    :param df: pandas Dataframe containing the data to visualize
    :param window_id: window id to use when registering components to dash
    :return: html.Div([widgets]), dcc.Graph(plot)
    '''
    scenarios = df['scenario'].unique().tolist()
    regions = df['region'].unique().tolist()
    years = df['time'].unique().tolist()

    by_year_widgets = dmc.Select(
        label='Region',
        data=[{'label': region, 'value': region} for region in regions],
        value=regions[0],
        id={
            'type': 'copper-newcapacity-region-select',
            'index': window_id
        },
        style={'display': 'block'}

    )

    by_region_widgets = dmc.Select(
        label='Year',
        data=[{'label': year, 'value': year} for year in years],
        value=years[0],
        id={
            'type': 'copper-newcapacity-year-select',
            'index': window_id
        },

        style={'display': 'none'}
    )

    widget_layout = html.Div([
        dmc.Select(
            label='Plot Options',
            data=[{'label': plot, 'value': plot} for plot in ['By Year', 'By Region']],
            value='By Year',
            id={
                'type': 'copper-newcapacity-plot-select',
                'index': window_id
            },
        ),
        dmc.Switch('Aggregate',
                   checked=True,
                   id={
                       'type': 'copper-newcapacity-aggregate-switch',
                       'index': window_id}),
        dmc.MultiSelect(
            label='Scenarios',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=[scenarios[0]],
            id={
                'type': 'copper-newcapacity-scenario-multi-select',
                'index': window_id,
            }
        ),
        by_year_widgets,
        by_region_widgets
    ])

    plot_layout = dcc.Graph(
        figure=render_plot('By Year', df, True, [scenarios[0]],  regions[0], years[0],
                           title='New Capacity by Year',
                           x_axis_label='Year',
                           y_axis_label='GW'),
        id={
            'type': 'copper-newcapacity-canvas',
            'index': window_id},
        style={
            'width': '100%',
            'height': '100%'
        }
    )

    return widget_layout, plot_layout
