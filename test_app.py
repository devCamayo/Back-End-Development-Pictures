import pytest
from app import app
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'OK'

def test_count_empty(client):
    response = client.get('/count')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['count'] == 0

def test_get_pictures_empty(client):
    response = client.get('/pictures')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == []

def test_create_picture(client):
    new_picture = {
        'name': 'Test Picture',
        'url': 'http://example.com/pic.jpg'
    }
    response = client.post('/picture', 
                         data=json.dumps(new_picture),
                         content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == 'Test Picture'

def test_get_picture(client):
    response = client.get('/picture/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == 1

def test_update_picture(client):
    updated_data = {
        'name': 'Updated Picture',
        'url': 'http://example.com/updated.jpg'
    }
    response = client.put('/picture/1',
                         data=json.dumps(updated_data),
                         content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'Updated Picture'

def test_delete_picture(client):
    response = client.delete('/picture/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Picture deleted'
    
    # Verificar que ya no existe
    response = client.get('/picture/1')
    assert response.status_code == 404