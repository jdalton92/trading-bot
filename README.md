# **Alpaca Trading Bot**

Algorithmic trading bot using [Alpaca Web API](https://alpaca.markets/docs/api-documentation/) for real time data subscription, and paper trading account

// INSERT IMAGE

## Prototype

> [TBC]()

## Authors

- **James Dalton**

## Instructions

1. Clone app, install frontend dependencies

```sh
$ git clone https://github.com/jdalton92/trading-bot.git
$ cd client
$ npm install
$ npm start
```

2. Integrate backend to allow user creation, login, save dashboard, and contact form.

Create `.env` file in backend root directory with development environment variables shown in the below example `.env` file:

```sh
DJANGO_SECRET_KEY=<your-django-secret-key>
DEBUG='true'
LOG_LEVEL=DEBUG
LOG_REQUESTS='true'

APCA_API_SECRET_KEY=<your-alpaca-secret-key>
APCA_API_KEY_ID=<your-alpaca-api-key>
APCA_API_BASE_URL=https://paper-api.alpaca.markets

DB_NAME=<elephantsql-name>
DB_HOST=<elephantsql-host>
DB_PORT=5432
DB_USER=<elephantsql-user>
DB_PASSWORD=<elephantsql-password>
```

Then navidate to the server directory and install dependencies, and run the backend;

```sh
$ cd api
$ pipenv shell
$ python manage.py runserver
```

## Built with

- [React](https://create-react-app.dev/docs/adding-typescript/) - Bootstrapped using Create React App, and using TypeScript template.
- [Django](https://nodejs.org/en/) - Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design.
- [Django-Rest-Framework](https://www.django-rest-framework.org/) - Django REST framework is a powerful and flexible toolkit for building Web APIs.
- [ElephantSQL](https://www.elephantsql.com/) - ElephantSQL automates every part of setup and running of PostgreSQL clusters. Available on all major cloud and application platforms all over the world.
- [Visual Studio Code](https://code.visualstudio.com/) - IDE

## Licence

This project is licensed under the terms of the MIT license
