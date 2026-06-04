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
        white_list=["Skirt_Front.R", "Skirt_Front.R.001", "Skirt_Front.R.002", "Skirt_Side.R", "Skirt_Side.R.001", "Skirt_Side.R.002", "Skirt_Back.R", "Skirt_Back.R.001", "Skirt_Back.R.002",
                    "Skirt_Front.L", "Skirt_Front.L.001", "Skirt_Front.L.002", "Skirt_Side.L", "Skirt_Side.L.001", "Skirt_Side.L.002", "Skirt_Back.L", "Skirt_Back.L.001", "Skirt_Back.L.002",
                    "foot_ik.R", "foot_ik.L"],
        ui_type="slider",      
    )
}




