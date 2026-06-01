from ......core.rigify.settings import UI_Collections, BoneCollection
from ......core.operations import CollectionOperation, ParentBoneOperation, RigifyTypeOperation, DriverOperation
from ......core.generators import ConnectBone, ExtensionBone, CenterBone, CopyBone, SkinBone, BridgeBone
from ......core.shared import PoseOperations, BoneGroup, TransformLink, RigModule
from ......core.drivers import Driver, SinglePropertyVariable, TransformChannelVariable
from ......core import rigify
from ......core.constraints import CopyScaleConstraint

IRIS_CONTROLS = BoneGroup(
    name="Iris Controls",
    transform_link = [
        TransformLink(target="DEF-Iris", bone="j_f_irisprm_l", retarget="DEF", constraint=CopyScaleConstraint(target_bone="Iris", axis=(True, False, True), target_space="LOCAL", owner_space="LOCAL")),
        TransformLink(target="DEF-Pupil", bone="j_f_irisprm_l", retarget="DEF", constraint=CopyScaleConstraint(target_bone="Pupil", axis=(False, True, False), target_space="LOCAL", owner_space="LOCAL")),
        TransformLink(target="DEF-Iris", bone="j_f_irisprm_r", retarget="DEF", constraint=CopyScaleConstraint(target_bone="Iris", axis=(True, False, True), target_space="LOCAL", owner_space="LOCAL")),
        TransformLink(target="DEF-Pupil", bone="j_f_irisprm_r", retarget="DEF", constraint=CopyScaleConstraint(target_bone="Pupil", axis=(False, True, False), target_space="LOCAL", owner_space="LOCAL")),
    ],
    generators=[
        ExtensionBone(
            name="Iris",
            bone_a="Eye.L",
            axis="Y",
            axis_type="local",
            start="tail",
            parent="Eye.L",
            req_bones=["Eye.L"],
            operations=[
               RigifyTypeOperation(bone_name="Iris", rigify_type=rigify.types.basic_super_copy(widget_type="circle")),
               CollectionOperation(bone_name="Iris", collection_name="Face (Primary)"),
               DriverOperation(
                   driver_name="Iris Scale X",
                   data="iris",
                   property='["Eye Scale X"]',
                   driver=Driver(
                       type="SCRIPTED",
                       expression="1/iris_x",
                       variables=[
                           TransformChannelVariable(name="iris_x", target_bone="j_f_irisprm_l", transform_type="SCALE_X", transform_space="LOCAL_SPACE"),
                       ]
                   ),
                   time="Post",
               ),
               DriverOperation(
                   driver_name="Iris Scale Y",
                   data="iris",
                   property='["Eye Scale Y"]',
                   driver=Driver(
                       type="SCRIPTED",
                       expression="1/iris_y",
                       variables=[
                           TransformChannelVariable(name="iris_y", target_bone="j_f_irisprm_l", transform_type="SCALE_Z", transform_space="LOCAL_SPACE"),
                           #Don't mind that it's taking the Z scale, it works
                       ]
                   ),
                   time="Post",
               ),
            ]
        ),
        ExtensionBone(
            name="Pupil",
            bone_a="Eye.L",
            axis="Y",
            axis_type="local",
            start="tail",
            size_factor=0.5,
            parent="Eye.L",
            req_bones=["Eye.L"],
            operations=[
               RigifyTypeOperation(bone_name="Pupil", rigify_type=rigify.types.basic_super_copy(widget_type="circle")),
               CollectionOperation(bone_name="Pupil", collection_name="Face (Primary)"),
               DriverOperation(
                   driver_name="Iris Scale Z",
                   data="iris",
                   property='["Pupil Scale"]',
                   driver=Driver(
                       type="SCRIPTED",
                       expression="iris_z-1",
                       variables=[
                           TransformChannelVariable(name="iris_z", target_bone="j_f_irisprm_l", transform_type="SCALE_Y", transform_space="LOCAL_SPACE"),
                           #Don't mind that it's taking the Y scale, it works
                           #Admittedly this could be hella confusing on the user end if you haven't seen the code but I'll just write it in the wiki and call people stupid if they haven't read that -Oats
                       ]
                   ),
                   time="Post",
               ),
            ]
        ),
    ]
)
def get_rig_module() -> RigModule:
    return RigModule(
        name="Iris",
        type="Patch",
        bone_groups=[IRIS_CONTROLS],
        ui_collections = UI_Collections([
            BoneCollection(name="Face (Primary)", ui=True, color_set="Face_Primary", row_index=0, title="Face (Primary)", visible=True)
        ])
    )