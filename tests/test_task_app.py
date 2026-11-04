
import io
import tempfile
import unittest

from contextlib import redirect_stdout
from pathlib import Path

from task_app import (
    add_task,
    create_task,
    load_tasks,
    main,
    save_tasks
)


class TaskAppTests(unittest.TestCase):

    def test_blank_title_is_rejected(self):
        with self.assertRaises(ValueError):
            create_task("")

    def test_whitespace_title_is_rejected(self):
        with self.assertRaises(ValueError):
            create_task("   ")

    def test_title_is_trimmed(self):
        task = create_task("  Learn Python  ")

        self.assertEqual(task["title"], "Learn Python")

    def test_new_task_is_not_completed(self):
        task = create_task("Test task")

        self.assertFalse(task["completed"])

    def test_unicode_title_is_preserved(self):
        task = create_task("Изучить программирование")

        self.assertEqual(
            task["title"],
            "Изучить программирование"
        )

    def test_missing_file_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "missing.json"

            self.assertEqual(load_tasks(path), [])

    def test_save_and_load_round_trip(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "tasks.json"

            tasks = [create_task("First task")]

            save_tasks(tasks, path)

            self.assertEqual(load_tasks(path), tasks)

    def test_add_task_saves_new_task(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "tasks.json"

            task = add_task("New task", path)

            self.assertEqual(load_tasks(path), [task])

    def test_add_task_appends_to_existing_tasks(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "tasks.json"

            add_task("First task", path)
            add_task("Second task", path)

            tasks = load_tasks(path)

            self.assertEqual(len(tasks), 2)
            self.assertEqual(
                tasks[1]["title"],
                "Second task"
            )

    def test_invalid_json_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "tasks.json"
            path.write_text("{broken", encoding="utf-8")

            with self.assertRaises(ValueError):
                load_tasks(path)

    def test_json_object_instead_of_list_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "tasks.json"

            path.write_text(
                '{"title": "Task"}',
                encoding="utf-8"
            )

            with self.assertRaises(ValueError):
                load_tasks(path)

    def test_invalid_task_record_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "tasks.json"

            path.write_text(
                '[{"title": 123, "completed": false}]',
                encoding="utf-8"
            )

            with self.assertRaises(ValueError):
                load_tasks(path)

    def test_cli_help_returns_zero(self):
        with redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as result:
                main(["--help"])

        self.assertEqual(result.exception.code, 0)

    def test_cli_add_creates_file(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "tasks.json"

            with redirect_stdout(io.StringIO()):
                result = main([
                    "add",
                    "CLI task",
                    "--file",
                    str(path)
                ])

            self.assertEqual(result, 0)
            self.assertEqual(
                load_tasks(path)[0]["title"],
                "CLI task"
            )


if __name__ == "__main__":
    unittest.main()

