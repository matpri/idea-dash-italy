import dash_mantine_components as dmc
from dash import html, dcc
from components import ids
from profiles.copper_input.visualization_scripts.utils import bar_over_years, bar_over_regions, trend_over_years, pie_chart


def render_plot(type, df, scenarios, region, year):
    from profiles.copper_input.utils import plot_settings
    #print('rendering plot', type)
    name = plot_settings['Tech Evolution']['name']
    unit = plot_settings['Tech Evolution']['unit']
    if type == 'By Year':
        plot_info = plot_settings['Tech Evolution']['By Year']
        return bar_over_years.plot(df, scenarios, region, False, plot_info['title'], plot_info['x_label'], plot_info['y_label'], name, unit)
    else:
        plot_info = plot_settings['Tech Evolution']['By Tech']
        return bar_over_regions.plot(df, scenarios, False, year, plot_info['title'], plot_info['x_label'], plot_info['y_label'], name, unit)


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
        label='Technology',
        data=[{'label': region, 'value': region} for region in regions],
        value= 'CAN' if 'CAN' in regions else regions[0],
        id={
            'type': 'copper_input-tech_evolution-region-select',
            'index': window_id
        },
        style={'display': 'block'}

    )

    by_region_widgets = dmc.Select(
        label='Year',
        data=[{'label': year, 'value': year} for year in years],
        value=years[0],
        id={
            'type': 'copper_input-tech_evolution-year-select',
            'index': window_id
        },

        style={'display': 'none'}
    )

    widget_layout = html.Div([
        dmc.Select(
            label='Plot Options',
            data=[{'label': plot, 'value': plot} for plot in ['By Year', 'By Tech']],
            value='By Year',
            id={
                'type': 'copper_input-tech_evolution-plot-select',
                'index': window_id
            },
        ),
        dmc.MultiSelect(
            label='Scenarios',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=[scenarios[0]],
            id={
                'type': 'copper_input-tech_evolution-scenario-multi-select',
                'index': window_id,
            },
            style={'display': 'block'}
        ),
        
        by_year_widgets,
        by_region_widgets,
    ])

    plot_layout = dcc.Graph(
        figure=render_plot('By Year', df, [scenarios[0]], 'CAN' if 'CAN' in regions else regions[0], years[0]),
        id={
            'type': ids.FIGURE,
            'index': window_id,
            'profile': 'COPPER Input',
            'viz': 'tech_evolution'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )

    return widget_layout, plot_layout
