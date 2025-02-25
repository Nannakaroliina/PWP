# PWP SUMMER 2022
# WineTime API
# Group information
* Student 1. Nanna Setämaa and tanja.setamaa@oulu.fi
* Student 2. Henna Tammia and henna.tammia@student.oulu.fi

__Remember to include all required documentation and HOWTOs, including how to create and populate the database, how to run and test the API, the url to the entrypoint and instructions on how to setup and run the client__

# Set up the project

### Create ENV

```shell
python3 -m venv pwp
source pwp/bin/activate
```

## Required dependencies

The project is using Python 3.10.
To keep all requirements and pinned requirements up-to-date,
this project uses pip-tools and requirements.in file to provide 
all needed dependencies which needs to be installed:

- Flask for creating the web application
- Flask SQLAlchemy for SQLAlchemy support
- Flask RESTful for building REST API
- Flask-redoc for OpenAPI specification
- Flask Uploads for image uploads and serving
- boto3 for storing pictures and serving them
- python-dotenv for reading env configurations
- flask-jwt-extended for JSON Web Token based authentication
- pytest for testing
- pytest-cov for coverage report
- requests lib to make aws post calls
- gunicorn for WSGI HTTP Server (project is deployed in heroku)
- alembic & Flask-Migrate for database migration (deployment version uses postgresql db instead of sqlite3)
- flask-bootstrap for building the web app client for starting page


### Install pip-tools for package management

```shell
pip install pip-tools
```

### Install required packages with pip-tools

This will generate or update existing our requirements.txt file which
contains all needed dependencies and this is used for
pip-sync command which makes sure all the dependencies are installed.

```shell
pip-compile
```

or upgrade
```shell
pip-compile --upgrade-package <package>
```

### Sync the env with requirements

```shell
pip-sync
```

## Deployed project

The deployed project can be found from:
[Wine Time API & client](https://wine-time-api.herokuapp.com)
You can find the link to OpenAPI documentation from starting page.

For api end-points, use /api/<end-point> option,
e.g. api/wines to get all wines

Note! Since the project is using S3 Bucket with presigned urls, the picture urls expire within a week.

## Project runnable

The project works with flask, to run it let's first make script files runnable:

```shell
chmod +x run_app.sh
chmod +x delete_database.sh
```

After this you can run the project with:

```shell
./run_app.sh
```

After use, you can delete database if you wish:

```shell
./delete_database.sh
```


## Running tests

The test are done with pytest, it provides the results of the tests,
including the warnings if there is any. Finally, it gives coverage report.
To run them let's first make script files runnable:

```shell
chmod +x run_tests.sh
```

After this you can run the tests with:

```shell
./run_tests.sh
```
