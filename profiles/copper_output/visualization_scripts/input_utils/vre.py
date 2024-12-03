from dash import html
import dash_mantine_components as dmc
import plotly.graph_objects as go
import geopandas as gpd


def create_widgets(df, classes, window_id):
    seasons = []
    vre_variables = []
    vre_scenario = []
    if 'Vre Capacity Factors' in classes:
        seasons = ['Winter', 'Summer']
        vre_variables = ['Wind', 'Solar']
        vre_scenario = df[df['variable'].str.startswith('Vre Capacity Factors')]['scenario'].unique()

    vre_widget_layout = html.Div([

        dmc.Select(
            label='Scenario',
            data=[{'label': scenario, 'value': scenario} for scenario in vre_scenario],
            value=vre_scenario[0] if len(vre_scenario) else '',
            id={
                'type': 'copper-inputs-vre-scenario-select',
                'index': window_id
            },
        ),
        dmc.Select(
            label='Season',
            data=[{'label': season, 'value': season} for season in seasons],
            value=seasons[0] if len(seasons) else '',
            id={
                'type': 'copper-inputs-season-select',
                'index': window_id
            },
        ),
        dmc.Select(
            label='VRE Variable',
            data=[{'label': vre_variable, 'value': vre_variable} for vre_variable in vre_variables],
            value=vre_variables[0] if len(vre_variables) else '',
            id={
                'type': 'copper-inputs-vre-variable-select',
                'index': window_id
            },
        )
    ],
        style={'display': 'none'},
        id={
            'type': 'copper-inputs-vre-widget',
            'index': window_id
        }
    )
    return vre_widget_layout



def render(grid, variable, season, title, x_label, y_label, scenario, name, unit):

    grid = grid[grid['variable'] == variable]
    grid = grid[grid['time'] == season]
    grid = grid[grid['scenario'].isin(scenario)]

    # Check if grid is empty after filtering
    if grid.empty:
        fig = go.Figure()
        # add annotations
        fig.add_annotation(
            text="No data available for the selected variable and season",
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            font=dict(size=20),
            align='center',
            ax=0,
            ay=0,
        )
        return fig

    # convert the polygons to json
    grid = grid[['geometry', 'value', 'prov', 'region']]

    gdf = gpd.GeoDataFrame(grid, geometry='geometry')

    # Convert GeoDataFrame to GeoJSON
    geojson = gdf.__geo_interface__
    fig = go.Figure(
        go.Choroplethmapbox(
            geojson=geojson, locations=gdf['region'], z=gdf['value'],
            featureidkey="properties.region",
            customdata=gdf['prov'],
            colorscale='Inferno',
            marker_line_width=0,  # Add this line here to remove grid outlines
            hovertemplate=f"Variable: {variable}<br>Season: {season}<br>" + 'Value: %{z}<extra></extra>'
        )
    )

    # update layout
    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=2.5, mapbox_center={"lat": 54.0902, "lon": -95.7129},
        geo=dict(
            showframe=False,
            bgcolor='rgba(0,0,0,0)'),

    )


    fig.update_layout(title=title, xaxis_title=x_label, yaxis_title=y_label)

    fig.update_geos(projection_type="orthographic")
    fig.layout.template = None
    return fig