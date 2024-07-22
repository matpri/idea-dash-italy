import dash_mantine_components as dmc
import plotly.graph_objects as go
from dash import html, dcc


def render_plot(type, df, show_sectors, scenario):
    from profiles.cims_output.utils import plot_settings
    df = df[df.variable == type].copy()
    plot_settings = plot_settings['Overview'][type]

    return plot_overview(df, type, plot_settings['x_label'], plot_settings['y_label'], plot_settings['name'],
                         plot_settings['unit'], show_sectors, scenario)


def plot_overview(df, title, x_label, y_label, name, unit, show_sectors, scenario):
    fig = go.Figure()
    fig.update_layout(
        title_text=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        template="simple_white",
    )
    try:

        if show_sectors:
            df_scen = df[df.scenario == scenario]
            sectors = df_scen.sector.unique().tolist()
            for sector in sectors:
                data = df_scen[df_scen.sector == sector]
                data = data.sort_values(by=['time'])
                fig.add_scatter(x=data["time"], y=data["value"], name=sector, mode='lines+markers',
                                hovertemplate=f'<b>{sector}</b><br><br>' + 'Year: %{x}<br>' + f'{name}' + ': %{y:.2f} ' + f'{unit}' + '<br><extra></extra>')
        else:

            scenarios = df.scenario.unique().tolist()
            df_viz = df.copy()
            df_viz = df_viz.groupby(['scenario', 'time']).sum(numeric_only=True).reset_index()
            for scenario in scenarios:
                data = df_viz[df_viz.scenario == scenario]
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


def plot(df, window_id):
    '''

    :param df: pandas Dataframe containing the data to visualize
    :param window_id: window id to use when registering components to dash
    :return: html.Div([widgets]), dcc.Graph(plot)
    '''
    # print('plotting overview')
    classes = df['variable'].unique().tolist()
    scenarios = df['scenario'].unique().tolist()

    widget_layout = html.Div([
        dmc.Select(
            label='Plot Options',
            data=[{'label': plot, 'value': plot} for plot in classes],
            value=classes[0],
            id={
                'type': 'cims-overview-plot-select',
                'index': window_id
            },
        ),
        dmc.Switch(
            label='Show Sectors',
            id={'type': 'cims-overview-show-sectors', 'index': window_id},
            checked=False
        ),
        dmc.Select(
            'Select Scenario',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=scenarios[0],
            id={'type': 'cims-overview-scenario-select', 'index': window_id},
            style={'display': 'none'}
        ),

        dmc.Button('Download Data', id={'type': 'cims-overview-download-button', 'index': window_id},
                   variant='light',
                   # center the button
                   style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
        dcc.Download(id={'type': 'cims-overview-download', 'index': window_id}),
    ])

    plot_layout = dcc.Graph(
        figure=render_plot(classes[0], df, show_sectors=False, scenario=scenarios[0]),
        id={
            'type': 'figure',
            'index': window_id,
            'profile': 'cims_output',
            'viz': 'overview'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )
    return widget_layout, plot_layout
