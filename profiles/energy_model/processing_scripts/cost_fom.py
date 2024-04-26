import pandas as pd

from profiles.copper_output.processing_scripts import cost_fom as copper_cost_fom
from profiles.nextgrid_output.processing_scripts import cost_fom as nextgrid_cost_fom
from profiles.natem_output.processing_scripts import cost_fom as natem_cost_fom
from profiles.pithos_output.processing_scripts import cost_fom as pithos_cost_fom
from profiles.pypsa_output.processing_scripts import cost_fom as pypsa_cost_fom



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
            return copper_cost_fom.check(df)
        elif df.model.unique()[0] == "ECCC-NextGrid":
            return nextgrid_cost_fom.check(df)
        elif df.model.unique()[0] == "ESMIA-NATEM":
            return natem_cost_fom.check(df)
        elif df.model.unique()[0] == "ESMIA-PITHOS":
            return pithos_cost_fom.check(df)
        elif df.model.unique()[0] == "NRCan-PyPsa":
            return pypsa_cost_fom.check(df)
        else:
            return False
    except Exception as e:
        print("Emission check", e)
        return False


def process(selected: dict):
    dfs = []
    for scenario_name, db in selected.items():
        if db.model.unique()[0] == "copper":
            df = copper_cost_fom.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "ECCC-NextGrid":
            df = nextgrid_cost_fom.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "ESMIA-NATEM":
            df = natem_cost_fom.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "ESMIA-PITHOS":
            df = pithos_cost_fom.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "NRCan-PyPsa":
            df = pypsa_cost_fom.process({scenario_name: db})
            dfs.append(df)
        else:
            print("Model not implemented")
    return pd.concat(dfs)


