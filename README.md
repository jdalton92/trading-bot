# **Trading Bot**

Algorithmic trading bot using market data from [Alpaca API](https://alpaca.markets/docs/api-documentation/) for a real time data subscription, and paper trading account

Trades are placed with Alpaca Paper trading platform, with market data periodically sourced using Docker containers with Celery and Redis, and stored in a Postgresql database.

# **Alpaca API**

Alpaca Data API provides the market data available to the client user through the REST and websocket streaming interfaces. Alpaca Data API consolidates data sources from five different exchanges.

- IEX (Investors Exchange LLC)
- NYSE National, Inc.
- Nasdaq BX, Inc.
- Nasdaq PSX
- NYSE Chicago, Inc.

## Authors

- **James Dalton**

## Instructions to use

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop) and [Docker Compose](https://docs.docker.com/compose/install/). Navigate to `api` directory, and update `.env` file with the following:

```sh
DJANGO_SECRET_KEY=<your-django-secret-key>
DEBUG=true
LOG_LEVEL=DEBUG
LOG_REQUESTS=true

APCA_API_SECRET_KEY=<your-alpaca-secret-key>
APCA_API_KEY_ID=<your-alpaca-api-key>
APCA_API_BASE_URL=https://paper-api.alpaca.markets

POSTGRES_USER=tradingbot
POSTGRES_NAME=tradingbot
POSTGRES_DB=tradingbot
POSTGRES_PASSWORD=
POSTGRES_HOST=localhost
POSTGRES_HOST_AUTH_METHOD=trust
```
**Note:** setting `POSTGRES_HOST_AUTH_METHOD=trust` means postgresql does not require a password. This is used only in development mode, being run on localhost

2. Run `docker-compose up` to initialise postgres for databasing, and celery/celery-beat/redis for handling of background tasks.

```sh
$ docker-compose up
```

3. Run the api on localhost a separte terminal

```sh
$ pipenv shell
$ python manage.py runserver
```

## Testing

> TBC

## Built with

- [React](https://create-react-app.dev/docs/adding-typescript/) - Bootstrapped using Create React App, and using TypeScript template.
- [Django](https://nodejs.org/en/) - Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design.
- [Django-Rest-Framework](https://www.django-rest-framework.org/) - Django REST framework is a powerful and flexible toolkit for building Web APIs.
- [Docker](https://www.docker.com/) - Docker is a set of platform as a service products that use OS-level virtualization to deliver software in packages called containers.
- [Celery](https://docs.celeryproject.org/en/stable/index.html#) - Celery is a simple, flexible, and reliable distributed system to process vast amounts of messages, while providing operations with the tools required to maintain such a system. It’s a task queue with focus on real-time processing, while also supporting task scheduling.
- [Redis](https://redis.io/) - Redis is an open source (BSD licensed), in-memory data structure store, used as a database, cache and message broker
- [Visual Studio Code](https://code.visualstudio.com/) - IDE

## Licence

This project is licensed under the terms of the MIT license
