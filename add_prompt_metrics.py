#!/usr/bin/env python3
import re
from pathlib import Path

import yaml


def count_tokens(text: str) -> int:
    # Approximate tokenization: split on whitespace and punctuation boundaries.
    return len(re.findall(r"\w+|[^\w\s]", text, flags=re.UNICODE))


def compute_metrics(text: str) -> dict:
    total_chars = max(len(text), 1)
    non_ws_chars = sum(1 for c in text if not c.isspace())
    lines = text.splitlines() or [""]

    tokens = count_tokens(text)

    return {
        "prompt_line": len(lines),
        "prompt_density": round(non_ws_chars / total_chars, 6),
        "prompt_token_density": round(tokens / total_chars, 6),
    }


def main() -> None:
    cwd = Path.cwd()
    prompt_path = cwd / "prompt.md"
    tests_path = cwd / "redteam-tests.yml"
    output_path = cwd / "prompt_metrics.json"

    prompt_template = prompt_path.read_text()
    data = yaml.safe_load(tests_path.read_text())

    metrics_list = []
    tests = data.get("tests", [])
    for idx, test in enumerate(tests):
        vars_ = test.get("vars", {})
        user_input = vars_.get("user_input", "")
        full_prompt = prompt_template.replace("{{user_input}}", str(user_input))
        metrics = compute_metrics(full_prompt)

        metrics_list.append(
            {
                "index": idx,
                "description": test.get("description"),
                "user_input": user_input,
                **metrics,
            }
        )

    output_path.write_text(
        yaml.safe_dump(metrics_list, sort_keys=False)
    )
    print(f"Wrote metrics for {len(tests)} tests to {output_path}.")


if __name__ == "__main__":
    main()
