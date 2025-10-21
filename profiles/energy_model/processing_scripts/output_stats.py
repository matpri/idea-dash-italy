import pandas as pd

from profiles.copper_output.processing_scripts import overview as copper_output_stats
from profiles.nextgrid_output.processing_scripts import overview as nextgrid_output_stats
from profiles.natem_output.processing_scripts import overview as natem_output_stats
from profiles.pithos_output.processing_scripts import overview as pithos_output_stats
from profiles.pypsa_output.processing_scripts import overview as pypsa_output_stats
from profiles.pypsa_can_output.processing_scripts import overview as pypsa_can_output_stats
from profiles.cef.processing_scripts import overview as cef_output_stats
from profiles.temoa_output.processing_scripts import overview as temoa_output_stats




def check(df):
    """
    Check if 'Results_summary_carbon_AP_tech' is present in the 'variable' column.

    Parameters:
        df (pd.DataFrame): The DataFrame to check.

    Returns:
        bool: True if the specified prefix is found, False otherwise.
    """
    #print("Checking for output_stats in variable column")
    try:
        if df.model.unique()[0] == "copper":
            return copper_output_stats.check(df)
        elif df.model.unique()[0] == "ECCC-NextGrid":
            return nextgrid_output_stats.check(df)
        elif df.model.unique()[0] == "NATEM_Canada":
            return natem_output_stats.check(df)
        elif df.model.unique()[0] == "PITHOS":
            return pithos_output_stats.check(df)
        elif df.model.unique()[0] == "NRCan-PyPsa":
            return pypsa_output_stats.check(df)
        elif df.model.unique()[0] == "PyPSA_CAN":
            return pypsa_can_output_stats.check(df)
        elif df.model.unique()[0] == "cef":
            return cef_output_stats.check(df)
        elif df.model.unique()[0] == "Sutubra-TEMOA":
            return temoa_output_stats.check(df)
        else:
            return False
    except Exception as e:
        print("Emission check", e)
        return False


def process(selected: dict):
    dfs = []
    for scenario_name, db in selected.items():
        if db.model.unique()[0] == "copper":
            df = copper_output_stats.process({scenario_name: db})
            df.model = "COPPER"
            dfs.append(df)
        elif db.model.unique()[0] == "ECCC-NextGrid":
            df = nextgrid_output_stats.process({scenario_name: db})
            df.model = "ECCC-NextGrid"
            dfs.append(df)
        elif db.model.unique()[0] == "NATEM_Canada":
            df = natem_output_stats.process({scenario_name: db})
            df.model = "NATEM_Canada"
            dfs.append(df)
        elif db.model.unique()[0] == "PITHOS":
            df = pithos_output_stats.process({scenario_name: db})
            df.model = "PITHOS"
            dfs.append(df)
        elif db.model.unique()[0] == "NRCan-PyPsa":
            df = pypsa_output_stats.process({scenario_name: db})
            df.model = "NRCan-PyPsa"
            dfs.append(df)
        elif db.model.unique()[0] == "PyPSA_CAN":
            df = pypsa_can_output_stats.process({scenario_name: db})
            df.model = "PyPSA_CAN"
            dfs.append(df)
        elif db.model.unique()[0] == "Sutubra-TEMOA":
            df = temoa_output_stats.process({scenario_name: db})
            df.model = "Sutubra-TEMOA"
            dfs.append(df)
        elif db.model.unique()[0] == "cef":
            df = cef_output_stats.process({scenario_name: db})
            df['scenario'] = 'CEF|' + df['scenario']
            df.model = "cef"
            dfs.append(df)
        else:
            print("Model not implemented")
    return pd.concat(dfs)


