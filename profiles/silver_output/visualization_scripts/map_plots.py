import dash_mantine_components as dmc
import geojson
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd
from dash import html, dcc

from profiles.silver_output.visualization_scripts.utils import total_plot, region_plot

regions = ['British Columbia', 'Alberta', 'Saskatchewan', 'Manitoba', 'Ontario', 'Quebec', 'New Brunswick',
           'Nova Scotia', 'Prince Edward Island', 'Newfoundland and Labrador', 'Yukon', 'Northwest Territories',
           'Nunavut']
with open('profiles/copper_output/visualization_scripts/utils/canada.geojson') as f:
    canada = geojson.load(f)


def render_plot(type, df, scenario, time_size='hourly'):
    print('updating map plot')
    scen_df = df[(df['scenario'] == scenario) & (df['classes'] == type)].copy()
    scen_df['time'] = pd.to_datetime(scen_df['time'])
    scen_df = scen_df.dropna(axis=1, how='all')
    # groupby time based on time_size
    if time_size == 'daily':
        scen_df['time'] = scen_df['time'].dt.strftime('%Y-%m-%d')
    elif time_size == 'monthly':
        scen_df['time'] = scen_df['time'].dt.strftime('%Y-%m')
    elif time_size == 'yearly':
        scen_df['time'] = scen_df['time'].dt.strftime('%Y')
    else:
        scen_df['time'] = scen_df['time'].dt.strftime('%Y-%m-%d %H:%M:%S')

    cols = scen_df.columns.tolist()
    # remove value column
    cols.remove('value')
    scen_df = scen_df.groupby(cols).sum(numeric_only=True).reset_index()
    
    choropleth_layer = px.choropleth(
        geojson=canada, locations=regions, featureidkey="properties.name", color=regions,
        color_discrete_map={'British Columbia': 'lightgrey', 'Alberta': 'lightgrey', 'Saskatchewan': 'lightgrey',
                            'Manitoba': 'lightgrey', 'Ontario': 'lightgrey', 'Quebec': 'lightgrey',
                            'New Brunswick': 'lightgrey',
                            'Nova Scotia': 'lightgrey', 'Prince Edward Island': 'lightgrey',
                            'Newfoundland and Labrador': 'lightgrey',
                            'Yukon': 'lightgrey', 'Northwest Territories': 'lightgrey', 'Nunavut': 'lightgrey'},
        scope='north america',
    ).data
    
    for i in range(len(choropleth_layer)):
        choropleth_layer[i].showlegend = False

    fig = go.Figure()
    
    for trace in choropleth_layer:
        fig.add_trace(trace)

    techs = scen_df['variable'].unique()
    scen_df['latitude'] = scen_df['latitude'].astype(float)
    scen_df['longitude'] = scen_df['longitude'].astype(float)
    scen_df['value'] = scen_df['value'].astype(float)

    # Create a list to store frames for animation
    frames = []

    for time in scen_df['time'].unique():
        frame_data = list(choropleth_layer)
        for tech in techs:
            tech_df = scen_df[(scen_df['variable'] == tech) & (scen_df['time'] == time)]
            frame_data.append(go.Scattergeo(
                lon=tech_df['longitude'],
                lat=tech_df['latitude'],
                text=tech_df['variable'],
                name=tech,
                mode='markers',
                marker=dict(
                    size=tech_df['value'].abs()/20,
                    opacity=0.8,
                    line=dict(width=0)
                ),
                hovertemplate='<b>Technology: %{text}</b><br> Capacity: %{marker.size:.2f} MW<br>',
                showlegend=True
            ))
        frames.append(go.Frame(data=frame_data, name=str(time)))

    # Add the initial traces to the figure
    initial_time = scen_df['time'].min()
    for tech in techs:
        tech_df = scen_df[(scen_df['variable'] == tech) & (scen_df['time'] == initial_time)]
        fig.add_trace(go.Scattergeo(
            lon=tech_df['longitude'],
            lat=tech_df['latitude'],
            text=tech_df['variable'],
            name=tech,
            mode='markers',
            marker=dict(
                size=tech_df['value']/30,
                opacity=0.8,
                line=dict(width=0)
            ),
            hovertemplate='<b>Technology: %{text}</b><br> Capacity: %{marker.size:.2f} MW<br>',
            showlegend=True
        ))

    # Update layout to include slider and buttons only if there's more than one unique date
    if len(scen_df['time'].unique()) > 1:
        fig.update_layout(
            updatemenus=[dict(
                type='buttons',
                showactive=False,
                buttons=[
                    dict(label='▶',
                         method='animate',
                         args=[None, {'frame': {'duration': 500, 'redraw': True}, 'fromcurrent': True}]),
                    dict(label='⏸',
                         method='animate',
                         args=[[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate', 'transition': {'duration': 0}}])
                ],
                pad={"r": 10, "t": 10},
                x=0.1,
                xanchor="right",
                y=0,
                yanchor="top"
            )],
            sliders=[dict(
                steps=[dict(
                    method='animate',
                    args=[[f.name], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate'}],
                    label=f.name
                ) for f in frames],
                transition={'duration': 0},
                x=0.1,
                y=0,
                currentvalue={'font': {'size': 12}, 'prefix': 'Time: ', 'visible': True, 'xanchor': 'right'},
                len=0.9
            )]
        )
        # Add frames to the figure
        fig.frames = frames

    fig.update_geos(projection_type="orthographic")
    fig.update_layout(
        title_text='Generator Locations',
        geo=dict(
            showcountries=False, showcoastlines=False, showland=False,
            fitbounds="locations", showlakes=False,
            showrivers=False,
            subunitcolor='white',
            # Enable zoom
            projection_scale=1,
            center=dict(lat=56.1304, lon=-106.3468),
            visible=True,
        ),
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        # Set legend position using dict format
        legend=dict(y=0.2),
    )
    fig.layout.autosize = True
    fig.update_layout(legend={'itemsizing': 'constant'})
    return fig

def plot(df, window_id):
    '''

    :param df: pandas Dataframe containing the data to visualize
    :param window_id: window id to use when registering components to dash
    :return: html.Div([widgets]), dcc.Graph(plot)
    '''
    scenarios = df['scenario'].unique().tolist()
    classes = df['classes'].unique().tolist()

    classes = [cls for cls in classes if 'Line Flow' not in cls]

    widget_layout = html.Div([
        dmc.Select(
            label='Plot Options',
            data=[{'label': plot, 'value': plot} for plot in classes],
            value=classes[0],
            id={
                'type': 'silver-map_plots-plot-select',
                'index': window_id
            },
        ),
        dmc.Select(
            label='Scenario',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=scenarios[0],
            id={
                'type': 'silver-map_plots-scenario-select',
                'index': window_id,
            },
            style={'display': 'block'}
        ),
        dmc.Select(
            label='Timestep',
            data=[{'label': t_step, 'value': t_step} for t_step in ['hourly', 'daily', 'monthly', 'yearly']],
            value='hourly',
            id={
                'type': 'silver-map_plots-time_step-select',
                'index': window_id,
            },
            style={'display': 'block'}
        ),

        dmc.Button('Download Data', id={'type': 'silver-map_plots-download-button', 'index': window_id},
                   variant='light',
                   # center the button
                   style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
        dcc.Download(id={'type': 'silver-map_plots-download', 'index': window_id}),
    ])

    plot_layout = dcc.Graph(
        figure=render_plot(classes[0], df, scenarios[0]),
        id={
            'type': 'figure',
            'index': window_id,
            'profile': 'silver_output',
            'viz': 'map_plots'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )

    return widget_layout, plot_layout
