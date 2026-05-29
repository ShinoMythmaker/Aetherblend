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
        TransformLink(target="DEF-Iris.L", bone="j_f_irisprm_l", retarget="DEF", constraint=CopyScaleConstraint(target_bone="Iris.L", axis=(True, True, True), target_space="LOCAL", owner_space="LOCAL")),
        TransformLink(target="DEF-Iris.R", bone="j_f_irisprm_r", retarget="DEF", constraint=CopyScaleConstraint(target_bone="Iris.R", axis=(True, True, True), target_space="LOCAL", owner_space="LOCAL")),
    ],
    generators=[
        ExtensionBone(
            name="Iris.L",
            bone_a="Eye.L",
            axis="Y",
            axis_type="local",
            start="tail",
            parent="Eye.L",
            req_bones=["Eye.L"],
            operations=[
               RigifyTypeOperation(bone_name="Iris.L", rigify_type=rigify.types.basic_super_copy(widget_type="circle")),
               CollectionOperation(bone_name="Iris.L", collection_name="Face (Primary)"),
               DriverOperation(
                   driver_name="Iris.L Scale X",
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
                   driver_name="Iris.L Scale Y",
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
               DriverOperation(
                   driver_name="Iris.L Scale Z",
                   data="iris",
                   property='["Pupil Scale"]',
                   driver=Driver(
                       type="SCRIPTED",
                       expression="iris_z-1",
                       variables=[
                           TransformChannelVariable(name="iris_z", target_bone="j_f_irisprm_l", transform_type="SCALE_Y", transform_space="LOCAL_SPACE"),
                           #Don't mind that it's taking the Y scale, it works
                       ]
                   ),
                   time="Post",
               )
            ]
        ),
        ExtensionBone(
            name="Iris.R",
            bone_a="Eye.R",
            axis="Y",
            axis_type="local",
            start="tail",
            parent="Eye.R",
            req_bones=["Eye.R"],
            operations=[
               RigifyTypeOperation(bone_name="Iris.R", rigify_type=rigify.types.basic_super_copy(widget_type="circle")),
               CollectionOperation(bone_name="Iris.R", collection_name="Face (Primary)"),
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