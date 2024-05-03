import dash_mantine_components as dmc
import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc

from profiles.energy_model import utils


def render_plot(type, df, scenario_a, scenario_b, aggregate):
    from profiles.energy_model.utils import plot_settings
    print('rendering plot', type)
    df = df[df.variable.str.startswith(type + '|')]
    df['variable'] = df['variable'].str.replace(type + '|', '')
    df_a = df[df['scenario'] == scenario_a]
    df_b = df[df['scenario'] == scenario_b]
    diff = pd.merge(df_a, df_b, on=['time', 'variable'], suffixes=('_base', '_test'))
    diff['value'] = diff.value_test.fillna(0) - diff.value_base.fillna(0)
    diff['scenario'] = scenario_a + ' - ' + scenario_b

    plot_info = plot_settings['Matrix'][type]
    name = plot_info['name']
    unit = plot_info['unit']
    return plot_comparison(diff, aggregate, plot_info['title'], plot_info['x_label'], plot_info['y_label'], name, unit)


def plot_comparison(diff, aggregate, title, x_label, y_label, name, unit):
    fig = go.Figure()
    scen = diff['scenario'].unique()[0]
    if aggregate:
        diff['variable'] = diff["variable"].map(utils.get_group).fillna(diff["variable"])
        diff = diff.groupby(["variable", "time", 'scenario']).sum(numeric_only=True).reset_index()
    else:
        diff['variable'] = diff["variable"].map(utils.get_name).fillna(diff["variable"])
        diff = diff.groupby(["variable", "time", 'scenario']).sum(numeric_only=True).reset_index()

    if diff.empty:
        print("No data available, since the results are all zero.")
        fig.add_annotation(
            x=0.5,
            y=0.5,
            text="No data available, since the results are all zero.",
            showarrow=False,
            font=dict(
                size=16,
                color="black"
            ),
            align="center",
            valign="middle",
        )
        return fig

    fig.update_layout(
        title_text=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        template="simple_white",
    )
    try:
        for tech in diff['variable'].unique():
            tech_df = diff[diff['variable'] == tech]
            if aggregate:
                color = utils.get_group_colors(tech)
            else:
                color = utils.get_color(tech)
            fig.add_bar(x=tech_df['time'], y=tech_df['value'], name=tech, marker_color=color,
                        hovertemplate=f'{scen}<br>Technology: {tech}<br>'
                                      + 'Year: %{x}<br>Value: %{y:.2f}')
        fig.update_layout(barmode='relative')
        fig.update_yaxes(showgrid=True)
    except Exception as e:
        print('ERROR', title, 'plot:', e)

    fig.layout.autosize = True
    return fig


def plot(df, window_id):
    '''

    :param df: pandas Dataframe containing the data to visualize
    :param window_id: window id to use when registering components to dash
    :return: html.Div([widgets]), dcc.Graph(plot)
    '''
    print('plotting comparison')
    classes = df['variable'].str.split('|', expand=True)[0].unique().tolist()

    widget_layout = html.Div([
        dmc.Select(
            label='Plot Options',
            data=[{'label': plot, 'value': plot} for plot in classes],
            value=classes[0],
            id={
                'type': 'energy_model-comparison-plot-select',
                'index': window_id
            },
        ),
        dmc.Text('Select the scenarios to compare:', size='sm', weight=500, align='center', style={'margin-top': '4px'}),
        html.Div(
            [
                dmc.Select(
                    label='Scenario A',
                    data=[{'label': scenario, 'value': scenario} for scenario in df['scenario'].unique()],
                    value=df['scenario'].unique().tolist()[0],
                    id={
                        'type': 'energy_model-comparison-scenario_a-select',
                        'index': window_id
                    },
                ),
                dmc.Select(
                    label='Scenario B',
                    data=[{'label': scenario, 'value': scenario} for scenario in df['scenario'].unique()],
                    value=df['scenario'].unique().tolist()[0],
                    id={
                        'type': 'energy_model-comparison-scenario_b-select',
                        'index': window_id
                    },
                ),
            ],
            style={'display': 'flex', 'justify-content': 'space-between'}),
        dmc.Switch(
            label='Aggregate',
            checked=True,
            id={
                'type': 'energy_model-comparison-aggregate-switch',
                'index': window_id,
            },
        ),
        dmc.Button('Download Data', id={'type': 'energy_model-comparison-download-button', 'index': window_id},
                   variant='light',
                   # center the button
                   style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
        dcc.Download(id={'type': 'energy_model-comparison-download', 'index': window_id}),
    ])

    plot_layout = dcc.Graph(
        figure=render_plot(classes[0], df, df['scenario'].unique().tolist()[0], df['scenario'].unique().tolist()[0],
                            True),
        id={
            'type': 'figure',
            'index': window_id,
            'profile': 'energy_model',
            'viz': 'comparison'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )
    return widget_layout, plot_layout
