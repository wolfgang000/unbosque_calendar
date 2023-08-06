### Setup local virtualenv + install dependencies

If you don't use asdf make sure to create the virtualenv with the same python version as the one defined on .tool-versions

```sh
python -m venv venv
source venv/bin/activate
pip install -U pip setuptools
pip install poetry==1.5.1
poetry install
```


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

