```terminal
poetry lock
poetry install --no-root --only main
poetry update
poetry run pytest
poetry run python run.py -b 0.0.0.0:5000 app:app
```