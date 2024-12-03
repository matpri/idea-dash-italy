import os
import argparse  # Import argparse for CLI argument parsing

from utils.data_handler import DataHandler

# Set up argument parser
parser = argparse.ArgumentParser(description='Save files from data into IDEA pkl at this path.')
parser.add_argument('autosave', type=str, help='Path to save the datahandler to.')

args = parser.parse_args()  # Parse the arguments
autosave = args.autosave

# get all files in data folder that end either with csv or xlsx
data_files = [f for f in os.listdir('data') if f.endswith('.csv') or f.endswith('.xlsx')]
data_handler: DataHandler = DataHandler()
data_handler.preload_data(data_files)
print(f"Autosaving datahandler to {autosave}")
# Ensure the directory exists, but do not create a directory for a file path
autosave_dir = os.path.dirname(autosave)
if autosave_dir != '' and not os.path.exists(autosave_dir):
    os.makedirs(autosave_dir)
data_handler.save(autosave)  # Save the datahandler to the specified file path