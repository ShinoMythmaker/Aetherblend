---
title: Preferences
group: Development
order: 230
sub: true
---
# Operators: Preferences

Back to [[Operators]].

## `aether.preferences_toggle_feature_set`

**Where:** add-on preferences (Edit → Preferences → Add-ons → AetherBlend).

Enables or disables a *feature set*. Feature sets decide which optional dependencies (Rigify, Meddle Tools, FFGear) AetherBlend checks for. The choice is stored in the preferences.

| Name | Type | Description |
|------|------|-------------|
| `feature_set` | string (hidden) | Token of the feature set to toggle |

Common feature sets cannot be toggled.

## Preferences That Affect Operators

| Preference | Effect |
|------------|--------|
| Auto navigate tabs | Import and Generate switch to the next tab when they finish |
| Show N panel | Show the AetherBlend tab in the 3D Viewport sidebar |
| Show properties tool tab | Mirror the panels in the Properties editor Tool tab |
| Default Meddle import path | Start folder for import and shader file dialogs |
| Default pose export path | Start folder for pose export |
| Default anim export path | Start folder for animation export |
