# [Bug] MaterialPropertiesDialog misclassifies Concrete Deck as Structural Steel due to unhandled member key and internal whitespace in grade name, causing missing fck and design failure

## 1. Description & Summary
When configuring bridge material properties in OsdagBridge, selecting the Concrete Deck member properties dialog incorrectly identifies the concrete deck as structural steel. This prevents the user from viewing or editing concrete compressive strength ($f_{ck}$), tensile strength ($f_{ctm}$), and modulus of elasticity ($E_{cm}$). Furthermore, if exported, it leaves `material.deck.fck` unpopulated, triggering a fatal `ValueError` in downstream design checks.

---

## 2. Steps to Reproduce

1. Launch OsdagBridge and select the Plate Girder Bridge module.
2. In the `InputDock`, observe the **Deck Concrete Grade** field, which displays values such as `"M 35"` or `"M 40"` (containing a space).
3. Click the info button next to Deck Concrete Grade, or change the selection.
4. Observe the dialog that appears: it displays **Structural Steel** parameters (Yield Strength $F_y$, Ultimate Tensile Strength $F_u$, Shear Modulus $G$) instead of concrete parameters ($f_{ck}, f_{ctm}, E_{cm}$).
5. Click **Design**.

Alternatively, run the headless verification script:

```python
from osdagbridge.desktop.ui.dialogs.material_properties import MaterialPropertiesDialog
from PySide6.QtWidgets import QApplication
import sys

app = QApplication.instance() or QApplication(sys.argv)
dlg = MaterialPropertiesDialog(read_only=True, selected_material='M 35', member='material.deck')
print('is_deck_material:', dlg.is_deck_material)
print('Exported fields:', dlg.get_export_fields())
```

---

## 3. Expected Result
The dialog should recognize `member="material.deck"` and grade `"M 35"` as concrete, presenting compressive strength $f_{ck}$, tensile strength $f_{ctm}$, elastic modulus $E_{cm}$, and concrete density $\rho_{conc}$. Downstream design routines should receive a validated `material.deck.fck` value.

---

## 4. Actual Result & Evidence

### Dialog Property State:
```
is_deck_material: False
Exported fields: {'material.deck.density': '76.4', 'material.deck.fy': '350.0', 'material.deck.fu': '490.0', 'material.deck.e': '200.0', 'material.deck.g': '76.9', 'material.deck.poisson': '0.30', 'material.deck.thermal': '11.7'}
```

### Downstream Design Crash:
```
Traceback (most recent call last):
  File "src/osdagbridge/core/bridge_types/plate_girder/plategirderbridge.py", line 2297, in _run_dcr_checks
    _, engine, design_results = run_design_check(...)
  File "src/osdagbridge/core/bridge_types/plate_girder/designer.py", line 3235, in run_design_check
    config = BridgeConfig.from_plate_girder_bridge(plate_girder_bridge)
  File "src/osdagbridge/core/bridge_types/plate_girder/designer.py", line 332, in from_plate_girder_bridge
    fck = float(_req(bridge.input_dict.get(KEY_MATERIAL_DECK_FCK), KEY_MATERIAL_DECK_FCK))
  File "src/osdagbridge/core/bridge_types/plate_girder/designer.py", line 95, in _req
    raise ValueError(
ValueError: 'material.deck.fck' is required but was not found in 'input_dict'. Populate 'material.deck.fck' before running the design check.
```

---

## 5. Root Cause Analysis
The defect involves two compounding issues:
1. **Member Key Discrepancy**: In `InputDock`, the key passed to `MaterialPropertiesDialog` is `comm.KEY_DECK_CONCRETE_GRADE_BASIC` (`"material.deck"`). However, `MaterialPropertiesDialog.__init__` at line 180 checks only:
   ```python
   self.is_deck_material = (self.member == "Deck") or self._is_deck_material(self.selected_material)
   ```
   Since `self.member` is `"material.deck"`, `self.member == "Deck"` evaluates to `False`.
2. **Whitespace Mismatch in Grade Lookup**: The fallback method `self._is_deck_material("M 35")` evaluates:
   ```python
   normalized = (material_name or "").strip()
   return (normalized in concrete_properies or normalized.lower().startswith(CUSTOM_CONCRETE_PREFIX))
   ```
   The SQLite database table `Concrete_Grade_Properties` stores grades without spaces (`"M35"`, `"M40"`). Because `"M 35"` retains its inner space, `normalized in concrete_properies` fails. Consequently, `is_deck_material` remains `False`.

---

## 6. Suggested Code Fix

### Diff for `src/osdagbridge/desktop/ui/dialogs/material_properties.py`:
```diff
--- a/src/osdagbridge/desktop/ui/dialogs/material_properties.py
+++ b/src/osdagbridge/desktop/ui/dialogs/material_properties.py
@@ -177,7 +177,10 @@ class MaterialPropertiesDialog(QDialog):
         self.selected_material = selected_material or ""
         self.member = member
         self.custom_fields = custom_fields
-        self.is_deck_material = (self.member == "Deck") or self._is_deck_material(self.selected_material)
+        self.is_deck_material = (
+            self.member in ("Deck", KEY_DECK_CONCRETE_GRADE_BASIC) or
+            self._is_deck_material(self.selected_material)
+        )
         self.setWindowTitle(DIALOG_TITLE_MATERIAL_PROPERTIES)
         self.setObjectName("material_properties_dialog")
@@ -433,7 +436,8 @@ class MaterialPropertiesDialog(QDialog):
         return widget
 
     def _is_deck_material(self, material_name: str) -> bool:
-        normalized = (material_name or "").strip()
-        return (normalized in concrete_properies or 
+        normalized = (material_name or "").replace(" ", "").upper()
+        db_grades = [g.replace(" ", "").upper() for g in concrete_properies]
+        return (normalized in db_grades or 
                 normalized.lower().startswith(CUSTOM_CONCRETE_PREFIX))
```

### Diff for `src/osdagbridge/core/bridge_types/plate_girder/plategirderbridge.py`:
```diff
--- a/src/osdagbridge/core/bridge_types/plate_girder/plategirderbridge.py
+++ b/src/osdagbridge/core/bridge_types/plate_girder/plategirderbridge.py
@@ -1221,6 +1221,7 @@ class PlateGirderBridge:
             raw_fck = self.input_dict.get(KEY_MATERIAL_DECK_FCK)
             fck = float(raw_fck) if raw_fck not in (None, "") else 25.0
+        self.input_dict[KEY_MATERIAL_DECK_FCK] = fck
 
         fctm = self._lookup_material(concrete_grade, "fctm")
         if fctm is None:
```
