from . import spring_bones_ot, spring_bones_pt, spring_breast_ot, spring_ear_ot, spring_tail_ot

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
