
import argparse
import json
from pathlib import Path
from typing import Any

Task = dict[str, Any]


def create_task(title: str) -> Task:
    # if not isinstance(title, str) or not title.strip():
    #     raise ValueError("Название задачи не может быть пустым.")

    return {
        "title": title.strip(),
        "completed": False
    }


def load_tasks(file_path: str | Path) -> list[Task]:
    path = Path(file_path)

    if not path.exists():
        return []

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(
            "Файл задач содержит некорректный JSON."
        ) from error

    if not isinstance(data, list):
        raise ValueError(
            "Файл задач должен содержать JSON-массив."
        )

    for task in data:
        if (
            not isinstance(task, dict)
            or not isinstance(task.get("title"), str)
            or not isinstance(task.get("completed"), bool)
        ):
            raise ValueError(
                "Файл содержит задачу в неправильном формате."
            )

    return data


def save_tasks(
    tasks: list[Task],
    file_path: str | Path
) -> None:
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        json.dumps(tasks, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )


def add_task(title: str, file_path: str | Path) -> Task:
    tasks = load_tasks(file_path)

    task = create_task(title)
    tasks.append(task)

    save_tasks(tasks, file_path)

    return task


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Простой менеджер задач."
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    add_parser = subparsers.add_parser(
        "add",
        help="Добавить задачу"
    )

    add_parser.add_argument(
        "title",
        help="Название задачи"
    )

    add_parser.add_argument(
        "--file",
        default="tasks.json",
        help="Путь к JSON-файлу"
    )

    list_parser = subparsers.add_parser(
        "list",
        help="Показать список задач"
    )

    list_parser.add_argument(
        "--file",
        default="tasks.json",
        help="Путь к JSON-файлу"
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "add":
            task = add_task(args.title, args.file)

            print(f"Добавлена задача: {task['title']}")

        elif args.command == "list":
            tasks = load_tasks(args.file)

            if not tasks:
                print("Список задач пуст.")
            else:
                for index, task in enumerate(tasks, start=1):
                    status = (
                        "выполнена"
                        if task["completed"]
                        else "не выполнена"
                    )

                    print(
                        f"{index}. {task['title']} — {status}"
                    )

    except ValueError as error:
        parser.error(str(error))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

