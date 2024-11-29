import pandas as pd

from profiles.macromodel.processing_scripts import banks, central_Bank, central_government, credit_market, government_entities


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
        if banks.check(df):
            return True
        if central_Bank.check(df):
            return True
        if central_government.check(df):
            return True
        if credit_market.check(df):
            return True
        if government_entities.check(df):
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
        if banks.check(db):
            df = banks.process({scenario_name: db})
            df['variable'] = 'Banks'
            dfs.append(df)
        if central_Bank.check(db):
            df = central_Bank.process({scenario_name: db})
            df['variable'] = 'Central Bank'
            dfs.append(df)
        if central_government.check(db):
            df = central_government.process({scenario_name: db})
            df['variable'] = 'Central Government'
            dfs.append(df)
        if credit_market.check(db):
            df = credit_market.process({scenario_name: db})
            df['variable'] = 'Credit Market'
            dfs.append(df)
        if government_entities.check(db):
            df = government_entities.process({scenario_name: db})
            df['variable'] = 'Government Entities'
            dfs.append(df)

    full_df = pd.concat(dfs)

    full_df = full_df[full_df['region']=='CAN']
    full_df = full_df.groupby(['scenario', 'variable','time', 'unit']).sum(numeric_only=True).reset_index()
    return full_df[['scenario', 'variable', 'time', 'value', 'unit']]
