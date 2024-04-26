import pandas as pd

from profiles.copper_output.processing_scripts import generation_capacity as copper_generation_capacity
from profiles.nextgrid_output.processing_scripts import generation_capacity as nextgrid_generation_capacity
from profiles.natem_output.processing_scripts import generation_capacity as natem_generation_capacity
from profiles.pithos_output.processing_scripts import generation_capacity as pithos_generation_capacity
from profiles.pypsa_output.processing_scripts import generation_capacity as pypsa_generation_capacity



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
            return copper_generation_capacity.check(df)
        elif df.model.unique()[0] == "ECCC-NextGrid":
            return nextgrid_generation_capacity.check(df)
        elif df.model.unique()[0] == "ESMIA-NATEM":
            return natem_generation_capacity.check(df)
        elif df.model.unique()[0] == "ESMIA-PITHOS":
            return pithos_generation_capacity.check(df)
        elif df.model.unique()[0] == "NRCan-PyPsa":
            return pypsa_generation_capacity.check(df)
        else:
            return False
    except Exception as e:
        print("Emission check", e)
        return False


def process(selected: dict):
    dfs = []
    for scenario_name, db in selected.items():
        if db.model.unique()[0] == "copper":
            df = copper_generation_capacity.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "ECCC-NextGrid":
            df = nextgrid_generation_capacity.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "ESMIA-NATEM":
            df = natem_generation_capacity.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "ESMIA-PITHOS":
            df = pithos_generation_capacity.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "NRCan-PyPsa":
            df = pypsa_generation_capacity.process({scenario_name: db})
            dfs.append(df)
        else:
            print("Model not implemented")
    return pd.concat(dfs)


