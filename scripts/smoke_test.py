
import json
import subprocess
import sys

from pathlib import Path
from tempfile import TemporaryDirectory


def main():
    if len(sys.argv) != 2:
        raise SystemExit(
            "Usage: smoke_test.py <path-to-task_app.py>"
        )

    app_path = Path(sys.argv[1]).resolve()

    if not app_path.is_file():
        raise SystemExit("Application file not found.")

    help_result = subprocess.run(
        [sys.executable, str(app_path), "--help"],
        capture_output=True,
        text=True
    )

    if help_result.returncode != 0:
        raise SystemExit(
            f"Help check failed: {help_result.stderr}"
        )

    with TemporaryDirectory() as temp:
        data_path = Path(temp) / "tasks.json"

        add_result = subprocess.run(
            [
                sys.executable,
                str(app_path),
                "add",
                "CI smoke test",
                "--file",
                str(data_path)
            ],
            capture_output=True,
            text=True
        )

        if add_result.returncode != 0:
            raise SystemExit(
                f"Task creation failed: {add_result.stderr}"
            )

        data = json.loads(
            data_path.read_text(encoding="utf-8")
        )

        expected = [
            {
                "title": "CI smoke test",
                "completed": False
            }
        ]

        if data != expected:
            raise SystemExit("Unexpected task data.")

    report = Path("deployment.txt")

    report.write_text(
        "Deployment smoke test: SUCCESS\n"
        "Environment: test/tasks\n"
        "--help: PASS\n"
        "Create task in temporary JSON file: PASS\n",
        encoding="utf-8"
    )

    print("Smoke test completed successfully.")
    print("deployment.txt created.")


if __name__ == "__main__":
    main()

