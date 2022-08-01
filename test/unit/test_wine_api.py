from test.unit.conftest import client


def test_homepage(client):
    response = client.get('/')
    homepage = response.data.decode()

    assert response.status_code == 200
    assert "Hello, world!" in homepage
