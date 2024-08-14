# Extending IDEA

## How to add a New Model Profile

This guide outlines the steps to add a custom model profile to our project. A model profile is used to define the
processing and visualization functions for specific data sets. If you have your own data source or custom requirements,
you can create a custom model profile to integrate it seamlessly.

## Folder Structure

To keep your project organized, we recommend following this folder structure for adding your custom model profile:

```
- profiles
   - custom_model
     - custom_model.py
     - plots.yaml
     - technologies.yaml
     - processing_scripts
         - viz_type1.py
         - viz_type2.py
         - ...
     - viz_scripts
         - viz_type1.py
         - viz_type2.py
         - ...
     - callbacks
         - viz_type1.py
         - viz_type2.py
         - ...
```

This is optional, but what is necessary for IDEA to find your profile and seamlessly add it to the platform is the
custom_model folder and the custom_model.py file.
The folder and the file can have any name but inside the file you must define a class that is a subclass of BaseProfile

## Steps to Add a Custom Model Profile

1. **Create a New Folder:**

   Start by creating a new folder inside the project's `profiles` directory to hold your custom model profile. Use a
   descriptive name for the folder, which will be your profile's name. For example, let's call it `custom_model`.


2. **Define the Profile Class:**

   Inside your new folder, create a Python class in a file named custom_model.py that defines your custom model profile.
   This class should inherit from the BaseProfile class and include the necessary imports. Here's an example:

    ```python

   from profiles.base_profile.base_profile import BaseProfile
   from dash import html
   
   from profiles.custom_model.processing_scripts import viz_type1 as processing_viz1,
                                                        viz_type2 as processing_viz2,
                                                        viz_type3 as processing_viz3,
                                                        ... 
   
   from profiles.custom_model.viz_scripts import viz_type1 as viz1,
                                               viz_type2 as viz2,
                                               viz_type3 as viz3,
                                               ... 
   
   from profiles.custom_model.callbacks import viz_type1 as viz1_callback,
                                               viz_type2 as viz2_callback,
                                               viz_type3 as viz3_callback,
                                               ... 
   
   
   
   class CustomModel(BaseProfile):
        name = 'Custom Model Profile'
        db_name = 'custom'
        description = 'This is a custom model profile' # Add a description for your profile, is shown on highlight in IDEA
        settings = html.Div(
           [
               dmc.Text('Implement Settings for your profile'),
           ]
        )
   
        plot_order = ['Viz1', 'Viz2', 'Viz3', ...]
   
        viz_options = {
         'Viz1':
            {
                'check': processing_viz1.check_folder,
                'process': processing_viz1.process,
                'viz': viz1.plot,
                'callback': viz1.link
   
            },
         'Viz2':
            {
                'check': processing_viz2.check_folder,
                'process': processing_viz2.process,
                'viz': viz2.plot,
                'callback': viz2_callback.link
            },
        'Viz3':
            {
                'check': processing_viz3.check_folder,
                'process': processing_viz3.process,
                'viz': viz3.plot,
                'callback': viz3_callback.link
            },
            ...
        }
        def __init__(self):
            super().__init__()
            self.settings = self.render_settings()
    
        def link(self, app):
            settings_callbacks.link(app)
            super().link(app)
    
        def render_settings(self):
            """
                Define layout of settings for this profile (simply and copy and paste from other profiles if no custom settings needed)
            """
    
            return layout
    
        
    
        
    ```
    
   Replace `Custom Model Profile` with your specific profile name and add `viz_options`.
   In addition to visualizations, you can also implement settings which can be accessed through IDEA.


3. **Processing Scripts:**

   Inside the `processing_scripts` folder, create Python files for each visualization type that you want to support, e.g.,
   viz_type1.py, viz_type2.py, and so on. In each of these files, define the check, processing and check_db and
   processing_db functions specific to that visualization type and include necessary imports. For example:

   
   ```python
   import pandas as pd
   from typing import Dict
   
   
   def check(df: pd.DataFrame) -> bool:
       # Implement your custom check logic here to check if visualization is possible with data found at path (a path to a folder)
       return True  # Modify based on your requirements
   
   
   def process(scenario_paths: Dict) -> pd.DataFrame:
       # Implement your custom processing logic here, scenario_paths is a dictionary with scenario names as keys and the db as a pd.DataFrame as values
       return custom_dataframe  # Replace with your actual data processing code
   ```
   
   Repeat this for each visualization type.


4. **Visualization Scripts:**

   Inside the viz_scripts folder, create Python files for each visualization type, e.g., viz_type1.py, viz_type2.py, and so
   on. In each of these files, define the plot function specific to that visualization type and include necessary imports.
   For example:
   
   ```python
   import pandas as pd
   from typing import Tuple
   from dash import dcc, html
   
   def plot(data_frame: pd.DataFrame, window_id: int) -> Tuple[html.Div, dcc.Graph]:
      # Implement your custom visualization logic here
      # Returns an html.Div object that contains the widgets and a dcc.Graph object that contains the plot
      # To allow callbacks to link correctly with the visualization, the dcc.Graph object should have 
      widgets = html.Div('Custom Widgets')
      dcc.Graph(
         id={
            'type': 'figure',
            'index': window_id,
            'profile': 'copper_output',
            'viz': 'cost_fom'
        },   
        style={
            'width': '100%',
            'height': '100%'
        }
      )
      return widgets, plot
   ```
   Repeat this for each visualization type.

---
By following these steps and adhering to the recommended folder structure, you can successfully add a custom model
profile to the project, enabling you to work with your specific data sources and requirements seamlessly.

5. **Callback Scripts:**

   Inside the `callbacks` folder, create Python files for each visualization type that you want to support, e.g.,
   viz_type1.py, viz_type2.py, and so on. In each of these files, define the callback functions specific to that visualization type and its widgets and include necessary imports. For example:

   
   ```python
   import pandas as pd
   from typing import Dict
   from dash import Output, Input
   
   
   def link(app):
      @app.callback(
         Output('figure', 'figure'),
         Input('widget', 'value')
      )
      def update_figure(value):
         # Implement your custom callback logic here
         return figure

   ```
   
   Repeat this for each visualization type.