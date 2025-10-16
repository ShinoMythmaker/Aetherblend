
# AetherBlend Python Add-on Style Guide

## General Python Style
- **PEP8 Compliance:**  
  Follow [PEP8](https://peps.python.org/pep-0008/) for general Python code style (indentation, spacing, line length, etc.).
- **Type Hints:**  
  Use type hints for function arguments and return values where possible for clarity and editor support. For Blender types, use type hints if available in the Blender API, or use `Any`/`object` if unsure.

## Operator Classes
- **Class Names:**  
  Must start with `AETHER_OT_`, e.g. `AETHER_OT_OperatorName`
- **bl_idname:**  
  Must be lowercase and use dot notation, e.g. `aether.operator_name`
- **bl_description:**  
  Always include the `bl_description` variable in operator classes. No Docstring for Operators Classes
- **File Naming:**  
  Operator type modules must end with `_ot.py`.

## Panel Classes
- **File Naming:**  
  Panel type modules must end with `_pt.py`.

## Property Classes
- **File Naming:**  
  Property type modules must end with `_prop.py`.

## Functions
- **Naming:**  
  Functions must be lowercase with underscores, e.g. `function_name`.
- **Docstrings:**  
  Functions must have a description under the function name in triple quotes (`""" ... """`).
- **Type Hints:**  
  Use type hints where possible, especially for public utility functions. For Blender types, use the Blender API type or `Any`/`object` if unsure.
- **Constants:**  
  Use ALL_CAPS for constants.
- **Private/Internal Functions:**  
  Prefix internal-use functions with an underscore, e.g. `_helper_function`.
- **Utility Functions:**  
  - Name functions with the module context in mind.  
    For example, in `utility.bone.exist()`, the function should be named `exist`, not `bone_exist`.
  - Utility functions should always restore the original mode after execution.

## Console Messages
- **Format:**  
  All console messages must start with `[AetherBlend] ...`
- **Reporting:**  
  - Operators should use `self.report`.
  - Utility modules should use `print`.
- **Error Messages:**  
  Always provide clear, actionable error messages in `self.report` or `print`.

## Module Structure & Imports
- **Operator Modules:**  
  - Should only contain code specific to that operator.
  - Any reusable function should be placed in a utility module.
- **Utility Imports:**  
  - Always use `from . import utility` to import utility modules as a whole.
  - Never import individual functions or use wildcard imports (e.g. `from module import *`).
- **Import Order:**  
  Standard library imports first, then third-party, then local imports.
- **Module Docstrings:**  
  Each module should start with a brief docstring describing its purpose.


## Example Usage

```python
# Operator class
class AETHER_OT_MyOperator(bpy.types.Operator):
    bl_idname = "aether.my_operator"
    bl_label = "My Operator"
    bl_description = "Does something useful"
    # ...

# Utility function
def exist(armature, bone_names):
    """
    Checks if the specified bone(s) exist in the armature.
    """
    # ...