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
energy transition data, models, and scenarios. With Dash we were able to create a more seamless and modern user experience.
Specifically, we added resizable and draggable windows, so users can create their own custom dashboards. Additionally, we allow users to hide the UI from the windows, so they can have a clean view of the plots for presentations.

But, due to technical limitations we had to remove compatibility with non-PYAM formatted data.
If you are using non-PYAM formatted data, please refer to the [IDEA Panel repository](https://gitlab.com/sesit/idea) or use one of our provided converters to convert your data to PYAM format (e.g. [COPPER Converter](https://gitlab.com/sesit/copper-pyam)).

If you are interested in seeing your model results in IDEA, please refer to the [Extending IDEA](extending-idea.md) section for instructions on how to add a new model profile or contact us for a possible collaboration.


## Sections
- [Setup and Installation](setup-and-installation.md)
- [Extending IDEA](extending-idea.md)
