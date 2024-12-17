import pandas as pd

from profiles.copper_output.processing_scripts import cost_total as copper_cost_total
from profiles.nextgrid_output.processing_scripts import cost_total as nextgrid_cost_total
from profiles.natem_output.processing_scripts import cost_total as natem_cost_total
from profiles.pithos_output.processing_scripts import cost_total as pithos_cost_total
from profiles.pypsa_output.processing_scripts import cost_total as pypsa_cost_total
from profiles.pypsa_can_output.processing_scripts import cost_total as pypsa_can_cost_total
from profiles.temoa_output.processing_scripts import cost_total as temoa_cost_total



def check(df):
    """
    Check if 'Results_summary_carbon_AP_tech' is present in the 'variable' column.

    Parameters:
        df (pd.DataFrame): The DataFrame to check.

    Returns:
        bool: True if the specified prefix is found, False otherwise.
    """
    #print("Checking for emissions in variable column")
    try:
        if df.model.unique()[0] == "copper":
            return copper_cost_total.check(df)
        elif df.model.unique()[0] == "ECCC-NextGrid":
            return nextgrid_cost_total.check(df)
        elif df.model.unique()[0] == "NATEM_Canad":
            return natem_cost_total.check(df)
        elif df.model.unique()[0] == "HEC-PITHOS":
            return pithos_cost_total.check(df)
        elif df.model.unique()[0] == "NRCan-PyPsa":
            return pypsa_cost_total.check(df)
        elif df.model.unique()[0] == "PyPSA_CAN":
            return pypsa_can_cost_total.check(df)
        elif df.model.unique()[0] == "Sutubra-TEMOA":
            return temoa_cost_total.check(df)
        else:
            return False
    except Exception as e:
        print("Emission check", e)
        return False


def process(selected: dict):
    dfs = []
    for scenario_name, db in selected.items():
        if db.model.unique()[0] == "copper":
            df = copper_cost_total.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "ECCC-NextGrid":
            df = nextgrid_cost_total.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "NATEM_Canad":
            df = natem_cost_total.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "HEC-PITHOS":
            df = pithos_cost_total.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "NRCan-PyPsa":
            df = pypsa_cost_total.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "PyPSA_CAN":
            df = pypsa_can_cost_total.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "Sutubra-TEMOA":
            df = temoa_cost_total.process({scenario_name: db})
            dfs.append(df)
        else:
            print("Model not implemented")
    return pd.concat(dfs)


