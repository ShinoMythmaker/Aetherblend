from ...definitions import Template
from ..modules import arms, clothing, ears, face, genitals, hair, hands, legs, mouth, spine, tail, toes, ui

FFXIV_DEFAULT = Template(
    name="FFXIV-Default",
    modules=[
        [ears.ffxiv_miqo],
        [hair.ffxiv_default],
        [face.ffxiv_detailed],
        [mouth.ffxiv_default],
        [spine.ffxiv_default],
        [arms.ffxiv_default],
        [hands.ffxiv_ivcs, hands.ffxiv_default],
        [legs.ffxiv_default],
        [toes.ffxiv_ivcs],
        [clothing.ffxiv_default],
        [tail.ffxiv_spline, tail.ffxiv_fk],
        [genitals.ffxiv_ivcs_both],
        [ui.debug],
    ],
)
