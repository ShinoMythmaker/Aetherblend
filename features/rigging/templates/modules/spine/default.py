from ......core.bone_generators import ConnectBone, ExtensionBone
from ......core.operations import ParentBoneOperation, ConstraintOperation, RigifyTypeOperation, CollectionOperation
from ......core.shared import PoseOperations, BoneGroup, TransformLink, RigModule
from ......core import rigify
from ......core.rigify.settings import UI_Collections, BoneCollection

SPINE = BoneGroup(
        name="spine",
        transform_link= [
            TransformLink(target="DEF-Spine.001", bone="j_kosi", retarget="FK-Spine.001"),
            TransformLink(target="MCH-pivot", bone="n_hara", retarget="Torso"),
            TransformLink(target="DEF-Spine.002", bone="j_sebo_a", retarget="FK-Spine.002"),
            TransformLink(target="DEF-Spine.003", bone="j_sebo_b", retarget="FK-Spine.003"),
            TransformLink(target="DEF-Spine.004", bone="j_sebo_c", retarget="FK-Spine.004"),
            TransformLink(target="DEF-Chest.R", bone="j_mune_r"),
            TransformLink(target="DEF-Chest.L", bone="j_mune_l"),
        ],
        generators = [
            #Spine
            ConnectBone(
                name="Spine.001",
                bone_a="j_kosi",
                bone_b="j_kosi",
                start="tail",
                end="head",
                parent="root",
                is_connected=False,
                req_bones=["j_kosi"],
                operations=[
                            RigifyTypeOperation(time="Pre", bone_name="Spine.001", rigify_type=rigify.types.spines_basic_spine(fk_coll="Torso (Tweak)", tweak_coll="Torso (Tweak)", pivot_pos=1)),
                            CollectionOperation(time="Pre", bone_name="Spine.001", collection_name="Torso"),
                            ]
            ),
            ConnectBone(
                name="Spine.002",
                bone_a="j_sebo_a",
                bone_b="j_sebo_b",
                parent="Spine.001",
                is_connected=True,
                req_bones=["j_sebo_a", "j_sebo_b"],
                operations=[
                            CollectionOperation(time="Pre", bone_name="Spine.002", collection_name="Torso"),
                            ]
            ),
            ConnectBone(
                name="Spine.003",
                bone_a="j_sebo_b",
                bone_b="j_sebo_c",
                parent="Spine.002",
                is_connected=True,
                req_bones=["j_sebo_b", "j_sebo_c"],
                operations=[
                            CollectionOperation(time="Pre", bone_name="Spine.003", collection_name="Torso"),
                            ]
            ),
            ConnectBone(
                name="Spine.004",
                bone_a="j_sebo_c",
                bone_b="j_kubi",
                parent="Spine.003",
                is_connected=True,
                req_bones=["j_sebo_c", "j_kubi"],
                operations=[
                            CollectionOperation(time="Pre", bone_name="Spine.004", collection_name="Torso"),
                            ]
            ),
            #Chest
            ExtensionBone(
                name="Chest.R",
                bone_a="j_mune_r",
                start="head",
                axis_type="local",
                axis="Y",
                roll=-48,
                parent="Spine.003",
                req_bones=["j_mune_r"],
                operations=[
                            RigifyTypeOperation(time="Pre", bone_name="Chest.R", rigify_type=rigify.types.basic_super_copy(widget_type="bone")),
                            CollectionOperation(time="Pre", bone_name="Chest.R", collection_name="Torso"),
                            ]
            ),
            ExtensionBone(
                name="Chest.L",
                bone_a="j_mune_l",
                start="head",
                axis_type="local",
                axis="Y",
                roll=-132,
                parent="Spine.003",
                req_bones=["j_mune_l"],
                operations=[
                            RigifyTypeOperation(time="Pre", bone_name="Chest.L", rigify_type=rigify.types.basic_super_copy(widget_type="bone")),
                            CollectionOperation(time="Pre", bone_name="Chest.L", collection_name="Torso"),
                            ]
            ),
        ],
)

def get_rig_module() -> RigModule:
    return RigModule(
        name="Default",
        type="Generation",
        bone_groups=[SPINE],
        ui = UI_Collections([
            BoneCollection(name="Torso", ui=True, color_set="Torso", row_index=1, title="Torso"),
            BoneCollection(name="Torso (Tweak)", ui=True, color_set="Torso_Tweak", row_index=2, title="Tweak", visible=False),
        ])
    )
    