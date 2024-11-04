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
After following these steps, IDEA should now be running on your local system. The program will automatically open the page in your default browser. If it is not showing up, open this page in your browser: http://localhost:8050/.
Enjoy exploring and analyzing data with IDEA!

### Repo Structure
- **assets**: files defining style and static content
  - **help**: definition of the pages in the help section
- **callbacks**: functions linking to the app to create functionality of IDEA
- **components**: visual components defining widgets and page layout (some include simple callbacks)
- **profiles**: custom logic defined for specific data (so called model profiles)
  - "profile name"
    - callbacks
    - processing_scripts
    - visualization_scripts
    - "profile name".py
    - plots.yaml
    - technologies.yaml
- **utils**
  - **generic_profile**: logic defining generic visualizations that are created when data does not fit any defined profiles but follow IAMC format
  - **data_handler**: logic for loading, checking and processing data in IDEA, calls functions from profiles
- **main.py**: instantiates app, links callbacks to app and creates starting page