import pandas as pd

from profiles.copper_output.processing_scripts import new_capacity as copper_new_capacity
from profiles.nextgrid_output.processing_scripts import new_capacity as nextgrid_new_capacity
from profiles.natem_output.processing_scripts import new_capacity as natem_new_capacity
from profiles.pithos_output.processing_scripts import new_capacity as pithos_new_capacity
from profiles.pypsa_output.processing_scripts import new_capacity as pypsa_new_capacity
from profiles.pypsa_can_output.processing_scripts import new_capacity as pypsa_can_new_capacity



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
            return copper_new_capacity.check(df)
        elif df.model.unique()[0] == "ECCC-NextGrid":
            return nextgrid_new_capacity.check(df)
        elif df.model.unique()[0] == "NATEM-POWER":
            return natem_new_capacity.check(df)
        elif df.model.unique()[0] == "ESMIA-PITHOS":
            return pithos_new_capacity.check(df)
        elif df.model.unique()[0] == "NRCan-PyPsa":
            return pypsa_new_capacity.check(df)
        elif df.model.unique()[0] == "PyPSA_CAN":
            return pypsa_can_new_capacity.check(df)
        else:
            return False
    except Exception as e:
        print("Emission check", e)
        return False


def process(selected: dict):
    dfs = []
    for scenario_name, db in selected.items():
        if db.model.unique()[0] == "copper":
            df = copper_new_capacity.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "ECCC-NextGrid":
            df = nextgrid_new_capacity.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "NATEM-POWER":
            df = natem_new_capacity.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "ESMIA-PITHOS":
            df = pithos_new_capacity.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "NRCan-PyPsa":
            df = pypsa_new_capacity.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "PyPSA_CAN":
            df = pypsa_can_new_capacity.process({scenario_name: db})
            dfs.append(df)
        else:
            print("Model not implemented")
    return pd.concat(dfs)


