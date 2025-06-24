import pandas as pd

from profiles.messageix_output.processing_scripts import (capital_cost, emissions, capacity,
                                                            total_cost, capacity_additions, primary_energy,
secondary_energy, useful_energy, final_energy)


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
        if capital_cost.check(df):
            return True
        if capacity.check(df):
            return True
        if capacity_additions.check(df):
            return True
        if emissions.check(df):
            return True
        if total_cost.check(df):
            return True
        if final_energy.check(df):
            return True
        if primary_energy.check(df):
            return True
        if secondary_energy.check(df):
            return True
        if useful_energy.check(df):
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
        if capacity.check(db):
            df = capacity.process({scenario_name: db})
            df['variable'] = 'Capacity'
            dfs.append(df)
        if total_cost.check(db):
            df = total_cost.process({scenario_name: db})
            df['variable'] = 'Total Cost'
            dfs.append(df)
        if capacity_additions.check(db):
            df = capacity_additions.process({scenario_name: db})
            df['variable'] = 'Capacity Additions'
            dfs.append(df)
        if emissions.check(db):
            df = emissions.process({scenario_name: db})
            df['variable'] = 'Emissions'
            dfs.append(df)
        if capital_cost.check(db):
            df = capital_cost.process({scenario_name: db})
            df['variable'] = 'Capital Cost'
            dfs.append(df)
        if final_energy.check(db):
            df = final_energy.process({scenario_name: db})
            df['variable'] = 'Final Energy'
            dfs.append(df)
        if primary_energy.check(db):
            df = primary_energy.process({scenario_name: db})
            df['variable'] = 'Primary Energy'
            dfs.append(df)
        if secondary_energy.check(db):
            df = secondary_energy.process({scenario_name: db})
            df['variable'] = 'Secondary Energy'
            dfs.append(df)
        if useful_energy.check(db):
            df = useful_energy.process({scenario_name: db})
            df['variable'] = 'Useful Energy'
            dfs.append(df)

    full_df = pd.concat(dfs)

    full_df = full_df[full_df['region']=='Canada']
    full_df = full_df.groupby(['scenario', 'variable','time']).sum(numeric_only=True).reset_index()
    return full_df[['scenario', 'variable', 'time', 'value']]
