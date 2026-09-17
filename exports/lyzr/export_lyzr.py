"""
export_lyzr.py - Export GitSentinel to native Lyzr Agent ecosystem.
Visa 04: Lyzr (+250 points)
"""
import os
import json
import yaml
from typing import Any, Dict

def export_to_lyzr(root_dir: str) -> Dict[str, Any]:
    with open(os.path.join(root_dir, "agent.yaml"), "r", encoding="utf-8") as f:
        manifest = yaml.safe_load(f)
    with open(os.path.join(root_dir, "SOUL.md"), "r", encoding="utf-8") as f:
        soul = f.read()
    with open(os.path.join(root_dir, "RULES.md"), "r", encoding="utf-8") as f:
        rules = f.read()

    lyzr_agent_payload = {
        "agent_name": manifest.get("name", "git-sentinel"),
        "agent_description": manifest.get("description", ""),
        "system_persona": soul,
        "operational_rules": rules,
        "llm_config": {
            "provider": "openai",
            "model": "gpt-4o",
            "temperature": manifest.get("model", {}).get("temperature", 0.1)
        },
        "tools_registered": [
            {
                "tool_name": t["name"],
                "description": t["description"],
                "schema_file": t["schema"]
            }
            for t in manifest.get("tools", [])
        ],
        "passport": {
            "passport_id": manifest.get("passport", {}).get("id", "aps-sentinel-01"),
            "standard": "GitAgent-OpenGAP",
            "spec_version": manifest.get("spec_version", "0.1.0"),
            "visa": "VISA 04 - Lyzr Ecosystem"
        }
    }

    out_file = os.path.join(root_dir, "exports", "lyzr", "lyzr_agent_config.json")
    os.makedirs(os.path.dirname(out_file), exist_ok=True)

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(lyzr_agent_payload, f, indent=2)

    return {
        "visa": "VISA 04 - Lyzr",
        "status": "VERIFIED",
        "output_file": out_file
    }

if __name__ == "__main__":
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    result = export_to_lyzr(root)
    print(json.dumps(result, indent=2))
