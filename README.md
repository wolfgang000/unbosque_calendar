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

```
dokku apps:create unbosque-calendar-back

# Setup database
dokku postgres:create unbosque-calendar-db
dokku postgres:link unbosque-calendar-db unbosque-calendar-back

# Setup rabbitmq
dokku rabbitmq:create unbosque-calendar-rabbitmq
dokku rabbitmq:link unbosque-calendar-rabbitmq unbosque-calendar-back
```