import click
from flask import Flask, render_template
from flask.cli import with_appcontext
from flask_jwt_extended import JWTManager
from flask_restful import Api

from src.database import db
from src.libs.aws import AwsBucket
from src.models.country import Country
from src.models.grape import Grape
from src.models.producer import Producer
from src.models.region import Region
from src.models.wine import Wine
from src.models.wine_type import Wine_type
from src.resources.user import UserLogin, UserLogout, UserRegister, UserItem

app = Flask(__name__)
app.config.from_object('config.Config')
jwt = JWTManager(app)
db.init_app(app)
s3 = AwsBucket()
api = Api(app)


@app.route("/")
def hello_world():
    return render_template('index.html')


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
    """
    Populate the base contents of database
    :return db content:
    """
    italy = Country(name='Italy')
    italy.add()
    france = Country(name='France')
    france.add()
    portugal = Country(name='Portugal')
    portugal.add()

    tuscany = Region(name='Tuscany')
    tuscany.country = italy
    tuscany.add()

    loire_valley = Region(name='Loire Valley')
    loire_valley.country = france
    loire_valley.add()

    norte = Region(name='Norte')
    norte.country = portugal
    norte.add()

    tenuta_sette_ponti = Producer(name='Tenuta Sette Ponti',
                                  description="A story of passion, dedication, and especially a great love for "
                                              "vineyards and their traditions. Our business philosophy is based on "
                                              "quality, research, long-lasting knowledge, age-old customs, respect "
                                              "for the land and its balance, and staying in step with genuine "
                                              "agricultural and ecological expertise.")
    tenuta_sette_ponti.region = tuscany
    tenuta_sette_ponti.add()

    chateau_du_poyet = Producer(name='Château du Poyet',
                                description='Château du Poyet is well regarded estate producing Muscadet '
                                            'Sèvre-et-Maine from around 43 hectares in the village of Chapelle '
                                            'Heulin. It is owned by the Bonneau family.')
    chateau_du_poyet.region = loire_valley
    chateau_du_poyet.add()

    grahams = Producer(name='W. & J. Graham\'s',
                       description='The story of two families across three centuries. For almost two hundred '
                                   'years W & J Graham’s has been an independent family business renowned '
                                   'for producing the finest Port wines. Graham’s has always been a pioneer. '
                                   'Graham\'s was one of the first Port companies to invest in its own '
                                   'vineyards in Portugal’s Douro Valley in 1890 and is now at the cutting '
                                   'edge of innovation in winemaking techniques. Today, five Symington '
                                   'cousins share responsibility for every aspect of the company and '
                                   'personally make the Graham’s wines. They too have been involved with '
                                   'Port and the Douro for many generations, with ancestry dating back to '
                                   'the mid-17th century.')
    grahams.region = norte
    grahams.add()

    red = Wine_type(type='red')
    red.add()
    white = Wine_type(type='white')
    white.add()
    port = Wine_type(type='port')
    port.add()

    sangiovese = Grape(name='Sangiovese',
                       description='Sangiovese is the most cultivated red grape variety in Italy, known all over the '
                                   'world for the production of excellences such as Chianti Classico, Brunello di '
                                   'Montalcino and Supertuscan. "Sour and bitter to eat, but juicy and full of wine", '
                                   'Sangiovese is the undisputed king of the red wines of central Italy.')
    sangiovese.region = tuscany
    sangiovese.add()

    melon_de_bourgogne = Grape(name='Melon de Bourgogne',
                               description='Melon de Bourgogne is the white grape synonymous with the Muscadet '
                                           'appellation in the western Loire Valley. The variety has naturally high '
                                           'acidity, but often struggles to achieve good concentration of flavor. The '
                                           'best wines show apple and citrus flavors, with underlying mineral notes. '
                                           'A saltiness can sometimes identified in the wine, suggestive of the '
                                           'region\'s maritime geography.')
    melon_de_bourgogne.region = loire_valley
    melon_de_bourgogne.add()

    touriga_nacional = Grape(name='Touriga Nacional',
                             description='Touriga Nacional is a dark-skinned grape variety that is currently very '
                                         'fashionable and is widely believed to produce the finest red wines of '
                                         'Portugal. Extensively planted in the Portugal\'s northern Dao and Douro '
                                         'wine regions, the variety is a key ingredient in both dry red wines and the '
                                         'fortified wines of Oporto. Touriga Nacional has firm tannins, is expressive '
                                         'as a varietal wine and shows great aging potential.')
    touriga_nacional.region = norte
    touriga_nacional.add()

    crognolo_picture = s3.get_file_url('tenuta-sette-ponti-crognolo-toscana.png')
    crognolo_toscana = Wine(name='Crognolo Toscana', year_produced=2018, alcohol_percentage=14.5, volume=750,
                            picture=crognolo_picture,
                            description='Made with 85% Sangiovese, 8% Merlot and 7% Cabernet Sauvignon, this opens '
                                        'with aromas of plum, tobacco and baking spice. The concentrated palate '
                                        'offers blackberry jam, licorice and powdered sage alongside grainy tannins.',
                            style='Savory and Classic')
    crognolo_toscana.wine_type = red
    crognolo_toscana.producer = tenuta_sette_ponti
    crognolo_toscana.grape = sangiovese
    crognolo_toscana.add()

    muscadet_picture = s3.get_file_url('chateau-de-poyet-muscadet-sevre-et-maine-sur-lie.png')
    muscadet = Wine(name='Muscadet Sèvre et Maine Sur Lie', year_produced=2018, alcohol_percentage=14.5, volume=750,
                    picture=muscadet_picture,
                    description='A nice crisp drink. Pale in colour with a nice "tang" on the mouth. Absolutely '
                                'quaffable. As all Muscadet Sèvre et Maine sur Lie, Château du Poyet keeps its wine '
                                'on lees all over the winter and cannot bottle them before the 3rd Thursday of March. '
                                'The whole process allows this wine a lovely freshness.',
                    style='Green and Flinty')
    muscadet.wine_type = white
    muscadet.producer = chateau_du_poyet
    muscadet.grape = melon_de_bourgogne
    muscadet.add()

    grahams_picture = s3.get_file_url('grahams-20-years-old-tawny-port.png')
    grahams_port = Wine(name='20 year old tawny port', year_produced=2018, alcohol_percentage=20, volume=750,
                        picture=grahams_picture,
                        description='Graham’s 20 Year Old Tawny has an amber, golden tawny colour. On the nose, '
                                    'it shows an excellent bouquet with a characteristic ‘nutty’ character and '
                                    'delicious mature fruit with hints of orange peel, exquisitely mellowed by '
                                    'careful ageing. On the palate, it is rich, softly sweet and smooth, '
                                    'perfectly balanced, with a long and elegant finish.',
                        style='Rich and Warming')
    grahams_port.wine_type = port
    grahams_port.producer = grahams
    grahams_port.grape = touriga_nacional
    grahams_port.add()


app.cli.add_command(create_tables_cmd)
app.cli.add_command(delete_tables_cmd)
app.cli.add_command(populate_database_cmd)

api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(UserRegister, "/register")
api.add_resource(UserItem, "/user")
