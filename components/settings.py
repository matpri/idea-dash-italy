import dash_mantine_components as dmc
from dash import html


def render():
    """
    Render the settings modal.

    :return: The rendered settings modal.
    """
    from main import data_handler
    tab_contents = []
    tabs = []
    for profile_name, profile in data_handler.profiles.items():
        tabs.append(
            dmc.Tab(
                value=profile_name,
                children=profile_name
            )
        )

        tab_contents.append(
            dmc.TabsPanel(
                value=profile_name,
                children=profile.settings
            )
        )

    return dmc.Modal(
        title='Settings',
        opened=False,
        id='settings-modal',
        size='70%',
        children=html.Div(
            [
                dmc.Tabs(
                    [
                        dmc.TabsList(children=tabs),
                        *tab_contents,
                    ],
                ),
            ]
        )
    )
