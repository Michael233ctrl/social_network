# Social network

Simple REST API for making posts, liking them and registering new users.

## Installation

Use the package manager [pipenv](https://pipenv.pypa.io/en/latest/) to install all requirements for the project.

``` bash
$ pipenv install --dev
```

## Usage
First you need to apply migrations for the project.

``` bash
python manage.py migrate
```
To run server use this command.

``` bash
python manage.py runserver
```

## Running the tests

To run test bot, use following command.

``` bash
python bot.py
```

All settings for bot placed in 'config_for_script.py' file.

```
"""
Settings for testing api script
"""
NUMBER_OF_USERS = 20
MAX_POSTS_PER_USER = 10
MAX_LIKES_PER_USER = 10
BACKEND_URL = "http://127.0.0.1:8000"
```
