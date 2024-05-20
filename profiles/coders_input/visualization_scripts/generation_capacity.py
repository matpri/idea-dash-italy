import dash_mantine_components as dmc
import plotly.graph_objects as go
from dash import html, dcc

from profiles.coders_input import utils


def map_color(tech, aggregate):
    if aggregate:
        return utils.get_group_colors(tech)
    else:
        return utils.get_color(tech)


def render_plot(df, aggregate):
    fig = go.Figure()
    df['facility_installed_capacity'] = df['facility_installed_capacity'].astype(float)
    df['latitude'] = df['latitude'].astype(float)
    df['longitude'] = df['longitude'].astype(float)

    if aggregate:
        df['gen_type_copper'] = df['gen_type_copper'].apply(lambda x: utils.get_group(x))

    df['color'] = df['gen_type_copper'].apply(lambda x: map_color(x, aggregate))

    for i, row in df.iterrows():
        fig.add_trace(go.Scattergeo(
            lon=[row['longitude']],
            lat=[row['latitude']],
            text=row['gen_type_copper'],
            mode='markers',
            marker=dict(
                size=row['facility_installed_capacity'] / 100,
                color=row['color'],
                opacity=0.8,
                line=dict(width=0)
            )
        ))

    fig.update_geos(projection_type="natural earth")
    fig.update_layout(
        title_text='Generator Locations',
        showlegend=False,
        geo=dict(
            showland=True,
            landcolor="rgb(243, 243, 243)",
            countrycolor="rgb(204, 204, 204)",
        ),
    )

    return fig


def plot(df, window_id):
    '''

    :param df: pandas Dataframe containing the data to visualize
    :param window_id: window id to use when registering components to dash
    :return: html.Div([widgets]), dcc.Graph(plot)
    '''

    widget_layout = html.Div(
        [
            dmc.Switch('Aggregate',
                       checked=True,
                       id={
                           'type': 'coders_input-gencap-aggregate-switch',
                           'index': window_id}
                       ),
        ],
        style={'textAlign': 'center'})
    plot_layout = dcc.Graph(
        figure=render_plot(df, True),
        id={
            'type': 'figure',
            'index': window_id,
            'profile': 'coders_input',
            'viz': 'gencap'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )

    return widget_layout, plot_layout
