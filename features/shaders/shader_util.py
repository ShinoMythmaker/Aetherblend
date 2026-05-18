from pathlib import Path

import bpy

_ASSET_DIR = Path(__file__).resolve().parents[2] / "assets" / "blend"
_NODE_GROUPS_BLEND = _ASSET_DIR / "node_groups.blend"

def append_node_group(group_name):
    if not _NODE_GROUPS_BLEND.exists():
        raise FileNotFoundError(f"Node group asset not found: {_NODE_GROUPS_BLEND}")

    with bpy.data.libraries.load(str(_NODE_GROUPS_BLEND)) as (data_from, data_to):
        if group_name in data_from.node_groups:
            data_to.node_groups.append(group_name)
        else:
            raise ValueError(f"Node group '{group_name}' not found in {_NODE_GROUPS_BLEND}")
    return bpy.data.node_groups[group_name]

def add_node_group_to_node_tree(material, node_group):
    if not material.node_tree:
        raise ValueError(f"Material '{material.name}' does not have a node tree.")

    node_tree = material.node_tree
    group_node = node_tree.nodes.new('ShaderNodeGroup')
    group_node.node_tree = node_group
    return group_node
    

def find_material_by_property(
    meshes: list[bpy.types.Object],
    property_name: str,
    property_value=None,
) -> list[bpy.types.Material]:
    """Finds materials used by meshes driven by the armature that have a custom property matching the filter criteria."""
    materials = set()
    for mesh in meshes:
        if not mesh.data or not hasattr(mesh.data, 'materials'):
            continue

        for material_slot in mesh.material_slots:
            material = material_slot.material
            if not material or property_name not in material:
                continue

            if property_value is None or material[property_name] == property_value:
                materials.add(material)

    return list(materials)
