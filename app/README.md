```terminal
poetry lock
poetry install --no-root --only main
poetry update
poetry run pytest
poetry run python run.py -b 0.0.0.0:5000 app:app
```

## Docker

```terminal
docker build --build-arg=DEBIAN_NAME=bullseye --build-arg=PYTHON_VERSION=3.9 --build-arg=PYTHON_DISTROLESS_IMAGE=al3xos/python-distroless:3.9-debian11 -t phrasee-app .
docker run --rm -p 5000:5000 phrasee-app
```