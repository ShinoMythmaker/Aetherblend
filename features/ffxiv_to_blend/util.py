import bpy

ASSET_DIR = "assets/blend/"

def append_node_group(group_name):
    with bpy.data.libraries.load(ASSET_DIR + "node_groups.blend") as (data_from, data_to):
        if group_name in data_from.node_groups:
            data_to.node_groups.append(group_name)
        else:
            raise ValueError(f"Node group '{group_name}' not found in {ASSET_DIR}node_groups.blend")
    return bpy.data.node_groups[group_name]