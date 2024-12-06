import pandas as pd

from profiles.macromodel.processing_scripts import financial_markets, government


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
        if government.check(df):
            return True
        if financial_markets.check(df):
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
        if government.check(db):
            df = government.process({scenario_name: db})
            df['variable'] = 'Central Government'
            dfs.append(df)
        if financial_markets.check(db):
            df = financial_markets.process({scenario_name: db})
            df['variable'] = 'Financial Markets'
            dfs.append(df)

    full_df = pd.concat(dfs)

    full_df = full_df[full_df['region']=='CAN']
    full_df = full_df.groupby(['scenario', 'variable','time', 'unit']).sum(numeric_only=True).reset_index()
    return full_df[['scenario', 'variable', 'time', 'value', 'unit']]
