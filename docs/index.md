# IDEA (Integrated Dashboard for Energy Transition Analysis)

## About IDEA

In today's complex landscape of energy transition, data and models are essential components for informed
decision-making. IDEA recognizes the importance of having open-source, flexible, and adaptable solutions that can
effectively interface with various models and databases hosted on the M3 Modeling platform. This integration is pivotal
for creating a comprehensive understanding of energy transition processes and facilitating effective collaboration among
diverse stakeholders.

IDEA is more than just a program; it's a catalyst for change, an open door to the world of energy transition analysis,
and a collaborative platform that brings stakeholders and the general public together to shape a sustainable future.

## Overview

IDEA (Integrated Dashboard for Energy Transition Analysis) is a powerful tool designed to revolutionize the way we
interact with, visualize, and interpret energy transition data. In an era where data and modeling results play a pivotal
role in shaping the future of our energy systems, IDEA provides the key to making this information accessible, usable,
and understandable for stakeholders and the general public.

For those interested in the previous version of IDEA, please refer to the [IDEA Panel repository](https://gitlab.com/sesit/idea).
This updated version is based on Dash, a Python web application framework that enables the creation of interactive,
web-based data visualizations. IDEA leverages Dash's capabilities to provide a user-friendly interface for exploring
energy transition data, models, and scenarios. 

The platform is tile-based, allowing users to add multiple tiles/windows to the page that they can manipulate to create a custom dashboard. Each tile features two layers of tabs at the top, enabling users to swap between models and plots within a model. All plots are interactable and can be updated using widgets to switch between representations, time periods, or regions. Users can also dynamically hide the widgets and tabs to display only the plots within the windows, so they can have a clean view of the plots for presentations. Additionally, editing features are available, allowing users to modify scenario names, technologies, and set colors and aggregation groups for technologies.

If you are interested in seeing your model results in IDEA, please refer to the [Extending IDEA](extending-idea.md) section for instructions on how to add a new model profile or contact us for a possible collaboration.

At the moment, we have custom plots for our COPPER, SILVER, MESSAGE, LabourABM, and CIMS models and any results following the [IAMC format](iamc-format.md) can be visualized with generic plots. Additionally, we have plots showcasing some of the data accessible through the CODERS database, commonly used for our energy models.

## Sections
- [Setup and Installation](setup-and-installation.md)
- [Extending IDEA](extending-idea.md)
- [IAMC Format](iamc-format.md)
- [User Guide](user-guide.md)
