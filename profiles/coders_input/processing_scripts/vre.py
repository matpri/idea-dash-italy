import pandas as pd
import os
import geopandas as gpd
import shapely

from profiles.coders_input import utils


def check(df):
    """
    Check if 'Results_summary_carbon_AP_tech' is present in the 'variable' column.

    Parameters:
        df (pd.DataFrame): The DataFrame to check.

    Returns:
        bool: True if the specified prefix is found, False otherwise.
    """
    #print("Checking for emissions in variable column")
    try:
        if (df.model == 'CODERS').any():
            if 'VRE Capacity Factor' in df.type.unique():
                return True
        return False
    except Exception as e:
        #print("Emission check", e)
        return False

def process(selected: dict):
    dfs = []
    for scenario_name, db in selected.items():
        df = db.copy()
        # filter where 'Results_summary_carbon_AP_tech|' in variable column entry and remove the prefix
        df = df[df.type == 'VRE Capacity Factor']

        df['scenario'] = scenario_name
        dfs.append(df)
    full_df = pd.concat(dfs)

    for i, row in full_df.iterrows():
        full_df.loc[i, 'geometry'] = shapely.geometry.box(row['longitude'] - 0.3125, row['latitude'] - 0.25,
                                                            row['longitude'] + 0.3125, row['latitude'] + 0.25)
    full_gdf = gpd.GeoDataFrame(full_df, geometry='geometry')
    return full_gdf
