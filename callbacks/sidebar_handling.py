import dash
from dash import Output, Input, State, html
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from assets.styles import view_button_style, hide_button_style
from components import ids
from components.plot_window import window, tabs


def link(app):
    """
    :param app: The Dash app object.
    :return: None.

    Registers the callbacks for the given Dash app object to handle events from various input components and update the corresponding output components.

    Callbacks:
    - `link(app)` registers the callback for editing cards.
        - Inputs:
            - `add-card`: number of clicks on the "Add Card" button.
            - `delete-card`: number of clicks on the "Delete Card" button.
            - `trash-button`: number of clicks on the "Trash" button.
            - `cancel-delete-card`: number of clicks on the "Cancel" button for deleting a card.
            - `data-change`: number of clicks on the "Data Change" button.
            - `settings-change`: number of clicks on the "Settings Change" button.
            - `after-change`: number of clicks on the "After Change" button.
            - `plot-canvas`: children of the plot canvas component.
            - `window-clear`: state of the window-clear component.
        - Outputs:
            - `plot-canvas`: children of the plot canvas component.
            - `window-clear`: state of the window-clear component.

    - `show_settings_modal(n_clicks, opened, children)` registers the callback for showing the settings modal.
        - Inputs:
            - `settings`: number of clicks on the "Settings" button.
            - `settings-modal`: state of the settings modal component.
            - `settings-modal`: children of the settings modal component.
        - Outputs:
            - `settings-modal`: opened state of the settings modal component.
            - `settings-modal`: children of the settings modal component.

    - `update_windows(opened, n_clicks)` registers the callback for updating the settings change.
        - Inputs:
            - `settings-modal`: opened state of the settings modal component.
            - `settings-change`: number of clicks on the settings-change button.
        - Outputs:
            - `settings-change`: number of clicks on the settings-change button.

    """
    app.callback(
        Output(ids.PLOT_CANVAS, 'children'),
        Output('window-clear', 'is_open'),
        Input('add-card', 'n_clicks'),
        Input('delete-card', 'n_clicks'),
        Input('trash-button', 'n_clicks'),
        Input('cancel-delete-card', 'n_clicks'),
        Input(ids.DATA_CHANGE, 'n_clicks'),
        Input(ids.SETTINGS_CHANGE, 'n_clicks'),
        Input(ids.AFTER_CHANGE, 'n_clicks'),
        State(ids.PLOT_CANVAS, 'children'),
        State('window-clear', 'is_open'),
        prevent_initial_call=True,
    )(edit_cards)

    app.callback(
        Output('settings-modal', 'opened'),
        Output('settings-modal', 'children'),
        Input('settings', 'n_clicks'),
        State('settings-modal', 'opened'),
        State('settings-modal', 'children'),
        prevent_initial_call=True,
    )(show_settings_modal)

    app.callback(
        Output(ids.SETTINGS_CHANGE, 'n_clicks'),
        Input('settings-modal', 'opened'),
        State(ids.SETTINGS_CHANGE, 'n_clicks'),
        prevent_initial_call=True,
    )(update_windows)

    # Callback to handle sidebar collapse/expand
    app.callback(
        Output('sidebar-collapse', 'is_open'),
        Output('collapse-sidebar-container', 'position', allow_duplicate=True),
        Input('collapse-sidebar', 'n_clicks'),
        Input('view-sidebar', 'n_clicks'),
        State('sidebar-collapse', 'is_open'),
        prevent_initial_call=True
    )(toggle_sidebar)

    app.callback(
        Output('collapse-sidebar', 'style'),
        Output('view-sidebar', 'style'),
        Output('collapse-sidebar-container', 'position', allow_duplicate=True),
        Input('sidebar-collapse', 'is_open'),
        prevent_initial_call=True
    )(toggle_button)



def update_windows(is_open, n_clicks):
    """
    Update the windows based on the values of `is_open` and `n_clicks`.

    :param is_open: A boolean indicating if the window is open.
    :param n_clicks: An integer indicating the number of clicks.

    :return:
        - If `is_open` is None, returns `dash.no_update`.
        - If `is_open` is False and `n_clicks` is None, returns 1.
        - If `is_open` is False and `n_clicks` is not None, returns `n_clicks + 1`.
        - Otherwise, returns `dash.no_update`.
    """
    if is_open is None:
        return dash.no_update
    if not is_open:
        if n_clicks is None:
            return 1
        return n_clicks + 1
    return dash.no_update


def edit_cards(add_clicks, delete_click, trash_click, cancel_click, d_change, s_change, a_change,
               widgets, is_open):
    """
    Edit the list of widgets based on the trigger.

    :param add_clicks: Number of times the add button was clicked.
    :param delete_click: Boolean indicating if the delete button was clicked.
    :param trash_click: Boolean indicating if the trash button was clicked.
    :param cancel_click: Boolean indicating if the cancel button was clicked.
    :param d_change: Boolean indicating if the data was changed.
    :param s_change: Boolean indicating if the settings were changed.
    :param a_change: Boolean indicating if the after change was triggered.
    :param widgets: List of widgets.
    :param is_open: Boolean indicating if the widget is open.
    :return: Updated list of widgets and the updated value of is_open.
    """
    ctx = dash.callback_context
    if not ctx.triggered:
        return widgets

    trigger = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger == 'add-card':
        widgets.append(window.render())
        return widgets, is_open
    if trigger == 'delete-card':
        ids.card_ids = []
        return [], False
    if trigger == 'trash-button':
        return widgets, True
    if trigger == 'cancel-delete-card':
        return widgets, False
    if trigger in [ids.DATA_CHANGE, ids.SETTINGS_CHANGE, ids.AFTER_CHANGE]:
        ids.card_ids = []
        updated_widgets = []
        for widget in widgets:
            updated_widgets.append(window.render())
        return updated_widgets, is_open


def show_settings_modal(n_clicks, is_open, _children):
    """
    Show settings modal.

    :param n_clicks: The number of times the modal is clicked.
    :param is_open: Boolean value indicating if the modal is open or closed.
    :param _children: The children elements of the modal.

    :return: A tuple containing the updated value of is_open and _children.

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

    _children = html.Div(
            [
                dmc.Tabs(
                    [
                        dmc.TabsList(children=tabs),
                        *tab_contents,
                    ],
                ),
            ]
        )
    if n_clicks:
        return not is_open, _children
    return is_open, _children



def toggle_sidebar(n_hide, n_view, is_open):
    print('toggle_sidebar')
    if is_open:
        return False, dash.no_update
    else:
        return True, {'top': '50%', 'left': '62px'}

def toggle_button(is_open):
    if is_open:
        return view_button_style, hide_button_style, dash.no_update
    else:
        return hide_button_style, view_button_style, {'top': '50%', 'left': '0px'}