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
        if (df.model == 'copper').any():
            if df.variable.str.startswith("Merra Capacity").any():
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
        df = df[df.variable.str.startswith("Merra Capacity|")]
        df['variable'] = df['variable'].str.replace("Merra Capacity|", "")

        df['scenario'] = scenario_name
        dfs.append(df)
    full_df = pd.concat(dfs)
    full_df['region'] = full_df['region'].astype(int)
    subsets = []

    for year in full_df['time'].unique():
        subset = full_df[full_df['time'] <= year]
        subset = subset.groupby(['region', 'variable', 'scenario']).sum().reset_index()
        subset['time'] = year
        subsets.append(subset)

    full_df = pd.concat(subsets)


    # load merra info
    merra_info = pd.read_csv('./profiles/copper_output/merra_info.csv')

    full_df = full_df.merge(merra_info, left_on='region', right_on='grid_cell', how='left')
    full_df['prov'] = full_df['ba'].apply(lambda x: x.split('.')[0])



    for i, row in full_df.iterrows():
        full_df.loc[i, 'geometry'] = shapely.geometry.box(row['lon'] - 0.3125, row['lat'] - 0.25,
                                                            row['lon'] + 0.3125, row['lat'] + 0.25)
    full_gdf = gpd.GeoDataFrame(full_df, geometry='geometry')
    return full_gdf
