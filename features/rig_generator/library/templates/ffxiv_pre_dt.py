from ...module import Template
from ..modules import arms, clothing, ears, genitals, hair, hands, legs, spine, tail, toes, ui

FFXIV_PRE_DT = Template(
    name="FFXIV-PreDT",
    modules=[
        [ears.ffxiv_miqo],
        [hair.ffxiv_default],
        [spine.ffxiv_default],
        [arms.ffxiv_default],
        [hands.ffxiv_ivcs, hands.ffxiv_default],
        [legs.ffxiv_default],
        [toes.ffxiv_ivcs],
        [clothing.ffxiv_default],
        [tail.ffxiv_fk, tail.ffxiv_spline],
        [genitals.ffxiv_ivcs_both],
        [ui.debug],
    ],
)

