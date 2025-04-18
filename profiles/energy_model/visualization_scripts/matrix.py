import dash_mantine_components as dmc
import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc
from components import ids
from plotly.subplots import make_subplots

from profiles.energy_model import utils


def render_plot(type, df, scenarios, aggregate, region):
    from profiles.energy_model.utils import plot_settings
    #print('rendering plot', type)
    df = df[df.variable.str.startswith(type + '|')]
    df = df[df.region == region]

    plot_info = plot_settings['Matrix'][type]
    name = plot_info['name']
    unit = plot_info['unit']
    return plot_matrix(df, type, scenarios, aggregate, plot_info['title'], plot_info['x_label'], plot_info['y_label'],
                       name, unit)


def plot_matrix(base_df, variable, scenarios, aggregate, title, x_label, y_label, name, unit):
    if len(scenarios) == 0:
        fig = go.Figure()
        fig.add_annotation(
            x=0.5,
            y=0.5,
            text="Please select at least one scenario",
            showarrow=False,
            font=dict(
                size=16,
                color="black"
            ),
            align="center",
            valign="middle",
        )
        return fig
    fig = make_subplots(rows=len(scenarios), cols=len(scenarios), shared_xaxes=True, shared_yaxes=True,
                        vertical_spacing=0.02, horizontal_spacing=0.02,
                        subplot_titles=[scenario for scenario in scenarios])
    base_df = base_df[base_df['variable'].str.startswith(variable)]
    base_df['variable'] = base_df['variable'].str.replace(variable + '|', '')
    if aggregate:
        base_df['variable'] = base_df["variable"].map(utils.get_group).fillna(base_df["variable"])
        base_df = base_df.groupby(["variable", "time", 'scenario']).sum(numeric_only=True).reset_index()
    else:
        base_df['variable'] = base_df["variable"].map(utils.get_name).fillna(base_df["variable"])
        base_df = base_df.groupby(["variable", "time", 'scenario']).sum(numeric_only=True).reset_index()

    if base_df[base_df['scenario'].isin(scenarios)].empty:
        #print("No data available, since the results are all zero.")
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

    dfs = [base_df[(base_df['scenario'] == scenario)] for scenario in scenarios]
    fig.update_layout(
        title_text=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        template="simple_white",
    )
    try:
        for i, scenario in enumerate(dfs):
            for j, other_scenario in enumerate(dfs):
                if i == j:
                    df = scenario
                    df = df.groupby(['time', 'variable']).sum(numeric_only=True).reset_index()
                    scen = scenario['scenario'].unique()[0]
                    subfig = go.Figure()
                    for tech in df['variable'].unique():
                        tech_df = df[df['variable'] == tech]
                        if aggregate:
                            color = utils.get_group_colors(tech)
                        else:
                            color = utils.get_color(tech)
                        subfig.add_bar(x=tech_df['time'], y=tech_df['value'], name=tech, marker_color=color,
                                       hovertemplate=f'{scen}<br>Technology: {tech}<br>'
                                                     + 'Year: %{x}<br>Value: %{y:.2f}', legendgroup=tech,
                                       legendgrouptitle_text=tech)
                    subfig.update_layout(barmode='relative', legend_traceorder="reversed")
                    subfig.update_yaxes(showgrid=True)
                    for trace in subfig.data:
                        fig.add_trace(trace, row=i + 1, col=j + 1)
                    fig.update_layout(barmode='relative', legend_traceorder="reversed")
                else:
                    df = scenario
                    df = df.groupby(['time']).sum(numeric_only=True).reset_index()
                    other_df = other_scenario
                    other_df = other_df.groupby(['time', 'variable']).sum(numeric_only=True).reset_index()
                    diff = pd.merge(df, other_df, on=['time'], suffixes=('_base', '_test'), how='outer')
                    diff['value'] = diff.value_test.fillna(0) - diff.value_base.fillna(0)

                    scen = scenario['scenario'].unique()[0]
                    other_scen = other_scenario['scenario'].unique()[0]

                    subfig = go.Figure()
                    for tech in diff['variable'].unique():
                        tech_diff = diff[diff['variable'] == tech]
                        if aggregate:
                            color = utils.get_group_colors(tech)
                        else:
                            color = utils.get_color(tech)
                        subfig.add_bar(x=tech_diff['time'], y=tech_diff['value'], name=tech, marker_color=color,
                                       hovertemplate=f'{scen} - {other_scen}<br>Technology: {tech}<br>'
                                                     + 'Year: %{x}<br>Difference: %{y:.2f}', legendgroup=tech,
                                       legendgrouptitle_text=tech)
                    subfig.update_layout(barmode='relative', legend_traceorder="reversed")
                    subfig.update_yaxes(showgrid=True)
                    for trace in subfig.data:
                        fig.add_trace(trace, row=i + 1, col=j + 1)
                    fig.update_layout(barmode='relative', legend_traceorder="reversed")

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
    #print('plotting matrix')
    classes = df['variable'].str.split('|', expand=True)[0].unique().tolist()
    regions = df['region'].unique().tolist()

    widget_layout = html.Div([
        dmc.Select(
            label='Plot Options',
            data=[{'label': plot, 'value': plot} for plot in classes],
            value=classes[0],
            id={
                'type': 'energy_model-matrix-plot-select',
                'index': window_id
            },
        ),
        dmc.MultiSelect(
            label='Scenarios',
            data=[{'label': scenario, 'value': scenario} for scenario in df['scenario'].unique()],
            value=[],
            id={
                'type': 'energy_model-matrix-scenario-select',
                'index': window_id
            },
        ),
        dmc.Switch(
            label='Aggregate',
            checked=True,
            id={
                'type': 'energy_model-matrix-aggregate-switch',
                'index': window_id,
            },
        ),
        dmc.Select(
            label='Region',
            data=[{'label': region, 'value': region} for region in regions],
            value='CAN' if 'CAN' in regions else regions[0],
            id={
                'type': 'energy_model-matrix-region-select',
                'index': window_id
            },
        ),
        dmc.Button('Download Data', id={'type': 'energy_model-matrix-download-button', 'index': window_id},
                   variant='light',
                   # center the button
                   style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
        dcc.Download(id={'type': 'energy_model-matrix-download', 'index': window_id}),
    ])

    plot_layout = dcc.Graph(
        figure=render_plot(classes[0], df, [], True, 'CAN' if 'CAN' in regions else regions[0]),
        id={
            'type': ids.FIGURE,
            'index': window_id,
            'profile': 'Power System Models',
            'viz': 'Comparison Matrix'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )
    return widget_layout, plot_layout
