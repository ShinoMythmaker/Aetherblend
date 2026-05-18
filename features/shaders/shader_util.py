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
    group_node.label = node_group.name
    group_node.name = node_group.name
    return group_node

def get_value_from_material_property(material, property_name, default=None):
    if property_name in material:
        return material[property_name]
    return default


def apply_material_property_to_socket(input_socket, material_prop):
    """Apply a material custom property to a node input socket default value."""
    if material_prop is None:
        return

    default_value = getattr(input_socket, "default_value", None)
    if default_value is None:
        return

    try:
        source_values = list(material_prop)
    except TypeError:
        source_values = [material_prop]

    if not source_values:
        return

    if isinstance(default_value, (float, int, bool)):
        input_socket.default_value = source_values[0]
        return

    try:
        target_len = len(default_value)
    except TypeError:
        input_socket.default_value = source_values[0]
        return

    for idx in range(min(target_len, len(source_values))):
        input_socket.default_value[idx] = source_values[idx]
    

def get_socket_by_name(node_tree, node_label, socket_name):
    for node in node_tree.nodes:
        if node.label == node_label:
            for socket in node.inputs:
                if socket.name == socket_name:
                    return socket
    return None


def refresh_shader_dependency_state(context, objects, material):
    """Force evaluation so object-property-driven shader nodes update immediately."""
    for obj in objects:
        if obj is None:
            continue
        try:
            obj.update_tag()
        except Exception:
            pass

        obj_data = getattr(obj, "data", None)
        if obj_data is not None:
            try:
                obj_data.update_tag()
            except Exception:
                pass

    node_tree = getattr(material, "node_tree", None)
    if node_tree is not None:
        try:
            node_tree.update_tag()
        except Exception:
            pass

    try:
        material.update_tag()
    except Exception:
        pass

    # Force depsgraph evaluation now instead of waiting for user interaction.
    scene = context.scene
    scene.frame_set(scene.frame_current)
    context.view_layer.update()


def find_material_by_property(
    meshes: list[bpy.types.Object],
    property_name: str,
    property_value=None,
) -> list[tuple[bpy.types.Object, bpy.types.Material]]:
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
                materials.add((mesh, material))

    return list(materials)
