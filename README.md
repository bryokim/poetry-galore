# ![Alt logo](/docs/images/logo-icon.svg)Poetry Galore

![Alt screenshot](/docs/images/screenshot.png)

For the love of poetry.

You can view the live demo [here](<https://bryokim.github.io/poetry-galore>)

_**Authors:**_

- **Brian**

[![Alt github](https://img.shields.io/badge/GitHub-181717.svg?style=for-the-badge&logo=GitHub&logoColor=white)](<https://github.com/bryokim>)
[![Alt linkedin](https://img.shields.io/badge/LinkedIn-0A66C2.svg?style=for-the-badge&logo=LinkedIn&logoColor=white)](<https://www.linkedin.com/in/brian-kimathi01/>)

- **Reagan**

[![Alt github](https://img.shields.io/badge/GitHub-181717.svg?style=for-the-badge&logo=GitHub&logoColor=white)](<https://github.com/thatboyreegan>)
[![Alt linkedin](https://img.shields.io/badge/LinkedIn-0A66C2.svg?style=for-the-badge&logo=LinkedIn&logoColor=white)](<https://www.linkedin.com/in/brian-kimathi01/>)

## Installation

To run the application, you first need to clone this [repository](<https://github.com/bryokim/poetry-galore>) and move into the
poetry-galore directory.

Next you need to install all the requirements required to run the application.

```Bash
kim@eternity ~/poetry-galore
$ pip install -r requirements.txt
```

## Usage

### Setup Database

You'll also need a database to store and persist the data. You can opt to use SQLite for ease of setup or MySQL if you want more control over the database.

- #### Using SQLite

To use the SQLite database, set the `DATABASE_URL` env variable to `sqlite:///<db_name>.sqlite`

For example:

```Bash
export DATABASE_URL="sqlite:///poetry_galore_db.sqlite"
```

- #### Using MySQL

First of all you need to have MySQL installed. You can follow this [tutorial](.) to install and set up
your MySQL.

After installing MySQL, you can create a new database to be used.

```Bash
mysql -u <username> -p -e 'CREATE DATABASE <db_name>'
```

Replace `username` with your MySQL username and `db_name` with the database name.

Now set the `DATABASE_URL` env variable to `mysql+mysqldb://<username>:<password>@localhost/<db_name>`

For example:

```Bash
export DATABASE_URL="mysql+mysqldb://root:password@localhost/poetry_galore_db"
```

#### Initialize Database

After setting up the database of your choice, you need to initialize and upgrade the database. Run the following commands to finish setting up your database.

```Bash
flask db init
flask db migrate
flask db upgrade
```

### Set env variables

Apart from `DATABASE_URL`, you'll be required to set the following environment variables.

| Env variable | Description | Value |
| :--- | --- |--- |
| `FLASK_APP` | Flask application to run | `app` |
| `APP_SETTINGS` |  Configuration to be used by the app as in [config.py](config.py). | `config.TestingConfig` -> Testing config. `config.DevelopmentConfig` -> Development config. `config.ProductionConfig` -> Production config.|
| `SECRET_KEY`| Secret key for session encryption. | A secret value. Defaults to `guess-me` |
| `SECURITY_PASSWORD_SALT` | Salt used for password encryption | A secret value. Defaults to `very-important` |

### Starting the app

After setting the environment variables, you can start the app.

```Bash
flask run
```

You can navigate to <http://127.0.0.1:5000> to view the application and use it.

## Contributing

You're always welcome to contributing.

## License

`poetry-galore` is licensed under the [MIT](LICENSE) license.
