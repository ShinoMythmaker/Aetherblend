from ...core.shared import UILink

# ---------------------------------------------------------------------------
# Registry: flag_key -> UILink
# ---------------------------------------------------------------------------
UI_LINKS: dict[str, UILink] = {
    # Add UILink definitions here.
    # "my.flag_key": UILink(
    #     property_name="...",
    #     title="...",
    #     bone_name="...",          # optional
    #     constraint_name="...",    # optional
    #     white_list=["..."],       # optional – filter by selected bone
    #     ui_type="checkbox",       # "checkbox" | "slider" | "dropdown"
    # ),
    
    "Skirt Automation": UILink(
        property_name="skirt_automation",
        title="Skirt Automation",
        white_list=["Skirt_Front.R", "Skirt_Back.R", "Skirt_Front.L", "Skirt_Back.L"],
        ui_type="slider",      
    ),
}
