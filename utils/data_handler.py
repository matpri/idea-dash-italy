import base64
import io
import json
import urllib.request as urllib

import pandas as pd

import profiles
from utils.generic_profile.generic_profile import GenericProfile
from utils.generic_profile.callbacks import generic_callback

model_mapping = {
    'copper': ['COPPER Output', 'Power System Models'],
    'cef': ['Canada Energy Futures', 'Power System Models'],
    'ECCC-NextGrid': ['ECCC-NextGrid Output', 'Power System Models'],
    'NATEM-POWER': ['NATEM-POWER Output', 'Power System Models'],
    'ESMIA-PITHOS': ['ESMIA-PITHOS Output', 'Power System Models'],
    'NRCAN-PyPsa': ['NRCAN-PyPsa Output', 'Power System Models'],
}


def create_generic_profile(df, model):
    classes = df.variable.str.split('|').str[0].unique().tolist()

    profile = GenericProfile(model, classes)
    return profile


class DataHandler:
    """
    Class responsible for handling data and generating visualizations.

    Attributes:
        api_key (str): API key for accessing data.
        profiles (dict): Dictionary of available profile models.
        data (dict): Dictionary holding data for each file.
        processed_data (dict): Dictionary holding processed data for each profile and visualization.
        viz (dict): Dictionary holding selected visualizations for each file.
        runs (pd.DataFrame): DataFrame holding information about runs.

    Methods:
        select_run(profile: str, scenario: str, author: str) -> None:
            Selects a specific run based on profile, scenario, and author.

        process_data() -> None:
            Processes the collected data and generates processed data for visualizations.

        get_viz(profile: str, viz: str, window_id: str) -> Any:
            Retrieves a specific visualization for a given profile and viz option.

        get_viz_options() -> dict:
            Retrieves the available visualization options.

        load_profiles() -> dict:
            Loads the available profile models.

        link(app: Any) -> None:
            Links the profile models to the application.

        check_content(filename: str, content: str) -> None:
            Checks the content of a file and updates the data and visualizations accordingly.
    """

    def __init__(self):
        self.api_key = ''
        self.profiles = self.load_profiles()
        self.data = {}
        self.processed_data = {}
        self.viz = {}
        self.runs = pd.DataFrame()

    def select_run(self, profile, scenario, author):
        print('Selecting run', profile, scenario, author)
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
        else:
            url = f'http://206.12.95.102/results?key={self.api_key}&scenario={scenario}&model={profile}'
            print(url)
            response = urllib.urlopen(url)
            data = json.loads(response.read())
            df = pd.DataFrame(data)
            # infer data type for each column in df
            df = df.infer_objects()
            df.value = pd.to_numeric(df.value, errors='coerce')

        filename = f'{profile}-{scenario}-{author}'

        if filename not in self.data:
            self.data[filename] = {}

        self.data[filename]['content'] = df

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
        self.processed_data = {}
        data_collection = {}
        for fname, data in self.data.items():
            for profile, viz_options in data['selected'].items():
                scenario = data['scenario']
                if profile == 'Power System Models':
                    model = data['content']['model'].unique()[0]
                    scenario = model + '|' + scenario

                for viz in viz_options:
                    if data_collection.get(profile) is None:
                        data_collection[profile] = {}
                    if data_collection[profile].get(viz) is None:
                        data_collection[profile][viz] = {}
                    data_collection[profile][viz][scenario] = data['content'].copy()

        for profile, viz_options in data_collection.items():
            for viz, data in viz_options.items():
                if self.processed_data.get(profile) is None:
                    self.processed_data[profile] = {}
                try:
                    self.processed_data[profile][viz] = self.profiles[profile].viz_options[viz]['process'](
                        data_collection[profile][viz])
                except Exception as e:
                    print(f"Error processing data for {profile} - {viz}: {e}")
                    self.processed_data[profile][viz] = pd.DataFrame()

    def get_viz(self, profile: str, viz: str, window_id: str):
        return self.profiles[profile].viz_options[viz]['viz'](self.processed_data[profile][viz], window_id)

    def get_viz_options(self):
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

    def check_content(self, filename, content):
        if content is None:
            return

        # decode the content string
        content_type, content_string = content.split(',')
        decoded = base64.b64decode(content_string)

        try:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        except pd.errors.EmptyDataError:
            df = pd.DataFrame()

        # make all headers lowercase
        df.columns = df.columns.str.lower()

        # check if df.columns contain all of the following: model, scenario, variable, value, unit
        if not all(col in df.columns for col in ['model', 'scenario', 'variable', 'value', 'unit', 'region', 'time']):
            print(f"Columns missing in {filename}")
            return

        df = df[['model', 'scenario', 'variable', 'value', 'unit', 'region', 'time']]

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

        visualizations = {}
        selected = {}
        for profile_name, profile in profiles_to_check.items():
            for viz_name, viz_dict in profile.viz_options.items():
                # if viz_name not in visualizations:
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
