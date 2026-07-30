import json
from models.models import User

def test_register_success(client, db):
    # Test registration succeeds with valid data
    response = client.post('/register', data={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['message'] == 'Conta criada com sucesso!'

    # Verify user exists in database and has user role
    user = User.query.filter_by(email='test@example.com').first()
    assert user is not None
    assert user.name == 'Test User'
    assert user.is_writer is False # Standard user, not writer by default

def test_register_duplicate_email(client, db, create_user):
    # Pre-create user
    create_user('Original', 'original@example.com', 'password123')

    # Try duplicate registration
    response = client.post('/register', data={
        'name': 'Duplicate',
        'email': 'original@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False
    assert 'este e-mail já está cadastrado' in data['error'].lower()

def test_login_success(client, db, create_user):
    # Pre-create user
    create_user('Login User', 'login@example.com', 'password123')

    # Test login
    response = client.post('/login', data={
        'email': 'login@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'bem-vindo de volta' in data['message'].lower()

def test_login_invalid_password(client, db, create_user):
    create_user('Login User', 'login@example.com', 'password123')

    response = client.post('/login', data={
        'email': 'login@example.com',
        'password': 'wrongpassword'
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False
    assert 'e-mail ou senha incorretos' in data['error'].lower()

def test_logout(client, db, create_user):
    # Login first
    create_user('Login User', 'login@example.com', 'password123')
    client.post('/login', data={
        'email': 'login@example.com',
        'password': 'password123'
    })

    # Logout
    response = client.get('/logout')
    assert response.status_code == 302 # Redirect to home page

def test_profile_update(client, db, create_user):
    user = create_user('Profile User', 'profile@example.com', 'password123')
    
    # Login
    client.post('/login', data={
        'email': 'profile@example.com',
        'password': 'password123'
    })

    # Update profile name
    response = client.post('/profile/update', data={
        'name': 'Updated User Name'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['name'] == 'Updated User Name'

    # Check db
    updated_user = db.session.get(User, user.id)
    assert updated_user.name == 'Updated User Name'

def test_account_delete(client, db, create_user):
    user = create_user('Delete User', 'delete@example.com', 'password123')
    client.post('/login', data={
        'email': 'delete@example.com',
        'password': 'password123'
    })

    # Delete
    response = client.post('/profile/delete')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True

    # Check db
    deleted_user = db.session.get(User, user.id)
    assert deleted_user is None
