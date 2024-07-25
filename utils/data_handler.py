import base64
import io
import json
import urllib.request as urllib
import multiprocessing as mp
from typing import Tuple, Callable
from collections import defaultdict

import pandas as pd

import profiles
from utils.generic_profile.generic_profile import GenericProfile
from utils.generic_profile.callbacks import generic_callback

model_mapping = {
    'silver' : ['SILVER Output'],
    'copper': ['COPPER Output', 'Power System Models'],
    'cef': ['Canada Energy Futures', 'Power System Models'],
    'ECCC-NextGrid': ['ECCC-NextGrid Output', 'Power System Models'],
    'NATEM-POWER': ['NATEM-POWER Output', 'Power System Models'],
    'HEC-PITHOS': ['HEC-PITHOS Output', 'Power System Models'],
    'NRCan-PyPsa': ['NRCan-PyPsa Output', 'Power System Models'],
    'PyPSA_CAN': ['PyPSA_CAN Output', 'Power System Models'],
    'Sutubra-TEMOA': ['Sutubra-TEMOA Output', 'Power System Models'],
}




def create_generic_profile(df, model):
    """
    Creates a generic profile based on the data frame and model provided.

    :param df: A pandas DataFrame containing the data.
    :param model: The model used to create the profile.

    :return: The generated generic profile.
    """
    classes = df.variable.str.split('|').str[0].unique().tolist()
    variables = df.variable.apply(lambda x: '|'.join(x.split('|')[1:])).unique().tolist()
    profile = GenericProfile(model, classes, variables)
    return profile


def get_generators(api_key):
    """
    :param api_key: The API key required for access to the generator data.
    :return: A DataFrame containing the latitude, longitude, generator type, installed capacity, and facility code of each generator.

    This method makes an HTTP GET request to retrieve generator data from a remote server. It requires the `api_key` parameter, which is used to authenticate the request. The generator data
    * is then parsed and transformed into a DataFrame.

    Example usage:
    ```
    api_key = 'your_api_key'
    generators = get_generators(api_key)
    ```
    """
    table = 'generators'
    with urllib.urlopen(f'http://206.12.95.102/{table}?key={api_key}') as response:
        response_content = response.read()
        json_response = json.loads(response_content)
        data = pd.json_normalize(json_response)

    return data[['latitude', 'longitude', 'gen_type_copper', 'facility_installed_capacity', 'generation_facility_code']]


def get_transmission(api_key):
    """
    Retrieves transmission data from an API based on the given API key.

    :param api_key: API key for accessing the transmission data.
    :return: Dataframe containing transmission data.
    """
    table = 'transmission_lines'
    with urllib.urlopen(f'http://206.12.95.102/{table}?key={api_key}') as response:
        response_content = response.read()
        json_response = json.loads(response_content)
        data = pd.json_normalize(json_response)

    node_data = data[['starting_node_code', 'ending_node_code', 'summer_capacity']]

    table = 'nodes'
    with urllib.urlopen(f'http://206.12.95.102/{table}?key={api_key}') as response:
        response_content = response.read()
        json_response = json.loads(response_content)
        data = pd.json_normalize(json_response)

    line_data = data[['node_code', 'latitude', 'longitude']]

    df = pd.merge(node_data, line_data, left_on='starting_node_code', right_on='node_code', how='left')
    df = df.rename(columns={'latitude': 'latitude_start', 'longitude': 'longitude_start'})
    df = df.drop(columns=['node_code'])
    df = pd.merge(df, line_data, left_on='ending_node_code', right_on='node_code', how='left')
    df = df.rename(columns={'latitude': 'latitude_end', 'longitude': 'longitude_end'})
    df = df.drop(columns=['node_code'])

    return df

def get_vre_capacity_factors(api_key):
    """
    :param api_key: An API key used to authenticate and access the data.
    :return: A Pandas DataFrame containing VRE (Variable Renewable Energy) capacity factor data for wind and solar energy sources.
    """
    tables = ['wind_capacity_factor', 'solar_capacity_factor']
    dfs = []
    for table in tables:
        print(table)
        data = pd.read_csv(f'http://206.12.95.102/{table}?year=2021&key={api_key}', index_col=0)
        data = data.reset_index()
        data['variable'] = table
        dfs.append(data)

    vre_data = pd.concat(dfs)
    print(vre_data.head())
    vre_data = vre_data.melt(id_vars=['h', 'variable'], var_name='grid_cell', value_name='value')
    vre_data['grid_cell'] = vre_data['grid_cell'].astype(int)
    vre_data['value'] = vre_data['value'].astype(float)
    vre_data = vre_data.groupby(['grid_cell', 'variable']).mean().reset_index()
    # drop h
    vre_data = vre_data.drop(columns=['h'])
    table = 'grid_cell_info'
    with urllib.urlopen(f'http://206.12.95.102/{table}?key={api_key}') as response:
        response_content = response.read()
        json_response = json.loads(response_content)
        data = pd.json_normalize(json_response)

    grid_data = data[['grid_cell', 'latitude', 'longitude']]
    print(grid_data.head())
    vre_data = pd.merge(vre_data, grid_data, left_on='grid_cell', right_on='grid_cell', how='left')
    vre_data = vre_data.drop(columns=['grid_cell'])

    vre_data['latitude'] = vre_data['latitude'].astype(float)
    vre_data['longitude'] = vre_data['longitude'].astype(float)

    return vre_data


def get_demand(api_key):
    """
    Retrieves demand data for multiple provinces and years.

    :param api_key: The API key used for authentication.
    :return: A pandas DataFrame containing the demand data.
    """
    table = 'provincial_demand'
    demand_inputs = [['AB', '2021'], ['BC', '2021'], ['NB', '2021'], ['NL', '2021'], ['NS', '2021'],
                     ['ON', '2021'], ['QC', '2021'], ['SK', '2021'], ['MB', '2021'], ['PE', '2021']]
    timezone = {
        'AB': -7,
        'BC': -8,
        'NB': -4,
        'NL': -4,
        'NS': -4,
        'ON': -5,
        'QC': -5,
        'SK': -6,
        'MB': -6,
        'PE': -4
    }
    dfs = []
    for prov, year in demand_inputs:
        print(prov, year)
        with urllib.urlopen(f'http://206.12.95.102/{table}?province={prov}&year={year}&key={api_key}') as response:
            response_content = response.read()
            json_response = json.loads(response_content)
            prov_data = pd.json_normalize(json_response)

        prov_data['hour'] = prov_data['annual_hour_ending'] - timezone[prov] - 1
        prov_data = prov_data[['hour', 'demand_MWh', 'province', 'local_time']]
        dfs.append(prov_data)

    return pd.concat(dfs)

class DataHandler:
    """

    """
    profile_order = ['Power System Models', 'COPPER Output', 'Canada Energy Futures', 'ECCC-NextGrid Output',
                     'NATEM-POWER Output', 'HEC-PITHOS Output', 'NRCan-PyPsa Output', 'PyPSA_CAN Output',
                     'Sutubra-TEMOA Output']
    def __init__(self):
        self.api_key = ''
        self.profiles = self.load_profiles()
        self.data = {}
        self.processed = []
        self.processed_data = {}
        self.viz = {}
        self.runs = pd.DataFrame()


    def select_run(self, profile, scenario, author,db):
        """
        Loading data from the CODERS Database, according to the selected profile, scenario, author and database.

        :param profile: str: The selected profile
        :param scenario: str: The selected scenario
        :param author: str: The selected author
        :param db: str: The selected database, either 'MMCW' or 'results', where MMCW requires a different URL and special access
        :return:
        """
        print('Selecting run', profile, scenario, author, db)
        if scenario == 'CEF2023':
            tables = ["benchmark_prices", "butane", "crude_oil_production", "electricity_capacity",
                      "electricity_capacity_technology", "electricity_generation", "electricity_generation_technology",
                      "electricity_interchange", "electricity_primary_demand", "end_use_demand", "end_use_prices",
                      "ethane", "greenhouse_gas_emissions", "hydrogen_production", "macro_indicators",
                      "natural_gas_drilling", "natural_gas_production", "pentanes_plus", "propane"]
            table_dfs = []
            for table in tables:
                url = f'http://206.12.95.102/cef/{table}?key={self.api_key}'
                response = urllib.urlopen(url)
                data = json.loads(response.read())
                df = pd.DataFrame(data)
                # infer data type for each column in df
                df = df.infer_objects()
                # prepend table| to variable entries
                df['variable'] = table + '|' + df['variable']
                table_dfs.append(df)
            df = pd.concat(table_dfs)
            df.value = pd.to_numeric(df.value, errors='coerce')
            df['model'] = 'cef'
        elif scenario == 'CODERS2024':
            print('Getting Generators...')
            generators = get_generators(self.api_key)
            print(generators.head())
            print('Getting Transmission...')
            transmission = get_transmission(self.api_key)
            print(transmission.head())
            print('Getting VRE Capacity Factors...')
            vre_capacity_factors = get_vre_capacity_factors(self.api_key)
            print(vre_capacity_factors.head())
            print('Getting Demand...')
            demand = get_demand(self.api_key)
            print(demand.head())
            print('Data Pulled Successfully!')
            generators['type'] = 'Generation Capacity'
            transmission['type'] = 'Transmission'
            demand['type'] = 'Demand'
            vre_capacity_factors['type'] = 'VRE Capacity Factor'

            df = pd.concat([generators, transmission, demand, vre_capacity_factors])
            df['model'] = 'CODERS'
            df['scenario'] = 'CODERS2024'

        else:
            endpoint = 'MMCW' if db == 'MMCW' else 'results'
            url = f'http://206.12.95.102/{endpoint}?key={self.api_key}&scenario={scenario}&model={profile}'
            print(url)
            response = urllib.urlopen(url)
            data = json.loads(response.read())
            df = pd.DataFrame(data)
            # infer data type for each column in df
            df = df.infer_objects()
            df.value = pd.to_numeric(df.value, errors='coerce')

        filename = f'{profile}|{scenario}|{author}|{db}'

        if filename not in self.data:
            self.data[filename] = {}

        self.data[filename]['content'] = df

        # Check if the data has visualizations it can be processed into
        visualizations = {}
        selected = {}
        for profile_name, profile in self.profiles.items():
            for viz_name, viz_dict in profile.viz_options.items():
                if viz_name not in visualizations:
                    check_func = viz_dict.get('check')
                    if check_func(df):
                        if visualizations.get(profile.name) is None:
                            visualizations[profile.name] = []
                        visualizations[profile.name].append(viz_name)

                        if selected.get(profile.name) is None:
                            selected[profile.name] = []
                        selected[profile.name].append(viz_name)

        self.data[filename]['visualizations'] = visualizations
        self.data[filename]['selected'] = selected
        self.data[filename]['scenario'] = df.scenario.unique().tolist()[
            0] if not df.empty or 'scenario' in df.columns else filename

    def process_data(self):
        """
        Process the data that has been loaded into the data handler.
        :return:
        """

        # Collect data from all selected profiles
        data_collection = {}
        for fname, data in self.data.items():
            if not fname in self.processed:
                for profile, viz_options in data['selected'].items():
                    if profile != 'Power System Models':
                        scenario = data['scenario']

                        for viz in viz_options:
                            if data_collection.get(profile) is None:
                                data_collection[profile] = {}
                            if data_collection[profile].get(viz) is None:
                                data_collection[profile][viz] = {}
                            data_collection[profile][viz][scenario] = data['content'].copy()
                self.processed.append(fname)

        results = []
        for profile in data_collection.keys():
            results.extend(self.profiles[profile].process_data(data_collection[profile]))

        # Process profiles that are considered Power System Models
        power_system_results=self.profiles['Power System Models'].process_data(results)
        if power_system_results is not None:
            results.extend(power_system_results)

        # Collect results
        for profile, viz, processed_data in results:
            if self.processed_data.get(profile) is None:
                self.processed_data[profile] = {}
            if self.processed_data[profile].get(viz) is None:
                self.processed_data[profile][viz] = processed_data
            else:
                self.processed_data[profile][viz] = pd.concat([self.processed_data[profile][viz], processed_data])

    def get_viz(self, profile: str, viz: str, window_id: str):
        return self.profiles[profile].viz_options[viz]['viz'](self.processed_data[profile][viz], window_id)

    def get_viz_options(self):
        """
        Get the visualizations that are available for each profile.
        :return:
        """
        viz = {}
        for data in self.data.values():
            for profile, viz_options in data['selected'].items():
                if viz_options:
                    if viz.get(profile) is None:
                        viz[profile] = []
                    viz[profile].extend(viz_options)
        for profile, viz_options in viz.items():
            viz[profile] = list(set(viz_options))
        return viz

    def load_profiles(self):
        # Finds all profiles in the profiles folder and loads them
        found = {}
        for profile in profiles.__all__:
            module = __import__(f"{profile}", locals(), globals(), [profile])
            # Find the class in the module and instantiate it if it is not called BaseProfile
            for name in dir(module):
                obj = getattr(module, name)
                if isinstance(obj, type) and obj.__module__ == module.__name__ and obj.__name__ != 'BaseProfile':
                    model = obj()
                    found[model.name] = model

        return found

    def link(self, app):
        for profile in self.profiles.values():
            profile.link(app)
        generic_callback.link(app)

    def check_content(self, filename, content, extension):
        if content is None:
            return

        # decode the content string
        content_type, content_string = content.split(',')
        decoded = base64.b64decode(content_string)

        try:
            if extension == 'xlsx':
                xls = pd.ExcelFile(io.BytesIO(decoded))
                # Get all sheet names
                sheet_names = xls.sheet_names
                # Read all sheets into a DataFrame list
                df_list = []
                for sheet in sheet_names:
                    print(sheet)
                    _df = xls.parse(sheet)
                    # infer types of the column names
                    _df.columns = _df.columns.astype(str)
                    df_list.append(_df)
                # Combine all DataFrames into one
                df = pd.concat(df_list, ignore_index=True)
            else:
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        except pd.errors.EmptyDataError:
            df = pd.DataFrame()


        # make all headers lowercase
        df.columns = df.columns.str.lower()

        # check if df.columns contain all of the following: model, scenario, variable, value, unit
        if not all(col in df.columns for col in ['model', 'scenario', 'variable', 'value', 'region', 'time']):
            diff = {'model', 'scenario', 'variable', 'value', 'region', 'time'} - set(df.columns)
            print(f"Columns missing in {filename}", diff)
            return False, f"These Columns were expected: {diff}"

        if filename not in self.data:
            self.data[filename] = {}

        self.data[filename]['content'] = df

        model = df.model.unique()[0] if not df.empty and 'model' in df.columns else filename


        profile_options = model_mapping.get(model, None)
        if profile_options is None:
            profile = create_generic_profile(df, model)
            self.profiles[profile.name] = profile
            profile_options = [profile.name]

        profiles_to_check = {profile_name: self.profiles[profile_name] for profile_name in
                             profile_options} if profile_options else self.profiles

        visualizations = defaultdict(list)
        selected = defaultdict(list)
        for profile_name, profile in profiles_to_check.items():
            for viz_name, viz_dict in profile.viz_options.items():
                check_func = viz_dict.get('check')
                if check_func(df):
                    visualizations[profile.name].append(viz_name)
                    selected[profile.name].append(viz_name)

        self.data[filename]['visualizations'] = visualizations
        self.data[filename]['selected'] = selected
        self.data[filename]['scenario'] = df.scenario.unique().tolist()[
            0] if not df.empty or 'scenario' in df.columns else filename

        return True, "Data loaded successfully!"
