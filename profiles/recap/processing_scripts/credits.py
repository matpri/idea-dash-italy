import pandas as pd
from profiles.recap import utils


def check(df):
    """
    Check if the data contains credit-related variables
    """
    try:
        if (df.model == 'CIM2').any():
            if df.variable.str.startswith("Credits").any():
                return True
        return False
    except Exception as e:
        print("Credits check", e)
        return False


def process(selected: dict):
    """
    Process credit data from IAMC formatted files
    
    The data contains variables in format:
    - Credits|Credit Supply|[Sector]
    - Credits|Credit Demand|[Sector]
    - Credits|Net Balance|[Sector]
    """
    dfs = []
    
    for scenario_name, db in selected.items():
        df = db.copy()
        
        # Filter for credit-related variables
        credit_vars = df[
            df['variable'].str.startswith('Credits', na=False)
        ].copy()
        
        if not credit_vars.empty:
            # Add scenario name
            credit_vars['scenario'] = scenario_name
            
            # Map region names if needed
            if 'region' in credit_vars.columns:
                credit_vars['region'] = credit_vars['region'].map(utils.province_short).fillna(credit_vars['region'])
            
            # Parse variable structure: Credits|Credit Supply|Waste -> type: Credit Supply, sector: Waste
            credit_vars['credit_type'] = credit_vars['variable'].apply(
                lambda x: x.split('|')[1] if '|' in x and len(x.split('|')) > 1 else 'Unknown'
            )
            credit_vars['sector'] = credit_vars['variable'].apply(
                lambda x: x.split('|')[2] if '|' in x and len(x.split('|')) > 2 else 'Total'
            )
            
            # Create a simplified variable name for visualization
            credit_vars['display_variable'] = credit_vars['sector']
            
            # Group by relevant columns and sum values
            credit_vars = credit_vars.groupby([
                'region', 'scenario', 'time', 'credit_type', 'sector', 'display_variable', 'unit'
            ]).agg({'value': 'sum'}).reset_index()
            
            dfs.append(credit_vars)
    
    if dfs:
        full_df = pd.concat(dfs, ignore_index=True)
        # Ensure time column is numeric for plotting
        full_df['time'] = pd.to_numeric(full_df['time'], errors='coerce')
        return full_df
    else:
        # Return empty dataframe with expected columns if no data
        return pd.DataFrame(columns=['region', 'scenario', 'time', 'credit_type', 
                                    'sector', 'display_variable', 'value', 'unit'])