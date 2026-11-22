# OsdagBridge Video Demonstration Walkthrough & Script
**Screening Task: OsdagBridge Software Testing & Issue Reporting**  
**Candidate: Aman Jaiswal (`amanraj74`)**  
**FOSSEE Winter Internship 2026 | IIT Bombay**

---

## Overview
This document provides a concise step-by-step guide for recording the 2 to 3-minute screencast required for your FOSSEE submission.

> [!TIP]
> For the comprehensive scene-by-scene script with exact timestamps, mouse actions, word-for-word spoken voiceover dialogue, and silent text cards, see [testing/VIDEO_RECORDING_SCRIPT.md](file:///d:/my%20work/OsdagBridge/testing/VIDEO_RECORDING_SCRIPT.md).

- **Duration**: 2 to 3 minutes
- **Audio**: Spoken voiceover OR Silent screencast (both formats supported)
- **Tools**: Windows Game Bar (`Win + Alt + R`), OBS Studio, Loom, or ShareX
- **Key Sections to Show**:
  1. Application Launch (`python -m osdagbridge.desktop`)
  2. Baseline Design & 3D CAD / 2D Plot Visualization
  3. Custom Material Input Workflow & Info (ℹ) Button Misclassification Anomaly
  4. Consecutive Multi-Run Redesign & State Persistence Analysis (Resolving Issue #135)
  5. Overview of Test Artifacts (`.osi`, JSON dictionaries, and automated test suite)

---

## Step-by-Step Recording Sequence

### Scene 1: Desktop GUI Launch (0:00 - 0:25)
1. Open PowerShell / Command Prompt in your environment:
   ```powershell
   conda activate osdagbridge-env
   cd "d:\my work\OsdagBridge\src"
   python -m osdagbridge.desktop
   ```
2. The OsdagBridge main window appears.
3. Select **Plate Girder Bridge** under Bridge Design Modules.
4. Show the default layout with **Span**: `30.0 m`, **Carriageway Width**: `7.5 m`, **Girder Material**: `E 350A`, **Deck**: `M 35`.

---

### Scene 2: Baseline Design Run & 3D CAD / Plots (0:25 - 1:15)
1. Click the green **Design** button in the lower left corner.
2. The progress dock indicates linear stage execution (Grillage $\to$ Loads $\to$ Envelopes $\to$ Section Checks $\to$ Deck $\to$ CAD).
3. Once completed:
   - Click the **3D CAD** tab to show the fully rendered 3D bridge model in OpenCASCADE.
   - Rotate and zoom the model using the mouse to show the 4 plate girders, cross-bracings, stiffeners, and concrete deck.
   - In the 3D component selector, toggle components (Girder, Stiffener, Cross Bracing).
   - Click the **Output Dock** to display the governing Utilization Ratios (Bending 19.8%, Shear 39.9%, LTB 22.8%, Fatigue 157.3%, Deflection 45.8%).

---

### Scene 3: Custom Material Property Workflow & Anomaly (1:15 - 1:55)
1. Click **Unlock** in the Input Dock.
2. In the **Girder Material** dropdown, select **Custom...**.
   - Enter `custom_steel_1`, $F_y = 360$\,MPa, $F_u = 500$\,MPa, $E = 205$\,GPa, Density $= 80.0$\,kN/m$^3$. Click **OK**.
3. Now, navigate to **Deck Concrete Grade** and click the info icon (**ℹ**):
   - Notice the dialog that opens: it displays **Steel Material Properties** instead of Concrete Grade Properties (Bug 1)!
   - In the dropdown, select **Custom...** for concrete deck, enter $f_{ck} = 40.0$\,MPa, $E_{cm} = 34.0$\,GPa, Density $= 26.0$\,kN/m$^3$. Click **OK**.
4. Click **Design** again to demonstrate execution with custom parameters.

---

### Scene 4: Consecutive Multi-Run Redesign & State Verification (1:55 - 2:30)
1. Click **Unlock** to modify inputs for Run 2:
   - Point to the in-place unit division behavior across consecutive design runs in `_convert_girder_dims_mm_to_m()`.
   - Explain that this isolates the exact root cause of the second-run crash reported in GitHub Issue #135.
2. Show the proposed fix caching raw millimetre inputs before conversion.

---

### Scene 5: Verification Suite & Submission Artifacts (2:30 - 3:00)
1. In VS Code or File Explorer, briefly show:
   - `testing/run_tests.py` automated test runner
   - `testing/report/OsdagBridge_Testing_Report.pdf` (14-page compiled PDF report)
   - `testing/osi_files/` (8 reproducible `.osi` project files)
   - `testing/dictionaries/` (JSON input and output dictionaries)
   - `testing/issues/` (3 formal issue reports with code diffs)
   - `OsdagBridge_Testing_Submission.zip` (complete submission package)

---

## Submission Checklist
- [x] Record screencast (MP4, 1080p recommended).
- [x] Upload video to YouTube (as **Unlisted**) or Google Drive (set access to **Anyone with the link can view**).
- [x] Submit the video URL, Resume PDF, Report PDF, and ZIP archive through the FOSSEE Google Form.
