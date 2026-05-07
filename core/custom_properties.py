from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Literal, ClassVar
import bpy

PropertyType = Literal["FLOAT", "FLOAT_ARRAY", "INT", "INT_ARRAY", "BOOL", "BOOL_ARRAY", "STRING", "DATA_BLOCK", "PYTHON"]

@dataclass(frozen=True)
class CustomProperty(ABC):
    
    property_name: str
    property_value: float
    
    def apply(self, target):

        try:
            target[self.property_name] = self.property_value
            prop_type = getattr(type(target), self.property_name)
            prop_type = self.get_prop_settings()

        except Exception as e:
            print(f"[AetherBlend] Error applying CustomPropertyOperation for armature. : {e}")
        
    @abstractmethod 
    def get_prop_settings():
        pass

####################################################
# Property Types
####################################################       

@dataclass(frozen=True)
class FloatProperty(CustomProperty):

    max: float | None = None
    min: float | None = None
    
    def get_prop_settings(self) -> bpy.props.FloatProperty:
        """Applies float specific options to a custom property"""
        prop = bpy.props.FloatProperty(min = self.min, max = self.max)
        return prop

        
        
