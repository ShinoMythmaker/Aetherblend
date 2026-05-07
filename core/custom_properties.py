from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Literal, ClassVar
import bpy

PropertyType = Literal["FLOAT", "FLOAT_ARRAY", "INT", "INT_ARRAY", "BOOL", "BOOL_ARRAY", "STRING", "DATA_BLOCK", "PYTHON"]

@dataclass(frozen=True)
class CustomProperty(ABC):
    
    property_name: str
    property_value: float
    value_only: bool = False
    
    def apply(self, target):

        try:
            if self.value_only:
                target[self.property_name] = self.property_value
                return
            else:
                ## This is different to a default Custom Property in Blender. 
                # usually Scene["custom_prop"] = value
                # here it is Scene.custom_prop = value 
                # where custom_prop is defined as a bpy.props.Property. 
                setattr(type(target), self.property_name, self.get_prop()) ## Defines Property
                target[self.property_name] = self.property_value    ## This line ??? IDK it needs to be there need further testing
                setattr(target, self.property_name, self.property_value) ## Sets value of property
            
        except Exception as e:
            print(f"[AetherBlend] Error applying CustomPropertyOperation for armature. : {e}")

    @abstractmethod 
    def get_prop(self):
        pass

####################################################
# Property Types
####################################################       

@dataclass(frozen=True)
class FloatProperty(CustomProperty):

    max: float | None = None
    min: float | None = None
    default: float | None = None

    def get_prop(self) -> bpy.props.FloatProperty:
        """Applies float specific options to a custom property"""
        prop_kwargs = {}

        if self.max is not None:
            prop_kwargs["max"] = self.max
        if self.min is not None:
            prop_kwargs["min"] = self.min
        if self.default is not None:
            prop_kwargs["default"] = self.default

        return bpy.props.FloatProperty(**prop_kwargs)
    

        
        
