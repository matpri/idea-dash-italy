import pandas as pd

from profiles.copper_output.processing_scripts import emissions as copper_emissions
from profiles.nextgrid_output.processing_scripts import emissions as nextgrid_emissions
from profiles.natem_output.processing_scripts import emissions as natem_emissions
from profiles.pithos_output.processing_scripts import emissions as pithos_emissions
from profiles.pypsa_output.processing_scripts import emissions as pypsa_emissions
from profiles.pypsa_can_output.processing_scripts import emissions as pypsa_can_emissions
from profiles.cef.processing_scripts import emissions as cef_emissions



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
            return copper_emissions.check(df)
        elif df.model.unique()[0] == "ECCC-NextGrid":
            return nextgrid_emissions.check(df)
        elif df.model.unique()[0] == "NATEM-POWER":
            return natem_emissions.check(df)
        elif df.model.unique()[0] == "ESMIA-PITHOS":
            return pithos_emissions.check(df)
        elif df.model.unique()[0] == "NRCan-PyPsa":
            return pypsa_emissions.check(df)
        elif df.model.unique()[0] == "PyPSA_CAN":
            return pypsa_can_emissions.check(df)
        elif df.model.unique()[0] == "cef":
            return cef_emissions.check(df)
        else:
            return False
    except Exception as e:
        print("Emission check", e)
        return False


def process(selected: dict):
    dfs = []
    for scenario_name, db in selected.items():
        if db.model.unique()[0] == "copper":
            df = copper_emissions.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "ECCC-NextGrid":
            df = nextgrid_emissions.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "NATEM-POWER":
            df = natem_emissions.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "ESMIA-PITHOS":
            df = pithos_emissions.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "NRCan-PyPsa":
            df = pypsa_emissions.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "PyPSA_CAN":
            df = pypsa_can_emissions.process({scenario_name: db})
            dfs.append(df)
        elif db.model.unique()[0] == "cef":
            df = cef_emissions.process({scenario_name: db})
            df['scenario'] = 'CEF|' + df['scenario']
            dfs.append(df)
        else:
            print("Model not implemented")
    return pd.concat(dfs)


