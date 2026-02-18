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
    Check if 'Results_recap_carbon_AP_tech' is present in the 'variable' column.

    Parameters:
        df (pd.DataFrame): The DataFrame to check.

    Returns:
        bool: True if the specified prefix is found, False otherwise.
    """
    try:
        if (df.model == 'copper').any():
            return copper_cost_total.check(df)
        elif (df.model == 'ECCC-NextGrid').any():
            return nextgrid_cost_total.check(df)
        elif (df.model == 'NATEM_Canada').any():
            return natem_cost_total.check(df)
        elif (df.model == 'PITHOS').any():
            return pithos_cost_total.check(df)
        elif (df.model == 'NRCan-PyPsa').any():
            return pypsa_cost_total.check(df)
        elif (df.model == 'PyPSA_CAN').any():
            return pypsa_can_cost_total.check(df)
        elif (df.model == 'Sutubra').any():
            return temoa_cost_total.check(df)
        else:
            return False
    except Exception as e:
        print(f"ERROR in cost_total.check: {e}")
        return False


def process(selected: dict):
    dfs = []
    for scenario_name, db in selected.items():
        try:
            if (db.model == 'copper').any():
                df = copper_cost_total.process({scenario_name: db})
                dfs.append(df)
            elif (db.model == 'ECCC-NextGrid').any():
                df = nextgrid_cost_total.process({scenario_name: db})
                dfs.append(df)
            elif (db.model == 'NATEM_Canada').any():
                df = natem_cost_total.process({scenario_name: db})
                dfs.append(df)
            elif (db.model == 'PITHOS').any():
                df = pithos_cost_total.process({scenario_name: db})
                dfs.append(df)
            elif (db.model == 'NRCan-PyPsa').any():
                df = pypsa_cost_total.process({scenario_name: db})
                dfs.append(df)
            elif (db.model == 'PyPSA_CAN').any():
                df = pypsa_can_cost_total.process({scenario_name: db})
                dfs.append(df)
            elif (db.model == 'Sutubra').any():
                df = temoa_cost_total.process({scenario_name: db})
                dfs.append(df)
            else:
                print(f"Model not implemented for {scenario_name}")
        except Exception as e:
            print(f"Error processing {scenario_name}: {e}")

    if dfs:
        return pd.concat(dfs)
    else:
        return pd.DataFrame()


