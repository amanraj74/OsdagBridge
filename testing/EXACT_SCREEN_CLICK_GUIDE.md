# Exactly What to Click on Your Screen (Step-by-Step Visual Guide)
**For Aman Jaiswal (`amanraj74`) | FOSSEE Osdag Winter Internship 2026**

This guide matches **the exact screen you have open right now** in OsdagBridge. Follow these clicks one by one!

---

## 🧭 Overview of Your Screen

Look at the window on your screen:
1. **Top Menu**: `File`, `Graphics`, `Database`, `Help` (top left).
2. **Left Panel (Input Dock)**:
   - Green tab: `Basic Inputs`
   - White tab: `Additional Inputs`
   - Small **Lock Icon [🔓]**: Next to Additional Inputs (use this to Unlock).
   - Bottom-left: **`Save Input`** button.
   - Bottom-right: **`Design`** button (green with crossed tools icon ⚙️).
3. **Center/Right Canvas**: Shows the 2D bridge cross-section and top plan view.
4. **Top-Right Toolbar**: Contains view buttons: `C/R`, `TOP`, `[Isometric Cube]`, `[3D Solid Cube]`.
5. **Right Edge**: A vertical green bar labeled **`O U T P U T`**.

---

## 🎬 Exact Click-by-Click Action Plan (2 to 3 Minutes)

---

### STEP 1: Fill the Inputs (0:00 - 0:30)

You currently see **red boxes** around `Span` and `Carriageway Width` because they are empty. You have two very easy ways to fill them:

#### Option A: The Instant 2-Click Method (Recommended & Professional ⭐)
1. On the very top menu, click **`File`** $\longrightarrow$ click **`Load Input`** (or just press **`Ctrl + L`** on your keyboard).
2. A file selection window opens.
3. Browse to:
   ```text
   D:\my work\OsdagBridge\testing\osi_files
   ```
4. Double-click: **`TC01_Baseline_Standard_Design.osi`**.
5. **Watch the screen**: Instantly, `Span` fills with **`30.0`**, `Carriageway Width` fills with **`7.5`**, Location fills with **`Mumbai`**, and the red boxes disappear!

---

#### Option B: Or Type Manually
1. Click the box for **`Span (m)*`** $\longrightarrow$ Type `30`.
2. Click the box for **`Carriageway Width*`** $\longrightarrow$ Type `7.5`.
3. Click the green button **`Select Location`** $\longrightarrow$ Choose State: `Maharashtra`, District: `Mumbai` $\longrightarrow$ Click **`Save`** at the bottom of the popup.

---

### STEP 2: Run the Design & View 3D CAD (0:30 - 1:15)

1. **Click the green `Design` button** (bottom-right of the left panel, with the crossed tools icon).
2. Look at the bottom of the screen: The progress bar will fill up as it runs OpenSees analysis and section checks.
3. When it finishes:
   - Look at the **top-right toolbar** (near the minimize/maximize buttons).
   - Click the **3D Solid Cube icon** (4th button in that group, labeled *"Toggle 3D CAD View"*).
   - The center canvas switches to the **3D OpenCASCADE Model**!
   - **Click and hold the left mouse button, then drag slowly**: Rotate the 3D bridge in the air so the reviewer sees all 4 steel plate girders, stiffeners, and concrete deck in 3D!
4. **Open the Output Dock**:
   - Look at the far right edge of your screen.
   - Click the vertical strip that says **`O U T P U T`**.
   - The Output Dock slides open, showing the design numbers:
     * Flexure: `19.8%`
     * Shear: `39.9%`
     * Fatigue: `157.3%`
   - Point your mouse at these numbers for 3 seconds.

---

### STEP 3: Show Bug 1 (The Deck Concrete Dialog Anomaly) (1:15 - 1:55)

1. Look at the top of the left panel:
   - Click the small **Lock Icon [🔓]** button (right next to the `Additional Inputs` tab) to unlock the fields.
2. In the left panel, scroll down past *Superstructure* until you see the section **`Material Inputs`**.
3. Look at the field **`Deck Concrete Grade`** (it currently shows `M 35`).
4. **Right next to the `M 35` dropdown, click the small circular info icon `(ℹ)`**:
   - **A popup window opens!**
   - **Look at the popup title**: It says **`Steel Material Properties`**!
   - It shows Yield Strength ($F_y$) and Ultimate Strength ($F_u$) instead of Concrete Compressive Strength ($f_{ck}$)!
   - **Move your mouse in a circle around this popup title** for 3–4 seconds to show the reviewer this clear bug!
5. Click **Cancel** or the **`X`** to close that popup.

---

### STEP 4: Explain Bug 2 (Consecutive Run Stability / Issue #135) (1:55 - 2:30)

1. With the model still unlocked, click the green **`Design`** button again (Run 2).
2. Point out:
   - *"In previous versions, running Design a second time divided the girder dimensions by 1000 in-place ($1670\text{ mm} \to 1.67\text{ m} \to 1.67\text{ mm}$), causing negative web depth and crashing with `math domain error` (GitHub Issue #135)."*
   - *"With our snapshot-and-restore contract, dimensions remain strictly stable at $1.670\text{ m}$ across Run 1, Run 2, and Run 3."*

---

### STEP 5: Show the Test Files & Report PDF (2:30 - 3:00)

1. Minimize or switch away from OsdagBridge to **File Explorer** or **VS Code**:
   - Show the folder: `D:\my work\OsdagBridge\testing`
   - Point to:
     * `run_tests.py` (the test script)
     * `osi_files/` (the 8 project models)
     * `dictionaries/` (input/output JSON data)
2. Double-click and open: **`OsdagBridge_Testing_Report.pdf`**
   - Show the cover page with Candidate Name: **Aman Jaiswal** (`amanraj74`).
   - Scroll down to show **Table 1** (the 8 test scenarios matrix) and the CAD screenshots on pages 9–10.
3. Conclude the video:
   - *"All deliverables are compiled into `OsdagBridge_Testing_Submission.zip` and pushed to my GitHub fork. Thank you!"*
4. Press **`Win + Alt + R`** to stop recording!

---

## 🎯 Quick Cheat-Sheet (Print or Keep on Phone)

```text
1. Ctrl + L  --->  Open TC01_Baseline_Standard_Design.osi  (inputs auto-fill!)
2. Click [Design] (bottom right)  --->  Solves in 5 seconds
3. Click [3D Cube] (top right)    --->  Rotate 3D model with mouse
4. Click [O U T P U T] (far right)--->  Show 19.8% & 39.9%
5. Click [Lock icon] (top left)   --->  Unlock
6. Scroll down to "Deck Concrete Grade"  --->  Click (ℹ) button (shows Steel bug!)
7. Switch to PDF Report           --->  Scroll 14-page document & conclude!
```
