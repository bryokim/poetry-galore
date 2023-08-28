# poetry-galore

For the love of poetry.

## Project structure

* [app](./app)
    * [__init__.py](./app/__init__.py)
    * [forms](./app/forms)
        * [__init__.py](./app/forms/__init__.py)
        * [post_poem.py](./app/forms/post_poem.py)
        * [login.py](./app/forms/login.py)
        * [register.py](./app/forms/register.py)
    * [models](./app/models)
        * [engine](./app/models/engine)
            * [__init__.py](./app/models/engine/__init__.py)
            * [db_storage.py](./app/models/engine/db_storage.py)
        * [__init__.py](./app/models/__init__.py)
        * [category.py](./app/models/category.py)
        * [comment.py](./app/models/comment.py)
        * [poem.py](./app/models/poem.py)
        * [theme.py](./app/models/theme.py)
        * [base_model.py](./app/models/base_model.py)
        * [user.py](./app/models/user.py)
    * [templates](./app/templates)
        * [core](./app/templates/core)
            * [poem.html](./app/templates/core/poem.html)
        * [accounts](./app/templates/accounts)
            * [register.html](./app/templates/accounts/register.html)
            * [home.html](./app/templates/accounts/home.html)
            * [post_poem.html](./app/templates/accounts/post_poem.html)
            * [profile.html](./app/templates/accounts/profile.html)
            * [login.html](./app/templates/accounts/login.html)
        * [navigation.html](./app/templates/navigation.html)
        * [_base.html](./app/templates/_base.html)
    * [utils](./app/utils)
        * [decorators.py](./app/utils/decorators.py)
    * [views](./app/views)
        * [__init__.py](./app/views/__init__.py)
        * [core](./app/views/core)
            * [__init__.py](./app/views/core/__init__.py)
            * [categories.py](./app/views/core/categories.py)
            * [comments.py](./app/views/core/comments.py)
            * [poems_likes.py](./app/views/core/poems_likes.py)
            * [themes.py](./app/views/core/themes.py)
            * [poems.py](./app/views/core/poems.py)
            * [users.py](./app/views/core/users.py)
        * [account](./app/views/account)
            * [__init__.py](./app/views/account/__init__.py)
            * [home.py](./app/views/account/home.py)
            * [register.py](./app/views/account/register.py)
            * [login.py](./app/views/account/login.py)
    * [static](./app/static)
        * [scripts](./app/static/scripts)
            * [bootstrap.bundle.min.js](./app/static/scripts/bootstrap.bundle.min.js)
            * [bootstrap.bundle.min.js.map](./app/static/scripts/bootstrap.bundle.min.js.map)
            * [script.js](./app/static/scripts/script.js)
        * [styles](./app/static/styles)
            * [bootstrap.min.css](./app/static/styles/bootstrap.min.css)
            * [bootstrap.min.css.map](./app/static/styles/bootstrap.min.css.map)
            * [style.css](./app/static/styles/style.css)
        * [images](./app/static/images)
            * [logo-no-background.svg](./app/static/images/logo-no-background.svg)
* [LICENSE](./LICENSE)
* [README.md](./README.md)
* [console.py](./console.py)
* [mysql](./mysql)
* [config.py](./config.py)
* [requirements.txt](./requirements.txt)

## Starting up the application

To run the application, you first need to clone this repository.

Next you need to install all the requirements required to run the application.

```Bash
kim@eternity ~/poetry-galore
$ pip install -r requirements.txt
```

You also need to have a MySQL installation in order for the application to be able
to read and write data to the database. You can follow this tutorial to install and set up
your MySQL.

You'll need to set the following environment variables that are required by the application.

```Text
APP_SETTINGS -> Sets the configuration object that contains the configuration on which the app is to run on.
SECRET_KEY -> Sets the secret key.
SECURITY_PASSWORD_SALT -> Sets the salt used for password encryption.
FLASK_APP -> Name of the flask application to run. In this case it's "app".
DATABASE_URL -> The MySQL database to connect to.
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
