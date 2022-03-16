# FastAPI Default

Шаблон сервиса с использованием fastapi/sqlalchemy/pytest

Запуск для локальной разработки
```shell script
uvicorn --app-dir src main:app --reload
```

Запуск для продакшен
```shell script
uvicorn --app-dir src main:app
```

Запуск тестов
```shell script
python -m pytest
```

Создание миграций
```shell script
alembic revision --autogenerate
```

Применение миграций
```shell script
alembic upgrade head
```
