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

### Install pip-tools for package management

```shell
pip install pip-tools
```

### Install required packages with pip-tools

```shell
pip-compile ./requirements.in
```

or upgrade
```shell
pip-compile --upgrade-package <package>
```

### Sync the env with requirements

```shell
pip-sync
```

### Project runnable

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
