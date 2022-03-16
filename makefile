format:
	isort . && black .

tests:
	pytest src

check:
	black . --check && \
	isort . --check && \
    flake8 . && \
    mypy src/

create_migrations:
	cd src && \
	alembic revision --autogenerate

migrate:
	cd src && \
	alembic upgrade head