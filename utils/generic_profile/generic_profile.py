from utils.generic_profile.visualization_scripts.generic_viz import create_generic_plots
from utils.generic_profile.processing_scripts import generic_processing
from utils.generic_profile.callbacks import generic_callback

class GenericProfile:
    def __init__(self, name, classes):
        self.name = name

        self.color = '#000000'
        self.description = 'Generic Profile'

        self.plot_order = classes
        self.plot_order.sort()

        self.viz_options = {}

        for class_name in classes:
            self.viz_options[class_name] = {
                'check': generic_processing.create_check(class_name, name),
                'db_check': generic_processing.create_check(class_name, name),
                'process': generic_processing.create_process(name),
                'db_process': generic_processing.create_process(name),
                'viz': create_generic_plots(name, class_name),
                'callback': generic_callback.create_link(name, class_name)
            }

