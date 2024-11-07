import base64
import io
import json
import os
import pickle
import urllib.request as urllib
import multiprocessing as mp
from typing import Tuple, Callable
from collections import defaultdict

import chardet
import pandas as pd

import profiles
from utils.generic_profile.generic_profile import GenericProfile
from utils.constants import model_mapping, exclude_from_comparison

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
    profile_order = ['Power System Models', 'COPPER', 'Canada Energy Futures', 'ECCC-NextGrid',
                     'NATEM Canada', 'HEC-PITHOS', 'NRCan-PyPsa', 'PyPSA_CAN',
                     'Sutubra-TEMOA']
    def __init__(self):
        self.api_key = ''
        self.profiles = self.load_profiles()
        for profile in self.profiles.values():
            if profile.name not in model_mapping.keys():
                model_mapping[profile.name] = [profile.display_name]
        self.data = {}
        self.processed = []
        self.processed_data = {}
        self.viz = {}
        self.to_delete = []
        self.runs = pd.DataFrame()

    def preload_data(self, data_files):
        data_files = [file for file in data_files if file not in self.data.keys()]
        fail = False
        for file in data_files:
            print('Preloading', file)
            f_name, extension = os.path.splitext(file)
            if extension == '.csv':
                df = pd.read_csv(os.path.join('data', file))
            elif extension == '.xlsx':
                dfs = []
                xls = pd.ExcelFile(os.path.join('data', file))
                for sheet in xls.sheet_names:
                    _df = xls.parse(sheet)
                    # infer types of the column names
                    _df.columns = _df.columns.astype(str)
                    dfs.append(_df)
                # Combine all DataFrames into one
                df = pd.concat(dfs, ignore_index=True)
            else:
                fail = True
                print(f'{file}: File type not supported, only .csv and .xlsx are supported')
                continue

            checked, message, file = self.check_content(file, df, file.split('.')[-1], False)
            if not checked:
                fail = True
            else:
                profiles = list(self.data[file]['visualizations'].keys())
                colors = []
                for p in profiles:
                    colors.append(self.profiles[p].color)

        if fail:
            print(fail)

        self.process_data()



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

        if filename in self.data:
            counter = 1
            while f'{filename}_{counter}' in self.data:
                counter += 1
            filename = f'{filename}_{counter}'

        self.data[filename] = {}

        self.data[filename]['content'] = df

        # make all headers lowercase
        df.columns = df.columns.str.lower()

        model = df.model.unique()[0] if not df.empty and 'model' in df.columns else filename

        profile_options = model_mapping.get(model, None)
        if profile_options is None:
            # if df has columns model, scenario, unit, region, variable, value
            if all(col in df.columns for col in ['model', 'scenario', 'variable', 'value', 'region', 'time']):
                profile = create_generic_profile(df, model)
                self.profiles[profile.display_name] = profile
                profile_options = [profile.display_name]

        profiles_to_check = {profile_name: self.profiles[profile_name] for profile_name in
                             profile_options} if profile_options else self.profiles

        visualizations = defaultdict(list)
        selected = defaultdict(list)
        for profile_name, profile in profiles_to_check.items():
            for viz_name, viz_dict in profile.viz_options.items():
                check_func = viz_dict.get('check')
                if check_func(df):
                    visualizations[profile.display_name].append(viz_name)
                    selected[profile.display_name].append(viz_name)

        self.data[filename]['visualizations'] = visualizations
        self.data[filename]['selected'] = selected
        self.data[filename]['scenario'] = df.scenario.unique().tolist()[
            0] if not df.empty or 'scenario' in df.columns else filename

        return filename

    def process_data(self, reset=False):
        """
        Process the data that has been loaded into the data handler.
        :return:
        """

        # Collect results
        if reset:
            self.processed_data = {}
            self.processed = []
        # Collect data from all selected profiles
        data_collection = {}
        process_power_system = False
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
                    else:
                        process_power_system = True
                self.processed.append(fname)

        results = []
        for profile in data_collection.keys():
            results.extend(self.profiles[profile].process_data(data_collection[profile]))

        if process_power_system:
            power_system_results=self.profiles['Power System Models'].process_data(results)
            if power_system_results is not None:
                results.extend(power_system_results)


        for profile, viz, processed_data in results:
            if self.processed_data.get(profile) is None:
                self.processed_data[profile] = {}
            if self.processed_data[profile].get(viz) is None:
                self.processed_data[profile][viz] = processed_data
            else:
                self.processed_data[profile][viz] = pd.concat([self.processed_data[profile][viz], processed_data])

        dfs = {}
        classes = []
        variables = []
        for model, viz_option in self.processed_data.items():
            print('Processing', model)
            if model in exclude_from_comparison:
                continue
            if model == 'Power System Models' or model == 'Generic Comparison':
                continue
            for viz, viz_data in viz_option.items():
                if viz == 'Overview':
                    continue
                columns = viz_data.columns.tolist()
                # check if column of viz_data contains 'variable', 'value', 'region', 'time', 'scenario'
                if all(col in columns for col in ['variable', 'value', 'region', 'time', 'scenario']):
                    df = viz_data.copy()
                    variables += df.variable.unique().tolist()
                    df['variable'] = viz + '|' + df['variable']
                    df['scenario'] = model + '|' + df['scenario']
                    df['unit'] = 'unit'
                    if dfs.get(viz, None) is None:
                        dfs[viz] = [df]
                    else :
                        dfs[viz].append(df)
                    classes.append(viz)
                else:
                    print(f"Data for {model} - {viz} does not contain the necessary columns")

        if classes:
            classes = list(set(classes))
            profile = GenericProfile('Generic Comparison', classes, variables)
            self.profiles['Generic Comparison'] = profile
            self.processed_data['Generic Comparison'] = {}
            for viz in classes:
                self.processed_data['Generic Comparison'][viz] = pd.concat(dfs[viz])
            overview_data = []
            for viz in classes:
                overview_dfs = []
                for df in dfs[viz]:
                    # if CAN in region, remove all other regions
                    if 'region' in df.columns:
                        if 'CAN' in df['region'].unique():
                            df = df[df['region'] == 'CAN']
                        elif 'National' in df['region'].unique():
                            df = df[df['region'] == 'National']

                    # if time is a Timestamp, convert to int only keeping the year
                    if df['time'].dtype == 'datetime64[ns]':
                        df['time'] = df['time'].dt.year

                    overview_dfs.append(df)

                data = pd.concat(overview_dfs)
                data['variable'] = viz

                data = data.groupby(['scenario', 'variable', 'time']).sum(numeric_only=True).reset_index()

                data['region'] = 'National'

                overview_data.append(data)

            full_df = pd.concat(overview_data)
            self.processed_data['Generic Comparison']['Overview'] = full_df[['scenario', 'variable', 'time', 'value', 'region']]

        print("processed", self.processed_data)


    def get_viz(self, profile: str, viz: str, window_id: str):
        return self.profiles[profile].viz_options[viz]['viz'](self.processed_data[profile][viz], window_id)

    def get_viz_options(self):
        """
        Get the visualizations that are available for each profile.
        :return:
        """
        viz = {}
        for model, viz_options in self.processed_data.items():
            for viz_name in viz_options.keys():
                if viz.get(model) is None:
                    viz[model] = []
                viz[model].append(viz_name)
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
                    found[model.display_name] = model

        return found

    def link(self, app):
        for profile in self.profiles.values():
            profile.link(app)
        GenericProfile.link(app)

    def check_content(self, filename, content, extension, encoded=True):
        if content is None:
            return
        if encoded:
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
                    # Detect the encoding using chardet
                    detected_encoding = chardet.detect(decoded)['encoding']
                    print(f"Detected encoding: {detected_encoding}")

                    # Use the detected encoding to decode the file content
                    df = pd.read_csv(io.StringIO(decoded.decode(detected_encoding)))
            except pd.errors.EmptyDataError:
                df = pd.DataFrame()
            except UnicodeDecodeError as e:
                print(f"Decoding error: {e}")
                # Fallback to a common alternative encoding (ISO-8859-1)
                df = pd.read_csv(io.StringIO(decoded.decode('ISO-8859-1')))
        else:
            df = content


        # make all headers lowercase
        df.columns = df.columns.str.lower()

        if 'model' in df.columns:
            model = df.model.unique()[0]
            if model not in model_mapping:
                # check if df.columns contain all the following: model, scenario, variable, value, unit
                if not all(col in df.columns for col in ['model', 'scenario', 'variable', 'value', 'region', 'time']):
                    diff = {'model', 'scenario', 'variable', 'value', 'region', 'time'} - set(df.columns)
                    print(f"Columns missing in {filename}", diff)
                    return False, f"These Columns were expected: {diff}", filename

            else:
                # make sure scenario is in the columns
                if 'scenario' not in df.columns:
                    return False, "Scenario column is missing from the data.", filename

        if filename in self.data:
            counter = 1
            while f'{filename}_{counter}' in self.data:
                counter += 1
            filename = f'{filename}_{counter}'

        model = df.model.unique()[0] if not df.empty and 'model' in df.columns else filename


        profile_options = model_mapping.get(model, None)
        if profile_options is None:
            # if df has columns model, scenario, unit, region, variable, value
            if all(col in df.columns for col in ['model', 'scenario', 'variable', 'value', 'region', 'time']):
                profile = create_generic_profile(df, model)
                self.profiles[profile.display_name] = profile
                profile_options = [profile.display_name]

            else:
                return False, f"Could not find the profile for {filename} and can't generate generic plots since the data is not following IAMC format", filename


        self.data[filename] = {}

        self.data[filename]['content'] = df

        profiles_to_check = {profile_name: self.profiles[profile_name] for profile_name in
                             profile_options} if profile_options else self.profiles

        visualizations = defaultdict(list)
        selected = defaultdict(list)
        for profile_name, profile in profiles_to_check.items():
            for viz_name, viz_dict in profile.viz_options.items():
                check_func = viz_dict.get('check')
                if check_func(df):
                    visualizations[profile.display_name].append(viz_name)
                    selected[profile.display_name].append(viz_name)

        self.data[filename]['visualizations'] = visualizations
        self.data[filename]['selected'] = selected
        self.data[filename]['scenario'] = df.scenario.unique().tolist()[
            0] if not df.empty or 'scenario' in df.columns else filename

        return True, "Data loaded successfully!", filename

    def save(self, filename):
        """
        Save self.data, self.processed_data, self.processedto a file.
        :param filename: The name of the file to save the data handler to.
        :return:
        """

        # pickle self.data, self.processed_data, self.processed to a file
        with open(filename, 'wb') as f:
            pickle.dump([self.data, self.processed_data, self.processed], f)


    def load(self, filename):
        """
        Load self.data, self.processed_data, self.processed from a file.
        :param filename: The name of the file to load the data handler from.
        :return:
        """
        with open(filename, 'rb') as f:
            self.data, self.processed_data, self.processed = pickle.load(f)



