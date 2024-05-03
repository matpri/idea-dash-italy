import pandas as pd

from profiles.copper_output.processing_scripts import cost_gencap as copper_cost_gencap
from profiles.nextgrid_output.processing_scripts import cost_gencap as nextgrid_cost_gencap
from profiles.natem_output.processing_scripts import cost_gencap as natem_cost_gencap
from profiles.pithos_output.processing_scripts import cost_gencap as pithos_cost_gencap
from profiles.pypsa_output.processing_scripts import cost_gencap as pypsa_cost_gencap



def check(df):
    """
    Check if 'Results_summary_carbon_AP_tech' is present in the 'variable' column.

    Parameters:
        df (pd.DataFrame): The DataFrame to check.

    Returns:
        bool: True if the specified prefix is found, False otherwise.
    """
    print("Checking for emissions in variable column")
    try:
        if df.model.unique()[0] == "copper":
            return copper_cost_gencap.check(df)
        elif df.model.unique()[0] == "ECCC-NextGrid":
            return nextgrid_cost_gencap.check(df)
        elif df.model.unique()[0] == "NATEM-POWER":
            return natem_cost_gencap.check(df)
        elif df.model.unique()[0] == "ESMIA-PITHOS":
            return pithos_cost_gencap.check(df)
        elif df.model.unique()[0] == "NRCan-PyPsa":
            return pypsa_cost_gencap.check(df)
        else:
            return False
    except Exception as e:
        print("Emission check", e)
        return False


def process(selected: dict):
    dfs = []
    for scenario_name, db in selected.items():
        if db.model.unique()[0] == "copper":
            df = copper_cost_gencap.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "ECCC-NextGrid":
            df = nextgrid_cost_gencap.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "NATEM-POWER":
            df = natem_cost_gencap.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "ESMIA-PITHOS":
            df = pithos_cost_gencap.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "NRCan-PyPsa":
            df = pypsa_cost_gencap.process({scenario_name: db})
            dfs.append(df)
        else:
            print("Model not implemented")
    return pd.concat(dfs)


