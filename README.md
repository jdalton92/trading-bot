# **Trading Bot**

Headless algorithmic trading bot using market data from [Alpaca API](https://alpaca.markets/docs/api-documentation/) for real time data subscription/a paper trading account, and implemented using a bespoke Django wrapper for Alpaca's Python client.

Trades are placed with Alpaca Paper trading platform, with market data periodically sourced using Docker containers running Celery and Redis, and stored using a Postgresql database.

Current supported strategies:

- 14 day moving average
- 7 day moving average
- TO DO

# Author

- [James Dalton](https://jamesdalton.io)

# Built with

- [Django](https://nodejs.org/en/) - Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design.
- [Django-Rest-Framework](https://www.django-rest-framework.org/) - Django REST framework is a powerful and flexible toolkit for building Web APIs.
- [Docker](https://www.docker.com/) - Docker is a set of platform as a service products that use OS-level virtualization to deliver software in packages called containers.
- [Celery](https://docs.celeryproject.org/en/stable/index.html#) - Celery is a simple, flexible, and reliable distributed system to process vast amounts of messages, while providing operations with the tools required to maintain such a system. It’s a task queue with focus on real-time processing, while also supporting task scheduling.
- [Redis](https://redis.io/) - Redis is an open source (BSD licensed), in-memory data structure store, used as a database, cache and message broker
- [Visual Studio Code](https://code.visualstudio.com/) - IDE

# Instructions

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop). Create your own [Alpaca API Account](https://app.alpaca.markets/signup).

2. Navigate to your `server` directory, and create a `.env` file. Copy the included `.env.example` in this repo for a starter file;

```sh
$ cd server
$ cp .env.example .env
```

**Note:** setting `POSTGRES_HOST_AUTH_METHOD=trust` means Postgresql does not require a password. This is used only in development mode, being run on localhost

3. Activate your virtual environment, and navigate back into your project folder if necessary

```sh
$ pipenv shell
```

4. Run `docker compose up` to initialise django server, postgres for databasing, and celery/celery-beat/redis for handling of background tasks.

```sh
$ (server) docker compose up
```

**Note:** you may have to give `wait-for-it.sh` and `docker-entrypoint.sh` executable permissions

```sh
$ (server) chmod +x ./wait-for-it.sh && chmod +x ./docker-entrypoint.sh
```

5. To run the server for the first time, you will have to run database migrations. and create a superuser, and test data (refer `core.management.bootstrap.py` for detail on these commands). To do this you can use `docker compose` and the `web` container

```sh
# Run migrations
$ (server) docker compose exec web python manage.py migrate
# Create superuser account
$ (server) docker compose exec web python manage.py bootstrap -cs
# Create example data
$ (server) docker compose exec web python manage.py bootstrap -ced
```

6. Create a strategy via POST to `http://localhost:8000/v1/strategies/` or through your browser using Django's admin at `http://localhost:8000/admin/core/strategy/`

7. Keep the docker, and your local server running for periodic tasks to perform the given strategy created in **6.**

# Testing

```sh
$ (server) docker compose exec web python manage.py test
```

- Optionally add `--keepdb` to persist database between tests, and `--verbosity=2` to receive verbose output of tests

```sh
$ (server) docker compose exec web python manage.py test --keepdb --verbosity=2
```

# Dependencies

```
[packages]
django
djangorestframework
django-environ
alpaca-trade-api
celery
django-celery-beat
psycopg2
psycopg2-binary

[dev-packages]
django-debug-toolbar
freezegun
```

# Note

To make running `docker compose` commands on your local machine easier, use alias' in `.bashrc`/`.zshrc` configuration files eg.

```sh
# ~/.zshrc file
[...]
alias pm="docker compose exec web python manage.py"
```

Then the command `docker compose exec web python manage.py test server` becomes `pm test server`

# Licence

This project is licensed under the terms of the MIT license
