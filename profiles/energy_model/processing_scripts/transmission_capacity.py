import pandas as pd

from profiles.copper_output.processing_scripts import transmission_capacity_plotly as copper_generation_supply
from profiles.nextgrid_output.processing_scripts import transmission_capacity_plotly as nextgrid_generation_supply
from profiles.natem_output.processing_scripts import transmission_capacity_plotly as natem_generation_supply
from profiles.pithos_output.processing_scripts import transmission_capacity_plotly as pithos_generation_supply
from profiles.pypsa_output.processing_scripts import transmission_capacity_plotly as pypsa_generation_supply
from profiles.pypsa_can_output.processing_scripts import transmission_capacity_plotly as pypsa_can_generation_supply
from profiles.temoa_output.processing_scripts import transmission_capacity_plotly as temoa_generation_supply



def check(df):
    """
    Check if 'Results_summary_carbon_AP_tech' is present in the 'variable' column.

    Parameters:
        df (pd.DataFrame): The DataFrame to check.

    Returns:
        bool: True if the specified prefix is found, False otherwise.
    """
    print("Checking for generation_supply in variable column")
    try:
        if df.model.unique()[0] == "copper":
            return copper_generation_supply.check(df)
        elif df.model.unique()[0] == "ECCC-NextGrid":
            return nextgrid_generation_supply.check(df)
        elif df.model.unique()[0] == "NATEM-POWER":
            return natem_generation_supply.check(df)
        elif df.model.unique()[0] == "HEC-PITHOS":
            return pithos_generation_supply.check(df)
        elif df.model.unique()[0] == "NRCan-PyPsa":
            return pypsa_generation_supply.check(df)
        elif df.model.unique()[0] == "PyPSA_CAN":
            return pypsa_can_generation_supply.check(df)
        elif df.model.unique()[0] == "Sutubra-TEMOA":
            return temoa_generation_supply.check(df)
        else:
            return False
    except Exception as e:
        print("Emission check", e)
        return False


def process(selected: dict):
    dfs = []
    for scenario_name, db in selected.items():
        if db.model.unique()[0] == "copper":
            df = copper_generation_supply.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "ECCC-NextGrid":
            df = nextgrid_generation_supply.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "NATEM-POWER":
            df = natem_generation_supply.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "HEC-PITHOS":
            df = pithos_generation_supply.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "NRCan-PyPsa":
            df = pypsa_generation_supply.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "PyPSA_CAN":
            df = pypsa_can_generation_supply.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "Sutubra-TEMOA":
            df = temoa_generation_supply.process({scenario_name: db})
            dfs.append(df)
        else:
            print("Model not implemented")
    return pd.concat(dfs)


