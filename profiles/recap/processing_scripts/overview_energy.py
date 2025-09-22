import pandas as pd

from profiles.recap.processing_scripts.utils import requested_quantities

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

        if requested_quantities.check(df):
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
        if requested_quantities.check(db):
            df = requested_quantities.process({scenario_name: db})
            df['tab'] = 'Energy Demand'
            dfs.append(df)


    full_df = pd.concat(dfs)
    return full_df
