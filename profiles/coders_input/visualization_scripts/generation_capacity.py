import dash_mantine_components as dmc
import geojson
import plotly.express as px
import plotly.graph_objects as go
from dash import html, dcc

from profiles.coders_input import utils


def map_color(tech, aggregate):
    if aggregate:
        return utils.get_group_colors(tech)
    else:
        return utils.get_color(tech)


regions = ['British Columbia', 'Alberta', 'Saskatchewan', 'Manitoba', 'Ontario', 'Quebec', 'New Brunswick',
           'Nova Scotia', 'Prince Edward Island', 'Newfoundland and Labrador', 'Yukon', 'Northwest Territories',
           'Nunavut']

with open('profiles/copper_output/visualization_scripts/utils/canada.geojson') as f:
    canada = geojson.load(f)

def render_plot(df, aggregate):

    fig_base = px.choropleth(
        geojson=canada, locations=regions, featureidkey="properties.name", color=regions,
        color_discrete_map={'British Columbia': 'lightgrey', 'Alberta': 'lightgrey', 'Saskatchewan': 'lightgrey',
                            'Manitoba': 'lightgrey', 'Ontario': 'lightgrey', 'Quebec': 'lightgrey',
                            'New Brunswick': 'lightgrey',
                            'Nova Scotia': 'lightgrey', 'Prince Edward Island': 'lightgrey',
                            'Newfoundland and Labrador': 'lightgrey',
                            'Yukon': 'lightgrey', 'Northwest Territories': 'lightgrey', 'Nunavut': 'lightgrey'},
        scope='north america',
    )
    fig_base.update_geos(projection_type="natural earth")

    fig = go.Figure(
        data=fig_base.data,
        layout=go.Layout(
        )
    )

    if aggregate:
        df['gen_type_copper'] = df['gen_type_copper'].apply(lambda x: utils.get_group(x))
    else:
        df['gen_type_copper'] = df['gen_type_copper'].apply(lambda x: utils.get_name(x))

    df['facility_installed_capacity'] = df['facility_installed_capacity'].astype(float)
    df['latitude'] = df['latitude'].astype(float)
    df['longitude'] = df['longitude'].astype(float)



    df['color'] = df['gen_type_copper'].apply(lambda x: map_color(x, aggregate))

    techs = df['gen_type_copper'].unique()

    for tech in techs:
        tech_df = df[df['gen_type_copper'] == tech]
        fig.add_trace(go.Scattergeo(
            lon=tech_df['longitude'],
            lat=tech_df['latitude'],
            text=tech_df['gen_type_copper'],
            name=tech_df['gen_type_copper'].unique()[0],
            mode='markers',
            marker=dict(
                size=tech_df['facility_installed_capacity'] / 50,
                color=map_color(tech, aggregate),
                opacity=0.8,
                line=dict(width=0)
            ),
            hovertemplate='<b>Technology: %{text}</b><br> Capacity: %{marker.size:.2f} MW<br>'
        ))

    fig.update_geos(projection_type="natural earth")
    fig.update_layout(
        title_text='Generator Locations',
        showlegend=True,
        geo=dict(
            showcountries=False, showcoastlines=False, showland=False,
            fitbounds="locations", showlakes=False,
            showrivers=False,
            subunitcolor='white'
        ),
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )

    fig.layout.autosize = True
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
            dmc.Button('Download Data', id={'type': 'coders_input-gencap-download-button', 'index': window_id},
                       variant='light',
                       # center the button
                       style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
            dcc.Download(id={'type': 'coders_input-gencap-download', 'index': window_id}),
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
