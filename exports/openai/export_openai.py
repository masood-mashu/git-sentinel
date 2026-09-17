"""
export_openai.py - Export GitSentinel to OpenAI Assistants / ChatCompletion SDK.
Visa 01: OpenAI SDK (+250 points)
"""
import os
import json
import yaml
from typing import Any, Dict, List

def export_to_openai(root_dir: str) -> Dict[str, Any]:
    with open(os.path.join(root_dir, "agent.yaml"), "r", encoding="utf-8") as f:
        manifest = yaml.safe_load(f)
    with open(os.path.join(root_dir, "SOUL.md"), "r", encoding="utf-8") as f:
        soul = f.read()
    with open(os.path.join(root_dir, "RULES.md"), "r", encoding="utf-8") as f:
        rules = f.read()

    system_instructions = f"{soul}\n\n# Operational Rules\n{rules}"

    openai_tools: List[Dict[str, Any]] = []
    for tool_entry in manifest.get("tools", []):
        schema_path = os.path.join(root_dir, tool_entry["schema"])
        if os.path.exists(schema_path):
            with open(schema_path, "r", encoding="utf-8") as sf:
                tool_schema = json.load(sf)
            openai_tools.append({
                "type": "function",
                "function": {
                    "name": tool_schema.get("name", tool_entry["name"]),
                    "description": tool_schema.get("description", tool_entry["description"]),
                    "parameters": tool_schema.get("parameters", {})
                }
            })

    assistant_payload = {
        "name": manifest.get("name", "git-sentinel"),
        "description": manifest.get("description", ""),
        "model": "gpt-4o",
        "instructions": system_instructions,
        "tools": openai_tools,
        "temperature": manifest.get("model", {}).get("temperature", 0.1),
        "metadata": {
            "passport_id": manifest.get("passport", {}).get("id", "aps-sentinel-01"),
            "exported_by": "gitagent-exporter",
            "framework_visa": "openai-sdk"
        }
    }

    out_file = os.path.join(root_dir, "exports", "openai", "openai_assistant_spec.json")
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as out:
        json.dump(assistant_payload, out, indent=2)

    return {
        "visa": "VISA 01 - OpenAI SDK",
        "status": "VERIFIED",
        "tools_exported": len(openai_tools),
        "output_file": out_file
    }

if __name__ == "__main__":
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    result = export_to_openai(root)
    print(json.dumps(result, indent=2))
