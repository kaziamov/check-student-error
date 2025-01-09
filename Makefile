start:
	uv run python3 manage.py runserver 0.0.0.0:8080

test:
	poetry run python3 manage.py test tests/

console:
	uv run django-admin shell
