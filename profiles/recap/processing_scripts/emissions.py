import pandas as pd

from profiles.copper_output.processing_scripts import emissions as copper_emissions
from profiles.nextgrid_output.processing_scripts import emissions as nextgrid_emissions
from profiles.natem_output.processing_scripts import emissions as natem_emissions
from profiles.pithos_output.processing_scripts import emissions as pithos_emissions
from profiles.pypsa_output.processing_scripts import emissions as pypsa_emissions
from profiles.pypsa_can_output.processing_scripts import emissions as pypsa_can_emissions
from profiles.cef.processing_scripts import emissions as cef_emissions
from profiles.temoa_output.processing_scripts import emissions as temoa_emissions



def check(df):
    """
    Check if 'Results_summary_carbon_AP_tech' is present in the 'variable' column.

    Parameters:
        df (pd.DataFrame): The DataFrame to check.

    Returns:
        bool: True if the specified prefix is found, False otherwise.
    """
    try:
        if (df.model == "copper").any():
            return copper_emissions.check(df)
        elif (df.model == "ECCC-NextGrid").any():
            return nextgrid_emissions.check(df)
        elif (df.model == "NATEM_Canada").any():
            return natem_emissions.check(df)
        elif (df.model == "PITHOS").any():
            return pithos_emissions.check(df)
        elif (df.model == "NRCan-PyPsa").any():
            return pypsa_emissions.check(df)
        elif (df.model == "PyPSA_CAN").any():
            return pypsa_can_emissions.check(df)
        elif (df.model == "Sutubra").any():
            return temoa_emissions.check(df)
        elif (df.model == "cef").any():
            return cef_emissions.check(df)
        else:
            return False
    except Exception as e:
        print(f"ERROR in emissions.check: {e}")
        return False


def process(selected: dict):
    dfs = []
    for scenario_name, db in selected.items():
        try:
            if (db.model == "copper").any():
                df = copper_emissions.process({scenario_name: db})
                dfs.append(df)
            elif (db.model == "ECCC-NextGrid").any():
                df = nextgrid_emissions.process({scenario_name: db})
                dfs.append(df)
            elif (db.model == "NATEM_Canada").any():
                df = natem_emissions.process({scenario_name: db})
                dfs.append(df)
            elif (db.model == "PITHOS").any():
                df = pithos_emissions.process({scenario_name: db})
                dfs.append(df)
            elif (db.model == "NRCan-PyPsa").any():
                df = pypsa_emissions.process({scenario_name: db})
                dfs.append(df)
            elif (db.model == "PyPSA_CAN").any():
                df = pypsa_can_emissions.process({scenario_name: db})
                dfs.append(df)
            elif (db.model == "Sutubra").any():
                df = temoa_emissions.process({scenario_name: db})
                dfs.append(df)
            elif (db.model == "cef").any():
                df = cef_emissions.process({scenario_name: db})
                df['scenario'] = 'CEF|' + df['scenario']
                dfs.append(df)
            else:
                print(f"Model not implemented for {scenario_name}")
        except Exception as e:
            print(f"Error processing {scenario_name}: {e}")

    if dfs:
        return pd.concat(dfs)
    else:
        return pd.DataFrame()


