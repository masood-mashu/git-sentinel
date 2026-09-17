"""
secret_detector.py - Precision token, credential, and entropy scanner.
Pure Python 3.9+ without external dependencies.
"""
import json
import math
import re
import sys
from typing import Any, Dict, List

SECRET_SIGNATURES = [
    ("OpenAI API Key", r"sk-[a-zA-Z0-9]{20,}|sk-proj-[a-zA-Z0-9_-]{30,}", "CRITICAL"),
    ("GitHub Personal Access Token", r"gh[pousr]-[a-zA-Z0-9]{36,}", "CRITICAL"),
    ("AWS Access Key ID", r"(?:A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}", "CRITICAL"),
    ("AWS Secret Key", r"(?i)aws_secret_access_key\s*[:=]\s*['\"][a-zA-Z0-9/+=]{40}['\"]", "CRITICAL"),
    ("Slack Token", r"xox[baprs]-[0-9a-zA-Z]{10,48}", "HIGH"),
    ("Stripe Secret Key", r"sk_live_[0-9a-zA-Z]{24}", "CRITICAL"),
    ("RSA/OpenSSH Private Key", r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", "CRITICAL"),
    ("Generic Password/Secret Assignment", r"(?i)(?:api_key|secret_key|auth_token|password|passwd)\s*[:=]\s*['\"][^\s'\"]{10,}['\"]", "HIGH"),
    ("JSON Web Token (JWT)", r"eyJ[a-zA-Z0-9_-]{10,}\.eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}", "HIGH"),
]

def shannon_entropy(data: str) -> float:
    if not data:
        return 0.0
    entropy = 0.0
    for x in set(data):
        p_x = float(data.count(x)) / len(data)
        if p_x > 0:
            entropy += - p_x * math.log2(p_x)
    return entropy

def redact(val: str) -> str:
    if len(val) <= 8:
        return "***"
    return f"{val[:3]}...{val[-3:]}"

def detect_secrets(content: str, redact_output: bool = True) -> Dict[str, Any]:
    lines = content.splitlines()
    findings: List[Dict[str, Any]] = []

    for idx, line in enumerate(lines, start=1):
        for name, pattern, severity in SECRET_SIGNATURES:
            match = re.search(pattern, line)
            if match:
                raw_match = match.group(0)
                findings.append({
                    "type": name,
                    "line": idx,
                    "severity": severity,
                    "value": redact(raw_match) if redact_output else raw_match,
                    "entropy": round(shannon_entropy(raw_match), 2)
                })

    return {
        "secrets_found": findings,
        "clean": len(findings) == 0,
        "total_violations": len(findings)
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8", errors="ignore") as f:
            raw = f.read()
    else:
        raw = sys.stdin.read()
    print(json.dumps(detect_secrets(raw), indent=2))
