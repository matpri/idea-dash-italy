import pandas as pd

from profiles.silver_output.processing_scripts import  (
    price_opf, uc_results, uc_emissions, uc_curtailment, 
    opf_results, opf_emissions, opf_curtailment, opf_costs, 
    opf_lineflow, uc_lineflow
)


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
        if price_opf.check(df):
            return True
        if uc_results.check(df):
            return True
        if uc_emissions.check(df):
            return True
        if uc_curtailment.db_check(df):
            return True
        if opf_results.db_check(df):
            return True
        if opf_emissions.db_check(df):
            return True
        if opf_curtailment.db_check(df):
            return True
        if opf_costs.check(df):
            return True
        if opf_lineflow.db_check(df):
            return True
        if uc_lineflow.db_check(df):
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
        if price_opf.check(db):
            df = price_opf.process({scenario_name: db})
            df['variable'] = 'Price OPF'
            dfs.append(df)
        if uc_results.check(db):
            df = uc_results.process({scenario_name: db})
            df['variable'] = 'UC Results'
            dfs.append(df)
        if uc_emissions.check(db):
            df = uc_emissions.process({scenario_name: db})
            df['variable'] = 'UC Emissions'
            dfs.append(df)
        if uc_curtailment.db_check(db):
            df = uc_curtailment.process({scenario_name: db})
            df['variable'] = 'UC VRE Curtailment'
            dfs.append(df)
        if opf_results.db_check(db):
            df = opf_results.process({scenario_name: db})
            df['variable'] = 'OPF Results'
            dfs.append(df)
        if opf_emissions.db_check(db):
            df = opf_emissions.process({scenario_name: db})
            df['variable'] = 'OPF Emissions'
            dfs.append(df)
        if opf_curtailment.db_check(db):
            df = opf_curtailment.process({scenario_name: db})
            df['variable'] = 'OPF VRE Curtailment'
            dfs.append(df)
        if opf_costs.check(db):
            df = opf_costs.process({scenario_name: db})
            df['variable'] = 'OPF Costs'
            dfs.append(df)
        if opf_lineflow.db_check(db):
            df = opf_lineflow.process({scenario_name: db})
            df['variable'] = 'OPF Line Flow'
            dfs.append(df)
        if uc_lineflow.db_check(db):
            df = uc_lineflow.process({scenario_name: db})
            df['variable'] = 'UC Line Flow'
            dfs.append(df)

    full_df = pd.concat(dfs)

    # full_df = full_df[full_df['region']=='CAN']
    full_df = full_df.groupby(['scenario', 'variable','time']).sum(numeric_only=True).reset_index()
    return full_df[['scenario', 'variable', 'time', 'value']]
