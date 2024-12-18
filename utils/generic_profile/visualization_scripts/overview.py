import dash_mantine_components as dmc
import plotly.graph_objects as go
from dash import html, dcc

from components import ids


def render_plot(type, df, unit):
    df = df[df.variable == type].copy()
    df = df[df.unit == unit]
    return plot_overview(df, type, 'Year', type, type, unit)


def plot_overview(df, title, x_label, y_label, name, unit):
    fig = go.Figure()
    fig.update_layout(
        title_text=f'Overview of {title}',
        xaxis_title=x_label,
        yaxis_title=y_label + f' ({unit})' if unit != 'NA' else y_label,
        template="simple_white",
    )
    try:

        scenarios = df.scenario.unique().tolist()

        for scenario in scenarios:
            data = df[df.scenario == scenario]
            data = data.sort_values(by=['time'])

            fig.add_scatter(x=data["time"], y=data["value"], name=scenario, mode='lines+markers',
                            hovertemplate=f'<b>{scenario}</b><br><br>' + 'Year: %{x}<br>' + f'{name}' + ': %{y:.2f} ' + f'{unit}' + '<br><extra></extra>')

        fig.update_yaxes(showgrid=True)
        if df.empty:
            # print("No data available, since the results are all zero.")
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


def create_overview_plot(model, is_comparison=False):
    def plot(df, window_id):
        '''

        :param df: pandas Dataframe containing the data to visualize
        :param window_id: window id to use when registering components to dash
        :return: html.Div([widgets]), dcc.Graph(plot)
        '''
        # print('plotting overview')
        classes = df['variable'].unique().tolist()
        units = df[df['variable'] == classes[0]]['unit'].unique().tolist()

        comparison_widgets = []
        if is_comparison:
            base_scenarios = df['base_scenario'].unique().tolist()
            base_scenarios = ['ALL'] + base_scenarios

            comparison_widgets = [
                dmc.Select(
                    label='Scenario Group',
                    data=[{'label': scenario, 'value': scenario} for scenario in base_scenarios],
                    value='ALL',
                    id={
                        'type': 'scenario-group-select',
                        'model': model,
                        'index': window_id,
                        'viz': 'overview'
                    },
                    style={'display': 'block'}
                ),
            ]

        widget_layout = html.Div([
            dmc.Select(
                label='Plot Options',
                data=[{'label': plot, 'value': plot} for plot in classes],
                value=classes[0],
                id={
                    'type': 'plot-select',
                    'model': model,
                    'index': window_id,
                    'viz': 'overview'
                },
            ),

            *comparison_widgets,

            dmc.Select(
                label='Unit',
                data=[{'label': unit, 'value': unit} for unit in units],
                value=units[0],
                id={
                    'type': 'unit-select',
                    'model': model,
                    'index': window_id,
                    'viz': 'overview'
                },
            ),
            dmc.Button('Download Data', id={'type': 'download-button', 'index': window_id, 'model': model,
                                            'viz': 'overview'},
                       variant='light',
                       # center the button
                       style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
            dcc.Download(id={'type': 'download', 'index': window_id, 'model': model,
                             'viz': 'overview'}),
        ])

        plot_layout = dcc.Graph(
            figure=render_plot(classes[0], df, units[0]),
            id={
                'type': ids.FIGURE,
                'index': window_id,
                'model': model,
                'viz': 'overview'
            },
            style={
                'width': '100%',
                'height': '100%'
            }
        )
        return widget_layout, plot_layout

    return plot
