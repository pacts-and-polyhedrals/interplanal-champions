"""Player options: the Asmodeun Scriptorium's three subclasses (carried over) and Interplanal Champions' three new ones."""
from scriptorium_v2 import (SCHOOL, OATH, DOMAIN, WIZ_FEATURES, PAL_FEATURES, CLE_FEATURES, OATH_SPELLS, DOMAIN_SPELLS)
import scriptorium_v2 as _V
import playeroptions_ic as IC

SUBCLASSES = IC.SUBCLASSES + _V.SUBCLASSES
FEATURE_FOLDERS = dict(IC.FEATURES)
FEATURE_FOLDERS.update({"School of Infernal Contracts — Features": WIZ_FEATURES,
                        "Oath of the Infernal Lord — Features": PAL_FEATURES,
                        "Contract Domain — Features": CLE_FEATURES})
FEATURES = [f for v in FEATURE_FOLDERS.values() for f in v]
SUB_NOTES = IC.SUB_NOTES + [
    "<strong>Asmodeun Scriptorium subclasses</strong> (School of Infernal Contracts, Oath of the Infernal Lord, Contract Domain) "
    "are carried over unchanged from <em>The Night of the Red Clause</em>; Orren, Caldris and Nema use them.",
]
