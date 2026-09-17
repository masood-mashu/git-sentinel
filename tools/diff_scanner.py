"""
diff_scanner.py - Core diff and syntax risk analyzer for GitSentinel.
Compatible with pure Python 3.9+ without external dependencies.
"""
import json
import re
import sys
from typing import Any, Dict, List

RISKY_PATTERNS = [
    (r"eval\s*\(", "Dangerous eval() execution detected"),
    (r"exec\s*\(", "Dangerous exec() execution detected"),
    (r"subprocess\.Popen\(.*shell\s*=\s*True", "Shell command injection risk with shell=True"),
    (r"os\.system\s*\(", "Potentially unsafe os.system() execution"),
    (r"innerHTML\s*=", "Potential Cross-Site Scripting (XSS) via innerHTML assignment"),
    (r"SELECT\s+.*\s+FROM\s+.*WHERE\s+.*['\"]\s*\+", "Raw SQL string concatenation (SQL Injection risk)"),
    (r"disable_web_security", "Chrome/Electron web security disabled flag"),
    (r"verify\s*=\s*False", "Disabled SSL/TLS certificate verification"),
]

def scan_diff(diff_text: str, max_lines: int = 1000) -> Dict[str, Any]:
    lines = diff_text.splitlines()[:max_lines]
    current_file = "unknown"
    files_changed: List[str] = []
    additions = 0
    deletions = 0
    suspicious: List[Dict[str, Any]] = []
    line_number = 0

    for line in lines:
        if line.startswith("diff --git"):
            parts = line.split(" ")
            if len(parts) >= 4:
                current_file = parts[3].lstrip("b/")
                if current_file not in files_changed:
                    files_changed.append(current_file)
        elif line.startswith("+++ b/"):
            current_file = line[6:].strip()
            if current_file not in files_changed:
                files_changed.append(current_file)
        elif line.startswith("@@"):
            match = re.search(r"\+(\d+)", line)
            if match:
                line_number = int(match.group(1)) - 1
        elif line.startswith("+") and not line.startswith("+++"):
            additions += 1
            line_number += 1
            content = line[1:]
            for pattern, issue in RISKY_PATTERNS:
                if re.search(pattern, content, re.IGNORECASE):
                    suspicious.append({
                        "file": current_file,
                        "line": line_number,
                        "issue": issue,
                        "snippet": content.strip()[:120]
                    })
        elif line.startswith("-") and not line.startswith("---"):
            deletions += 1
        else:
            line_number += 1

    return {
        "files_changed": files_changed,
        "additions_count": additions,
        "deletions_count": deletions,
        "suspicious_patterns": suspicious,
        "clean": len(suspicious) == 0
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8", errors="ignore") as f:
            raw = f.read()
    else:
        raw = sys.stdin.read()
    result = scan_diff(raw)
    print(json.dumps(result, indent=2))
