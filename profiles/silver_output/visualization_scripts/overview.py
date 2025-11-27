import dash_mantine_components as dmc
import plotly.graph_objects as go
from dash import html, dcc
from components import ids

def render_plot(type, df, can=True):
    from profiles.silver_output.utils import plot_settings
    #print('rendering plot', type)
    df = df[df.variable == type].copy()

    plot_info = plot_settings['Overview'][type]
    name = plot_info['name']
    unit = plot_info['unit']
    return plot_overview(df, plot_info['total']['title'], plot_info['total']['x_label'], plot_info['total']['y_label'], name, unit)


def plot_overview(df, title, x_label, y_label, name, unit):
    fig = go.Figure()
    fig.update_layout(
        title_text=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
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
    #print('plotting overview')
    classes = df['variable'].unique().tolist()

    widget_layout = html.Div([
        dmc.Select(
            label='Plot Options',
            data=[{'label': plot, 'value': plot} for plot in classes],
            value=classes[0],
            id={
                'type': 'silver-overview-plot-select',
                'index': window_id
            },
        ),
        dmc.Button('Download Data', id={'type': 'silver-overview-download-button', 'index': window_id},
                   variant='light',
                   # center the button
                   style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
        dcc.Download(id={'type': 'silver-overview-download', 'index': window_id}),
    ])

    plot_layout = dcc.Graph(
        figure=render_plot(classes[0], df),
        id={
            'type': ids.FIGURE,
            'index': window_id,
            'profile': 'SILVER',
            'viz': 'Overview'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )
    return widget_layout, plot_layout
