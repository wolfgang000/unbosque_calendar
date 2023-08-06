### Setup local virtualenv + install dependencies

If you don't use asdf make sure to create the virtualenv with the same python version as the one defined on .tool-versions

```sh
python -m venv venv
source venv/bin/activate
pip install -U pip setuptools
pip install poetry==1.5.1
poetry install
```

# Get started

```sh
touch .env.local.dev
```

You need to add the following env variables to the env file:

```
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=http://localhost:8000/accounts/oauth/google_callback
```

We need to generate the Google OAuth credentials to get the values for `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`

- Follow [this](https://developers.google.com/identity/protocols/oauth2/web-server#creatingcred) Google's tutorial to generate the authorization credentials
- Add a new redirect URI "http://localhost:8000/accounts/oauth/google_callback"

```sh
# Start the containers
docker compose up
```

Site: http://localhost:8000

DB(Postgres): `postgres://test_user:test_password@localhost:8004/postgres_dev`

Message Broker(Rabbitmq): `localhost:8005`

### Format the code

```sh
make format
```

# Deployment

## Setup server

```
dokku apps:create unbosque-calendar
dokku config:set unbosque-calendar \
  # Set the variables from .env.example.prod

# Setup database
dokku postgres:create unbosque-calendar-db
dokku postgres:link unbosque-calendar-db unbosque-calendar

# Setup rabbitmq
dokku rabbitmq:create unbosque-calendar-rabbitmq
dokku rabbitmq:link unbosque-calendar-rabbitmq unbosque-calendar

# Setup SSL certificate
# Remember to open the 443 port

dokku letsencrypt:set unbosque-calendar email test@mail.com
dokku letsencrypt:enable unbosque-calendar

dokku letsencrypt:cron-job --add

# Setup domain
dokku domains:set unbosque-calendar unbosque-calendar.example.com
```

## Deploy and push changes

```
git remote add server dokku@example.com:unbosque-calendar

git push server
```

# Production debugging

## Enter to the container

```
dokku enter unbosque-calendar web /bin/sh
```

## Open a remote python shell

```
dokku enter unbosque-calendar web python manage.py shell
```

## Show logs

```
dokku logs unbosque-calendar
```

## Open a psql terminal

```
dokku postgres:connect unbosque-calendar-db
```
