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
            if df.variable.str.startswith("Input").any():
                return True
        return False
    except Exception as e:
        print("Emission check", e)
        return False
    
def vre(vre_data):
    vre_data['region'] = vre_data['region'].astype(int)

    # load merra info
    merra_info = pd.read_csv('./profiles/copper_output/merra_info.csv')

    vre_data = vre_data.merge(merra_info, left_on='region', right_on='grid_cell', how='left')
    vre_data['prov'] = vre_data['ba'].apply(lambda x: x.split('.')[0])

    for i, row in vre_data.iterrows():
        vre_data.loc[i, 'geometry'] = shapely.geometry.box(row['lon'] - 0.3125, row['lat'] - 0.25,
                                                          row['lon'] + 0.3125, row['lat'] + 0.25)
    return gpd.GeoDataFrame(vre_data, geometry='geometry')

def extant_transmission(data):
    data['variable'] = data['variable'].apply(lambda x: x.split("|")[1])
    # rename time to period
    # sort by region, variable, period
    data["region"] = data.region.apply(lambda x: x.split(".")[0])
    data["variable"] = data.variable.apply(lambda x: x.split(".")[0])
    # remove where variable == region
    data = data[data.region != data.variable]
    data = data.groupby(["region", "variable", "time", 'scenario']).sum(numeric_only=True).reset_index()

    data = data.groupby(["region", "variable", "time", 'scenario']).sum(numeric_only=True).reset_index()
    prov_cord = pd.read_csv('./profiles/copper_output/visualization_scripts/utils/arrow_coords.csv')
    data['short_region'] = data['region'].map(utils.province_short)
    data['short_variable'] = data['variable'].map(utils.province_short)
    data = pd.merge(data, prov_cord, how='inner', left_on=['region', 'variable'],
                      right_on=['region', 'variable'])
    data['from_lat'] = data['from_lat'].astype(float)
    data['from_lon'] = data['from_lon'].astype(float)
    data['variable'] = 'Extant Transmission|' + data['variable']
    return data


def extant_capacity(data):
    data["region"] = data["region"].apply(lambda x: x.split(".")[0])
    data['region'] = data['region'].map(utils.province_short).fillna(data['region'])
    data = data.groupby(['region', 'variable', 'time', 'scenario']).sum(numeric_only=True).reset_index()
    return data


def process(selected: dict):
    dfs = []
    for scenario_name, db in selected.items():
        df = db.copy()
        # filter where 'Results_summary_carbon_AP_tech|' in variable column entry and remove the prefix
        df = df[df.variable.str.startswith("Input|")]
        df['variable'] = df['variable'].str.replace("Input|", "")
        df['scenario'] = scenario_name
        classes = df.variable.apply(lambda x: x.split('|')[0]).unique()
        
        for cls in classes:
            data = df[df.variable.str.startswith(cls)]
            if cls == 'Vre Capacity Factors':
                dfs.append(vre(data))
            elif cls == 'Extant Transmission':
                dfs.append(extant_transmission(data))
            elif cls == 'Extant Capacity':
                dfs.append(extant_capacity(data))
            else:
                dfs.append(data)

    full_df = pd.concat(dfs)
    return full_df
                
