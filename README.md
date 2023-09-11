# poetry-galore

For the love of poetry.

## Project structure

* [app](./app)
  * [__init__.py](./app/__init__.py)
  * [static](./app/static)
    * [styles](./app/static/styles)
      * [bootstrap.min.css](./app/static/styles/bootstrap.min.css)
      * [bootstrap.min.css.map](./app/static/styles/bootstrap.min.css.map)
      * [style.css](./app/static/styles/style.css)
    * [images](./app/static/images)
      * [logo-no-background.svg](./app/static/images/logo-no-background.svg)
      * [icon.svg](./app/static/images/icon.svg)
    * [scripts](./app/static/scripts)
      * [bootstrap.bundle.min.js](./app/static/scripts/bootstrap.bundle.min.js)
      * [bootstrap.bundle.min.js.map](./app/static/scripts/bootstrap.bundle.min.js.map)
      * [update_user.js](./app/static/scripts/update_user.js)
      * [script.js](./app/static/scripts/script.js)
      * [comments.js](./app/static/scripts/comments.js)
      * [create_poem.js](./app/static/scripts/create_poem.js)
  * [models](./app/models)
    * [engine](./app/models/engine)
      * [__init__.py](./app/models/engine/__init__.py)
      * [db_storage.py](./app/models/engine/db_storage.py)
    * [__init__.py](./app/models/__init__.py)
    * [category.py](./app/models/category.py)
    * [comment.py](./app/models/comment.py)
    * [theme.py](./app/models/theme.py)
    * [user.py](./app/models/user.py)
    * [poem.py](./app/models/poem.py)
    * [base_model.py](./app/models/base_model.py)
  * [forms](./app/forms)
    * [__init__.py](./app/forms/__init__.py)
    * [login_form.py](./app/forms/login_form.py)
    * [register_form.py](./app/forms/register_form.py)
    * [poem_form.py](./app/forms/poem_form.py)
  * [templates](./app/templates)
    * [post_poem.html](./app/templates/post_poem.html)
    * [update_poem.html](./app/templates/update_poem.html)
    * [profile.html](./app/templates/profile.html)
    * [_base.html](./app/templates/_base.html)
    * [footer.html](./app/templates/footer.html)
    * [update_user.html](./app/templates/update_user.html)
    * [navigation.html](./app/templates/navigation.html)
    * [register.html](./app/templates/register.html)
    * [home.html](./app/templates/home.html)
    * [login.html](./app/templates/login.html)
    * [poem.html](./app/templates/poem.html)
  * [utils](./app/utils)
    * [decorators.py](./app/utils/decorators.py)
  * [views](./app/views)
    * [poems_likes.py](./app/views/poems_likes.py)
    * [themes.py](./app/views/themes.py)
    * [api](./app/views/api)
      * [categories_api.py](./app/views/api/categories_api.py)
      * [comments_api.py](./app/views/api/comments_api.py)
      * [__init__.py](./app/views/api/__init__.py)
      * [likes_api.py](./app/views/api/likes_api.py)
      * [poems_api.py](./app/views/api/poems_api.py)
      * [search_api.py](./app/views/api/search_api.py)
      * [themes_api.py](./app/views/api/themes_api.py)
      * [users_api.py](./app/views/api/users_api.py)
    * [categories.py](./app/views/categories.py)
    * [comments.py](./app/views/comments.py)
    * [home.py](./app/views/home.py)
    * [poems.py](./app/views/poems.py)
    * [login.py](./app/views/login.py)
    * [logout.py](./app/views/logout.py)
    * [register.py](./app/views/register.py)
    * [__init__.py](./app/views/__init__.py)
    * [users.py](./app/views/users.py)
* [tests](./tests)
  * [__init__.py](./tests/__init__.py)
  * [unit](./tests/unit)
    * [test_models](./tests/unit/test_models)
      * [__init__.py](./tests/unit/test_models/__init__.py)
      * [test_engine](./tests/unit/test_models/test_engine)
        * [test_db_storage.py](./tests/unit/test_models/test_engine/test_db_storage.py)
      * [test_theme.py](./tests/unit/test_models/test_theme.py)
      * [test_poem.py](./tests/unit/test_models/test_poem.py)
      * [test_user.py](./tests/unit/test_models/test_user.py)
      * [test_category.py](./tests/unit/test_models/test_category.py)
      * [test_comment.py](./tests/unit/test_models/test_comment.py)
      * [test_base_model.py](./tests/unit/test_models/test_base_model.py)
  * [functional](./tests/functional)
    * [__init__.py](./tests/functional/__init__.py)
    * [test_logout.py](./tests/functional/test_logout.py)
    * [test_login.py](./tests/functional/test_login.py)
    * [test_register.py](./tests/functional/test_register.py)
    * [test_home.py](./tests/functional/test_home.py)
  * [conftest.py](./tests/conftest.py)
* [dev](./dev)
  * [google_login.py](./dev/google_login.py)
* [console.py](./console.py)
* [mysql](./mysql)
* [LICENSE](./LICENSE)
* [project-structure.sh](./project-structure.sh)
* [README.md](./README.md)
* [config.py](./config.py)
* [requirements.txt](./requirements.txt)

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
