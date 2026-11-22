# OsdagBridge Screening Task: Video Recording Script & Director's Guide
**Project**: FOSSEE Winter Internship 2026 | IIT Bombay  
**Task Category**: OsdagBridge Software Testing & Issue Reporting  
**Candidate**: Aman Jaiswal (`amanraj74`)  
**Target Duration**: 2 minutes 45 seconds to 3 minutes  
**Format**: MP4 (1080p, 60fps or 30fps) | Spoken Voiceover OR Silent Screencast  

---

## 1. Pre-Recording Setup (Do This Before Recording)

1. **Screen Resolution**: Set display to **1920 × 1080 (100% scaling)** for crisp text.
2. **Recording Software**:
   - **Windows Built-in**: Press `Win + Alt + R` to start/stop recording (via Xbox Game Bar).
   - **OBS Studio / Loom / ShareX**: Capture full desktop or application window.
3. **Have These Ready in the Background**:
   - **Terminal** (PowerShell or Anaconda Prompt) with environment activated:
     ```powershell
     conda activate osdagbridge-env
     cd "d:\my work\OsdagBridge\src"
     ```
   - **PDF Viewer**: `OsdagBridge_Testing_Report.pdf` open to Page 1.
   - **Web Browser**: Tab open to `https://github.com/amanraj74/OsdagBridge/tree/dev`.
   - **File Explorer / VS Code**: Open at `d:\my work\OsdagBridge\testing`.

---

## 2. Complete Scene-by-Scene Timeline & Script

```
+---------------+-----------------------------------------------+-------------------+
| Timeline      | Scene Name                                    | Screen Focus      |
+---------------+-----------------------------------------------+-------------------+
| 0:00 - 0:30   | Scene 1: Introduction & GUI Launch            | Desktop & GUI     |
| 0:30 - 1:15   | Scene 2: Baseline Design & 3D CAD OpenCASCADE | 3D Model & Output |
| 1:15 - 1:55   | Scene 3: Custom Materials & Bug 1 Anomaly     | Dialog & Inputs   |
| 1:55 - 2:30   | Scene 4: Multi-Run Stability (Issue #135)     | Solver & Code     |
| 2:30 - 3:00   | Scene 5: Verification Suite & Submission Wrap | PDF & Artifacts   |
+---------------+-----------------------------------------------+-------------------+
```

---

### Scene 1: Introduction & Desktop GUI Launch
- **Timestamp**: `0:00 – 0:30` (30 seconds)
- **What is on Screen**: PowerShell window launching OsdagBridge, followed by the main GUI opening.

#### Step-by-Step Actions:
1. In PowerShell, type and run:
   ```powershell
   python -m osdagbridge.desktop
   ```
2. The OsdagBridge main window appears. Maximize the window.
3. In the left module panel, click **Plate Girder Bridge**.
4. The Input Dock populates with default parameters.
5. Move the mouse cursor smoothly across:
   - **Span**: `30.0 m`
   - **Carriageway Width**: `7.5 m`
   - **Girder Steel**: `E 350A`
   - **Deck Concrete**: `M 35`

#### Spoken Voiceover Script (Word-for-Word):
> *"Hello, I am Aman Jaiswal, candidate for the FOSSEE Osdag Winter Internship 2026. This video demonstrates functional testing and software verification for the short-span steel plate girder bridge module in OsdagBridge. We begin by launching the desktop application in our Conda environment and selecting the Plate Girder Bridge design module with standard 30-meter baseline parameters."*

*(If recording silent: Keep mouse pointer steady over the module selector and the Input Dock for 4 seconds).*

---

### Scene 2: Baseline Design Run, 3D CAD Visualization & Design Docks
- **Timestamp**: `0:30 – 1:15` (45 seconds)
- **What is on Screen**: Design execution, OpenCASCADE 3D viewer, and Output Dock metrics.

#### Step-by-Step Actions:
1. Move the mouse to the bottom-left and click the green **Design** button.
2. The Progress Dock tracks execution across the 14 linear stages (Grillage mesh generation $\to$ OpenSees analysis $\to$ Section capacity $\to$ CAD drafting).
3. Once completed (progress reaches 100%):
   - Click the **3D CAD** tab in the main canvas.
   - Use the mouse left-click + drag to rotate the full 3D OpenCASCADE model smoothly.
   - Zoom in on the plate girders, cross-frame bracings, and stiffeners.
   - Toggle component checkboxes in the 3D tree (e.g. uncheck/recheck Concrete Deck or Cross Bracing to demonstrate component separation).
4. Click the **Output Dock** to highlight the governing structural utilization ratios:
   - Flexure DCR: **19.79%** ($M_u / M_d = 2219.12 / 11215.89\text{ kNm}$)
   - Shear DCR: **39.91%** ($V_u / V_{cr} = 287.47 / 720.21\text{ kN}$)
   - Deflection Ratio: **45.78%** ($\delta_{total} = 22.89\text{ mm} \le 50.0\text{ mm}$)
   - Fatigue DCR: **157.26%** ($1.57$, governing check)

#### Spoken Voiceover Script (Word-for-Word):
> *"Next, we execute the automated design solver. The grillage model is assembled in OpenSees, live-load envelopes are evaluated, and section capacity checks are performed per IRC 24 and IS 800. In the 3D CAD tab, we inspect the rendered OpenCASCADE solid geometry, verifying girder spacing, vertical stiffeners, and cross-bracings. In the Output Dock, we confirm software pipeline execution succeeded, with flexure at 19.8% and shear at 39.9% utilization, while fatigue governs structural compliance."*

---

### Scene 3: Custom Materials Workflow & Bug 1 Anomaly
- **Timestamp**: `1:15 – 1:55` (40 seconds)
- **What is on Screen**: Input Dock unlocking, Custom Material entry, and the Material Properties Dialog bug.

#### Step-by-Step Actions:
1. In the Input Dock, click the **Unlock** button.
2. In the **Girder Material** dropdown, select **Custom...**:
   - Show custom dialog: enter Grade `custom_steel_1`, Yield Strength $F_y = 360$\,MPa, Ultimate $F_u = 500$\,MPa, Density $= 80.0$\,kN/m$^3$. Click **OK**.
3. Now navigate to the **Deck Concrete Grade** field (`M 35`):
   - Click the information icon (**ℹ**) directly next to the combo box.
   - **Notice Bug 1**: The dialog window opens titled *"Steel Material Properties"* and displays Yield Strength and Tensile Strength instead of Concrete Compressive Strength ($f_{ck}$)!
   - Circle the mouse cursor around the title and fields for 3 seconds to highlight the defect.
   - Close the dialog.
4. Select **Custom...** for Deck Concrete:
   - Enter Grade `custom_concrete_1`, $f_{ck} = 40$\,MPa, Elastic Modulus $= 34$\,GPa, Density $= 26.0$\,kN/m$^3$. Click **OK**.

#### Spoken Voiceover Script (Word-for-Word):
> *"Now we explore custom material specification and uncover our first isolated bug. When clicking the information icon next to the Deck Concrete Grade, the dialog incorrectly opens Steel Material Properties with yield and tensile fields, rather than concrete compressive strength. Our code investigation traced this to a member key mismatch and database whitespace inconsistency in `MaterialPropertiesDialog.py`, for which we have authored a verified drop-in fix."*

---

### Scene 4: Consecutive Redesign Stability & Bug 2 (Resolving Issue #135)
- **Timestamp**: `1:55 – 2:30` (35 seconds)
- **What is on Screen**: Multi-run redesign behavior, dimension degradation, and verified code patch.

#### Step-by-Step Actions:
1. With the model still unlocked, explain repeated run stability:
   - When a user redesigns a bridge without re-priming default dimensions, `_convert_girder_dims_mm_to_m()` previously divided dimensions by 1000 in-place.
   - On Run 1, 1670\,mm becomes 1.670\,m. On Run 2, 1.670\,m divided by 1000 becomes 0.00167\,m (1.67\,mm).
   - This causes clear web depth to become negative ($1.67 - 2 \times 22 = -42.3\text{ mm}$), resulting in a `math domain error` in the square-root calculation of Lateral Torsional Buckling ($M_{cr}$).
2. Quickly switch to VS Code or open `testing/issues/issue_2_consecutive_runs_unit_division.md`:
   - Highlight the **snapshot-and-restore implementation** in `plategirderbridge.py`:
     ```python
     # Save raw UI millimetre snapshot before conversion
     self._raw_ui_dims_mm = {k: inp[k] for k in keys_to_convert}
     # Restore raw UI mm on subsequent executions
     if getattr(self, "_raw_ui_dims_mm", None):
         for k, mm_val in self._raw_ui_dims_mm.items():
             self.input_dict[k] = mm_val
     ```
   - Show the regression verification table: Run 1 (1.670\,m), Run 2 (1.670\,m), Run 3 (1.670\,m) — all passing.

#### Spoken Voiceover Script (Word-for-Word):
> *"Next, we address consecutive redesign stability. In existing versions, re-running design divided girder dimensions in-place on each execution. On Run 2, girder depth collapsed to 1.67 millimeters, producing a negative clear web depth and triggering the crash reported in GitHub Issue #135. We resolved this by implementing an architectural snapshot-and-restore contract in `plategirderbridge.py`, empirically verifying section stability across three consecutive executions."*

---

### Scene 5: Verification Test Suite, Deliverables & Conclusion
- **Timestamp**: `2:30 – 3:00` (30 seconds)
- **What is on Screen**: File Explorer / VS Code showing test files, followed by `OsdagBridge_Testing_Report.pdf`.

#### Step-by-Step Actions:
1. Switch to File Explorer or VS Code showing the repository root:
   - Point to `testing/run_tests.py` (automated test runner for TC01–TC08).
   - Show `testing/osi_files/` (8 reproducible `.osi` project models).
   - Show `testing/dictionaries/` (JSON input and output dictionaries).
   - Show `testing/issues/` (the 3 markdown defect reports).
2. Open `OsdagBridge_Testing_Report.pdf`:
   - Show the Cover Page with Candidate Name **Aman Jaiswal** (`amanraj74`).
   - Scroll through Page 4 (Table 1: 8 Test Scenarios Matrix with separated Software vs. Structural verdicts).
   - Scroll through Page 9–10 (2D CAD drawings and 3D OpenCASCADE renders).
   - Scroll to Page 12 (Issue 2 fix and regression verification).
3. Conclude on the clean GitHub repository fork: `https://github.com/amanraj74/OsdagBridge/tree/dev`.

#### Spoken Voiceover Script (Word-for-Word):
> *"All 8 automated test cases, reproducible OSI models, JSON data dictionaries, and our complete 14-page publication-quality LaTeX report are packaged inside `OsdagBridge_Testing_Submission.zip` and pushed to my GitHub fork at `amanraj74/OsdagBridge`. Thank you for reviewing my submission for the FOSSEE Winter Internship 2026."*

---

## 3. Alternative: Silent Video On-Screen Titles / Text Cards
If you prefer not to record audio or voiceover, you can display short text overlays (or briefly show a clean Notepad window with titles before each scene):

- **Card 1 (0:00)**:  
  *FOSSEE Osdag Winter Internship 2026 | Candidate: Aman Jaiswal (`amanraj74`)*  
  *Screening Task: OsdagBridge Software Testing & Structural Verification*
- **Card 2 (0:30)**:  
  *Baseline Design Run (30m Span) | 3D OpenCASCADE CAD Model & Output Dock DCRs*
- **Card 3 (1:15)**:  
  *Custom Materials Workflow | Bug 1: Concrete Deck Info Dialog Steel Misclassification*
- **Card 4 (1:55)**:  
  *Consecutive Run Stability | Bug 2: Resolving GitHub Issue #135 with Snapshot-and-Restore Fix*
- **Card 5 (2:30)**:  
  *Automated Test Harness (TC01-TC08), OSI Models, and 14-Page LaTeX Technical Report*

---

## 4. Post-Recording Quality Checklist

Before submitting the video link, check:
- [ ] **Length**: Between 2:30 and 3:00 minutes.
- [ ] **Resolution**: High definition (1080p, text clearly readable).
- [ ] **Audio**: Speech is clear and audible (or smooth silent screencast).
- [ ] **Visibility**: No sensitive personal browser data or notifications visible.
- [ ] **Upload**:
  - If **YouTube**: Set visibility to **Unlisted** (NOT Private!).
  - If **Google Drive**: Set General Access to **"Anyone with the link can view"** (NOT Restricted!).
- [ ] **Test Link**: Open the link in a Private/Incognito browser window to verify anyone can watch it without logging in.
