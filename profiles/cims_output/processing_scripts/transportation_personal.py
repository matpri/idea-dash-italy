import pandas as pd
import os

from profiles.cims_output.processing_scripts.utils import requested_quantities, ghg, stock_lcc

emissions_mapping = {
    'Net Emissions': ['total_cumul_net_emissions',
                      'total_cumul_avoided_emissions',
                      'total_cumul_negative_emissions',
                      'total_cumul_bio_emissions'],
    'Avoided Emissions': ['total_cumul_avoided_emissions'],
    'Negative Emissions': ['total_cumul_negative_emissions'],
    'Emitted Emissions': ['total_cumul_net_emissions', 'total_cumul_bio_emissions'],
    'Emissions Costs': ['total_cumul_emissions_cost']}


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
        if (df.model == 'CIMS').any():
            if (df.sector == 'Transportation Personal').any():
                df = df[df.sector == 'Transportation Personal']
                if stock_lcc.check(df):
                    return True
                if requested_quantities.check(df):
                    return True
                if ghg.check(df):
                    return True
        return False
    except Exception as e:
        print("Emission check", e)
        return False


def process(selected: dict):
    dfs = []
    for scenario_name, db in selected.items():
        df = db.copy()
        df = df[df.sector == 'Transportation Personal']
        # remove where region is CAN
        df_ghg = df.copy()
        df_ghg = ghg.process({scenario_name: df_ghg})
        ghg_ls = []
        for name, emission_list in emissions_mapping.items():
            subset = df_ghg[df_ghg.parameter.isin(emission_list)][
                ['region', 'year', 'value_num', 'scenario', 'context', 'sub_context']].groupby(
                ['region', 'year', 'scenario', 'context', 'sub_context']).sum().reset_index()
            subset['parameter'] = name
            ghg_ls.append(subset)
        df_ghg = pd.concat(ghg_ls)
        df_ghg['plot'] = 'Emissions'

        df_stock = df.copy()
        df_stock = stock_lcc.process({scenario_name: df_stock})
        df_stock['plot'] = 'Technology Stocks'
        df_rq = df.copy()
        df_rq = requested_quantities.process({scenario_name: df_rq})
        df_rq['plot'] = 'Energy Demand'
        dfs.append(df_ghg)
        dfs.append(df_stock)
        dfs.append(df_rq)
    full_df = pd.concat(dfs)
    return full_df
