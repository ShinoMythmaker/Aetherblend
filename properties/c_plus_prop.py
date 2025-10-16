import bpy

class AETHER_PROP_CustomizePlus(bpy.types.PropertyGroup):
    code: bpy.props.StringProperty(
        name="C+ String",
        description="Paste your Customize+ string here"
    )  # type: ignore
    applied: bpy.props.BoolProperty(
        name="C+ Applied",
        description="Tracks if C+ is currently applied to this armature",
        default=False
    ) # type: ignore


def register():
    bpy.utils.register_class(AETHER_PROP_CustomizePlus)
    bpy.types.Object.aether_cplus = bpy.props.PointerProperty(type=AETHER_PROP_CustomizePlus)

def unregister():
    if hasattr(bpy.types.Object, 'aether_cplus'):
        del bpy.types.Object.aether_cplus
    bpy.utils.unregister_class(AETHER_PROP_CustomizePlus)