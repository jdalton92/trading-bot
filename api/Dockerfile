FROM python:3

ENV PYTHONUNBUFFERED 1

# Install latest Postgres client tools.
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ buster-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
    && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
    && apt-get update \
    && apt-get install -y --no-install-recommends postgresql-client-9.6

# Copy requirements.txt
COPY ./requirements.txt ./trading-bot/requirements.txt
RUN pip install -r ./trading-bot/requirements.txt

# Copy code into docker build
COPY . /trading-bot/
WORKDIR /trading-bot

# These are the environment variables that K8s must define for Django.
ENV DB_NAME=trading-bot
ENV DB_HOST=postgres
ENV DB_PASSWORD=
ENV DB_USER=trading-bot

# ENV CELERY_BROKER_USER=
# ENV CELERY_BROKER_PASSWORD=
# ENV CELERY_BROKER_HOST=
# ENV CELERY_BROKER_PORT=5672

# Django will serve on this container port.
EXPOSE 8000
