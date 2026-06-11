from ......core.generators import ConnectBone, ExtensionBone
from ......core.operations import ParentBoneOperation, RigifyTypeOperation, CollectionOperation, WidgetOperation
from ......core.shared import PoseOperations, BoneGroup, RigModule, TransformLink
from ......core import rigify
from ......core.rigify.settings import UI_Collections, BoneCollection
from ......features.rigging.templates.colorsets.cs_aetherblend import CS_AETHER_BLEND

def _hex_to_srgb(hex_color: str) -> tuple:
    """Converts a hex color string to raw sRGB (0-1) without linear conversion.
    pose_bone.color.custom expects sRGB values, unlike rigify_colors which expects linear."""
    hex_color = hex_color.lstrip('#')
    lv = len(hex_color)
    return tuple(int(hex_color[i:i + lv // 3], 16) / 255.0 for i in range(0, lv, lv // 3))

_IVCS = CS_AETHER_BLEND["ivcs"]
_IVCS_NORMAL = _hex_to_srgb(_IVCS.normal)
_IVCS_SELECT = _hex_to_srgb(_IVCS.select)
_IVCS_ACTIVE = _hex_to_srgb(_IVCS.active)

def _ivcs_widget(bone_name: str, scale_factor: float = 0.5) -> WidgetOperation:
    return WidgetOperation(
        bone_name=bone_name,
        scale_factor=scale_factor,
        color_set="CUSTOM",
        custom_color_normal=_IVCS_NORMAL,
        custom_color_select=_IVCS_SELECT,
        custom_color_active=_IVCS_ACTIVE,
    )

GENITALS_M = BoneGroup(
    name="Male Genitals",
    transform_link=[
        TransformLink(target="DEF-Penis", bone="iv_ochinko_a"),
        TransformLink(target="DEF-Penis.001", bone="iv_ochinko_b"),
        TransformLink(target="DEF-Penis.002", bone="iv_ochinko_c"),
        TransformLink(target="DEF-Penis.003", bone="iv_ochinko_d"),
        TransformLink(target="DEF-Penis.004", bone="iv_ochinko_e"),
        TransformLink(target="DEF-Penis.005", bone="iv_ochinko_f"),
        TransformLink(target="DEF-Testicle.R", bone="iv_kougan_r"),
        TransformLink(target="DEF-Testicle.L", bone="iv_kougan_l")
    ],
    generators=[
        ConnectBone(
            name="Penis",
            bone_a="iv_ochinko_a",
            bone_b="iv_ochinko_b",
            parent=["Spine.001", "j_kosi"],
            is_connected=False,
            req_bones=["iv_ochinko_a", "iv_ochinko_b"],
            operations=[
                RigifyTypeOperation(time="Pre", bone_name="Penis", rigify_type=rigify.types.limbs_spline_tentacle(sik_stretch_control="MANUAL_STRETCH")),
                CollectionOperation(time="Pre", bone_name="Penis", collection_name="AB-Meta"),
            ]
        ),
        ConnectBone(
            name="Penis.001",
            bone_a="iv_ochinko_b",
            bone_b="iv_ochinko_c",
            parent="Penis",
            is_connected=True,
            req_bones=["iv_ochinko_b", "iv_ochinko_c"],
            operations=[
                CollectionOperation(bone_name="Penis.001", collection_name="AB-Meta"),
            ]
        ),
        ConnectBone(
            name="Penis.002",
            bone_a="iv_ochinko_c",
            bone_b="iv_ochinko_d",
            parent="Penis.001",
            is_connected=True,
            req_bones=["iv_ochinko_c", "iv_ochinko_d"],
            operations=[
                CollectionOperation(bone_name="Penis.002", collection_name="AB-Meta"),
            ],
        ),
        ConnectBone(
            name="Penis.003",
            bone_a="iv_ochinko_d",
            bone_b="iv_ochinko_e",
            parent="Penis.002",
            is_connected=True,
            req_bones=["iv_ochinko_d", "iv_ochinko_e"],
            operations=[
                CollectionOperation(bone_name="Penis.003", collection_name="AB-Meta"),
            ]
        ),
        ConnectBone(
            name="Penis.004",
            bone_a="iv_ochinko_e",
            bone_b="iv_ochinko_f",
            parent="Penis.003",
            is_connected=True,
            req_bones=["iv_ochinko_e", "iv_ochinko_f"],
            operations=[
                CollectionOperation(bone_name="Penis.004", collection_name="AB-Meta"),
            ],
        ),
        ExtensionBone(
            name="Penis.005",
            bone_a="iv_ochinko_f",
            parent="Penis.004",
            is_connected=True,
            req_bones=["iv_ochinko_f"],
            operations=[
                CollectionOperation(bone_name="Penis.005", collection_name="AB-Meta"),
            ]
        ),
        ExtensionBone(
            name="Testicle.R",
            bone_a="iv_kougan_r",
            parent=["Spine.001", "j_kosi"],
            is_connected=False,
            start="head",
            size_factor=0.5,
            req_bones=["iv_kougan_r"],
            operations=[
                RigifyTypeOperation(bone_name="Testicle.R", rigify_type=rigify.types.skin_basic_chain(skin_control_orientation_bone="Spine.001")),
                CollectionOperation(bone_name="Testicle.R", collection_name="Genitals (Male)")
            ]
        ),
        ExtensionBone(
            name="Testicle.L",
            bone_a="iv_kougan_l",
            parent=["Spine.001", "j_kosi"],
            is_connected=False,
            start="head",
            size_factor=0.5,
            req_bones=["iv_kougan_l"],
            operations=[
                RigifyTypeOperation(bone_name="Testicle.L", rigify_type=rigify.types.skin_basic_chain(skin_control_orientation_bone="Spine.001")),
                CollectionOperation(bone_name="Testicle.L", collection_name="Genitals (Male)")
            ]
        )
    ]
)

def get_rig_module() -> RigModule:
    return RigModule(
        name="IVCS Male",
        type="Generation",
        bone_groups=[GENITALS_M],
        ui_collections = UI_Collections([
            BoneCollection(name="Genitals (Male)", ui=True, color_set="IVCS", row_index=1, title="Genitals (Male)", visible=False),
            BoneCollection(name="AB-Meta", ui=False, color_set="IVCS", row_index=2, title="", visible=False),
        ]),
        operations=[
            CollectionOperation(time="Post", bone_name="Penis-master", collection_name="Genitals (Male)"),
            CollectionOperation(time="Post", bone_name="Penis-start01", collection_name="Genitals (Male)"),
            CollectionOperation(time="Post", bone_name="Penis-mid01", collection_name="Genitals (Male)"),
            CollectionOperation(time="Post", bone_name="Penis-end01", collection_name="Genitals (Male)"),
            CollectionOperation(time="Post", bone_name="Penis-end", collection_name="Genitals (Male)"),
            CollectionOperation(time="Post", bone_name="Penis-end-twist", collection_name="Genitals (Male)"),
            _ivcs_widget("Penis-master"),
            _ivcs_widget("Penis-start01"),
            _ivcs_widget("Penis-mid01"),
            _ivcs_widget("Penis-end01"),
            _ivcs_widget("Penis-end"),
            _ivcs_widget("Penis-end-twist"),
        ]
    )
