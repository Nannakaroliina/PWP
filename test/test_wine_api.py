"""
Module for API testing
"""
import json
from copy import deepcopy

from src.schemas.schemas import WineSchema
from test.conftest import client  # pylint: disable=unused-import

wine_schema = WineSchema()
wine_list_schema = WineSchema(many=True)


def _get_access_token_header(client):

    data = {
        "username": "tester",
        "password": "Test-password1234",
        "role": "developer"
    }

    client.post("/api/register", json=data)
    response = client.post("/api/login", json=data)
    headers = {'Authorization': json.loads(response.data)}
    return headers


def _get_resource(client, resource_url):
    response = client.get(resource_url)
    return json.loads(response.data)


def test_homepage(client):
    response = client.get('/')
    homepage = response.data.decode()

    assert response.status_code == 200
    assert "Welcome to Wine Time" in homepage


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

        headers = _get_access_token_header(client)
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
        headers = _get_access_token_header(client)
        data = {
            'data': json.dumps({}),
            'file': None
        }
        response = client.post(self.RESOURCE_URL, data=data, headers=headers)
        assert response.status_code == 400

    def test_validation_error_post(self, client):
        headers = _get_access_token_header(client)
        data = {
            'data': json.dumps({"description": "test"}),
            'file': None
        }
        response = client.post(self.RESOURCE_URL, data=data, headers=headers)
        assert response.status_code == 400

    def test_wine_exists_post(self, client):
        headers = _get_access_token_header(client)
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

    RESOURCE_URL = "/api/wines"
    WINE_URL = RESOURCE_URL + '/test%20wine%201'
    FAKE_URL = RESOURCE_URL + '/test%20wine%206'

    request_data = {
        "description": "patching"
    }

    data = {
        'data': json.dumps(request_data),
        'file': None
    }

    def test_get(self, client):
        response = client.get(self.WINE_URL)
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

    def test_get_not_found(self, client):
        response = client.get(self.FAKE_URL)
        assert response.status_code == 404

    def test_delete(self, client):
        headers = _get_access_token_header(client)
        response = client.delete(self.WINE_URL, headers=headers)
        assert response.status_code == 200
        wines = _get_resource(client, self.RESOURCE_URL)
        assert len(wines) == 1

    def test_not_found_on_deletion(self, client):
        headers = _get_access_token_header(client)
        response = client.delete(self.FAKE_URL, headers=headers)
        assert response.status_code == 404

    def test_delete_no_auth(self, client):
        response = client.delete(self.WINE_URL, data=self.data)
        assert response.status_code == 401

    def test_patch(self, client):
        headers = _get_access_token_header(client)
        response = client.patch(self.WINE_URL, data=self.data, headers=headers)
        assert response.status_code == 200
        wine = _get_resource(client, self.WINE_URL)
        assert wine["description"] == "patching"

    def test_patch_not_found(self, client):
        headers = _get_access_token_header(client)
        response = client.patch(self.FAKE_URL, data=self.data, headers=headers)
        assert response.status_code == 404

    def test_patch_producer_not_found(self, client):
        request_data = {
            "producer": {
                "name": "fake producer"
            }
        }

        self.data['data'] = json.dumps(request_data)
        headers = _get_access_token_header(client)
        response = client.patch(self.WINE_URL, data=self.data, headers=headers)
        assert response.status_code == 404

    def test_patch_validation_error(self, client):
        request_data = {
            "producer": {
                "description": "test validation fail"
            }
        }
        self.data['data'] = json.dumps(request_data)
        headers = _get_access_token_header(client)
        response = client.patch(self.WINE_URL, data=self.data, headers=headers)
        assert response.status_code == 400

    def test_patch_no_auth(self, client):
        response = client.patch(self.WINE_URL, data=self.data)
        assert response.status_code == 401


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
        headers = _get_access_token_header(client)
        response = client.post(self.RESOURCE_URL, json=self.request_data, headers=headers)
        assert response.status_code == 201
        body = json.loads(response.data)
        assert body["type"] == self.request_data["type"]

    def test_invalid_data_type_post(self, client):
        headers = _get_access_token_header(client)
        response = client.post(self.RESOURCE_URL, json={}, headers=headers)
        assert response.status_code == 415

    def test_validation_error_post(self, client):
        headers = _get_access_token_header(client)
        response = client.post(self.RESOURCE_URL, json={"description": "test"}, headers=headers)
        assert response.status_code == 400

    def test_wine_type_exists_post(self, client):
        request_data = {
            "type": "test type 1"
        }

        headers = _get_access_token_header(client)
        response = client.post(self.RESOURCE_URL, json=request_data, headers=headers)
        assert response.status_code == 409

    def test_no_auth_post(self, client):
        response = client.post(self.RESOURCE_URL, json=self.request_data)
        assert response.status_code == 401


class TestWine_typeItem(object):

    RESOURCE_URL = "/api/wine_types"
    WINE_TYPE_URL = RESOURCE_URL + "/test%20type%201"
    FAKE_URL = RESOURCE_URL + "/test%20type%206"
    request_data = {
        "type": "new type"
    }

    def test_get(self, client):
        response = client.get(self.WINE_TYPE_URL)
        assert response.status_code == 200
        body = json.loads(response.data)
        assert body is not None
        assert "type" in body
        assert "wines" in body

    def test_get_not_found(self, client):
        response = client.get(self.FAKE_URL)
        assert response.status_code == 404

    def test_delete(self, client):
        headers = _get_access_token_header(client)
        response = client.delete(self.WINE_TYPE_URL, headers=headers)
        assert response.status_code == 200
        wine_types = _get_resource(client, self.RESOURCE_URL)
        assert len(wine_types) == 1

    def test_not_found_on_deletion(self, client):
        headers = _get_access_token_header(client)
        response = client.delete(self.FAKE_URL, headers=headers)
        assert response.status_code == 404

    def test_delete_no_auth(self, client):
        response = client.delete(self.WINE_TYPE_URL, json=self.request_data)
        assert response.status_code == 401

    def test_patch(self, client):
        headers = _get_access_token_header(client)
        response = client.patch(self.WINE_TYPE_URL, json=self.request_data, headers=headers)
        assert response.status_code == 200
        wine_type = _get_resource(client, self.RESOURCE_URL + "/new%20type")
        assert wine_type["type"] == "new type"

    def test_patch_not_found(self, client):
        headers = _get_access_token_header(client)
        response = client.patch(self.FAKE_URL, json=self.request_data, headers=headers)
        assert response.status_code == 404

    def test_patch_validation_error(self, client):
        request_data = {
            "description": "test validation fail"
        }

        headers = _get_access_token_header(client)
        response = client.patch(self.WINE_TYPE_URL, json=request_data, headers=headers)
        assert response.status_code == 400

    def test_patch_no_auth(self, client):
        response = client.patch(self.WINE_TYPE_URL, json=self.request_data)
        assert response.status_code == 401


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
        headers = _get_access_token_header(client)
        response = client.post(self.RESOURCE_URL, json=self.request_data, headers=headers)
        assert response.status_code == 201
        body = json.loads(response.data)
        assert body["name"] == self.request_data["name"]
        assert body["description"] == self.request_data["description"]
        assert body["region"]["name"] == self.request_data["region"]["name"]

    def test_invalid_data_type_post(self, client):
        headers = _get_access_token_header(client)
        response = client.post(self.RESOURCE_URL, data={}, headers=headers)
        assert response.status_code == 415

    def test_validation_error_post(self, client):
        headers = _get_access_token_header(client)
        response = client.post(self.RESOURCE_URL, json={"description": "test"}, headers=headers)
        assert response.status_code == 400

    def test_producer_exists_post(self, client):
        request_data = {
            "name": "test producer 1"
        }

        headers = _get_access_token_header(client)
        response = client.post(self.RESOURCE_URL, json=request_data, headers=headers)
        assert response.status_code == 409

    def test_no_auth_post(self, client):
        response = client.post(self.RESOURCE_URL, json=self.request_data)
        assert response.status_code == 401


class TestProducerItem(object):

    RESOURCE_URL = "/api/producers"
    PRODUCER_URL = RESOURCE_URL + "/test%20producer%201"
    FAKE_URL = RESOURCE_URL + "/test%20producer%206"
    request_data = {
        "description": "patching"
    }

    def test_get(self, client):
        response = client.get(self.PRODUCER_URL)
        assert response.status_code == 200
        body = json.loads(response.data)
        assert body is not None
        assert "name" in body
        assert "description" in body
        assert "region" in body
        assert "wines" in body

    def test_get_not_found(self, client):
        response = client.get(self.FAKE_URL)
        assert response.status_code == 404

    def test_delete(self, client):
        headers = _get_access_token_header(client)
        response = client.delete(self.PRODUCER_URL, headers=headers)
        assert response.status_code == 200
        producers = _get_resource(client, self.RESOURCE_URL)
        assert len(producers) == 1

    def test_not_found_on_deletion(self, client):
        headers = _get_access_token_header(client)
        response = client.delete(self.FAKE_URL, headers=headers)
        assert response.status_code == 404

    def test_delete_no_auth(self, client):
        response = client.delete(self.PRODUCER_URL, json=self.request_data)
        assert response.status_code == 401

    def test_patch(self, client):
        headers = _get_access_token_header(client)
        response = client.patch(self.PRODUCER_URL, json=self.request_data, headers=headers)
        assert response.status_code == 200
        producer = _get_resource(client, self.PRODUCER_URL)
        assert producer["description"] == "patching"

    def test_patch_not_found(self, client):
        headers = _get_access_token_header(client)
        response = client.patch(self.FAKE_URL, json=self.request_data, headers=headers)
        assert response.status_code == 404

    def test_patch_region_not_found(self, client):
        request_data = {
            "region": {
                "name": "fake region"
            }
        }

        headers = _get_access_token_header(client)
        response = client.patch(self.PRODUCER_URL, json=request_data, headers=headers)
        assert response.status_code == 404

    def test_patch_validation_error(self, client):
        request_data = {
            "wine": {
                "description": "test validation fail"
            }
        }

        headers = _get_access_token_header(client)
        response = client.patch(self.PRODUCER_URL, json=request_data, headers=headers)
        assert response.status_code == 400

    def test_patch_no_auth(self, client):
        response = client.patch(self.PRODUCER_URL, json=self.request_data)
        assert response.status_code == 401


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
        headers = _get_access_token_header(client)
        response = client.post(self.RESOURCE_URL, json=self.request_data, headers=headers)
        assert response.status_code == 201
        body = json.loads(response.data)
        assert body["name"] == self.request_data["name"]
        assert body["description"] == self.request_data["description"]
        assert body["region"]["name"] == self.request_data["region"]["name"]

    def test_invalid_data_type_post(self, client):
        headers = _get_access_token_header(client)
        response = client.post(self.RESOURCE_URL, data={}, headers=headers)
        assert response.status_code == 415

    def test_validation_error_post(self, client):
        headers = _get_access_token_header(client)
        response = client.post(self.RESOURCE_URL, json={"description": "test"}, headers=headers)
        assert response.status_code == 400

    def test_grape_exists_post(self, client):
        request_data = {
            "name": "test grape 1"
        }

        headers = _get_access_token_header(client)
        response = client.post(self.RESOURCE_URL, json=request_data, headers=headers)
        assert response.status_code == 409

    def test_no_auth_post(self, client):
        response = client.post(self.RESOURCE_URL, json=self.request_data)
        assert response.status_code == 401


class TestGrapeItem(object):

    RESOURCE_URL = "/api/grapes"
    GRAPE_URL = RESOURCE_URL + "/test%20grape%201"
    FAKE_URL = RESOURCE_URL + "/test%20grape%206"
    request_data = {
        "description": "patching"
    }

    def test_get(self, client):
        response = client.get(self.GRAPE_URL)
        assert response.status_code == 200
        body = json.loads(response.data)
        assert body is not None
        assert "name" in body
        assert "description" in body
        assert "region" in body
        assert "wines" in body

    def test_get_not_found(self, client):
        response = client.get(self.FAKE_URL)
        assert response.status_code == 404

    def test_delete(self, client):
        headers = _get_access_token_header(client)
        response = client.delete(self.GRAPE_URL, headers=headers)
        assert response.status_code == 200
        grapes = _get_resource(client, self.RESOURCE_URL)
        assert len(grapes) == 1

    def test_not_found_on_deletion(self, client):
        headers = _get_access_token_header(client)
        response = client.delete(self.FAKE_URL, headers=headers)
        assert response.status_code == 404

    def test_delete_no_auth(self, client):
        response = client.delete(self.GRAPE_URL, json=self.request_data)
        assert response.status_code == 401

    def test_patch(self, client):
        headers = _get_access_token_header(client)
        response = client.patch(self.GRAPE_URL, json=self.request_data, headers=headers)
        assert response.status_code == 200
        grape = _get_resource(client, self.GRAPE_URL)
        assert grape["description"] == "patching"

    def test_patch_not_found(self, client):
        headers = _get_access_token_header(client)
        response = client.patch(self.FAKE_URL, json=self.request_data, headers=headers)
        assert response.status_code == 404

    def test_patch_region_not_found(self, client):
        request_data = {
            "region": {
                "name": "fake region"
            }
        }

        headers = _get_access_token_header(client)
        response = client.patch(self.GRAPE_URL, json=request_data, headers=headers)
        assert response.status_code == 404

    def test_patch_validation_error(self, client):
        request_data = {
            "region": {
                "description": "test validation fail"
            }
        }

        headers = _get_access_token_header(client)
        response = client.patch(self.GRAPE_URL, json=request_data, headers=headers)
        assert response.status_code == 400

    def test_patch_no_auth(self, client):
        response = client.patch(self.GRAPE_URL, json=self.request_data)
        assert response.status_code == 401


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
        headers = _get_access_token_header(client)
        response = client.post(self.RESOURCE_URL, json=self.request_data, headers=headers)
        assert response.status_code == 201
        body = json.loads(response.data)
        assert body["name"] == self.request_data["name"]
        assert body["country"]["name"] == self.request_data["country"]["name"]

    def test_invalid_data_type_post(self, client):
        headers = _get_access_token_header(client)
        response = client.post(self.RESOURCE_URL, data={}, headers=headers)
        assert response.status_code == 415

    def test_validation_error_post(self, client):
        headers = _get_access_token_header(client)
        response = client.post(self.RESOURCE_URL, json={"description": "test"}, headers=headers)
        assert response.status_code == 400

    def test_region_exists_post(self, client):
        request_data = {
            "name": "test region 1"
        }

        headers = _get_access_token_header(client)
        response = client.post(self.RESOURCE_URL, json=request_data, headers=headers)
        assert response.status_code == 409

    def test_no_auth_post(self, client):
        response = client.post(self.RESOURCE_URL, json=self.request_data)
        assert response.status_code == 401


class TestRegionItem(object):

    RESOURCE_URL = "/api/regions"
    REGION_URL = RESOURCE_URL + "/test%20region%201"
    FAKE_URL = RESOURCE_URL + "/test%20region%206"
    request_data = {
        "country": {
            "name": "test country 1"
        }
    }

    def test_get(self, client):
        response = client.get(self.REGION_URL)
        assert response.status_code == 200
        body = json.loads(response.data)
        assert body is not None
        assert "name" in body
        assert "producers" in body
        assert "country" in body
        assert "grapes" in body

    def test_get_not_found(self, client):
        response = client.get(self.FAKE_URL)
        assert response.status_code == 404

    def test_delete(self, client):
        headers = _get_access_token_header(client)
        response = client.delete(self.REGION_URL, headers=headers)
        assert response.status_code == 200
        regions = _get_resource(client, self.RESOURCE_URL)
        assert len(regions) == 1

    def test_not_found_on_deletion(self, client):
        headers = _get_access_token_header(client)
        response = client.delete(self.FAKE_URL, headers=headers)
        assert response.status_code == 404

    def test_delete_no_auth(self, client):
        response = client.delete(self.REGION_URL, json=self.request_data)
        assert response.status_code == 401

    def test_patch(self, client):
        headers = _get_access_token_header(client)
        response = client.patch(self.REGION_URL, json=self.request_data, headers=headers)
        assert response.status_code == 200
        region = _get_resource(client, self.REGION_URL)
        assert region["country"]["name"] == "test country 1"

    def test_patch_not_found(self, client):
        headers = _get_access_token_header(client)
        response = client.patch(self.FAKE_URL, json=self.request_data, headers=headers)
        assert response.status_code == 404

    def test_patch_country_not_found(self, client):
        request_data = {
            "country": {
                "name": "fake region"
            }
        }

        headers = _get_access_token_header(client)
        response = client.patch(self.REGION_URL, json=request_data, headers=headers)
        assert response.status_code == 404

    def test_patch_validation_error(self, client):
        request_data = {
            "region": {
                "description": "test validation fail"
            }
        }

        headers = _get_access_token_header(client)
        response = client.patch(self.REGION_URL, json=request_data, headers=headers)
        assert response.status_code == 400

    def test_patch_no_auth(self, client):
        response = client.patch(self.REGION_URL, json=self.request_data)
        assert response.status_code == 401


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
        headers = _get_access_token_header(client)
        response = client.post(self.RESOURCE_URL, json=self.request_data, headers=headers)
        assert response.status_code == 201
        body = json.loads(response.data)
        assert body["name"] == self.request_data["name"]

    def test_invalid_data_type_post(self, client):
        headers = _get_access_token_header(client)
        response = client.post(self.RESOURCE_URL, data={}, headers=headers)
        assert response.status_code == 415

    def test_validation_error_post(self, client):
        headers = _get_access_token_header(client)
        response = client.post(self.RESOURCE_URL, json={"description": "test"}, headers=headers)
        assert response.status_code == 400

    def test_country_exists_post(self, client):
        request_data = {
            "name": "test country 1"
        }

        headers = _get_access_token_header(client)
        response = client.post(self.RESOURCE_URL, json=request_data, headers=headers)
        assert response.status_code == 409

    def test_no_auth_post(self, client):
        response = client.post(self.RESOURCE_URL, json=self.request_data)
        assert response.status_code == 401


class TestCountryItem(object):

    RESOURCE_URL = "/api/countries"
    COUNTRY_URL = RESOURCE_URL + "/test%20country%201"
    FAKE_URL = RESOURCE_URL + "/test%20country%206"
    request_data = {
        "name": "new name"
    }

    def test_get(self, client):
        response = client.get(self.COUNTRY_URL)
        assert response.status_code == 200
        body = json.loads(response.data)
        assert body is not None
        assert "name" in body
        assert "regions" in body

    def test_get_not_found(self, client):
        response = client.get(self.FAKE_URL)
        assert response.status_code == 404

    def test_delete(self, client):
        headers = _get_access_token_header(client)
        response = client.delete(self.COUNTRY_URL, headers=headers)
        assert response.status_code == 200
        countries = _get_resource(client, self.RESOURCE_URL)
        assert len(countries) == 1

    def test_not_found_on_deletion(self, client):
        headers = _get_access_token_header(client)
        response = client.delete(self.FAKE_URL, headers=headers)
        assert response.status_code == 404

    def test_delete_no_auth(self, client):
        response = client.delete(self.COUNTRY_URL, json=self.request_data)
        assert response.status_code == 401

    def test_patch(self, client):
        headers = _get_access_token_header(client)
        response = client.patch(self.COUNTRY_URL, json=self.request_data, headers=headers)
        assert response.status_code == 200
        country = _get_resource(client, self.RESOURCE_URL + "/new%20name")
        assert country["name"] == "new name"

    def test_patch_not_found(self, client):
        headers = _get_access_token_header(client)
        response = client.patch(self.FAKE_URL, json=self.request_data, headers=headers)
        assert response.status_code == 404

    def test_patch_validation_error(self, client):
        request_data = {
            "description": "test validation fail"
        }

        headers = _get_access_token_header(client)
        response = client.patch(self.COUNTRY_URL, json=request_data, headers=headers)
        assert response.status_code == 400

    def test_patch_no_auth(self, client):
        response = client.patch(self.COUNTRY_URL, json=self.request_data)
        assert response.status_code == 401


class TestUserRegister(object):

    RESOURCE_URL = "/api/register"
    request_data = {
        "username": "test",
        "password": "test-passWord-1234",
        "email": "test@email.com",
        "role": "developer"
    }

    def test_post(self, client):
        response = client.post(self.RESOURCE_URL, json=self.request_data)
        assert response.status_code == 201
        user = _get_resource(client, "/api/user/test")
        assert user["username"] == "test"
        assert user["email"] == "test@email.com"
        assert user["role"] == "developer"

    def test_post_validation_error(self, client):
        copy = deepcopy(self.request_data)
        copy["password"] = "testi"
        response = client.post(self.RESOURCE_URL, json=copy)
        assert response.status_code == 400

    def test_post_user_exists(self, client):
        copy = deepcopy(self.request_data)
        copy["username"] = "test user 2"
        response = client.post(self.RESOURCE_URL, json=copy)
        assert response.status_code == 409


class TestUserItem(object):

    RESOURCE_URL = "/api/user"
    USER_URL = RESOURCE_URL + "/test%20user%201"
    FAKE_URL = RESOURCE_URL + "/test%20user%206"

    def test_get(self, client):
        response = client.get(self.USER_URL)
        assert response.status_code == 200
        body = json.loads(response.data)
        assert body["username"] == "test user 1"
        assert body["email"] == "testi@email.com"
        assert body["role"] == "developer"

    def test_get_not_found(self, client):
        response = client.get(self.FAKE_URL)
        assert response.status_code == 404

    def test_delete(self, client):
        headers = _get_access_token_header(client)
        response = client.delete(self.USER_URL, headers=headers)
        assert response.status_code == 200

    def test_delete_not_found(self, client):
        headers = _get_access_token_header(client)
        response = client.delete(self.FAKE_URL, headers=headers)
        assert response.status_code == 404

    def test_delete_no_auth(self, client):
        response = client.delete(self.RESOURCE_URL + "/test%20user%202")
        assert response.status_code == 401


class TestUserLogin(object):

    RESOURCE_URL = "/api/login"
    request_data = {
        "username": "test user 2",
        "password": "Test-password1234"
    }

    def test_post(self, client):
        response = client.post(self.RESOURCE_URL, json=self.request_data)
        assert response.status_code == 200
        body = json.loads(response.data)
        assert "Bearer" in body

    def test_post_not_found(self, client):
        copy = deepcopy(self.request_data)
        copy["username"] = "fake user"
        response = client.post(self.RESOURCE_URL, json=copy)
        assert response.status_code == 404

    def test_post_validation_error(self, client):
        copy = deepcopy(self.request_data)
        copy["password"] = "testi"
        response = client.post(self.RESOURCE_URL, json=copy)
        assert response.status_code == 400

    def test_post_invalid_credentials(self, client):
        copy = deepcopy(self.request_data)
        copy["username"] = "test user 2"
        copy["password"] = "Test-password1234123"
        response = client.post(self.RESOURCE_URL, json=copy)
        assert response.status_code == 401


class TestUserLogout(object):

    RESOURCE_URL = "/api/logout"

    def test_post(self, client):
        headers = _get_access_token_header(client)
        response = client.post(self.RESOURCE_URL, headers=headers)
        assert response.status_code == 200

    def test_post_no_auth(self, client):
        response = client.post(self.RESOURCE_URL)
        assert response.status_code == 401
