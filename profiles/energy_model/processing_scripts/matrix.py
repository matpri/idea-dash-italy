import pandas as pd

from profiles.copper_output.processing_scripts import matrix as copper_matrix
from profiles.nextgrid_output.processing_scripts import matrix as nextgrid_matrix
from profiles.natem_output.processing_scripts import matrix as natem_matrix
from profiles.pithos_output.processing_scripts import matrix as pithos_matrix
from profiles.pypsa_output.processing_scripts import matrix as pypsa_matrix
from profiles.cef.processing_scripts import matrix as cef_matrix



def check(df):
    """
    Check if 'Results_summary_carbon_AP_tech' is present in the 'variable' column.

    Parameters:
        df (pd.DataFrame): The DataFrame to check.

    Returns:
        bool: True if the specified prefix is found, False otherwise.
    """
    print("Checking for matrix in variable column")
    try:
        if df.model.unique()[0] == "copper":
            return copper_matrix.check(df)
        elif df.model.unique()[0] == "ECCC-NextGrid":
            return nextgrid_matrix.check(df)
        elif df.model.unique()[0] == "NATEM-POWER":
            return natem_matrix.check(df)
        elif df.model.unique()[0] == "ESMIA-PITHOS":
            return pithos_matrix.check(df)
        elif df.model.unique()[0] == "NRCan-PyPsa":
            return pypsa_matrix.check(df)
        elif df.model.unique()[0] == "cef":
            return cef_matrix.check(df)
        else:
            return False
    except Exception as e:
        print("Emission check", e)
        return False


def process(selected: dict):
    dfs = []
    for scenario_name, db in selected.items():
        if db.model.unique()[0] == "copper":
            df = copper_matrix.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "ECCC-NextGrid":
            df = nextgrid_matrix.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "NATEM-POWER":
            df = natem_matrix.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "ESMIA-PITHOS":
            df = pithos_matrix.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "NRCan-PyPsa":
            df = pypsa_matrix.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "cef":
            df = cef_matrix.process({scenario_name: db})
            df['scenario'] = 'CEF|' + df['scenario']
            dfs.append(df)
        else:
            print("Model not implemented")
    return pd.concat(dfs)


