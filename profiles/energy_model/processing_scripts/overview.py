import pandas as pd

from profiles.copper_output.processing_scripts import overview as copper_overview
from profiles.nextgrid_output.processing_scripts import overview as nextgrid_overview
from profiles.natem_output.processing_scripts import overview as natem_overview
from profiles.pithos_output.processing_scripts import overview as pithos_overview
from profiles.pypsa_output.processing_scripts import overview as pypsa_overview
from profiles.pypsa_can_output.processing_scripts import overview as pypsa_can_overview
from profiles.cef.processing_scripts import overview as cef_overview
from profiles.temoa_output.processing_scripts import overview as temoa_overview




def check(df):
    """
    Check if 'Results_summary_carbon_AP_tech' is present in the 'variable' column.

    Parameters:
        df (pd.DataFrame): The DataFrame to check.

    Returns:
        bool: True if the specified prefix is found, False otherwise.
    """
    print("Checking for overview in variable column")
    try:
        if df.model.unique()[0] == "copper":
            return copper_overview.check(df)
        elif df.model.unique()[0] == "ECCC-NextGrid":
            return nextgrid_overview.check(df)
        elif df.model.unique()[0] == "NATEM-POWER":
            return natem_overview.check(df)
        elif df.model.unique()[0] == "HEC-PITHOS":
            return pithos_overview.check(df)
        elif df.model.unique()[0] == "NRCan-PyPsa":
            return pypsa_overview.check(df)
        elif df.model.unique()[0] == "PyPSA_CAN":
            return pypsa_can_overview.check(df)
        elif df.model.unique()[0] == "cef":
            return cef_overview.check(df)
        elif df.model.unique()[0] == "Sutubra-TEMOA":
            return temoa_overview.check(df)
        else:
            return False
    except Exception as e:
        print("Emission check", e)
        return False


def process(selected: dict):
    dfs = []
    for scenario_name, db in selected.items():
        if db.model.unique()[0] == "copper":
            df = copper_overview.process({scenario_name: db})
            df.model = "COPPER"
            dfs.append(df)
        elif db.model.unique()[0] == "ECCC-NextGrid":
            df = nextgrid_overview.process({scenario_name: db})
            df.model = "ECCC-NextGrid"
            dfs.append(df)
        elif db.model.unique()[0] == "NATEM-POWER":
            df = natem_overview.process({scenario_name: db})
            df.model = "NATEM-POWER"
            dfs.append(df)
        elif db.model.unique()[0] == "HEC-PITHOS":
            df = pithos_overview.process({scenario_name: db})
            df.model = "HEC-PITHOS"
            dfs.append(df)
        elif db.model.unique()[0] == "NRCan-PyPsa":
            df = pypsa_overview.process({scenario_name: db})
            df.model = "NRCan-PyPsa"
            dfs.append(df)
        elif db.model.unique()[0] == "PyPSA_CAN":
            df = pypsa_can_overview.process({scenario_name: db})
            df.model = "PyPSA_CAN"
            dfs.append(df)
        elif db.model.unique()[0] == "Sutubra-TEMOA":
            df = temoa_overview.process({scenario_name: db})
            df.model = "Sutubra-TEMOA"
            dfs.append(df)
        elif db.model.unique()[0] == "cef":
            df = cef_overview.process({scenario_name: db})
            df['scenario'] = 'CEF|' + df['scenario']
            df.model = "cef"
            dfs.append(df)
        else:
            print("Model not implemented")
    return pd.concat(dfs)


