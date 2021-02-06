FROM python:3

ENV PYTHONUNBUFFERED 1

# Install postgres client tools
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ buster-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
    && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
    && apt-get update \
    && apt-get install -y --no-install-recommends postgresql-client-9.6

# Copy trading-bot code into docker build
RUN mkdir -p /trading-bot
COPY . /trading-bot
WORKDIR /trading-bot

# Copy and install requirements.txt
COPY ./Pipfile ./trading-bot/Pipfile
RUN pip install pipenv && pipenv install --system --deploy --dev

ENTRYPOINT ["./bin/docker-entrypoint.sh"]

# Django will serve on this container port.
EXPOSE 8000
