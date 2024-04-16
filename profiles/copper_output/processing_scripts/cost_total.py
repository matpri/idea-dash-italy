import pandas as pd
import os

from profiles.copper_output import utils

def check(df):
    """
    Check if 'cost' is present in the 'variable' column.

    Args:
        df (DataFrame): The DataFrame to check.

    Returns:
        bool: True if the specified prefix is found, False otherwise.
    """
    print("Checking for cost in variable column")
    try:
        if df.model.str.contains("copper").any():
            if df.variable.str.contains("Costs|").any():
                return df[df.variable.str.contains("Costs|")]['value'].sum() != 0
        return False
    except Exception as e:
        print("cost check", e)
        return False

def format_df(df):
    """
    Extracts province, year, and other relevant information from column names in the DataFrame.

    Args:
        df (DataFrame): Input DataFrame containing cost data.

    Returns:
        DataFrame: Formatted data with extracted information.
    """
    df['region'] = df['region'].map(utils.province_short).fillna(df['region'])
    df = df.groupby(['region', 'variable', 'time','scenario']).sum(numeric_only=True).reset_index()
    return df


def calculate_generation_capacity(df):
    """
    Calculates the generation capacity data from the DataFrame.

    Args:
        df (DataFrame): Input DataFrame containing cost data.

    Returns:
        DataFrame: Calculated generation capacity data.

    """
    # Extract generation capacity data from df
    gen_cap_df = df[df.variable.str.startswith("Capital Costs|")].copy()
    gen_cap_df['variable'] = gen_cap_df['variable'].str.split("|").str[1]
    # Rename entries based on gen_cap_names_dict
    gen_cap_df = gen_cap_df.groupby(["variable", "region", "time", "scenario"], as_index=False).sum(numeric_only=True)

    # Compute Canadian total over all regions
    can_gen_cap_df = gen_cap_df.groupby(["variable", "time", "scenario"], as_index=False).sum(numeric_only=True)

    # Add a row with "Region" as "CAN"
    can_gen_cap_df = can_gen_cap_df.assign(region='CAN')

    # Concatenate the original DataFrame and the aggregated DataFrame
    gen_cap_df = pd.concat([gen_cap_df, can_gen_cap_df], ignore_index=True)

    # Rearrange indexes to ["variable", "region", "time", "scenario", "value"]
    gen_cap_df = gen_cap_df[["variable", "region", "time", "scenario", "value"]]
    return gen_cap_df


def calculate_fom(df):
    """
    Calculates the fixed operating and maintenance (FOM) cost data from the DataFrame.

    Args:
        df (DataFrame): Input DataFrame containing cost data.

    Returns:
        DataFrame: Calculated FOM cost data.

    """

    fom_df = df[df.variable.str.startswith("Fixed O&M Costs|")].copy()
    fom_df['variable'] = fom_df['variable'].str.split("|").str[1]
    fom_df.sort_values(by=["region", "time", 'variable'])
    fom_df = fom_df.groupby(["variable", "region", "time", "scenario"]).sum(numeric_only=False).reset_index()

    # Aggregate data over all regions by variable, time, and scenario and sum the values
    can_fom_df = fom_df.groupby(["variable", "time", "scenario"], as_index=False).sum(numeric_only=True)

    # Add a row with "Region" as "CAN"
    can_fom_df = can_fom_df.assign(region='CAN')

    # Concatenate the original DataFrame and the aggregated DataFrame
    fom_df = pd.concat([fom_df, can_fom_df], ignore_index=True)

    # Rearrange indexes to ["variable", "region", "time", "scenario", "value"]
    fom_df = fom_df[["variable", "region", "time", "scenario", "value"]]
    return fom_df


def calculate_vom(df):
    """
    Calculates the variable operating and maintenance (VOM) cost data from the DataFrame.

    Args:
        df (DataFrame): Input DataFrame containing cost data.

    Returns:
        DataFrame: Calculated VOM cost data.

    """
    vom_df = df[df.variable.str.startswith("Variable O&M Costs|")].copy()
    vom_df['variable'] = vom_df['variable'].str.split("|").str[1]
    vom_df = vom_df.groupby(["variable", "region", "time", "scenario"]).sum(numeric_only=False).reset_index()

    # Aggregate data over all regions by variable, time, and scenario and sum the values
    can_vom_df = vom_df.groupby(["variable", "time", "scenario"], as_index=False).sum(numeric_only=True)

    # Add a row with "Region" as "Can"
    can_vom_df = can_vom_df.assign(region='CAN')

    # Concatenate the original DataFrame and the aggregated DataFrame
    vom_df = pd.concat([vom_df, can_vom_df], ignore_index=True)

    # Rearrange indexes to ["variable", "region", "time", "scenario", "value"]
    vom_df = vom_df[["variable", "region", "time", "scenario", "value"]]
    return vom_df


def calculate_total_cost(formatted_cost, gen_capacity, fom, vom):
    """
    Calculates the total cost by combining various cost components.

    Args:
        formatted_cost (DataFrame): Formatted cost data.
        gen_capacity (DataFrame): Calculated generation capacity data.
        fom (DataFrame): Calculated FOM cost data.
        vom (DataFrame): Calculated VOM cost data.

    Returns:
        DataFrame: Total cost data.

    """
    # Capacity cost == sum across all variables for each region and time
    capacity_cost = gen_capacity.groupby(["time", "region", "scenario"], as_index=False)["value"].sum(
        numeric_only=True)
    capacity_cost = capacity_cost.assign(variable='capacity_cost')

    # Carbon cost == where variable is "Carbon Cost" in formatted df and then add row for Canada as sum of all regions

    carbon_cost = formatted_cost[formatted_cost.variable.str.startswith("Carbon Costs|")].copy()
    can_carbon_cost = carbon_cost.groupby(["time", "scenario"], as_index=False)["value"].sum(numeric_only=True)
    can_carbon_cost = can_carbon_cost.assign(region='CAN', variable='Carbon Cost')
    carbon_cost = pd.concat([carbon_cost, can_carbon_cost], ignore_index=True)
    # Rename values in variable from "Carbon Cost" to carbon_tax_cost
    carbon_cost = carbon_cost.assign(variable='carbon_tax_cost')

    # FOM cost == sum across all variables for each region and time
    fom_cost = fom.groupby(["time", "region", "scenario"], as_index=False)["value"].sum(numeric_only=True)
    fom_cost = fom_cost.assign(variable='fom_cost')

    # Variable OM cost weighted == sum across all variables for each region and time
    variable_om_cost_weighted = vom.groupby(["time", "region", "scenario"], as_index=False)["value"].sum(
        numeric_only=True)
    variable_om_cost_weighted = variable_om_cost_weighted.assign(variable='variable_om_cost_weighted')

    # Fuel cost weighted == where variable is "Supply" in formatted df and then add row for Canada as sum of all regions
    fuel_cost_weighted = formatted_cost[formatted_cost.variable.str.startswith("Fuel Costs|")].copy()
    can_fuel_cost_weighted = fuel_cost_weighted.groupby(["time", "scenario"], as_index=False)["value"].sum(
        numeric_only=True)
    can_fuel_cost_weighted = can_fuel_cost_weighted.assign(region='CAN')
    fuel_cost_weighted = pd.concat([fuel_cost_weighted, can_fuel_cost_weighted], ignore_index=True)
    # Rename values in variable from "Supply" to fuel_cost_weighted
    fuel_cost_weighted = fuel_cost_weighted.assign(variable='fuel_cost_weighted')

    # Put all costs together in one DataFrame
    total_costs_df = pd.concat([capacity_cost, carbon_cost, fom_cost, fuel_cost_weighted,
                                variable_om_cost_weighted], ignore_index=True)
    # Rearrange indexes to ["variable", "region", "time", "scenario", "value"]
    total_costs_df = total_costs_df[["variable", "region", "time", "scenario", "value"]]
    total_costs_df.variable = total_costs_df["variable"].map(utils.cost_type).fillna(total_costs_df["variable"])
    # Sort by region, then variable
    return total_costs_df.sort_values(by=['time', 'region', 'variable'], ascending=[True, True, True])

def process(data):
    """
    Process emission data from multiple scenarios based on the 'folders' dictionary.

    Parameters:
        folders (dict): Dictionary containing scenario names as keys and folder paths as values.
        target_dir (str): Target directory.

    Returns:
        pd.DataFrame: Processed DataFrame.
    """
    dfs = []
    for scenario_name, db in data.items():
        df = db.copy()
        df = df[df.variable.str.contains("Costs|")]
        formatted_df = format_df(df)
        gen_cap = calculate_generation_capacity(formatted_df)
        fom = calculate_fom(formatted_df)
        vom = calculate_vom(formatted_df)
        total_cost = calculate_total_cost(formatted_df, gen_cap, fom, vom)
        total_cost['scenario'] = scenario_name
        dfs.append(total_cost)
    full_df = pd.concat(dfs)
    full_df['unit'] = '$ Billions'
    full_df['value'] = full_df['value'].div(1e9)
    return full_df
