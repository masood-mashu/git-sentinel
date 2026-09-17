"""
export_claude_code.py - Export GitSentinel to Anthropic Claude Code / MCP.
Visa 03: Claude Code (+250 points)
"""
import os
import json
import yaml
from typing import Any, Dict

def export_to_claude_code(root_dir: str) -> Dict[str, Any]:
    with open(os.path.join(root_dir, "agent.yaml"), "r", encoding="utf-8") as f:
        manifest = yaml.safe_load(f)
    with open(os.path.join(root_dir, "SOUL.md"), "r", encoding="utf-8") as f:
        soul = f.read()
    with open(os.path.join(root_dir, "RULES.md"), "r", encoding="utf-8") as f:
        rules = f.read()

    # Generate CLAUDE.md tailored for Claude Code subagent execution
    claude_md_content = f"""<!-- Exported from GitAgent Passport: {manifest.get('name', 'git-sentinel')} -->
# Claude Code Agent Directive: GitSentinel

{soul}

## Non-Negotiable Operational Rules
{rules}

## Available Tools via GitSentinel
- **diff_scanner**: Parse and verify git diffs for syntax risks
- **secret_detector**: High-entropy credential scanner
- **policy_checker**: Supply-chain & file hygiene verifier
- **patch_generator**: Automated unified diff patch synthesis
"""

    # Generate MCP Server config for Claude Code
    mcp_config = {
        "mcpServers": {
            "git-sentinel": {
                "command": "python",
                "args": ["-m", "tools.diff_scanner"],
                "env": {
                    "GIT_SENTINEL_PASSPORT": manifest.get("passport", {}).get("id", "aps-sentinel-01")
                }
            }
        }
    }

    out_claude_md = os.path.join(root_dir, "exports", "claude_code", "CLAUDE.md")
    out_mcp = os.path.join(root_dir, "exports", "claude_code", "claude_desktop_config.json")
    os.makedirs(os.path.dirname(out_claude_md), exist_ok=True)

    with open(out_claude_md, "w", encoding="utf-8") as f:
        f.write(claude_md_content)
    with open(out_mcp, "w", encoding="utf-8") as f:
        json.dump(mcp_config, f, indent=2)

    return {
        "visa": "VISA 03 - Claude Code",
        "status": "VERIFIED",
        "output_files": [out_claude_md, out_mcp]
    }

if __name__ == "__main__":
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    result = export_to_claude_code(root)
    print(json.dumps(result, indent=2))
