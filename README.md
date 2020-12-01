# **Trading Bot**

Algorithmic trading bot using market data from [Alpaca API](https://alpaca.markets/docs/api-documentation/) for a real time data subscription, and paper trading account

Trades are placed with Alpaca Paper trading platform, with market data periodically sourced using Docker containers with Celery and Redis, and stored using a Postgresql database.

# **Alpaca API**

Alpaca Data API provides the market data available to the client user through the REST and websocket streaming interfaces. Alpaca Data API consolidates data sources from five different exchanges.

- IEX (Investors Exchange LLC)
- NYSE National, Inc.
- Nasdaq BX, Inc.
- Nasdaq PSX
- NYSE Chicago, Inc.

# Author

- [James Dalton](https://jamesdalton.io)

# Built with

- [Django](https://nodejs.org/en/) - Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design.
- [Django-Rest-Framework](https://www.django-rest-framework.org/) - Django REST framework is a powerful and flexible toolkit for building Web APIs.
- [Docker](https://www.docker.com/) - Docker is a set of platform as a service products that use OS-level virtualization to deliver software in packages called containers.
- [Celery](https://docs.celeryproject.org/en/stable/index.html#) - Celery is a simple, flexible, and reliable distributed system to process vast amounts of messages, while providing operations with the tools required to maintain such a system. It’s a task queue with focus on real-time processing, while also supporting task scheduling.
- [Redis](https://redis.io/) - Redis is an open source (BSD licensed), in-memory data structure store, used as a database, cache and message broker
- [React](https://create-react-app.dev/docs/adding-typescript/) - Bootstrapped using Create React App, and using TypeScript template.
- [Visual Studio Code](https://code.visualstudio.com/) - IDE

# Instructions

## Client

1. TBC

## Server

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop) and [Docker Compose](https://docs.docker.com/compose/install/). Create your own [Alpaca API Account](https://app.alpaca.markets/signup).

2. Navigate to your `server` directory, and create a `.env` file. Copy the included `.env.example` in this repo for a starter file;

```sh
$ cd server
$ cp .env.example .env
```

**Note:** setting `POSTGRES_HOST_AUTH_METHOD=trust` means Postgresql does not require a password. This is used only in development mode, being run on localhost

3. Activate your virtual environment, and install the necessary dependencies summarised in the `Pipfile`

```sh
$ pipenv shell
$ (sever) pipenv install
```

4. Run `docker-compose up` to initialise postgres for databasing, and celery/celery-beat/redis for handling of background tasks.

```sh
$ docker-compose up
```

5. Run the server on localhost a separte terminal and run database migrations, create a superuser (refer `.env.example` file for default superuser account details, and include `--no-input` command)

```sh
$ (server) python manage.py migrate
$ (server) python manage.py createsuperuser --no-input
$ (server) python manage.py runserver
```

# Testing

## Server

```sh
$ (server) python manage.py test server
```

- Optionally add `--keepdb` to persist database between tests, and `--verbosity=2` to recieve verbose output of tests

```sh
$ (server) python manage.py test server --keepdb --verbosity=2
```

## Client

```sh
$ TBC
```

# Server Dependencies

```
[packages]
django
djangorestframework
django-environ
alpaca-trade-api
django-filter
celery
django-celery-beat
psycopg2
psycopg2-binary

[dev-packages]
django-debug-toolbar
freezegun
```

# Licence

This project is licensed under the terms of the MIT license
