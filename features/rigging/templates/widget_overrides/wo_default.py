from .....core.shared import WidgetOverride


WO_DEFAULT = {
        #root
        "root": WidgetOverride(bone="root", scale_factor=0.2),
        #face
        "cheek_t_l": WidgetOverride(bone="Cheek.T.L",scale_factor=0.3,),
        "cheek_t_l_001": WidgetOverride(bone="Cheek.T.L.001",scale_factor=0.3,),
        "cheek_b_l_001": WidgetOverride(bone="Cheek.B.L.001",scale_factor=0.3,),
        "cheek_b_l": WidgetOverride(bone="Cheek.B.L",scale_factor=0.3,),
        "nose_l": WidgetOverride(bone="Nose.L",scale_factor=0.3,),
        "nostril_l": WidgetOverride(bone="Nostril.L",scale_factor=0.2,),    
        "nose": WidgetOverride(bone="Nose",scale_factor=0.2,),
        #Right Face
        "cheek_t_r": WidgetOverride(bone="Cheek.T.R",scale_factor=0.3,),
        "cheek_t_r_001": WidgetOverride(bone="Cheek.T.R.001",scale_factor=0.3,),
        "cheek_b_r_001": WidgetOverride(bone="Cheek.B.R.001",scale_factor=0.3,),
        "cheek_b_r": WidgetOverride(bone="Cheek.B.R",scale_factor=0.3,),
        "nose_r": WidgetOverride(bone="Nose.R",scale_factor=0.3,),
        "nostril_r": WidgetOverride(bone="Nostril.R",scale_factor=0.2,),
        #Mouth
        "teeth.T": WidgetOverride(bone="Teeth.T", rotation=[0.0, 0.0, 3.1415], scale_factor=1.7),
        "teeth.B": WidgetOverride(bone="Teeth.B", rotation=[0.0, 0.0, 3.1415], scale_factor=1.7),
        "jaw_master_mouth": WidgetOverride(bone="jaw_master_mouth", scale=[0.6, 1, 0.3]),
        #chest
        "chest.R": WidgetOverride(bone="Chest.R", translation=[0.0, 0.05, 0.0]),
        "chest.L": WidgetOverride(bone="Chest.L", translation=[0.0, 0.05, 0.0]),
    }