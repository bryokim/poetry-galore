# poetry-galore

For the love of poetry.

## Starting up the application

To run the application, you first need to clone this [repository](<https://github.com/bryokim/poetry-galore>) and run `cd poetry-galore`.

Next you need to install all the requirements required to run the application.

```Bash
kim@eternity ~/poetry-galore
$ pip install -r requirements.txt
```

You also need to have a MySQL installation in order for the application to be able
to read and write data to the database. You can follow this [tutorial](.) to install and set up
your MySQL.

You'll need to set the following environment variables that are required by the application.

```Text
APP_SETTINGS -> Sets the configuration object that contains the configuration on which the app is to run on.
SECRET_KEY -> Sets the secret key.
SECURITY_PASSWORD_SALT -> Sets the salt used for password encryption.
FLASK_APP -> Name of the flask application to run. In this case it's "app".
DATABASE_URL -> The MySQL database to connect to.
```

Next initialize and upgrade the database.

```Bash
kim@eternity ~/poetry-galore
$ flask db init

kim@eternity ~/poetry-galore
$ flask db migrate

kim@eternity ~/poetry-galore
$ flask db upgrade
```

After setting the environment variables, you can start the app.

```Bash
kim@eternity ~/poetry-galore
$ flask run
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

You can navigate to <http://127.0.0.1:5000> to view the application and use it.

## Project Summary

The app folder contains all code related to the Flask application.
The [__init__.py](./app/__init__.py) file in app directory contains the `create_app()` function that creates and
adds required extensions and configuration to the application.

The [models](./app/models) directory contains the database models used in creating the
database tables. The models represent each basic unit that is required by the app.
It also includes a [database storage class](./app/models/engine/db_storage.py) that provides
methods used in querying the database and writing to it.

The [views](./app/views) folder contains all the app endpoints and functions that define
the logic behind each one of them. Each file in views has endpoints specific to a certain
object in the database model.

The [templates](./app/templates) directory provides Jinja HTML templates that are used for
rendering the data acquired from the endpoints.

The [forms](./app/forms) directory includes various forms used for collecting information
from the user. These include the login, signup, poem and even profile updates.

The [utils](./app/utils) provides common functions that are used severally in different modules such as decorators for the endpoints in views.

All static files can be found in [static](./app/static). That includes JavaScript scripts, CSS files and images.

The [config.py](./config.py) file found at the root of the project is used to provide
configuration that is loaded during app creation. Configurations can be found in form of classes
that can be loaded into your flask app.
