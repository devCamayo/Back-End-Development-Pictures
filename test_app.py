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

def test_data_contains_pictures(client):
    """Verificar que después de crear imágenes, los datos existen"""
    # Crear algunas imágenes
    for i in range(3):
        client.post('/picture', 
                    data=json.dumps({'name': f'Test {i}', 'url': f'http://example.com/{i}.jpg'}),
                    content_type='application/json')
    
    response = client.get('/pictures')
    data = json.loads(response.data)
    assert len(data) == 3

def test_get_pictures_check_content_type_equals_json(client):
    """Verificar que el Content-Type es application/json"""
    response = client.get('/pictures')
    assert response.headers['Content-Type'] == 'application/json'

def test_get_single_picture_check_content_type_equals_json(client):
    """Verificar que el Content-Type para imagen individual es JSON"""
    # Crear una imagen primero
    client.post('/picture', 
                data=json.dumps({'name': 'Test', 'url': 'http://example.com/test.jpg'}),
                content_type='application/json')
    
    response = client.get('/picture/1')
    assert response.headers['Content-Type'] == 'application/json'

def test_get_pictures_response_structure(client):
    """Verificar la estructura de la respuesta JSON"""
    # Crear una imagen
    client.post('/picture', 
                data=json.dumps({'name': 'Test', 'url': 'http://example.com/test.jpg'}),
                content_type='application/json')
    
    response = client.get('/pictures')
    data = json.loads(response.data)
    
    # Verificar que cada imagen tiene los campos requeridos
    for picture in data:
        assert 'id' in picture
        assert 'name' in picture
        assert 'url' in picture
def test_post_picture(client):
    """Test para crear una nueva imagen - POST /picture"""
    new_picture = {
        'name': 'Test Picture',
        'url': 'http://example.com/test.jpg'
    }
    response = client.post('/picture', 
                         data=json.dumps(new_picture),
                         content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == 'Test Picture'
    assert data['url'] == 'http://example.com/test.jpg'
    assert 'id' in data

def test_post_picture_duplicate(client):
    """Test para crear imagen duplicada - POST /picture con datos repetidos"""
    # Primera creación
    new_picture = {
        'name': 'Duplicate Picture',
        'url': 'http://example.com/duplicate.jpg'
    }
    response1 = client.post('/picture', 
                           data=json.dumps(new_picture),
                           content_type='application/json')
    assert response1.status_code == 201
    
    # Segunda creación con mismos datos
    response2 = client.post('/picture', 
                           data=json.dumps(new_picture),
                           content_type='application/json')
    assert response2.status_code == 201
    data2 = json.loads(response2.data)
    assert data2['name'] == 'Duplicate Picture'
    # Verificar que se creó con un ID diferente
    data1 = json.loads(response1.data)
    assert data2['id'] != data1['id']

def test_update_picture_by_id(client):
    """Test para actualizar una imagen por ID - PUT /picture/<id>"""
    # Primero crear una imagen
    new_picture = {
        'name': 'Original Picture',
        'url': 'http://example.com/original.jpg'
    }
    create_response = client.post('/picture', 
                                  data=json.dumps(new_picture),
                                  content_type='application/json')
    assert create_response.status_code == 201
    created = json.loads(create_response.data)
    picture_id = created['id']
    
    # Actualizar la imagen
    updated_data = {
        'name': 'Updated Picture',
        'url': 'http://example.com/updated.jpg'
    }
    response = client.put(f'/picture/{picture_id}',
                         data=json.dumps(updated_data),
                         content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'Updated Picture'
    assert data['url'] == 'http://example.com/updated.jpg'
    assert data['id'] == picture_id

def test_delete_picture_by_id(client):
    """Test para eliminar una imagen por ID - DELETE /picture/<id>"""
    # Primero crear una imagen
    new_picture = {
        'name': 'Picture to Delete',
        'url': 'http://example.com/delete.jpg'
    }
    create_response = client.post('/picture', 
                                  data=json.dumps(new_picture),
                                  content_type='application/json')
    assert create_response.status_code == 201
    created = json.loads(create_response.data)
    picture_id = created['id']
    
    # Eliminar la imagen
    response = client.delete(f'/picture/{picture_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Picture deleted'
    
    # Verificar que ya no existe
    get_response = client.get(f'/picture/{picture_id}')
    assert get_response.status_code == 404