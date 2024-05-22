import pandas as pd
import os
import geopandas as gpd

from profiles.coders_input import utils


def check(df):
    """
    Check if 'Results_summary_carbon_AP_tech' is present in the 'variable' column.

    Parameters:
        df (pd.DataFrame): The DataFrame to check.

    Returns:
        bool: True if the specified prefix is found, False otherwise.
    """
    print("Checking for emissions in variable column")
    try:
        if (df.model == 'CODERS').any():
            if 'Generation Capacity' in df.type.unique():
                return True
        return False
    except Exception as e:
        print("Emission check", e)
        return False

def process(selected: dict):
    dfs = []
    for scenario_name, db in selected.items():
        df = db.copy()
        # filter where 'Results_summary_carbon_AP_tech|' in variable column entry and remove the prefix
        df = df[df.type == 'Generation Capacity']
        df = df.groupby(['generation_facility_code']).first().reset_index()
        # sort by capacity
        df = df.sort_values('facility_installed_capacity', ascending=False)
        df['scenario'] = scenario_name
        dfs.append(df)
    full_df = pd.concat(dfs)

    geometry = gpd.points_from_xy(full_df.longitude, full_df.latitude)
    full_gdf = gpd.GeoDataFrame(full_df, geometry=geometry)
    full_gdf.set_crs("EPSG:4326", inplace=True)
    full_gdf = full_gdf.to_crs("EPSG:5070")
    return full_gdf
