import pandas as pd

from profiles.copper_output.processing_scripts import qualifying_capacity as copper_qualifying_capacity
from profiles.nextgrid_output.processing_scripts import qualifying_capacity as nextgrid_qualifying_capacity
from profiles.natem_output.processing_scripts import qualifying_capacity as natem_qualifying_capacity
from profiles.pithos_output.processing_scripts import qualifying_capacity as pithos_qualifying_capacity
from profiles.pypsa_output.processing_scripts import qualifying_capacity as pypsa_qualifying_capacity



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
            return copper_qualifying_capacity.check(df)
        elif df.model.unique()[0] == "ECCC-NextGrid":
            return nextgrid_qualifying_capacity.check(df)
        elif df.model.unique()[0] == "ESMIA-NATEM":
            return natem_qualifying_capacity.check(df)
        elif df.model.unique()[0] == "ESMIA-PITHOS":
            return pithos_qualifying_capacity.check(df)
        elif df.model.unique()[0] == "NRCan-PyPsa":
            return pypsa_qualifying_capacity.check(df)
        else:
            return False
    except Exception as e:
        print("Emission check", e)
        return False


def process(selected: dict):
    dfs = []
    for scenario_name, db in selected.items():
        if db.model.unique()[0] == "copper":
            df = copper_qualifying_capacity.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "ECCC-NextGrid":
            df = nextgrid_qualifying_capacity.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "ESMIA-NATEM":
            df = natem_qualifying_capacity.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "ESMIA-PITHOS":
            df = pithos_qualifying_capacity.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "NRCan-PyPsa":
            df = pypsa_qualifying_capacity.process({scenario_name: db})
            dfs.append(df)
        else:
            print("Model not implemented")
    return pd.concat(dfs)


