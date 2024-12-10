import sys
import os
import pytest
import json
import logging


basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, basedir)
os.chdir(basedir)
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client: yield client

def test_game_page(client):
    response = client.get('/game_page/440')
    assert response.status_code == 200

def test_non_game_page(client):
    response = client.get('/game_page/441')
    assert response.status_code == 200

def test_index(client):
    response = client.get('/index')
    assert response.status_code == 200

def test_contact(client):
    response = client.get('/contact')
    assert response.status_code == 200




def test_about(client):
    response = client.get('/about')
    assert response.status_code == 200

def test_get_available_games_index_percent(client):
    data = {
        "game": "The Elder Scrolls V Skyrim",
        "percent": None,
        'tags': ""
    }
    response = client.post(
        '/get_available_games_index',
        json=data,
        content_type='application/json'
    )
    response_json = response.get_json()
    assert response.status_code == 200
    assert 'games' in response_json
    assert isinstance(response_json['games'], list)

def test_get_available_games_index_normal(client):
    data = {
        "game": "The Elder Scrolls V Skyrim",
        "percent": 70,
        'tags': "Action"
    }
    response = client.post(
        '/get_available_games_index',
        json=data,
        content_type='application/json'
    )
    response_json = response.get_json()
    assert response.status_code == 200
    assert 'games' in response_json
    assert isinstance(response_json['games'], list)

def test_get_available_games_index_empty_tags(client):
    data = {
        "game": "The Elder Scrolls V Skyrim",
        "percent": 70,
        'tags': ""
    }
    response = client.post(
        '/get_available_games_index',
        json=data,
        content_type='application/json'
    )
    response_json = response.get_json()
    assert response.status_code == 200
    assert 'games' in response_json
    assert isinstance(response_json['games'], list)


#rec page:
def test_get_available_games(client):
    response = client.get('/get_available_games')
    assert response.status_code == 200
    data = response.get_json()
    assert 'games' in data
    assert isinstance(data['games'], list)

def test_get_recommendations(client):
    data = {
        "1... 2... 3... KICK IT! (Drop That Beat Like an Ugly Baby)": 30,
        "1Heart": 42,
        "A Game of Thrones - Genesis": 35,
        "1953 NATO vs Warsaw Pact": 15,
        "0RBITALIS": 80
    }

    response = client.post(
        '/get_recommendations',
        data=json.dumps(data),
        content_type='application/json'
    )
    response_json = response.get_json()
    print(response_json)
    assert response.status_code == 200
    assert 'games' in response_json
    assert isinstance(response_json['games'], list)

#contact page:
def test_get_available_games(client):
    data = {
        'name': 'Greg',
        'email': 'greg@example.com',
        'message': 'Greg'
    }

    response = client.post('/saveMessage', json=data)
    assert response.status_code == 200
    assert response.json['message'] == 'Contact saved successfully'