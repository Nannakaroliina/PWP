import json

from src.schemas.schemas import WineSchema
from test.unit.conftest import client

wine_schema = WineSchema()
wine_list_schema = WineSchema(many=True)


def _get_access_token(client):

    data = {
        "username": "tester",
        "password": "Test-password1234"
    }

    client.post("/api/register", json=data)
    response = client.post("/api/login", json=data)
    return json.loads(response.data)


def test_homepage(client):
    response = client.get('/')
    homepage = response.data.decode()

    assert response.status_code == 200
    assert "Hello, world!" in homepage


class TestWineCollection(object):

    RESOURCE_URL = "/api/wines"

    def test_get(self, client):
        response = client.get(self.RESOURCE_URL)
        assert response.status_code == 200
        body = json.loads(response.data)
        assert len(body["wines"]) == 3
        for wine in body["wines"]:
            assert "name" in wine
            assert "volume" in wine
            assert "description" in wine
            assert "wine_type" in wine
            assert "picture" in wine
            assert "producer" in wine
            assert "grape" in wine
            assert "year_produced" in wine
            assert "style" in wine
            assert "alcohol_percentage" in wine

    def test_post(self, client):
        request_data = {
            "name": "test",
            "description": "test",
            "style": "test",
            "volume": 750,
            "picture": "no real picture",
            "year_produced": 2022,
            "alcohol_percentage": 22,
            "wine_type": {
                "type": "test"
            },
            "producer": {
                "name": "test"
            },
            "grape": {
                "name": "test"
            }
        }

        token = _get_access_token(client)
        headers = {'Authorization': token}
        data = {
            'data': json.dumps(request_data),
            'file': None
        }
        response = client.post(self.RESOURCE_URL, data=data, headers=headers)
        assert response.status_code == 201
        body = json.loads(response.data)
        assert body["name"] == request_data["name"]
        assert body["description"] == request_data["description"]
        assert body["style"] == request_data["style"]
        assert body["volume"] == request_data["volume"]
        assert body["picture"] == request_data["picture"]
        assert body["year_produced"] == request_data["year_produced"]
        assert body["alcohol_percentage"] == request_data["alcohol_percentage"]
        assert body["wine_type"]["type"] == request_data["wine_type"]["type"]
        assert body["producer"]["name"] == request_data["producer"]["name"]
        assert body["grape"]["name"] == request_data["grape"]["name"]

    def test_invalid_data_post(self, client):
        token = _get_access_token(client)
        headers = {'Authorization': token}
        data = {
            'data': json.dumps({}),
            'file': None
        }
        response = client.post(self.RESOURCE_URL, data=data, headers=headers)
        assert response.status_code == 400

    def test_validation_error_post(self, client):
        token = _get_access_token(client)
        headers = {'Authorization': token}
        data = {
            'data': json.dumps({"description": "test"}),
            'file': None
        }
        response = client.post(self.RESOURCE_URL, data=data, headers=headers)
        assert response.status_code == 400

    def test_wine_exists_post(self, client):
        token = _get_access_token(client)
        headers = {'Authorization': token}
        data = {
            'data': json.dumps({"name": "test wine 1"}),
            'file': None
        }
        response = client.post(self.RESOURCE_URL, data=data, headers=headers)
        assert response.status_code == 409

    def test_no_auth_post(self, client):
        data = {
            'data': json.dumps({"name": "test"}),
            'file': None
        }
        response = client.post(self.RESOURCE_URL, data=data)
        assert response.status_code == 401


class TestWineItem(object):

    RESOURCE_URL = "/api/wines/test%20wine%201"

    def test_get(self, client):
        response = client.get(self.RESOURCE_URL)
        assert response.status_code == 200
        body = json.loads(response.data)
        assert body is not None
        assert "name" in body
        assert "volume" in body
        assert "description" in body
        assert "wine_type" in body
        assert "picture" in body
        assert "producer" in body
        assert "grape" in body
        assert "year_produced" in body
        assert "style" in body
        assert "alcohol_percentage" in body


class TestWine_typeCollection(object):

    RESOURCE_URL = "/api/wine_types"
    request_data = {
        "type": "test"
    }

    def test_get(self, client):
        response = client.get(self.RESOURCE_URL)
        assert response.status_code == 200
        body = json.loads(response.data)
        assert len(body["wine_types"]) == 3
        for wine_type in body["wine_types"]:
            assert "type" in wine_type
            assert "wines" in wine_type

    def test_post(self, client):
        token = _get_access_token(client)
        headers = {'Authorization': token}
        response = client.post(self.RESOURCE_URL, json=self.request_data, headers=headers)
        assert response.status_code == 201
        body = json.loads(response.data)
        assert body["type"] == self.request_data["type"]

    def test_invalid_data_type_post(self, client):
        token = _get_access_token(client)
        headers = {'Authorization': token}
        response = client.post(self.RESOURCE_URL, json={}, headers=headers)
        assert response.status_code == 415

    def test_validation_error_post(self, client):
        token = _get_access_token(client)
        headers = {'Authorization': token}
        response = client.post(self.RESOURCE_URL, json={"description": "test"}, headers=headers)
        assert response.status_code == 400

    def test_wine_type_exists_post(self, client):
        request_data = {
            "type": "test type 1"
        }

        token = _get_access_token(client)
        headers = {'Authorization': token}
        response = client.post(self.RESOURCE_URL, json=request_data, headers=headers)
        assert response.status_code == 409

    def test_no_auth_post(self, client):
        response = client.post(self.RESOURCE_URL, json=self.request_data)
        assert response.status_code == 401


class TestWine_typeItem(object):

    RESOURCE_URL = "/api/wine_type/test%20type%201"

    def test_get(self, client):
        response = client.get(self.RESOURCE_URL)
        assert response.status_code == 200
        body = json.loads(response.data)
        assert body is not None
        assert "type" in body
        assert "wines" in body


class TestProducerCollection(object):

    RESOURCE_URL = "/api/producers"
    request_data = {
        "name": "test",
        "description": "test",
        "region": {
            "name": "test"
        }
    }

    def test_get(self, client):
        response = client.get(self.RESOURCE_URL)
        assert response.status_code == 200
        body = json.loads(response.data)
        assert len(body["producers"]) == 3
        for producer in body["producers"]:
            assert "name" in producer
            assert "description" in producer
            assert "region" in producer
            assert "wines" in producer

    def test_post(self, client):
        token = _get_access_token(client)
        headers = {'Authorization': token}
        response = client.post(self.RESOURCE_URL, json=self.request_data, headers=headers)
        assert response.status_code == 201
        body = json.loads(response.data)
        assert body["name"] == self.request_data["name"]
        assert body["description"] == self.request_data["description"]
        assert body["region"]["name"] == self.request_data["region"]["name"]

    def test_invalid_data_type_post(self, client):
        token = _get_access_token(client)
        headers = {'Authorization': token}
        response = client.post(self.RESOURCE_URL, data={}, headers=headers)
        assert response.status_code == 415

    def test_validation_error_post(self, client):
        token = _get_access_token(client)
        headers = {'Authorization': token}
        response = client.post(self.RESOURCE_URL, json={"description": "test"}, headers=headers)
        assert response.status_code == 400

    def test_producer_exists_post(self, client):
        request_data = {
            "name": "test producer 1"
        }

        token = _get_access_token(client)
        headers = {'Authorization': token}
        response = client.post(self.RESOURCE_URL, json=request_data, headers=headers)
        assert response.status_code == 409

    def test_no_auth_post(self, client):
        response = client.post(self.RESOURCE_URL, json=self.request_data)
        assert response.status_code == 401


class TestProducerItem(object):

    RESOURCE_URL = "/api/producers/test%20producer%201"

    def test_get(self, client):
        response = client.get(self.RESOURCE_URL)
        assert response.status_code == 200
        body = json.loads(response.data)
        assert body is not None
        assert "name" in body
        assert "description" in body
        assert "region" in body
        assert "wines" in body


class TestGrapeCollection(object):

    RESOURCE_URL = "/api/grapes"
    request_data = {
        "name": "test",
        "description": "test",
        "region": {
            "name": "test"
        }
    }

    def test_get(self, client):
        response = client.get(self.RESOURCE_URL)
        assert response.status_code == 200
        body = json.loads(response.data)
        assert len(body["grapes"]) == 3
        for grape in body["grapes"]:
            assert "name" in grape
            assert "description" in grape
            assert "region" in grape
            assert "wines" in grape

    def test_post(self, client):
        token = _get_access_token(client)
        headers = {'Authorization': token}
        response = client.post(self.RESOURCE_URL, json=self.request_data, headers=headers)
        assert response.status_code == 201
        body = json.loads(response.data)
        assert body["name"] == self.request_data["name"]
        assert body["description"] == self.request_data["description"]
        assert body["region"]["name"] == self.request_data["region"]["name"]

    def test_invalid_data_type_post(self, client):
        token = _get_access_token(client)
        headers = {'Authorization': token}
        response = client.post(self.RESOURCE_URL, data={}, headers=headers)
        assert response.status_code == 415

    def test_validation_error_post(self, client):
        token = _get_access_token(client)
        headers = {'Authorization': token}
        response = client.post(self.RESOURCE_URL, json={"description": "test"}, headers=headers)
        assert response.status_code == 400

    def test_grape_exists_post(self, client):
        request_data = {
            "name": "test grape 1"
        }

        token = _get_access_token(client)
        headers = {'Authorization': token}
        response = client.post(self.RESOURCE_URL, json=request_data, headers=headers)
        assert response.status_code == 409

    def test_no_auth_post(self, client):
        response = client.post(self.RESOURCE_URL, json=self.request_data)
        assert response.status_code == 401


class TestGrapeItem(object):

    RESOURCE_URL = "/api/grapes/test%20grape%201"

    def test_get(self, client):
        response = client.get(self.RESOURCE_URL)
        assert response.status_code == 200
        body = json.loads(response.data)
        assert body is not None
        assert "name" in body
        assert "description" in body
        assert "region" in body
        assert "wines" in body


class TestRegionCollection(object):

    RESOURCE_URL = "/api/regions"
    request_data = {
        "name": "test",
        "country": {
            "name": "test"
        }
    }

    def test_get(self, client):
        response = client.get(self.RESOURCE_URL)
        assert response.status_code == 200
        body = json.loads(response.data)
        assert len(body["regions"]) == 3
        for region in body["regions"]:
            assert "name" in region
            assert "producers" in region
            assert "country" in region
            assert "grapes" in region

    def test_post(self, client):
        token = _get_access_token(client)
        headers = {'Authorization': token}
        response = client.post(self.RESOURCE_URL, json=self.request_data, headers=headers)
        assert response.status_code == 201
        body = json.loads(response.data)
        assert body["name"] == self.request_data["name"]
        assert body["country"]["name"] == self.request_data["country"]["name"]

    def test_invalid_data_type_post(self, client):
        token = _get_access_token(client)
        headers = {'Authorization': token}
        response = client.post(self.RESOURCE_URL, data={}, headers=headers)
        assert response.status_code == 415

    def test_validation_error_post(self, client):
        token = _get_access_token(client)
        headers = {'Authorization': token}
        response = client.post(self.RESOURCE_URL, json={"description": "test"}, headers=headers)
        assert response.status_code == 400

    def test_region_exists_post(self, client):
        request_data = {
            "name": "test region 1"
        }

        token = _get_access_token(client)
        headers = {'Authorization': token}
        response = client.post(self.RESOURCE_URL, json=request_data, headers=headers)
        assert response.status_code == 409

    def test_no_auth_post(self, client):
        response = client.post(self.RESOURCE_URL, json=self.request_data)
        assert response.status_code == 401


class TestRegionItem(object):

    RESOURCE_URL = "/api/regions/test%20region%201"

    def test_get(self, client):
        response = client.get(self.RESOURCE_URL)
        assert response.status_code == 200
        body = json.loads(response.data)
        assert body is not None
        assert "name" in body
        assert "producers" in body
        assert "country" in body
        assert "grapes" in body


class TestCountryCollection(object):

    RESOURCE_URL = "/api/countries"
    request_data = {
        "name": "test"
    }

    def test_get(self, client):
        response = client.get(self.RESOURCE_URL)
        assert response.status_code == 200
        body = json.loads(response.data)
        assert len(body["countries"]) == 3
        for country in body["countries"]:
            assert "name" in country
            assert "regions" in country

    def test_post(self, client):
        token = _get_access_token(client)
        headers = {'Authorization': token}
        response = client.post(self.RESOURCE_URL, json=self.request_data, headers=headers)
        assert response.status_code == 201
        body = json.loads(response.data)
        assert body["name"] == self.request_data["name"]

    def test_invalid_data_type_post(self, client):
        token = _get_access_token(client)
        headers = {'Authorization': token}
        response = client.post(self.RESOURCE_URL, data={}, headers=headers)
        assert response.status_code == 415

    def test_validation_error_post(self, client):
        token = _get_access_token(client)
        headers = {'Authorization': token}
        response = client.post(self.RESOURCE_URL, json={"description": "test"}, headers=headers)
        assert response.status_code == 400

    def test_country_exists_post(self, client):
        request_data = {
            "name": "test country 1"
        }

        token = _get_access_token(client)
        headers = {'Authorization': token}
        response = client.post(self.RESOURCE_URL, json=request_data, headers=headers)
        assert response.status_code == 409

    def test_no_auth_post(self, client):
        response = client.post(self.RESOURCE_URL, json=self.request_data)
        assert response.status_code == 401


class TestCountryItem(object):

    RESOURCE_URL = "/api/countries/test%20country%201"

    def test_get(self, client):
        response = client.get(self.RESOURCE_URL)
        assert response.status_code == 200
        body = json.loads(response.data)
        assert body is not None
        assert "name" in body
        assert "regions" in body