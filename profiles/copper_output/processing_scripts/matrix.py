import pandas as pd

from profiles.copper_output.processing_scripts import (generation_capacity, emissions, new_capacity, net_new_capacity,
                                                       generation_supply,
                                                       cost_vom, cost_fom, cost_gencap, cost_total)


def check(df):
    """
    Check if 'cost' is present in the 'variable' column.

    Args:
        df (DataFrame): The DataFrame to check.

    Returns:
        bool: True if the specified prefix is found, False otherwise.
    """
    print("Checking for cost in variable column")
    try:
        if generation_capacity.check(df):
            return True
        if new_capacity.check(df):
            return True
        if net_new_capacity.check(df):
            return True
        if emissions.check(df):
            return True
        if generation_supply.check(df):
            return True
        if cost_vom.check(df):
            return True
        if cost_fom.check(df):
            return True
        if cost_gencap.check(df):
            return True
        if cost_total.check(df):
            return True
        return False
    except Exception as e:
        print("cost check", e)
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
        if new_capacity.check(db):
            df = new_capacity.process({scenario_name: db})
            df['variable'] = 'New Capacity|' + df['variable']
            dfs.append(df)
        if net_new_capacity.check(db):
            df = net_new_capacity.process({scenario_name: db})
            df['variable'] = 'Net New Capacity|' + df['variable']
            dfs.append(df)
        if emissions.check(db):
            df = emissions.process({scenario_name: db})
            df['variable'] = 'Emissions|' + df['variable']
            dfs.append(df)
        if generation_supply.check(db):
            df = generation_supply.process({scenario_name: db})
            df['variable'] = 'Supply|' + df['variable']
            dfs.append(df)
        if cost_vom.check(db):
            df = cost_vom.process({scenario_name: db})
            df['variable'] = 'VOM Cost|' + df['variable']
            dfs.append(df)
        if cost_fom.check(db):
            df = cost_fom.process({scenario_name: db})
            df['variable'] = 'FOM Cost|' + df['variable']
            dfs.append(df)
        if cost_gencap.check(db):
            df = cost_gencap.process({scenario_name: db})
            df['variable'] = 'Capacity Cost|' + df['variable']
            dfs.append(df)
        if cost_total.check(db):
            df = cost_total.process({scenario_name: db})
            df['variable'] = 'Total Cost|' + df['variable']
            dfs.append(df)

    full_df = pd.concat(dfs)
    return full_df[['scenario', 'variable', 'time', 'value', 'region']]
