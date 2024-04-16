import base64
import io
import json
import urllib.request as urllib

import dash_mantine_components as dmc
import pandas as pd
from dash import html, Output, Input

import profiles


class DataHandler:
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
        self.data[filename]['scenario'] = df.scenario.unique().tolist()[0] if not df.empty or 'scenario' in df.columns else filename


    def process_data(self):
        self.processed_data = {}
        data_collection = {}
        for fname, data in self.data.items():
            for profile, viz_options in data['selected'].items():
                for viz in viz_options:
                    if data_collection.get(profile) is None:
                        data_collection[profile] = {}
                    if data_collection[profile].get(viz) is None:
                        data_collection[profile][viz] = {}
                    data_collection[profile][viz][data['scenario']] = data['content'].copy()

        for profile, viz_options in data_collection.items():
            for viz, data in viz_options.items():
                if self.processed_data.get(profile) is None:
                    self.processed_data[profile] = {}
                self.processed_data[profile][viz] = self.profiles[profile].viz_options[viz]['process'](
                    data_collection[profile][viz])

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

        if filename not in self.data:
            self.data[filename] = {}

        self.data[filename]['content'] = df

        visualizations = {}
        selected = {}
        for profile_name, profile in self.profiles.items():
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
        self.data[filename]['scenario'] = df.scenario.unique().tolist()[0] if not df.empty or 'scenario' in df.columns else filename
