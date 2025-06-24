
def safe_hide_set(context, obj, hide):
    """Safely hides objects"""
    if obj and obj.name in context.view_layer.objects:
        obj.hide_set(hide)
            
def normalize_edit_mode(mode_str):
    """Normalizes edit mode strings to a standard format."""
    if mode_str[:4] == "EDIT":
        return "EDIT"
    return mode_str

