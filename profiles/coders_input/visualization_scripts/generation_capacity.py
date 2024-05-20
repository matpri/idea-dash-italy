import plotly.graph_objects as go
from dash import html, dcc


def render_plot(df):
    fig = go.Figure()
    df['facility_installed_capacity'] = df['facility_installed_capacity'].astype(float)
    df['latitude'] = df['latitude'].astype(float)
    df['longitude'] = df['longitude'].astype(float)

    for i, row in df.iterrows():
        fig.add_trace(go.Scattergeo(
            lon=[row['longitude']],
            lat=[row['latitude']],
            text=row['gen_type_copper'],
            mode='markers',
            marker=dict(
                size=row['facility_installed_capacity'] / 100,
                color='red',
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

    widget_layout = html.Div(['No widgets available for this visualization.'], style={'textAlign': 'center'})
    plot_layout = dcc.Graph(
        figure=render_plot(df),
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
