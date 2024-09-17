import dash_mantine_components as dmc
import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc

patterns = ['solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot']
colors = ['rgba(31, 119, 180, 0.3)', 'rgba(255, 127, 14, 0.3)', 'rgba(44, 160, 44, 0.3)', 'rgba(214, 39, 40, 0.3)',
          'rgba(148, 103, 189, 0.3)', 'rgba(140, 86, 75, 0.3)', 'rgba(227, 119, 194, 0.3)', 'rgba(127, 127, 127, 0.3)',]
scenario_colors = {}
scenario_patterns = {}
model_colors = {}
model_patterns = {}

def color_to_rgba(color, alpha=0.2):
    import colorsys
    h, l, s = color[4:-1].split(', ')
    h = float(h) / 360  # Convert degree to ratio
    l = float(l[:-1]) / 100  # Remove '%' and convert percentage to ratio
    s = float(s[:-1]) / 100  # Remove '%' and convert percentage to ratio
    r, g, b = [x * 255.0 for x in colorsys.hls_to_rgb(h, l, s)]
    return f"rgba({int(r)},{int(g)},{int(b)},{alpha})"

def get_scenario_color(scenario, alpha=0.8):
    if scenario not in scenario_colors:
        if len(scenario_colors) >= len(colors):
            hue = (len(scenario_colors) * 360 / 20) % 360   # More shades of base colors
            saturation = 50 + (len(scenario_colors) * 15 % 50)  # Varying saturation
            lightness = 50 + (len(scenario_colors) * 15 % 50)  # Varying lightness
            scenario_colors[scenario] = f"hsl({hue}, {saturation}%, {lightness}%)"
        else:
            scenario_colors[scenario] = colors[len(scenario_colors)]
    color = scenario_colors[scenario]
    return color

def get_model_color(model, alpha=0.8):
    alpha = round(alpha, 1)
    if model not in model_colors:
        if len(model_colors) >= len(colors):
            hue = (len(model_colors) * 360 / 20) % 360
            saturation = 50 + (len(model_colors) * 15 % 50)
            lightness = 50 + (len(model_colors) * 15 % 50)
            model_colors[model] = color_to_rgba(f"hsl({hue}, {saturation}%, {lightness}%)")
        else:
            model_colors[model] = colors[len(model_colors)]
    color = model_colors[model]

    return color


def get_scenario_pattern(scenario):
    if scenario not in scenario_patterns:
        scenario_patterns[scenario] = patterns[len(scenario_patterns) % len(patterns)]
    return scenario_patterns[scenario]


def get_model_pattern(model):
    if model not in model_patterns:
        model_patterns[model] = patterns[len(model_patterns) % len(patterns)]
    return model_patterns[model]


def render_plot(type, df, group_by_model, group_by_scenario, group_by_version, can=True, fill=True):
    from profiles.energy_model.utils import plot_settings
    #print('rendering plot', type)
    df = df[df.variable == type].copy()

    if can:
        df = df[df.region == 'CAN']
    else:
        df = df[df.region == 'AB+QC']

    plot_info = plot_settings['Overview'][type]
    name = plot_info['name']
    unit = plot_info['unit']
    return plot_overview(df, group_by_model, group_by_scenario, group_by_version, plot_info['title'], plot_info['x_label'],
                         plot_info['y_label'], name, unit, fill)


def plot_overview(df, group_by_model, group_by_scenario, group_by_version, title, x_label, y_label, name, unit, fill=True):
    fig = go.Figure()
    fig.update_layout(
        title_text=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        template="simple_white",
    )
    try:
        # sort df by time
        # make time int
        df.time = df.time.astype(int)
        df = df.sort_values(by=['time'])

        if group_by_model:
            df[['model', 'scenario']] = df['scenario'].apply(lambda x: pd.Series([x.split('|')[0], '|'.join(x.split('|')[1:])]))
            models = df.model.unique().tolist()
            for model in models:
                data = df[df.model == model]
                for i, scenario in enumerate(data.scenario.unique().tolist()):
                    data_scenario = data[data.scenario == scenario]
                    data_scenario = data_scenario.sort_values(by=['time'])
                    pattern = get_scenario_pattern(scenario)
                    fig.add_scatter(x=data_scenario["time"], y=data_scenario["value"], name=f'{model} - {scenario}',
                                    mode='lines+markers',
                                    line=dict(color=get_model_color(model),
                                              dash=pattern,
                                              width=2),
                                    fill=None if i == 0 or not fill else 'tonexty',
                                    fillcolor=get_model_color(model, 0.2),
                                    hovertemplate=f'<b>{model} - {scenario}</b><br><br>' + 'Year: %{x}<br>' + f'{name}' + ': %{y:.2f} ' + f'{unit}' + '<br><extra></extra>')
        elif group_by_scenario:
            df[['model', 'scenario']] = df['scenario'].apply(lambda x: pd.Series([x.split('|')[0], '|'.join(x.split('|')[1:])]))

            scenarios = df.scenario.unique().tolist()
            for scenario in scenarios:
                data = df[df.scenario == scenario]
                sub_fig = go.Figure()
                for i, model in enumerate(data.model.unique().tolist()):
                    scen, version = ('|'.join(scenario.split('|')[:-1]), scenario.split('|')[-1]) if '|' in scenario else (scenario, '')
                    data_model = data[data.model == model]
                    data_model = data_model.sort_values(by=['time'])
                    pattern = get_model_pattern(model)
                    sub_fig.add_scatter(x=data_model["time"], y=data_model["value"], name=f'{model} - {scenario}',
                                        mode='lines+markers',
                                        line=dict(color=get_scenario_color(scen),
                                                  dash=pattern,
                                                  width=2,
                                                  ),
                                        fill=None if i == 0 or not fill else 'tonexty',
                                        fillcolor=get_scenario_color(scen, 0.2),
                                        hovertemplate=f'<b>{model} - {scenario}</b><br><br>' + 'Year: %{x}<br>' + f'{name}' + ': %{y:.2f} ' + f'{unit}' + '<br><extra></extra>')
                fig.add_traces(data=sub_fig.data)
        elif group_by_version:
            versions = df.version.unique().tolist()
            for version in versions:
                data = df[df.version == version]
                data[['model', 'scenario']] = data['scenario'].apply(lambda x: pd.Series([x.split('|')[0], '|'.join(x.split('|')[1:])]))
                data['scenario'] = data['scenario'].apply(lambda x: '|'.join(x.split('|')[:-1]) if len(x.split('|')) > 1 else x)
                sub_fig = go.Figure()
                for i, model in enumerate(data.model.unique().tolist()):
                    data_model = data[data.model == model]
                    data_model = data_model.sort_values(by=['time'])
                    pattern = get_model_pattern(model)
                    for scenario in data_model.scenario.unique().tolist():
                        data_scenario = data_model[data_model.scenario == scenario]
                        sub_fig.add_scatter(x=data_scenario["time"], y=data_scenario["value"], name=f'{model} - {scenario} - {version}',
                                            mode='lines+markers',
                                            line=dict(color=get_scenario_color(version),
                                                      dash=pattern,
                                                      width=2,
                                                      ),
                                            fill=None if i == 0 or not fill else 'tonexty',
                                            fillcolor=get_scenario_color(version, 0.2),
                                            hovertemplate=f'<b>{model} - {scenario} - {version}</b><br><br>' + 'Year: %{x}<br>' + f'{name}' + ': %{y:.2f} ' + f'{unit}' + '<br><extra></extra>')
                fig.add_traces(data=sub_fig.data)

        else:
            scenarios = df.scenario.unique().tolist()
            for scenario in scenarios:
                data = df[df.scenario == scenario]
                data = data.sort_values(by=['time'])

                fig.add_scatter(x=data["time"], y=data["value"], name=scenario, mode='lines+markers',
                                hovertemplate=f'<b>{scenario}</b><br><br>' + 'Year: %{x}<br>' + f'{name}' + ': %{y:.2f} ' + f'{unit}' + '<br><extra></extra>')

        fig.update_yaxes(showgrid=True)
        if df.empty:
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
    except Exception as e:
        print(title, 'plot:', e)

    fig.layout.autosize = True
    return fig


def plot(df, window_id):
    '''

    :param df: pandas Dataframe containing the data to visualize
    :param window_id: window id to use when registering components to dash
    :return: html.Div([widgets]), dcc.Graph(plot)
    '''
    classes = df['variable'].unique().tolist()

    scenarios = df['scenario'].unique().tolist()

    base_scenarios = list(set([scenario.split('|')[1] for scenario in scenarios]))
    base_scenarios = ['ALL'] + base_scenarios

    widget_layout = html.Div([
        dmc.Select(
            label='Plot Options',
            data=[{'label': plot, 'value': plot} for plot in classes],
            value=classes[0],
            id={
                'type': 'energy_model-overview-plot-select',
                'index': window_id
            },
        ),
        dmc.Select(
            label='Group By',
            value=0,
            data=[
                {'label': 'No Grouping', 'value': 0},
                {'label': 'Group by Model', 'value': 1},
                {'label': 'Group by Scenario', 'value': 2},
                {'label': 'Group by Version', 'value': 3},
            ],
            id={
                'type': 'energy_model-overview-groupby-toggle',
                'index': window_id,
            },
        ),
        dmc.Select(
            label='Scenario Group',
            data=[{'label': scenario, 'value': scenario} for scenario in base_scenarios],
            value='ALL',
            id={
                'type': 'energy_model-overview-scenario-group-select',
                'index': window_id,
            },
            style={'display': 'block'}
        ),
        dmc.Select(
            label='Region',
            value='CAN',
            data=[
                {'label': 'CAN', 'value': 'CAN'},
                {'label': 'AB+QC', 'value': 'AB+QC'},
            ],
            id={
                'type': 'energy_model-overview-region-toggle',
                'index': window_id,
            },
        ),
        dmc.Switch(
            label='Fill Area',
            checked=True,
            id={
                'type': 'energy_model-overview-fill-switch',
                'index': window_id,
            },
        ),

        dmc.Button('Download Data', id={'type': 'energy_model-overview-download-button', 'index': window_id},
                   variant='light',
                   # center the button
                   style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
        dcc.Download(id={'type': 'energy_model-overview-download', 'index': window_id}),
    ])

    plot_layout = dcc.Graph(
        figure=render_plot(classes[0], df, False, False, False),
        id={
            'type': 'figure',
            'index': window_id,
            'profile': 'energy_model',
            'viz': 'overview'
        },
        style={
            'width': '100%',
            'height': '100%'
        }

    )

    return widget_layout, plot_layout
