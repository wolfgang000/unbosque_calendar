### Setup local virtualenv + install dependencies

If you don't use asdf make sure to create the virtualenv with the same python version as the one defined on .tool-versions

```sh
python -m venv venv
source venv/bin/activate
pip install -U pip setuptools
pip install poetry==1.5.1
poetry install
```