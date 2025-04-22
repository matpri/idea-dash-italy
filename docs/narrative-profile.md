# Narrative Profile Configuration Guide

## Overview

The Narrative Profile feature allows users to create custom dashboard tabs with markdown reports and associated data visualizations. This is configured using a TOML file in the repository's config path.

## Configuration Structure

Create a `.yaml` file with the following structure:

```yaml
name: "Profile Name" # The name displayed on the dashboard tab
report: "path/to/markdown/report.md"

descriptions:
  # Optional descriptions for specific profiles and visualizations
  ProfileName:
    VisualizationName: "Description text for this visualization."
    AnotherVisualization: "Another description text."

files:
# Data files and their associated profiles/tabs
    "path/to/datafile.csv":
      profiles:
        # Profiles that should appear
        ProfileName:
          # Visualizations to show (can be "All" for all visualizations)
          - "Visualization1"
          - "Visualization2"
        AnotherProfile:
          - "All" # This will include all visualizations in this profile
```

## Key Components

- **name**: Sets the name of the narrative profile
- **report**: Path to the markdown file that contains the report content
- **descriptions**: Optional section that maps profiles to visualizations with custom descriptions
- **files**: Data files to be included and the associated profiles and tabs where they should appear

## How It Works

1. The dashboard will create a new tab with the name specified in the `name` field
2. The markdown content from the `report` path will be loaded into this tab
3. Only visualizations for profiles and tabs specified in the config will be shown
4. Custom descriptions can be added to visualizations through the `descriptions` section

## Usage Notes

- Use absolute file paths to ensure reliable loading
- You can include multiple data files and associate them with different profiles
- For each profile, specify the tabs that should appear (use "All" to include in all tabs)
- The descriptions are optional but helpful for adding context to visualizations
