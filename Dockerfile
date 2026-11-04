
FROM python:3.12.7-slim

WORKDIR /app

COPY task_app.py .
COPY tasks.json.example .

CMD ["python", "task_app.py", "--help"]

