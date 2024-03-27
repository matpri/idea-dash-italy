# IDEA - Interactive Dashboard for Energy Assessment 

## Overview

IDEA is a **user-friendly, intuitive visualization platform** designed for the efficient visualization of Energy Modelling results. Built with Python's Dash framework, IDEA enables users to explore and analyze data in a more interactive and convenient manner.

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

## Feedback 

We appreciate user feedback! If you have any suggestions for improvements or new features, please share them with us.