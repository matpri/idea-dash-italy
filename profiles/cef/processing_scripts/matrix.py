import pandas as pd

from profiles.cef.processing_scripts import (generation_capacity, emissions,
                                             generation_supply)


def check(df):
    """
    Check if 'cost' is present in the 'variable' column.

    Args:
        df (DataFrame): The DataFrame to check.

    Returns:
        bool: True if the specified prefix is found, False otherwise.
    """
    #print("Checking for cost in variable column")
    try:
        if generation_capacity.check(df):
            return True
        if emissions.check(df):
            return True
        if generation_supply.check(df):
            return True
        return False
    except Exception as e:
        #print("cost check", e)
        return False


def process(data):
    """
    Process emission data from multiple scenarios based on the 'folders' dictionary.

    Parameters:
        folders (dict): Dictionary containing scenario names as keys and folder paths as values.
        target_dir (str): Target directory.

    Returns:
        pd.DataFrame: Processed DataFrame.
    """
    dfs = []
    for scenario_name, db in data.items():
        if generation_capacity.check(db):
            df = generation_capacity.process({scenario_name: db})
            df['variable'] = 'Capacity|' + df['variable']
            dfs.append(df)
        if emissions.check(db):
            df = emissions.process({scenario_name: db})
            df['variable'] = 'Emissions|' + df['variable']
            dfs.append(df)
        if generation_supply.check(db):
            df = generation_supply.process({scenario_name: db})
            df['variable'] = 'Supply|' + df['variable']
            dfs.append(df)

    full_df = pd.concat(dfs)
    return full_df[['scenario', 'variable', 'time', 'value', 'region']]
