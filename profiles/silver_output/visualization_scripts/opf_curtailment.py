import dash_mantine_components as dmc
import plotly.graph_objects as go
from dash import html, dcc

from profiles.silver_output.visualization_scripts.utils import total_plot, tech_plot


def render_plot(type, df, scenarios, time_size='hourly'):
    from profiles.silver_output.utils import plot_settings
    print('rendering plot', type)
    name = plot_settings['OPF_VRE_Curtailment']['name']
    unit = plot_settings['OPF_VRE_Curtailment']['unit']

    title = plot_settings['OPF_VRE_Curtailment'][type]['title']
    x_axis_label = plot_settings['OPF_VRE_Curtailment'][type]['x_label']
    y_axis_label = plot_settings['OPF_VRE_Curtailment'][type]['y_label']
    if type == 'Total':
        fig = total_plot.render(df, scenarios, title, x_axis_label, y_axis_label, time_size)
    else:
        fig = tech_plot.render(df, scenarios, title, x_axis_label, y_axis_label, time_size)
    return fig


def plot(df, window_id):
    '''

    :param df: pandas Dataframe containing the data to visualize
    :param window_id: window id to use when registering components to dash
    :return: html.Div([widgets]), dcc.Graph(plot)
    '''
    scenarios = df['scenario'].unique().tolist()

    widget_layout = html.Div([
        dmc.Select(
            label='Plot Options',
            data=[{'label': plot, 'value': plot} for plot in ['Total', 'By Technology']],
            value='Total',
            id={
                'type': 'silver-opf_vre_curtailment-plot-select',
                'index': window_id
            },
        ),
        dmc.MultiSelect(
            label='Scenarios',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=[scenarios[0]],
            id={
                'type': 'silver-opf_vre_curtailment-scenario-multi-select',
                'index': window_id,
            },
            style={'display': 'block'}
        ),
        dmc.Select(
            label='Scenario',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=scenarios[0],
            id={
                'type': 'silver-opf_vre_curtailment-scenario-select',
                'index': window_id,
            },
            style={'display': 'none'}
        ),
        dmc.Select(
            label='Timestep',
            data=[{'label': t_step, 'value': t_step} for t_step in ['hourly', 'daily', 'monthly', 'yearly']],
            value='hourly',
            id={
                'type': 'silver-opf_vre_curtailment-time_step-select',
                'index': window_id,
            },
            style={'display': 'block'}
        ),

        dmc.Button('Download Data', id={'type': 'silver-opf_vre_curtailment-download-button', 'index': window_id},
                   variant='light',
                   # center the button
                   style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
        dcc.Download(id={'type': 'silver-opf_vre_curtailment-download', 'index': window_id}),
    ])

    plot_layout = dcc.Graph(
        figure=render_plot('Total', df, [scenarios[0]]),
        id={
            'type': 'figure',
            'index': window_id,
            'profile': 'silver_output',
            'viz': 'opf_vre_curtailment'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )

    return widget_layout, plot_layout
