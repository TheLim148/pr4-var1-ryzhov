
# Task Manager

Простое консольное приложение для управления задачами.

## Возможности

- Создание задач.
- Проверка названия задачи.
- Сохранение данных в JSON.
- Просмотр списка задач.

## Требования

- Python 3.12.7

## Запуск

Показать справку:

```bash
uv run python task_app.py --help
```

Добавить задачу:

```bash
uv run python task_app.py add "Изучить Python"
```

Посмотреть задачи:

```bash
uv run python task_app.py list
```

Можно указать собственный JSON-файл:

```bash
uv run python task_app.py add "Новая задача" --file tasks.json
```

## Тестирование

```bash
uv run python -m unittest discover -s tests -v
```
Pull Request pipeline verification.
