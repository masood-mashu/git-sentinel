"""
run_all_exports.py - Master exporter and Foundation Visa verification harness.
Generates all 4 framework exports and validates cross-framework portability.
Target: Checkpoint 03 (Export) -> 1,000 Points (250 pts x 4 Visas)
"""
import os
import sys
import json
import importlib.util

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def load_module_from_file(module_name: str, file_path: str):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {file_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    exports_dir = os.path.join(root_dir, "exports")

    print("=" * 68)
    print("GITAGENT PASSPORT CHALLENGE: FOUNDATION VISA VALIDATOR")
    print("=" * 68)

    results = []
    total_points = 0

    # 1. Visa 01 - OpenAI SDK
    try:
        mod = load_module_from_file("export_openai_mod", os.path.join(exports_dir, "openai", "export_openai.py"))
        r1 = mod.export_to_openai(root_dir)
        print("[GRANTED] VISA 01: OpenAI SDK Export (+250 Points)")
        print(f"   -> Spec: {os.path.relpath(r1['output_file'], root_dir)}")
        total_points += 250
        results.append(r1)
    except Exception as e:
        print(f"[FAILED] VISA 01: OpenAI SDK - {e}")

    # 2. Visa 02 - CrewAI
    try:
        mod = load_module_from_file("export_crewai_mod", os.path.join(exports_dir, "crewai", "export_crewai.py"))
        r2 = mod.export_to_crewai(root_dir)
        print("[GRANTED] VISA 02: CrewAI Framework Export (+250 Points)")
        for f in r2["output_files"]:
            print(f"   -> Spec: {os.path.relpath(f, root_dir)}")
        total_points += 250
        results.append(r2)
    except Exception as e:
        print(f"[FAILED] VISA 02: CrewAI - {e}")

    # 3. Visa 03 - Claude Code
    try:
        mod = load_module_from_file("export_claude_mod", os.path.join(exports_dir, "claude_code", "export_claude_code.py"))
        r3 = mod.export_to_claude_code(root_dir)
        print("[GRANTED] VISA 03: Anthropic Claude Code / MCP (+250 Points)")
        for f in r3["output_files"]:
            print(f"   -> Spec: {os.path.relpath(f, root_dir)}")
        total_points += 250
        results.append(r3)
    except Exception as e:
        print(f"[FAILED] VISA 03: Claude Code - {e}")

    # 4. Visa 04 - Lyzr
    try:
        mod = load_module_from_file("export_lyzr_mod", os.path.join(exports_dir, "lyzr", "export_lyzr.py"))
        r4 = mod.export_to_lyzr(root_dir)
        print("[GRANTED] VISA 04: Native Lyzr Ecosystem (+250 Points)")
        print(f"   -> Spec: {os.path.relpath(r4['output_file'], root_dir)}")
        total_points += 250
        results.append(r4)
    except Exception as e:
        print(f"[FAILED] VISA 04: Lyzr - {e}")

    print("=" * 68)
    print(f"PASSPORT STATUS: {len(results)}/4 VISAS ISSUED | +{total_points} VISA POINTS")
    print("=" * 68)

    report_path = os.path.join(exports_dir, "visa_manifest.json")
    with open(report_path, "w", encoding="utf-8") as rf:
        json.dump({
            "passport_id": "aps-sentinel-01",
            "agent_name": "git-sentinel",
            "visas_earned": len(results),
            "total_visa_points": total_points,
            "visas": results
        }, rf, indent=2)

if __name__ == "__main__":
    main()
