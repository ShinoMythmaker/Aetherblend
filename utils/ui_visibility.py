from ..preferences import get_preferences


def visible_in_current_area(context):
    prefs = get_preferences()
    area = context.area
    if area is None:
        return True
    if area.type == 'VIEW_3D':
        return prefs.show_n_panel == 'ON'
    if area.type == 'PROPERTIES':
        return prefs.show_properties_tool_tab == 'ON'
    return True
