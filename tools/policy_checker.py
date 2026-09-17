"""
policy_checker.py - Compliance and supply-chain hygiene policy checker.
Pure Python 3.9+ without external dependencies.
"""
import json
import re
import sys
from typing import Any, Dict, List, Optional

FORBIDDEN_FILES = [
    r"^\.env(?:\..*)?$",
    r".*\.pem$",
    r".*\.key$",
    r"id_rsa(?:\.pub)?$",
    r"credentials\.json$",
    r"service-account.*\.json$",
]

def check_policies(
    repo_files: List[str],
    package_json_str: Optional[str] = None,
    requirements_txt_str: Optional[str] = None
) -> Dict[str, Any]:
    violations: List[Dict[str, Any]] = []

    # 1. Check for forbidden file commits
    for f in repo_files:
        clean_name = f.replace("\\", "/").split("/")[-1]
        for pattern in FORBIDDEN_FILES:
            if re.match(pattern, clean_name, re.IGNORECASE):
                violations.append({
                    "policy": "no-sensitive-files",
                    "status": "FAIL",
                    "details": f"Sensitive file committed: {f}"
                })

    # 2. Check package.json for unpinned dependencies
    if package_json_str:
        try:
            pkg = json.loads(package_json_str)
            for dep_type in ["dependencies", "devDependencies"]:
                for dep, ver in pkg.get(dep_type, {}).items():
                    if ver in ["*", "latest"] or ver.startswith(">"):
                        violations.append({
                            "policy": "pinned-dependencies",
                            "status": "WARN",
                            "details": f"Unpinned version for {dep}: '{ver}' (use exact semver)"
                        })
        except Exception as e:
            violations.append({
                "policy": "valid-manifest-json",
                "status": "FAIL",
                "details": f"Failed to parse package.json: {str(e)}"
            })

    # 3. Check requirements.txt for unpinned packages
    if requirements_txt_str:
        for idx, line in enumerate(requirements_txt_str.splitlines(), start=1):
            line = line.strip()
            if line and not line.startswith("#"):
                if "==" not in line and not line.startswith("-r"):
                    violations.append({
                        "policy": "pinned-dependencies",
                        "status": "WARN",
                        "details": f"Unpinned python dependency on line {idx}: '{line}'"
                    })

    return {
        "violations": violations,
        "passed": len([v for v in violations if v["status"] == "FAIL"]) == 0,
        "warnings_count": len([v for v in violations if v["status"] == "WARN"])
    }

if __name__ == "__main__":
    test_files = ["src/index.js", ".env", "package.json"]
    print(json.dumps(check_policies(test_files), indent=2))
