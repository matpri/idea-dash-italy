from os.path import dirname, basename, isfile, join, isdir
import glob

current_directory = dirname(__file__)

# find all folders in this directory
folders = glob.glob(join(current_directory, "*"))

modules = []

for folder in folders:
    if isdir(folder):
        python_files = glob.glob(join(folder, "*.py"))
        for f in python_files:
            if isfile(f) and not f.endswith('__init__.py'):
                modules.append(f"{basename(current_directory)}.{basename(folder)}.{basename(f)[:-3]}")

__all__ = modules

# Import all the modules in this directory
# for module in __all__:
#     __import__(module, locals(), globals())
