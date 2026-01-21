# AetherBlend Project Structure Guide

## Overview

AetherBlend follows a **feature-based architecture** with clear separation between business logic, user interface, and utilities. This structure is designed to be maintainable, scalable, and free of circular dependencies.

## Directory Structure

```
AetherBlend/
├── core/                      # Pure business logic (NO UI)
│   ├── shared.py              # Shared types to avoid circular imports
│   ├── constraints.py         # Constraint builder classes
│   ├── generators.py          # Bone generator classes
│   └── rigify/                # Rigify integration
│       ├── types.py           # Rigify type settings
│       └── settings.py        # BoneCollection, ColorSet
│
├── features/                  # Self-contained feature modules
│   ├── character/             # Character import workflow
│   │   ├── operators.py       # Import operators
│   │   └── panels.py          # UI panels
│   ├── rigging/               # Rig generation workflow
│   │   ├── operators.py       # Rig operators
│   │   ├── properties.py      # Rig properties
│   │   ├── panels.py          # UI panels
│   │   └── templates/         # Rig data templates (human.py)
│   ├── cplus/                 # Customization+ workflow
│   │   ├── operators.py       # C+ operators
│   │   ├── properties.py      # C+ properties
│   │   ├── panels.py          # UI panels
│   │   ├── editor_panel.py    # C+ editor UI
│   │   └── decoder.py         # C+ string parsing
│   ├── animation/             # Animation/Pose export
│   │   ├── export_anim.py     # Animation export
│   │   ├── export_pose.py     # Pose export
│   │   └── panels.py          # Export UI
│   └── vfx/                   # VFX export
│       └── operators.py       # VFX export operator
│
├── utils/                     # Low-level utility functions
│   ├── armature/              # Armature utilities
│   ├── collection.py          # Collection utilities
│   ├── object.py              # Object utilities
│   ├── viewport.py            # Viewport utilities
│   └── import_export.py       # Import/export wrappers
│
├── ui/                        # General UI panels
│   ├── info_panel.py          # Info/about panel
│   ├── aetherbridge_pt.py     # AetherBridge panel
│   └── spring_bone_pt.py      # Spring bone panel
│
├── properties/                # Global addon properties
│   └── tab_prop.py            # Tab navigation properties
│
├── preferences.py             # Addon preferences
└── __init__.py                # Addon registration
```

---

## Design Philosophy

### Core vs Features vs Utils

**Core** = "What" (Business Logic)
- Pure algorithms and data structures
- Builder patterns (e.g., `CopyLocationConstraint`)
- Orchestrators (e.g., `BoneGroup`, `AetherRigGenerator`)
- Can use Blender **data** API (`bpy.types.Object`, `bpy.data.*`)
- **NEVER** uses Blender **UI** API (`bpy.types.Operator`, `Panel`, `PropertyGroup`)

**Features** = "How" + "When" + "UI" (User Interaction)
- Blender operators (user actions)
- UI panels and properties
- Feature-specific workflows
- Orchestrates core logic
- Provides user feedback

**Utils** = "Helpers" (Generic Tools)
- Low-level helper functions
- No business logic
- Reusable across features
- Generic operations (merge objects, find armature, etc.)

---

## Dependency Flow (No Circular Imports!)

```
features/ → core/ → utils/
  (UI)      (Logic)  (Helpers)
```

**Rules:**
1. Features can import from core and utils
2. Core can import from utils
3. Utils cannot import from core or features
4. Core cannot import from features

**This one-way flow prevents circular imports.**

---

## Where Does Code Go?

### Decision Tree

```
┌─ Is it a Blender operator/panel/property?
│  └─ YES → features/[feature_name]/
│
├─ Does it show UI or handle user input?
│  └─ YES → features/[feature_name]/
│
├─ Is it an algorithm or data structure?
│  └─ YES → core/
│
├─ Is it a builder pattern (data + construction)?
│  └─ YES → core/
│
├─ Is it specific to one workflow (C+, export, import)?
│  └─ YES → features/[feature_name]/
│
└─ Is it a generic helper function?
   └─ YES → utils/
```

### Examples

**✅ Core:**
```python
# core/constraints.py
@dataclass(frozen=True)
class CopyLocationConstraint(Constraint):
    """Builder pattern - stores config + builds itself"""
    target_bone: str
    
    def apply(self, bone, armature):
        # Programmatic API - called by code, not users
        constraint = bone.constraints.new(type='COPY_LOCATION')
```

**✅ Features:**
```python
# features/rigging/operators.py
class AETHER_OT_Generate_Meta_Rig(bpy.types.Operator):
    """User action - orchestrates core logic"""
    
    def execute(self, context):
        generator = HUMAN  # From core
        generator.generate_meta_rig(armature)  # Calls core
        self.report({'INFO'}, "Done!")  # User feedback
```

**✅ Utils:**
```python
# utils/object.py
def merge_by_material(objects: list) -> list:
    """Generic helper - no business logic"""
    # Simple utility function
```

---

## Key Files Explained

### core/shared.py
**Purpose:** Shared types to avoid circular imports

**Contains:**
- `link` - Pure data model for linking bones
- `PoseOperations` - Builder for pose operations
- `BoneGroup` - Orchestrates multiple bone generators
- `AetherRigGenerator` - Orchestrates bone groups

**Why together?** These classes reference each other (e.g., `BoneGroup` has `list[BoneGenerator]`). Putting them in one file avoids circular imports.

### core/generators.py
**Purpose:** Bone generator implementations

**Contains:**
- `BoneGenerator` (ABC) - Base interface
- `ConnectBone` - Connects two bones
- `ExtensionBone` - Extends from a bone
- `CopyBone` - Copies a bone's transform

**Pattern:** Each generator is a dataclass that knows how to construct itself.

### core/constraints.py
**Purpose:** Constraint builder classes

**Contains:**
- `Constraint` (ABC) - Base interface
- `CopyLocationConstraint`, `CopyRotationConstraint`, etc.

**Pattern:** Immutable dataclasses (frozen=True) that build Blender constraints.

### features/rigging/templates/
**Purpose:** Rig data definitions

**Contains:**
- `human.py` - FFXIV human rig definition
- `__init__.py` - Exports `HUMAN` rig generator

**Note:** This is rig **data**, not logic, which is why it's in features (specific to rigging workflow) rather than core (generic logic).

---

## Avoiding Circular Imports

### Problem
```python
# generators.py needs PoseOperations
class BoneGenerator:
    pose_operations: PoseOperations | None

# shared.py needs BoneGenerator
class BoneGroup:
    bones: list[BoneGenerator] | None
```

### Solution 1: TYPE_CHECKING
```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .generators import BoneGenerator  # Only for type checkers

class BoneGroup:
    bones: 'list[BoneGenerator] | None' = None  # String quotes!
```

**How it works:**
- `TYPE_CHECKING` is `False` at runtime (no import)
- Type checkers (Pylance) pretend it's `True` (sees the import)
- Use string quotes around types

### Solution 2: Shared File
Put mutually dependent classes in one file (like `shared.py`).

---

## Feature Module Pattern

Each feature follows this pattern:

```python
# features/[feature_name]/__init__.py
from . import operators
from . import properties
from . import panels

modules = (properties, operators, panels)

def register():
    for mod in modules:
        mod.register()

def unregister():
    for mod in modules:
        mod.unregister()
```

**Benefits:**
- Self-contained
- Easy to enable/disable
- Clear structure

---

## Registration Pattern

### Main __init__.py
```python
from . import preferences
from . import features
from . import ui
from .properties import tab_prop

def register():
    preferences.register()
    tab_prop.register()
    features.register()  # All features at once
    ui.register()

def unregister():
    ui.unregister()
    features.unregister()
    tab_prop.unregister()
    preferences.unregister()
```

**Clean and simple** - all features registered with one call.

---

## Best Practices

### DO ✅
- Use explicit imports: `from core import shared`
- Put shared types in one file to avoid circular imports
- Use TYPE_CHECKING for type hints that would cause circular imports
- Keep core logic separate from UI
- Follow the dependency flow: features → core → utils

### DON'T ❌
- Import features from core
- Import core from utils
- Use wildcard imports (`from module import *`) in production code
- Put imports inside functions (unless absolutely necessary)
- Mix UI code with business logic

---

## Adding New Features

### Step 1: Create Feature Directory
```
features/
  └── my_feature/
      ├── __init__.py
      ├── operators.py
      ├── properties.py
      └── panels.py
```

### Step 2: Register Feature
```python
# features/my_feature/__init__.py
from . import operators, properties, panels

modules = (properties, operators, panels)

def register():
    for mod in modules:
        mod.register()

def unregister():
    for mod in modules:
        mod.unregister()
```

### Step 3: Add to features/__init__.py
```python
from . import my_feature

modules = (..., my_feature)
```

Done! Your feature is now integrated.

---

## Common Pitfalls

### Circular Import Error
**Symptom:** `ImportError: cannot import name 'X' from partially initialized module`

**Solution:**
1. Check dependency flow (features → core → utils)
2. Use TYPE_CHECKING for type hints
3. Move shared types to `core/shared.py`

### Import Not Found
**Symptom:** `ModuleNotFoundError: No module named 'X'`

**Solution:**
1. Use relative imports: `from ... import utils` (not `from utils import`)
2. Check that `__init__.py` exists in parent directories
3. Verify file was not deleted during refactoring

---

## Migration from Old Structure

If you have old code using the previous structure:

**Old Import:**
```python
from ..data.rig_data import HUMAN
from ..generator import BoneGenerator
from ..rigify import types
```

**New Import:**
```python
from ...features.rigging.templates import HUMAN
from ...core.generators import BoneGenerator
from ...core import rigify
```

---

## Testing Strategy

### Core (Unit Tests)
Core modules are pure logic and can be tested independently:
```python
def test_connect_bone():
    gen = ConnectBone(name="test", bone_a="a", bone_b="b")
    assert gen.name == "test"
```

### Features (Integration Tests)
Features require Blender runtime (operators, panels):
```python
def test_rig_generation(blender_context):
    bpy.ops.aether.generate_meta_rig()
    assert context.active_object.type == 'ARMATURE'
```

---

## Further Reading

- [Python Import System](https://docs.python.org/3/reference/import.html)
- [Blender Addon Best Practices](https://docs.blender.org/api/current/info_best_practice.html)
- [Feature-Based Architecture](https://en.wikipedia.org/wiki/Feature-oriented_programming)

---

**Last Updated:** January 21, 2026
**Structure Version:** 2.0 (Post Phase 2 Refactor)
