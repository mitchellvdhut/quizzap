# FastAPI Template by TijmenSimons

A layered architecture created my [@TijmenSimons](https://github.com/TijmenSimons/), [@Tientjie-san](https://github.com/tientjie-san/) and [@IvarDeViking](https://github.com/ivardeviking).

## About

This project uses the mysql database. For personalization, you can change the database in the `docker-compose.yml` and the `core\config.py`.

## Run in docker

Create an `.env` file in the root folder. Include the values found in the `env.example` files.

To run the project:
```cmd
docker compose up --build
```

## Run locally

Create an `.env` file in the root folder. Include the values found in the `env.example` files.

First setup the environment

```cmd
python -m virtualenv venv

.\venv\Scripts\activate
```

Then install the requirements.

```cmd
pip install -r ./requirements.txt
```

To run the project:

```cmd
python main.py
```

Add the `--env : ["local", "dev", "prod"]` flag for other configs. `local` is the default.

## Access

You can now access the application on [http://localhost:8002/api/latest/docs](http://localhost:8002/api/latest/docs).

If you're still using mysql, manage the database on [http://localhost:8081/](http://localhost:8081/) and log in with what you set the password to.

### Run tests

Unit + Coverage test

```cmd
pytest --cov=api --cov=app --cov=core --cov-report=html --cov-fail-under=85
```

## Additional information

For database migrations we use [alembic](https://alembic.sqlalchemy.org/en/latest/).
