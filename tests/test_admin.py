import json
from models.models import User, TributeContent

def test_toggle_writer_role_admin(client, db, create_user):
    admin = create_user('Admin User', 'admin@example.com', 'password123', role_slug='admin')
    target_user = create_user('Target User', 'target@example.com', 'password123', role_slug='user')

    client.post('/login', data={
        'email': 'admin@example.com',
        'password': 'password123'
    })

    # Initially, target_user is not a writer
    assert target_user.is_writer is False

    # Promote to writer
    response = client.post(f'/admin/toggle-role/{target_user.id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['is_writer'] is True
    assert 'concedida' in data['message'].lower()
    
    # Check db
    assert target_user.is_writer is True

    # Demote back to reader
    response = client.post(f'/admin/toggle-role/{target_user.id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['is_writer'] is False
    assert 'removida' in data['message'].lower()
    
    # Check db
    assert target_user.is_writer is False

def test_toggle_writer_role_unauthorized(client, db, create_user):
    writer = create_user('Writer User', 'writer@example.com', 'password123', role_slug='writer')
    target_user = create_user('Target User', 'target@example.com', 'password123', role_slug='user')

    client.post('/login', data={
        'email': 'writer@example.com',
        'password': 'password123'
    })

    response = client.post(f'/admin/toggle-role/{target_user.id}')
    assert response.status_code == 403
    data = json.loads(response.data)
    assert data['success'] is False
    assert 'acesso negado' in data['error'].lower()

def test_toggle_terminal_admin(client, db, create_user):
    create_user('Admin User', 'admin@example.com', 'password123', role_slug='admin')
    client.post('/login', data={
        'email': 'admin@example.com',
        'password': 'password123'
    })

    # Toggle terminal
    response = client.post('/admin/toggle-terminal')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    
    # Check db
    sec = TributeContent.query.filter_by(section_key='terminal_setting').first()
    assert sec is not None
    assert sec.content in ['true', 'false']

def test_list_users_admin(client, db, create_user):
    admin = create_user('Admin User', 'admin@example.com', 'password123', role_slug='admin')
    user1 = create_user('User One', 'user1@example.com', 'password123', role_slug='user')

    client.post('/login', data={'email': 'admin@example.com', 'password': 'password123'})

    response = client.get('/admin/users')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert len(data['users']) >= 2

def test_list_users_unauthorized(client, db, create_user):
    create_user('Normal User', 'normal@example.com', 'password123', role_slug='user')
    client.post('/login', data={'email': 'normal@example.com', 'password': 'password123'})

    response = client.get('/admin/users')
    assert response.status_code == 403

