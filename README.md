# IDEA (Integrated Dashboard for Energy Transition Analysis)

## Overview

IDEA (Integrated Dashboard for Energy Transition Analysis) is a powerful tool designed to revolutionize the way we
interact with, visualize, and interpret energy transition data. In an era where data and modeling results play a pivotal
role in shaping the future of our energy systems, IDEA provides the key to making this information accessible, usable,
and understandable for stakeholders and the general public.

For those interested in the previous version of IDEA, please refer to the [IDEA Panel repository](https://gitlab.com/sesit/idea).
This updated version is based on Dash, a Python web application framework that enables the creation of interactive,
web-based data visualizations. IDEA leverages Dash's capabilities to provide a user-friendly interface for exploring
energy transition data, models, and scenarios. With Dash we were able to create a more seamless and modern user experience.
Specifically, we added resizable and draggable windows, so users can create their own custom dashboards. Additionally, we allow users to hide the UI from the windows, so they can have a clean view of the plots for presentations.

But, due to technical limitations we had to remove compatibility with non-PYAM formatted data.
If you are using non-PYAM formatted data, please refer to the [IDEA Panel repository](https://gitlab.com/sesit/idea) or use one of our provided converters to convert your data to PYAM format (e.g. [COPPER Converter](https://gitlab.com/sesit/copper-pyam)).

If you are interested in seeing your model results in IDEA, please refer to the [Extending IDEA](#extending-idea) section for instructions on how to add a new model profile or contact us for a possible collaboration.

## About IDEA

In today's complex landscape of energy transition, data and models are essential components for informed
decision-making. IDEA recognizes the importance of having open-source, flexible, and adaptable solutions that can
effectively interface with various models and databases hosted on the M3 Modeling platform. This integration is pivotal
for creating a comprehensive understanding of energy transition processes and facilitating effective collaboration among
diverse stakeholders.

IDEA is more than just a program; it's a catalyst for change, an open door to the world of energy transition analysis,
and a collaborative platform that brings stakeholders and the general public together to shape a sustainable future.


## Setup and Installation

Follow these steps to set up and run IDEA on your local system.

### Prerequisites

1. [Anaconda](https://docs.anaconda.com/anaconda/install/): Anaconda is a popular Python/R package manager. You'll need it to create a virtual environment for running IDEA.

If you haven't installed Anaconda yet, please follow this [installation guide](https://docs.anaconda.com/anaconda/install/). Once you are done, proceed with the following installation steps for IDEA.

### Step by Step Installation

**Note:** All the commands below should be run in a terminal where the `conda` command is accessible. If you installed Anaconda and haven't added it to the PATH environment variable during installation, you might need to use the Anaconda prompt terminal.

1. **Clone the repository**: First, you need to download the IDEA codebase onto your machine using Git. Use the following command to clone the repository:
```bash
   git clone https://gitlab.com/sesit/idea-dash.git
   ```
2. **Navigate to the project directory**: Once you've cloned the repository, navigate to it using this command:
   ```bash
   cd idea-dash
   ```
3. **Create the Conda environment**: We've included a file named `environment.yml` in the IDEA directory where you just navigated. This file lists all the Python packages required to run IDEA. Use this command to create a new Conda environment named `idea-dash`, which has all these required packages:
```bash
   conda env create -f environment.yml
   ```
4. **Activate the Conda environment**: Now, activate the conda environment using this command:
   ```bash
   conda activate idea-dash
   ```
5. **Run IDEA application**: Finally, start the IDEA application with this command:
   ```bash
   python main.py
   ```
After following these steps, IDEA should now be running on your local system. Open the displayed local URL in your web browser to interact with the IDEA dashboard.

Enjoy exploring and analyzing data with IDEA! Please refer to the User Guide (if available) for more details on how to use IDEA.

## Extending IDEA

### How to add a New Model Profile

This guide outlines the steps to add a custom model profile to our project. A model profile is used to define the
processing and visualization functions for specific data sets. If you have your own data source or custom requirements,
you can create a custom model profile to integrate it seamlessly.

#### Folder Structure

To keep your project organized, we recommend following this folder structure for adding your custom model profile:

```
- profiles
   - custom_model
       - custom_model.py
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

#### Steps to Add a Custom Model Profile

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



## Feedback 

We appreciate user feedback! If you have any suggestions for improvements or new features, please share them with us.