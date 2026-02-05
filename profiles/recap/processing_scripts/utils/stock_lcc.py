import pandas as pd
import os

from profiles.cims_output import utils


def check(df):
    """
    Check if 'Results_summary_carbon_AP_tech' is present in the 'variable' column.

    Parameters:
        df (pd.DataFrame): The DataFrame to check.

    Returns:
        bool: True if the specified prefix is found, False otherwise.
    """
    # print("Checking for emissions in variable column")
    try:
        if (df.model == 'CIM2').any():
            if (df.parameter.str.contains('stock')).any():
                return True
        return False
    except Exception as e:
        print("stock check", e)
        return False


def process(selected: dict):
    dfs = []
    for scenario_name, db in selected.items():
        df = db.copy()
        df = df[df['parameter'].str.contains('stock')]
        df = df[~df['region'].str.contains('CAN')]
        df['parameter'] = df['parameter'].replace(
            {'new_stock': 'New Stock', 'stock_new': 'New Stock',
             'added_retrofit_stock': 'Added Retrofit Stock', 'stock_retrofit_added': 'Retrofit Added Stock',
             'stock_retrofit': 'Retrofit Stock', 'stock_total': 'Total Stock',
             'retrofit_stock': 'Retrofit Stock', 'total_stock': 'Total Stock'})
        # filter where 'Results_summary_carbon_AP_tech|' in variable column entry and remove the prefix
        df['scenario'] = scenario_name
        dfs.append(df)
    full_df = pd.concat(dfs)
    full_df['value_num'] = full_df['value_num'].astype(float)
    return full_df
