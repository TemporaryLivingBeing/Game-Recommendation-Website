import sys
import os
import pytest

sys.path.insert(0, '/Users/jacksbigmac/Downloads/Game-Recommendation-Website/app')
os.chdir('/Users/jacksbigmac/Downloads/Game-Recommendation-Website/app')
from app import app

@pytest.fixture
def client():
    with app.test_client() as client: yield client

def test_some_route(client):
    response = client.get('/www/game_page/440')
    assert response.status_code == 200