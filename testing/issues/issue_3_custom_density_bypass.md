# [Bug/Calculation] Custom material densities for steel and concrete are ignored during dead load and grillage analysis

## 1. Description & Summary
When a user defines custom densities for structural steel (`KEY_MATERIAL_GIRDER_DENSITY`, e.g. $80.0\text{ kN/m}^3$) or concrete deck slab (`KEY_MATERIAL_DECK_DENSITY`, e.g. lightweight concrete at $18.0\text{ kN/m}^3$ or dense concrete at $26.0\text{ kN/m}^3$), the structural analysis pipeline bypasses these inputs and hardcodes default values ($78.5\text{ kN/m}^3$ for steel and $25.0\text{ kN/m}^3$ for concrete). This leads to inaccurate self-weight computations, reaction envelopes, and dead load stresses.

---

## 2. Steps to Reproduce

1. Open OsdagBridge and select the Plate Girder Bridge module.
2. In the material properties settings, define a custom steel density (e.g. $80.0\text{ kN/m}^3$) and custom deck concrete density (e.g. $26.0\text{ kN/m}^3$).
3. Run **Design**.
4. Inspect the generated grillage loads and self-weight values printed in the execution logs or internal `grillage_model`.

Alternatively, verify via Python:

```python
from osdagbridge.core.bridge_types.plate_girder.plategirderbridge import PlateGirderBridge
from osdagbridge.core.bridge_types.plate_girder.defaults import BASIC_INPUT_DICT, solve_extend_basic_input_dict
import osdagbridge.core.utils.common as comm

inp = dict(BASIC_INPUT_DICT)
inp[comm.KEY_SPAN] = 30.0
inp[comm.KEY_CARRIAGEWAY_WIDTH] = 7.5
inp[comm.KEY_MATERIAL_GIRDER] = 'Custom'
inp[comm.KEY_MATERIAL_GIRDER_DENSITY] = 80.0
inp[comm.KEY_MATERIAL_DECK] = 'Custom'
inp[comm.KEY_MATERIAL_DECK_DENSITY] = 26.0
solve_extend_basic_input_dict(inp)

bridge = PlateGirderBridge()
bridge.set_input(inp)
bridge._build_material_props()

print("Assigned Steel Density (N/m³):", bridge.material_props.steel.rho)
```

---

## 3. Expected Result
The finite element model and dead load generators should calculate girder self-weight using $80.0\text{ kN/m}^3$ and deck slab self-weight using $26.0\text{ kN/m}^3$, directly reflecting the user's custom specifications.

---

## 4. Actual Result & Evidence

### Execution Log:
```
Assigned Steel Density (N/m³): 78500.0
```
Despite specifying $80.0\text{ kN/m}^3$, the density is assigned as $78500.0\text{ N/m}^3$ ($78.5\text{ kN/m}^3$).

### Code Evidence in `analyser.py:416`:
```python
# Hardcoded constant used instead of material property
beam_mag = girder_self_weight_kN_m(A_girder_m2, STEEL_UNIT_WEIGHT_kN_m3) * kN / m
```

### Code Evidence in `plategirderbridge.py:1333`:
```python
model = self.grillage_model
model.create_self_weight_load()
model.create_deck_load(slab_thickness_m=deck_t_m)  # concrete_density_kN_m3 omitted
```

---

## 5. Root Cause Analysis
Three compounding bypass points exist in the analysis pipeline:
1. **Girder Density Lookup Fallback**: In `plategirderbridge.py:1192–1195`, `_build_material_props` queries `_lookup_material(steel_grade, "Density")`. For custom steel grades, the SQLite query returns `None`. The fallback logic immediately assigns `_DEFAULT_DENSITY = 78500.0` without inspecting `self.input_dict.get(KEY_MATERIAL_GIRDER_DENSITY)`.
2. **Analysis Load Hardcoding**: In `analyser.py:416`, `create_self_weight_load()` computes beam dead load using the module-level constant `STEEL_UNIT_WEIGHT_kN_m3 = 78.5` rather than reading the density from the model's assigned `material_props`.
3. **Deck Load Parameter Omission**: In `plategirderbridge.py:1333`, `model.create_deck_load(slab_thickness_m=deck_t_m)` is invoked without supplying `concrete_density_kN_m3`. Consequently, `analyser.py:451` defaults to `25.0 kN/m³`.

---

## 6. Suggested Code Fix

### Diff for `src/osdagbridge/core/bridge_types/plate_girder/plategirderbridge.py`:
```diff
--- a/src/osdagbridge/core/bridge_types/plate_girder/plategirderbridge.py
+++ b/src/osdagbridge/core/bridge_types/plate_girder/plategirderbridge.py
@@ -1191,7 +1191,8 @@ class PlateGirderBridge:
 
          rho = self._lookup_material(steel_grade, "Density")
          if rho is None:
-            rho = _DEFAULT_DENSITY
+            raw_rho = self.input_dict.get(KEY_MATERIAL_GIRDER_DENSITY)
+            rho = float(raw_rho) * 1000.0 if raw_rho not in (None, "") else _DEFAULT_DENSITY
 
          fy = self._lookup_material(steel_grade, "Yield Strength")
@@ -1330,7 +1331,8 @@ class PlateGirderBridge:
 
          model = self.grillage_model
          model.create_self_weight_load()
-        model.create_deck_load(slab_thickness_m=deck_t_m)
+        deck_density = float(self.input_dict.get(KEY_MATERIAL_DECK_DENSITY, 25.0))
+        model.create_deck_load(slab_thickness_m=deck_t_m, concrete_density_kN_m3=deck_density)
          model.create_wearing_course_load(thickness_m=wc_t_m, density_kN_m3=wc_rho, partial_safety_factor=1.0)
```

### Diff for `src/osdagbridge/core/bridge_types/plate_girder/analyser.py`:
```diff
--- a/src/osdagbridge/core/bridge_types/plate_girder/analyser.py
+++ b/src/osdagbridge/core/bridge_types/plate_girder/analyser.py
@@ -413,7 +413,8 @@ class GrillageModel:
+        steel_rho_kN_m3 = (self.material_props.steel.rho / 1000.0) if hasattr(self, 'material_props') and self.material_props else STEEL_UNIT_WEIGHT_kN_m3
          for z_pos in model.Mesh_obj.noz[1:-1]:
              A_girder_m2 = _area_for_z(z_pos)
-            beam_mag = girder_self_weight_kN_m(A_girder_m2, STEEL_UNIT_WEIGHT_kN_m3) * kN / m
+            beam_mag = girder_self_weight_kN_m(A_girder_m2, steel_rho_kN_m3) * kN / m
              print(f"Self weight line load @ z={z_pos:.3f} m: {beam_mag:.2f} N/m (A={A_girder_m2:.5f} m²)")
```
