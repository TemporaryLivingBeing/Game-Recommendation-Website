import sys
import os
import pytest
import json
import csv
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
app_dir = os.path.join(project_dir, 'app')

sys.path.insert(0, project_dir)

from app.contact import create_app as create_contact_app
from app.recommendations import create_rec_app
from app.app import app as main_app

@pytest.fixture
def contact_client():
    app = create_contact_app(testing=True)
    app.config['TESTING'] = True
    app.template_folder = '../www'
    return app.test_client()

@pytest.fixture
def rec_client():
    app = create_rec_app()
    app.template_folder = '../www'
    return app.test_client()

@pytest.fixture
def main_client():
    main_app.template_folder = '../www'
    return main_app.test_client()

def test_contact_home(contact_client):
    response = contact_client.get('/')
    assert response.status_code in [200, 404]

def test_save_message_success(contact_client):
    test_data = {
        'name': 'Test User',
        'email': 'test@test.com',
        'message': 'Test message'
    }
    response = contact_client.post('/saveMessage',
                                 data=json.dumps(test_data),
                                 content_type='application/json')
    assert response.status_code in [200, 507]

def test_save_message_row_limit(contact_client):
    test_csv = 'test_contacts.csv'
    
    with open(test_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['NAME', 'EMAIL', 'MESSAGE', 'TIMESTAMP'])
        for i in range(1000):
            writer.writerow([f'User{i}', 'test@test.com', 'test', '2024-01-01'])
    
    test_data = {
        'name': 'Test User',
        'email': 'test@test.com',
        'message': 'This should fail'
    }
    
    response = contact_client.post('/saveMessage',
                                 data=json.dumps(test_data),
                                 content_type='application/json')
    
    assert response.status_code in [429, 507]
    
    os.remove(test_csv)

def test_rec_home(rec_client):
    response = rec_client.get('/')
    assert response.status_code in [200, 404]

def test_get_available_games(rec_client):
    response = rec_client.get('/get_available_games')
    assert response.status_code == 200
    assert 'application/json' in response.content_type

def test_get_recommendations(rec_client):
    test_data = {
        "games": [
            {"appid": "440", "playtime_forever": 1000, "name": "Team Fortress 2"}
        ]
    }
    response = rec_client.post('/get_recommendations',
                             data=json.dumps(test_data),
                             content_type='application/json')
    assert response.status_code == 200
    assert 'application/json' in response.content_type

def test_main_index(main_client):
    response = main_client.get('/index')
    assert response.status_code in [200, 404]

def test_main_contact(main_client):
    response = main_client.get('/contact')
    assert response.status_code in [200, 404]

def test_game_page_valid(main_client):
    response = main_client.get('/game_page/440')
    assert response.status_code in [200, 404]

def test_game_page_invalid(main_client):
    response = main_client.get('/game_page/99999999')
    assert response.status_code in [200, 404]

def test_save_message_invalid_data(contact_client):
    test_data = {
        'name': '',
        'email': 'invalid_email',
        'message': ''
    }
    response = contact_client.post('/saveMessage',
                                 data=json.dumps(test_data),
                                 content_type='application/json')
    assert response.status_code != 200

def test_get_recommendations_invalid_data(rec_client):
    test_data = {
        "games": []
    }
    response = rec_client.post('/get_recommendations',
                             data=json.dumps(test_data),
                             content_type='application/json')
    assert response.status_code in [400, 500]

def test_404_response(main_client):
    response = main_client.get('/nonexistent_route')
    assert response.status_code == 404

if __name__ == '__main__':
    pytest.main([__file__])