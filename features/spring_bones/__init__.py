from . import spring_bones_ot
from . import spring_tail_ot
from . import spring_ear_ot
from . import spring_breast_ot
from . import spring_bones_pt

modules = (
    # spring_bones_ot,
    # spring_tail_ot,
    # spring_ear_ot,
    # spring_breast_ot,
    # spring_bones_pt,
)


def register():
    for mod in modules:
        mod.register()


def unregister():
    for mod in reversed(modules):
        mod.unregister()
