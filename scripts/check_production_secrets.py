from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

PLACEHOLDER_VALUES = {
    "change-me",
    "replace-me",
    "replace-with-backend-service-token",
    "replace-with-bot-token",
    "replace-with-random-webhook-secret",
    "long-random-token",
}

PLACEHOLDER_VARIABLES = {
    "SNABIX_BOT_TOKEN",
    "SNABIX_BACKEND_SERVICE_TOKEN",
    "SNABIX_BOT_WEBHOOK_SECRET",
}

MIN_RANDOM_LENGTH_VARIABLES = {
    "SNABIX_BACKEND_SERVICE_TOKEN",
    "SNABIX_BOT_WEBHOOK_SECRET",
}


def parse_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        if not key:
            continue

        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]

        values[key] = value

    return values


def find_unsafe_production_secrets(values: dict[str, str]) -> list[str]:
    findings: list[str] = []

    for variable in PLACEHOLDER_VARIABLES:
        value = values.get(variable)

        if value is None:
            continue

        if value == "":
            findings.append(f"{variable} is empty; production must use a generated value.")
            continue

        if value.lower() in PLACEHOLDER_VALUES:
            findings.append(f'{variable} uses unsafe placeholder "{value}".')

    for variable in MIN_RANDOM_LENGTH_VARIABLES:
        value = values.get(variable)

        if value is not None and value != "" and len(value) < 32:
            findings.append(f"{variable} is too short; use at least 32 random characters.")

    return findings


def run_self_test() -> int:
    unsafe_findings = find_unsafe_production_secrets(
        {
            "SNABIX_BOT_TOKEN": "replace-with-bot-token",
            "SNABIX_BACKEND_SERVICE_TOKEN": "replace-with-backend-service-token",
            "SNABIX_BOT_WEBHOOK_SECRET": "replace-with-random-webhook-secret",
        }
    )
    safe_findings = find_unsafe_production_secrets(
        {
            "SNABIX_BOT_TOKEN": "1234567890:telegram-token-from-botfather",
            "SNABIX_BACKEND_SERVICE_TOKEN": "a" * 64,
            "SNABIX_BOT_WEBHOOK_SECRET": "b" * 64,
        }
    )

    if not unsafe_findings or safe_findings:
        print("Production secret guard self-test failed.", file=sys.stderr)
        return 1

    print("Production secret guard self-test passed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Check production bot env for dev placeholders.")
    parser.add_argument("--env-file", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()

    env_file = args.env_file or os.environ.get("PRODUCTION_ENV_FILE")

    if env_file is None or str(env_file) == "":
        parser.error("--env-file is required unless --self-test is used")

    env_path = Path(env_file)
    findings = find_unsafe_production_secrets(parse_env_file(env_path))

    if findings:
        print(f"Unsafe production secrets found in {env_path}:", file=sys.stderr)

        for finding in findings:
            print(f"- {finding}", file=sys.stderr)

        return 1

    print(f"Production secrets check passed: {env_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
