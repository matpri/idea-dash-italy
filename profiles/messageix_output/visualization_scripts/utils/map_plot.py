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

centroids = {
  "Alberta": {
    "lat": 53.9333,
    "lon": -116.5765
  },
  "British Columbia": {
    "lat": 53.7267,
    "lon": -127.6476
  },
  "Manitoba": {
    "lat": 49.8951,
    "lon": -97.1384
  },
  "New Brunswick": {
    "lat": 46.5653,
    "lon": -66.4619
  },
  "Newfoundland and Labrador": {
    "lat": 53.1355,
    "lon": -57.6604
  },
  "Nova Scotia": {
    "lat": 44.6820,
    "lon": -63.7443
  },
  "Ontario": {
    "lat": 51.2538,
    "lon": -85.3232
  },
  "Prince Edward Island": {
    "lat": 46.5107,
    "lon": -63.4168
  },
  "Quebec": {
    "lat": 52.9399,
    "lon": -71.2092
  },
  "Saskatchewan": {
    "lat": 52.1332,
    "lon": -106.6700
  },
  "Yukon": {
    "lat": 64.2823,
    "lon": -140.9984
  },
  "Northwest Territories": {
    "lat": 64.8255,
    "lon": -113.4732
  },
  "Nunavut": {
    "lat": 70.2998,
    "lon": -83.1076
  }
}


def plot_map(message_data, scenario, time, title, name, unit, variable='All', aggregate=False, is_emissions=False):

    title = f'{title} - {scenario} - in {time}'

    rep_data = message_data[(message_data['time'] == time) & (message_data['scenario'] == scenario)]

    if aggregate:
        rep_data['variable'] = rep_data['variable'].map(utils.groups).fillna(rep_data['variable'])
    else:
        rep_data['variable'] = rep_data['variable'].map(utils.names).fillna(rep_data['variable'])

    if variable != 'All':
        if is_emissions:
            rep_data = rep_data[rep_data['variable'].str.contains(variable)]
        else:
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
        colorscale='Blues',  # Color scale for the choropleth
        hovertemplate='%{location}: %{z}' + f'({unit})',  # Hover template
    ))

    # Overlay a scatter plot using centroids for annotations
    scatter_data = []
    min_value = rep_data['value'].min()
    max_value = rep_data['value'].max()
    for index, row in rep_data.iterrows():
        region = row['region']
        if region in centroids:
            # Round the value to three significant figures
            value_rounded = round(row['value'], 3)
            # Normalize the value for better visibility
            normalized_value = (value_rounded - min_value) / (max_value - min_value) if (max_value - min_value) != 0 else 0
            font_color = 'white' if normalized_value > 0.5 else 'black'  # Adjust threshold as needed
            scatter_data.append(go.Scattergeo(
                lon=[centroids[region]['lon']],
                lat=[centroids[region]['lat']],
                text=f"{value_rounded} ({unit})",
                mode='markers+text',
                marker=dict(size=4, color='black'),
                textposition="top center",
                textfont=dict(color=font_color, size=10), # Set the font color based on normalized value
                showlegend=False
            ))

    # Add scatter data to the figure
    for scatter in scatter_data:
        fig.add_trace(scatter)

    # Update geos and layout
    fig.update_geos(fitbounds="locations", visible=False, projection_type="orthographic")
    fig.update_layout(title=title)

    # Show the figure
    return fig
