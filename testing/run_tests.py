"""
OsdagBridge Automated Testing Suite
For FOSSEE Osdag Winter Internship 2026 Screening Task:
OsdagBridge Software Testing & Issue Reporting

Author: FOSSEE Osdag Candidate
Target: OsdagBridge dev branch
"""

import os
import sys
import json
import yaml
import time
import math
import traceback
import types
from pathlib import Path

# Set up paths
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = WORKSPACE_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

import osdagbridge.core.utils.common as comm
from osdagbridge.core.bridge_types.plate_girder.defaults import (
    BASIC_INPUT_DICT,
    solve_extend_basic_input_dict,
)
from osdagbridge.core.bridge_types.plate_girder.plategirderbridge import PlateGirderBridge
from osdagbridge.core.utils.osi_validator import validate_osi_inputs

OUTPUT_DIR = WORKSPACE_ROOT / "testing"
OSI_DIR = OUTPUT_DIR / "osi_files"
DICT_DIR = OUTPUT_DIR / "dictionaries"
LOG_DIR = OUTPUT_DIR / "logs"

for d in (OSI_DIR, DICT_DIR, LOG_DIR):
    d.mkdir(parents=True, exist_ok=True)


def to_serializable(val):
    """Recursively convert data structures to JSON-serializable types."""
    if isinstance(val, (types.MappingProxyType, dict)):
        return {str(k): to_serializable(v) for k, v in val.items()}
    elif isinstance(val, (list, tuple, set)):
        return [to_serializable(v) for v in val]
    elif hasattr(val, "__dict__"):
        return {str(k): to_serializable(v) for k, v in val.__dict__.items() if not str(k).startswith("_")}
    elif isinstance(val, (int, float, str, bool)) or val is None:
        if isinstance(val, float) and (math.isnan(val) or math.isinf(val)):
            return str(val)
        return val
    else:
        return str(val)


def save_osi(filepath: Path, input_dict: dict):
    """Save input dictionary as an .osi (YAML) file."""
    clean_dict = to_serializable(input_dict)
    with open(filepath, "w", encoding="utf-8") as f:
        yaml.dump(clean_dict, f, default_flow_style=False, sort_keys=False)


def run_test_case(tc_id: str, tc_name: str, overrides: dict, notes: str = "", multi_run_runs: int = 1):
    """
    Execute a single test case scenario and capture full results.
    """
    print(f"\n=======================================================")
    print(f"Executing {tc_id}: {tc_name}")
    print(f"Notes: {notes}")
    print(f"=======================================================")

    log_file = LOG_DIR / f"{tc_id}_{tc_name.replace(' ', '_')}.log"
    osi_file = OSI_DIR / f"{tc_id}_{tc_name.replace(' ', '_')}.osi"
    in_dict_file = DICT_DIR / f"{tc_id}_input_dict.json"
    out_dict_file = DICT_DIR / f"{tc_id}_output_dict.json"

    # Start with fresh default dictionary
    inp = dict(BASIC_INPUT_DICT)

    # Standard bridge required inputs
    inp[comm.KEY_SPAN] = 30.0
    inp[comm.KEY_CARRIAGEWAY_WIDTH] = 7.5
    inp[comm.KEY_PROJECT_LOCATION] = "Mumbai"
    inp[comm.KEY_FOOTPATH] = "None"
    inp[comm.KEY_INCLUDE_MEDIAN] = "No"
    inp[comm.KEY_SKEW_ANGLE] = 0.0
    inp[comm.KEY_DESIGN_MODE] = "Optimized"

    # Elasticity and material baseline
    inp[comm.KEY_MATERIAL_GIRDER_G] = 76.9
    inp[comm.KEY_MATERIAL_DECK_FCK] = 35.0
    inp[comm.KEY_MATERIAL_DECK_FCTM] = 2.8
    inp[comm.KEY_MATERIAL_DECK_ECM] = 32.0

    # Apply scenario overrides
    for k, v in overrides.items():
        inp[k] = v

    # Extend inputs
    solve_extend_basic_input_dict(inp)

    # Save initial OSI and input dictionary
    save_osi(osi_file, inp)
    with open(in_dict_file, "w", encoding="utf-8") as f:
        json.dump(to_serializable(inp), f, indent=2)

    val_res = validate_osi_inputs(inp)
    print(f"OSI Validation: valid={val_res.is_valid}, errors={val_res.errors}")

    results_summary = {
        "tc_id": tc_id,
        "tc_name": tc_name,
        "notes": notes,
        "osi_file": str(osi_file),
        "osi_valid": val_res.is_valid,
        "status": "UNKNOWN",
        "runs": []
    }

    bridge = PlateGirderBridge()
    bridge.set_input(inp)

    run_count = multi_run_runs
    for r in range(run_count):
        run_info = {"run_index": r + 1}
        print(f"\n--- Run {r + 1} of {run_count} ---")
        t0 = time.time()
        try:
            # Check girder depth before conversion
            depth_before = bridge.input_dict.get(comm.KEY_MP_GIRDER_DEPTH)
            run_info["girder_depth_before"] = depth_before
            print(f"Girder depth in input_dict before design(): {depth_before}")

            bridge.design()
            elapsed = time.time() - t0
            run_info["elapsed_seconds"] = round(elapsed, 2)
            run_info["success"] = True

            depth_after = bridge.input_dict.get(comm.KEY_MP_GIRDER_DEPTH)
            run_info["girder_depth_after"] = depth_after
            print(f"Design completed in {elapsed:.2f}s. Depth after design(): {depth_after}")

            # Capture key outputs
            out = dict(bridge.output_dict)
            run_info["output_keys_count"] = len(out)
            
            # Extract key engineering results
            dr = getattr(bridge, "design_results", {}) or {}
            run_info["max_dcr"] = dr.get("max_dcr")
            run_info["util_flexure"] = out.get(getattr(comm, "KEY_UTIL_FLEXURE", "util.flexure"))
            run_info["util_shear"] = out.get(getattr(comm, "KEY_UTIL_SHEAR", "util.shear"))
            run_info["util_ltb"] = out.get(getattr(comm, "KEY_UTIL_LTB", "util.ltb"))
            run_info["util_fatigue"] = out.get(getattr(comm, "KEY_UTIL_FATIGUE", "util.fatigue"))
            run_info["util_deflection"] = out.get(getattr(comm, "KEY_UTIL_DEFLECTION_CRACK", "util.deflection_crack"))
            run_info["deck_verdict"] = out.get("deck_design_verdict", "PASS")

            # Check CAD DTO
            try:
                cad_params = bridge.get_3d_cad_parameters()
                run_info["cad_params_generated"] = cad_params is not None
                run_info["cad_num_girders"] = getattr(cad_params, "num_girders", None)
            except Exception as ce:
                run_info["cad_params_generated"] = False
                run_info["cad_error"] = str(ce)

            # Dump output dictionary on first successful run
            if r == 0:
                with open(out_dict_file, "w", encoding="utf-8") as f:
                    json.dump(to_serializable(out), f, indent=2)

        except Exception as e:
            elapsed = time.time() - t0
            run_info["elapsed_seconds"] = round(elapsed, 2)
            run_info["success"] = False
            run_info["error_type"] = type(e).__name__
            run_info["error_message"] = str(e)
            run_info["traceback"] = traceback.format_exc()
            print(f"Run {r + 1} FAILED with {type(e).__name__}: {e}")

        results_summary["runs"].append(run_info)

        # If consecutive runs, modify parameter for subsequent run (e.g. span)
        if r + 1 < run_count:
            current_span = float(bridge.input_dict.get(comm.KEY_SPAN, 30.0))
            new_span = current_span + 2.0
            print(f"Simulating GUI unlock: updating span from {current_span} to {new_span}...")
            # Note: in real UI, input_dict retains mutated state unless re-primed!
            bridge.input_dict[comm.KEY_SPAN] = new_span
            solve_extend_basic_input_dict(bridge.input_dict)

    all_success = all(r["success"] for r in results_summary["runs"])
    results_summary["status"] = "PASS" if all_success else "FAIL"

    # Write summary log
    with open(log_file, "w", encoding="utf-8") as lf:
        json.dump(results_summary, lf, indent=2)

    return results_summary


def run_all_tests():
    print("================================================================================")
    print("STARTING OSDAGBRIDGE COMPREHENSIVE TEST SUITE EXECUTION")
    print("================================================================================")

    test_matrix = [
        # TC01: Baseline standard design
        {
            "id": "TC01",
            "name": "Baseline Standard Design",
            "overrides": {
                comm.KEY_SPAN: 30.0,
                comm.KEY_CARRIAGEWAY_WIDTH: 7.5,
                comm.KEY_PROJECT_LOCATION: "Mumbai",
                comm.KEY_SKEW_ANGLE: 0.0,
                comm.KEY_GIRDER: "E 350A",
                comm.KEY_DECK_CONCRETE_GRADE_BASIC: "M 35",
                comm.KEY_DESIGN_MODE: "Optimized",
            },
            "notes": "Standard 2-lane bridge with default IRC loading and optimized plate sizing.",
            "runs": 1,
        },
        # TC02: Short span boundary
        {
            "id": "TC02",
            "name": "Short Span Boundary",
            "overrides": {
                comm.KEY_SPAN: 20.0,
                comm.KEY_CARRIAGEWAY_WIDTH: 4.25,
                comm.KEY_PROJECT_LOCATION: "Delhi",
                comm.KEY_SKEW_ANGLE: 0.0,
                comm.KEY_GIRDER: "E 250A",
                comm.KEY_DECK_CONCRETE_GRADE_BASIC: "M 25",
                comm.KEY_MATERIAL_DECK_FCK: 25.0,
                comm.KEY_MATERIAL_DECK_FCTM: 2.2,
                comm.KEY_MATERIAL_DECK_ECM: 30.0,
                comm.KEY_DESIGN_MODE: "Optimized",
            },
            "notes": "Single-lane 20m bridge testing lower geometric boundary and E 250A/M 25.",
            "runs": 1,
        },
        # TC03: Long span boundary
        {
            "id": "TC03",
            "name": "Long Span Boundary",
            "overrides": {
                comm.KEY_SPAN: 40.0,
                comm.KEY_CARRIAGEWAY_WIDTH: 10.5,
                comm.KEY_PROJECT_LOCATION: "Kolkata",
                comm.KEY_SKEW_ANGLE: 0.0,
                comm.KEY_GIRDER: "E 410A",
                comm.KEY_DECK_CONCRETE_GRADE_BASIC: "M 40",
                comm.KEY_MATERIAL_DECK_FCK: 40.0,
                comm.KEY_MATERIAL_DECK_FCTM: 3.1,
                comm.KEY_MATERIAL_DECK_ECM: 34.0,
                comm.KEY_DESIGN_MODE: "Optimized",
            },
            "notes": "3-lane 40m bridge testing upper span range and heavy traffic multi-lane loading.",
            "runs": 1,
        },
        # TC04: Positive skew angle
        {
            "id": "TC04",
            "name": "Positive Skew Geometry",
            "overrides": {
                comm.KEY_SPAN: 30.0,
                comm.KEY_CARRIAGEWAY_WIDTH: 7.5,
                comm.KEY_PROJECT_LOCATION: "Chennai",
                comm.KEY_SKEW_ANGLE: 15.0,
                comm.KEY_GIRDER: "E 350A",
                comm.KEY_DECK_CONCRETE_GRADE_BASIC: "M 35",
                comm.KEY_DESIGN_MODE: "Optimized",
            },
            "notes": "Bridge with +15 deg skew to evaluate transverse grillage and support distortion.",
            "runs": 1,
        },
        # TC05: Negative skew angle
        {
            "id": "TC05",
            "name": "Negative Skew Geometry",
            "overrides": {
                comm.KEY_SPAN: 30.0,
                comm.KEY_CARRIAGEWAY_WIDTH: 7.5,
                comm.KEY_PROJECT_LOCATION: "Chennai",
                comm.KEY_SKEW_ANGLE: -15.0,
                comm.KEY_GIRDER: "E 350A",
                comm.KEY_DECK_CONCRETE_GRADE_BASIC: "M 35",
                comm.KEY_DESIGN_MODE: "Optimized",
            },
            "notes": "Bridge with -15 deg skew to check mirror symmetry against TC04.",
            "runs": 1,
        },
        # TC06: Custom material input
        {
            "id": "TC06",
            "name": "Custom Material Properties",
            "overrides": {
                comm.KEY_SPAN: 30.0,
                comm.KEY_CARRIAGEWAY_WIDTH: 7.5,
                comm.KEY_PROJECT_LOCATION: "Mumbai",
                comm.KEY_SKEW_ANGLE: 0.0,
                comm.KEY_GIRDER: "custom_steel_6",
                comm.KEY_MATERIAL_GIRDER_FY: 360.0,
                comm.KEY_MATERIAL_GIRDER_FU: 500.0,
                comm.KEY_MATERIAL_GIRDER_E: 205.0,
                comm.KEY_MATERIAL_GIRDER_G: 78.8,
                comm.KEY_MATERIAL_GIRDER_POISSON: 0.30,
                comm.KEY_MATERIAL_GIRDER_DENSITY: 80.0,
                comm.KEY_DECK_CONCRETE_GRADE_BASIC: "custom_concrete_6",
                comm.KEY_MATERIAL_DECK_FCK: 40.0,
                comm.KEY_MATERIAL_DECK_FCTM: 3.1,
                comm.KEY_MATERIAL_DECK_ECM: 34.0,
                comm.KEY_MATERIAL_DECK_DENSITY: 26.0,
                comm.KEY_DESIGN_MODE: "Optimized",
            },
            "notes": "Explicit custom steel (Fy=360) and concrete (fck=40) testing retention and density bypass.",
            "runs": 1,
        },
        # TC07: Multi-Run Consecutive Design Sequence
        {
            "id": "TC07",
            "name": "Consecutive Multi-Run Stability",
            "overrides": {
                comm.KEY_SPAN: 30.0,
                comm.KEY_CARRIAGEWAY_WIDTH: 7.5,
                comm.KEY_PROJECT_LOCATION: "Mumbai",
                comm.KEY_SKEW_ANGLE: 0.0,
                comm.KEY_GIRDER: "E 350A",
                comm.KEY_DECK_CONCRETE_GRADE_BASIC: "M 35",
                comm.KEY_DESIGN_MODE: "Optimized",
            },
            "notes": "3 consecutive design runs on the same bridge object to evaluate state persistence and unit division bug.",
            "runs": 3,
        },
        # TC08: Custom Sizing Mode
        {
            "id": "TC08",
            "name": "Custom Sizing Mode",
            "overrides": {
                comm.KEY_SPAN: 30.0,
                comm.KEY_CARRIAGEWAY_WIDTH: 7.5,
                comm.KEY_PROJECT_LOCATION: "Mumbai",
                comm.KEY_SKEW_ANGLE: 0.0,
                comm.KEY_GIRDER: "E 350A",
                comm.KEY_DECK_CONCRETE_GRADE_BASIC: "M 35",
                comm.KEY_DESIGN_MODE: "Custom",
                comm.KEY_MP_GIRDER_DEPTH: 1800.0,
                comm.KEY_MP_GIRDER_WEB_DEPTH: 1740.0,
                comm.KEY_MP_GIRDER_WEB_THICKNESS: 14.0,
                comm.KEY_MP_GIRDER_TOP_FLANGE_WIDTH: 550.0,
                comm.KEY_MP_GIRDER_TOP_FLANGE_THICKNESS: 30.0,
                comm.KEY_MP_GIRDER_BOTTOM_FLANGE_WIDTH: 550.0,
                comm.KEY_MP_GIRDER_BOTTOM_FLANGE_THICKNESS: 30.0,
            },
            "notes": "Custom Mode evaluating user-specified plate dimensions without auto-optimization.",
            "runs": 1,
        },
    ]

    suite_results = []
    for tc in test_matrix:
        res = run_test_case(
            tc_id=tc["id"],
            tc_name=tc["name"],
            overrides=tc["overrides"],
            notes=tc["notes"],
            multi_run_runs=tc["runs"]
        )
        suite_results.append(res)

    suite_summary_file = OUTPUT_DIR / "test_suite_summary.json"
    with open(suite_summary_file, "w", encoding="utf-8") as f:
        json.dump(suite_results, f, indent=2)

    print("\n================================================================================")
    print("TEST SUITE EXECUTION COMPLETE")
    print(f"Summary written to: {suite_summary_file}")
    print("================================================================================")


if __name__ == "__main__":
    run_all_tests()
