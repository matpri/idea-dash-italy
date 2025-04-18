import dash_mantine_components as dmc
from dash import html, dcc
from components import ids
from profiles.copper_input.visualization_scripts.utils import bar_over_years, bar_over_regions, trend_over_years, pie_chart


def render_plot(type, df, year, scenarios):
    from profiles.copper_input.utils import plot_settings
    #print('rendering plot', type)
    name = plot_settings['Transmission']['name']
    unit = plot_settings['Transmission']['unit']
    if type == 'Capacity':
        plot_info = plot_settings['Transmission']['Capacity']
        df = df[df.variable == 'Capacity'].copy()
        return bar_over_regions.plot(df, scenarios, False, year,  plot_info['title'], plot_info['x_label'], plot_info['y_label'], name, unit)
    elif type == 'Distance':
        plot_info = plot_settings['Transmission']['Distance']
        df = df[df.variable == 'Distance'].copy()
        return bar_over_regions.plot(df, scenarios, False, year, plot_info['title'], plot_info['x_label'], plot_info['y_label'], name, unit)
    elif type == 'Expansion_limits':
        plot_info = plot_settings['Transmission']['Expansion_limits']
        df = df[df.variable == 'Expansion_limits'].copy()
        return bar_over_regions.plot(df, scenarios, False, year, plot_info['title'], plot_info['x_label'], plot_info['y_label'], name, unit)


def plot(df, window_id):
    '''

    :param df: pandas Dataframe containing the data to visualize
    :param window_id: window id to use when registering components to dash
    :return: html.Div([widgets]), dcc.Graph(plot)
    '''
    scenarios = df['scenario'].unique().tolist()
    years = df['time'].unique().tolist()

    widget_layout = html.Div([
        dmc.Select(
            label='Plot Options',
            data=[{'label': plot, 'value': plot} for plot in ['Capacity', 'Distance', 'Expansion_limits']],
            value='Capacity',
            id={
                'type': 'copper_input-transmission-plot-select',
                'index': window_id
            },
        ),
        dmc.MultiSelect(
            label='Scenarios',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=[scenarios[0]],
            id={
                'type': 'copper_input-transmission-scenario-multi-select',
                'index': window_id,
            },
            style={'display': 'block'}
        ),
        dmc.Select(
            label='Year',
            data=[{'label': year, 'value': year} for year in years],
            value=years[0],
            id={
                'type': 'copper_input-transmission-year-select',
                'index': window_id
            },
        ),
        dmc.Button('Download Data', id={'type': 'copper_input-transmission-download-button', 'index': window_id},
                   variant='light',
                   # center the button
                     style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
        dcc.Download(id={'type': 'copper_input-transmission-download', 'index': window_id}),
    ])

    plot_layout = dcc.Graph(
        figure=render_plot('Capacity', df, years[0],[scenarios[0]]),
        id={
            'type': ids.FIGURE,
            'index': window_id,
            'profile': 'COPPER Input',
            'viz': 'transmission'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )

    return widget_layout, plot_layout
