import pandas as pd
import geojson

import plotly.graph_objects as go

from profiles.messageix_output import utils

region_mapping = {
    'BritishColumbia': 'British Columbia',
    'Alberta': 'Alberta',
    'Saskatchewan': 'Saskatchewan',
    'Manitoba': 'Manitoba',
    'Ontario': 'Ontario',
    'Quebec': 'Quebec',
    'NewBrunswick': 'New Brunswick',
    'NovaScotia': 'Nova Scotia',
    'NewfoundlandandLabrador': 'Newfoundland and Labrador',
    'PrinceEdwardIsland': 'Prince Edward Island',
    'NorthwestTerritories': 'Northwest Territories',
    'Nunavut': 'Nunavut',
    'Yukon': 'Yukon'
}

def plot_map(message_data, scenario, time, variable='All', aggregate=False):


    rep_data = message_data[(message_data['time'] == time) & (message_data['scenario'] == scenario)]

    if aggregate:
        rep_data['variable'] = rep_data['variable'].map(utils.groups).fillna(rep_data['variable'])
    else:
        rep_data['variable'] = rep_data['variable'].map(utils.names).fillna(rep_data['variable'])

    if variable != 'All':
        rep_data = rep_data[rep_data['variable'] == variable]


    with open('./profiles/messageix_output/visualization_scripts/utils/ca.json', 'r') as f:
        map_data = geojson.load(f)

    rep_data = rep_data.groupby('region').sum().reset_index()

    rep_data['region'] = rep_data['region'].map(region_mapping)
    # drop rows where region is not in region_mapping
    rep_data = rep_data[rep_data['region'].notnull()]
    # drop scenario column
    rep_data = rep_data.drop(columns=['scenario'])

    print(rep_data[['region', 'value']])




    # Create a choropleth map using plotly.graph_objects
    fig = go.Figure(data=go.Choropleth(
        geojson=map_data,
        locations=rep_data['region'],  # Regions from the rep_data
        z=rep_data['value'],  # Assuming 'value' is the column with the data to plot
        featureidkey="properties.name",  # Key to match the GeoJSON features
        colorscale='Viridis',  # Color scale for the choropleth
    ))

    # Update geos and layout
    fig.update_geos(fitbounds="locations", visible=False, projection_type="orthographic")
    fig.update_layout(title=f'{time}')

    # Show the figure
    return fig






