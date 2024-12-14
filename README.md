## intallation

```sh
git clone https://github.com/zharuk-alex/goit-pythonweb-hw-12.git
cd goit-pythonweb-hw-10
```

build docker

```sh
docker-compose up --build
```

migration

```sh
docker exec -it contacts-app alembic upgrade head
```

dependencies install

```sh
poetry shell
poetry install
```

start project

```sh
poetry run python main.py
```

### tests

```sh
poetry run pytest
```

### tests cov

```sh
pytest --cov=src tests/ --cov-report=html
cd htmlcov
python -m http.server 5679
```

### documentation

```sh
cd docs
make html
```

```sh
cd docs/_build/html
python -m http.server 5678
```
