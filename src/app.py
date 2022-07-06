import click
from flask import Flask
from flask.cli import with_appcontext
from database import populate_db, db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../db/winebase.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@click.command("create-tables")
@with_appcontext
def create_tables_cmd():
    db.create_all()


@click.command("delete-tables")
@with_appcontext
def delete_tables_cmd():
    db.drop_all()


@click.command("populate-database")
@with_appcontext
def populate_database_cmd():
    populate_db()


app.cli.add_command(create_tables_cmd)
app.cli.add_command(delete_tables_cmd)
app.cli.add_command(populate_database_cmd)
