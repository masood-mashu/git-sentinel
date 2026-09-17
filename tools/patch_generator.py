"""
patch_generator.py - Generates git-compatible unified diff patches.
Pure Python 3.9+ without external dependencies.
"""
import json
import sys
from typing import Any, Dict

def generate_unified_patch(file_path: str, original_snippet: str, remediated_snippet: str) -> Dict[str, Any]:
    orig_lines = original_snippet.strip().splitlines()
    rem_lines = remediated_snippet.strip().splitlines()

    orig_block = "\n".join(f"-{line}" for line in orig_lines)
    rem_block = "\n".join(f"+{line}" for line in rem_lines)

    patch = f"""diff --git a/{file_path} b/{file_path}
--- a/{file_path}
+++ b/{file_path}
@@ -1,{len(orig_lines)} +1,{len(rem_lines)} @@
{orig_block}
{rem_block}
"""
    return {
        "file_path": file_path,
        "unified_diff": patch.strip() + "\n",
        "git_apply_ready": True
    }

if __name__ == "__main__":
    example = generate_unified_patch(
        "src/config.py",
        "api_key = 'sk-proj-live-secret-key-12345'",
        "api_key = os.getenv('OPENAI_API_KEY')"
    )
    print(json.dumps(example, indent=2))
