"""
Module for database testing.
"""
import pytest
from sqlalchemy.exc import IntegrityError

from src.models.country import Country
from src.models.grape import Grape
from src.models.producer import Producer
from src.models.region import Region
from src.models.user import User
from src.models.wine import Wine
from src.models.wine_type import Wine_type
from test.conftest import db_handle  # pylint: disable=unused-import


def _get_wine_type():
    return Wine_type(type='test type')


def _get_country():
    return Country(name='test country')


def _get_region():
    return Region(name='test region')


def _get_producer():
    return Producer(name='test producer')


def _get_grape():
    return Grape(name='test grape')


def _get_wine():
    return Wine(name='test wine', year_produced=2022, alcohol_percentage=20, volume=750,
                picture='test picture', description='test description', style='test style')


def _get_user():
    return User(username='username', password='password', email='email@test.com', role='test')


def test_create_wine(db_handle):
    """ Test wine creation """
    wine = _get_wine()
    wine.wine_type = _get_wine_type()
    wine.producer = _get_producer()
    wine.grape = _get_grape()
    db_handle.session.add(wine)
    db_handle.session.commit()
    assert Wine.query.count() == 1


def test_delete_wine(db_handle):
    """ Test wine deletion """
    wine = _get_wine()
    db_handle.session.add(wine)
    db_handle.session.commit()
    db_handle.session.delete(wine)
    db_handle.session.commit()
    assert Wine.query.count() == 0


def test_create_wine_type(db_handle):
    """ Test wine type creation """
    wine_type = _get_wine_type()
    db_handle.session.add(wine_type)
    db_handle.session.commit()
    assert Wine_type.query.count() == 1


def test_delete_wine_type(db_handle):
    """ Test wine type deletion """
    wine_type = _get_wine_type()
    db_handle.session.add(wine_type)
    db_handle.session.commit()
    db_handle.session.delete(wine_type)
    db_handle.session.commit()
    assert Wine.query.count() == 0


def test_create_producer(db_handle):
    """ Test producer type creation """
    producer = _get_producer()
    producer.region = _get_region()
    db_handle.session.add(producer)
    db_handle.session.commit()
    assert Producer.query.count() == 1


def test_delete_producer(db_handle):
    """ Test producer deletion """
    producer = _get_producer()
    db_handle.session.add(producer)
    db_handle.session.commit()
    db_handle.session.delete(producer)
    db_handle.session.commit()
    assert Producer.query.count() == 0


def test_create_grape(db_handle):
    """ Test grape type creation """
    grape = _get_grape()
    grape.region = _get_region()
    db_handle.session.add(grape)
    db_handle.session.commit()
    assert Grape.query.count() == 1


def test_delete_grape(db_handle):
    """ Test grape deletion """
    grape = _get_grape()
    db_handle.session.add(grape)
    db_handle.session.commit()
    db_handle.session.delete(grape)
    db_handle.session.commit()
    assert Grape.query.count() == 0


def test_create_region(db_handle):
    """ Test region type creation """
    region = _get_region()
    region.country = _get_country()
    db_handle.session.add(region)
    db_handle.session.commit()
    assert Region.query.count() == 1


def test_delete_region(db_handle):
    """ Test region deletion """
    region = _get_region()
    db_handle.session.add(region)
    db_handle.session.commit()
    db_handle.session.delete(region)
    db_handle.session.commit()
    assert Region.query.count() == 0


def test_create_country(db_handle):
    """ Test country type creation """
    country = _get_country()
    db_handle.session.add(country)
    db_handle.session.commit()
    assert Country.query.count() == 1


def test_delete_country(db_handle):
    """ Test country deletion """
    country = _get_country()
    db_handle.session.add(country)
    db_handle.session.commit()
    db_handle.session.delete(country)
    db_handle.session.commit()
    assert Country.query.count() == 0


def test_create_user(db_handle):
    """ Test user type creation """
    user = _get_user()
    db_handle.session.add(user)
    db_handle.session.commit()
    assert User.query.count() == 1


def test_delete_user(db_handle):
    """ Test user deletion """
    user = _get_user()
    db_handle.session.add(user)
    db_handle.session.commit()
    db_handle.session.delete(user)
    db_handle.session.commit()
    assert User.query.count() == 0


def test_create_instances(db_handle):
    """
    Test creating all instances to database and check the instances and relationships.
    """

    # Create instances
    country = _get_country()
    region = _get_region()
    producer = _get_producer()
    grape = _get_grape()
    wine_type = _get_wine_type()
    wine = _get_wine()
    user = _get_user()

    # Set relations
    region.country = country
    producer.region = region
    grape.region = region
    wine.grape = grape
    wine.wine_type = wine_type
    wine.producer = producer

    # add to database
    db_handle.session.add(country)
    db_handle.session.add(region)
    db_handle.session.add(producer)
    db_handle.session.add(grape)
    db_handle.session.add(wine)
    db_handle.session.add(wine_type)
    db_handle.session.add(user)
    db_handle.session.commit()

    # Check that everything exists
    assert Country.query.count() == 1
    assert Region.query.count() == 1
    assert Producer.query.count() == 1
    assert Grape.query.count() == 1
    assert Wine.query.count() == 1
    assert Wine_type.query.count() == 1
    assert User.query.count() == 1
    db_country = Country.query.first()
    db_region = Region.query.first()
    db_producer = Producer.query.first()
    db_grape = Grape.query.first()
    db_wine = Wine.query.first()
    db_wine_type = Wine_type.query.first()

    # Check all relationships are set correctly
    assert db_wine in db_wine_type.wines
    assert db_wine.wine_type == db_wine_type
    assert db_wine.grape == grape
    assert db_wine.producer == producer
    assert db_wine in db_grape.wines
    assert db_grape.region == db_region
    assert db_producer.region == db_region
    assert db_wine in db_producer.wines
    assert db_region.country == db_country
    assert db_grape in db_region.grapes
    assert db_producer in db_region.producers
    assert db_region in db_country.regions


def test_wine_type_relations_on_deletion(db_handle):
    """
    Tests that wine type's relations are set to none or empty when the item
    is deleted.
    """

    wine_type = _get_wine_type()
    wine = _get_wine()
    wine_type.wines.append(wine)
    db_handle.session.add(wine_type)
    db_handle.session.commit()
    db_handle.session.delete(wine)
    db_handle.session.commit()

    assert wine not in wine_type.wines


def test_wine_relations_on_deletion(db_handle):
    """
    Tests that wine's relations are set to null or empty when the item
    is deleted.
    """

    wine = _get_wine()
    grape = _get_grape()
    producer = _get_producer()
    wine_type = _get_wine_type()
    wine.grape = grape
    wine.wine_type = wine_type
    wine.producer = producer
    db_handle.session.add(wine)
    db_handle.session.commit()
    db_handle.session.delete(grape)
    db_handle.session.delete(producer)
    db_handle.session.delete(wine_type)
    db_handle.session.commit()

    assert wine.grape is None
    assert wine.wine_type is None
    assert wine.producer is None


def test_grape_relations_on_deletion(db_handle):
    """
    Tests that grape's relations are set to none or empty when the item
    is deleted.
    """

    grape = _get_grape()
    region = _get_region()
    wine = _get_wine()
    grape.region = region
    grape.wines.append(wine)
    db_handle.session.add(grape)
    db_handle.session.commit()
    db_handle.session.delete(wine)
    db_handle.session.delete(region)
    db_handle.session.commit()

    assert wine not in grape.wines
    assert grape.region is None


def test_producer_relations_on_deletion(db_handle):
    """
    Tests that wine type's relations are set to none or empty when the item
    is deleted.
    """

    producer = _get_producer()
    wine = _get_wine()
    region = _get_region()
    producer.wines.append(wine)
    producer.region = region
    db_handle.session.add(producer)
    db_handle.session.commit()
    db_handle.session.delete(wine)
    db_handle.session.delete(region)
    db_handle.session.commit()

    assert producer.region is None
    assert wine not in producer.wines


def test_region_relations_on_deletion(db_handle):
    """
    Tests that region's relations are set to none or empty when the item
    is deleted.
    """

    region = _get_region()
    grape = _get_grape()
    producer = _get_producer()
    country = _get_country()
    region.country = country
    region.grapes.append(grape)
    region.producers.append(producer)
    db_handle.session.add(region)
    db_handle.session.commit()
    db_handle.session.delete(grape)
    db_handle.session.delete(producer)
    db_handle.session.delete(country)
    db_handle.session.commit()

    assert region.country is None
    assert grape not in region.grapes
    assert producer not in region.producers


def test_country_relations_on_deletion(db_handle):
    """
    Tests that country's relations are set to none or empty when the item
    is deleted.
    """

    country = _get_country()
    region = _get_region()
    country.regions.append(region)
    db_handle.session.add(country)
    db_handle.session.commit()
    db_handle.session.delete(region)
    db_handle.session.commit()

    assert region not in country.regions


def test_wine_required_columns(db_handle):
    """
    Tests that required columns in the wine.
    """

    wine = _get_wine()
    wine.name = None
    db_handle.session.add(wine)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()


def test_wine_type_required_columns(db_handle):
    """
    Tests that required columns in the wine type.
    """

    wine_type = _get_wine_type()
    wine_type.type = None
    db_handle.session.add(wine_type)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()


def test_grape_required_columns(db_handle):
    """
    Tests that required columns in the grape.
    """

    grape = _get_grape()
    grape.name = None
    db_handle.session.add(grape)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()


def test_region_required_columns(db_handle):
    """
    Tests that required columns in the region.
    """

    region = _get_region()
    region.name = None
    db_handle.session.add(region)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()


def test_country_required_columns(db_handle):
    """
    Tests that required columns in the country.
    """

    country = _get_country()
    country.name = None
    db_handle.session.add(country)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()


def test_user_required_columns(db_handle):
    """
    Tests that required columns in the user.
    """

    user = _get_user()
    user.username = None
    db_handle.session.add(user)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()

    db_handle.session.rollback()

    user = _get_user()
    user.password = None
    db_handle.session.add(user)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()
