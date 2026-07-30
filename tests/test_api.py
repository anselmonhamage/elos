import json
from models.models import Wish, WishLike

def test_like_wish_authenticated(client, db, create_user):
    user = create_user('User', 'user@example.com', 'password123')
    
    # Create wish
    wish = Wish(author='Author', message='Nice birthday!')
    db.session.add(wish)
    db.session.commit()

    # Login
    client.post('/login', data={
        'email': 'user@example.com',
        'password': 'password123'
    })

    # Like the wish
    response = client.post(f'/api/wishes/like/{wish.id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['likes'] == 1

    # Try liking again (should be blocked)
    response2 = client.post(f'/api/wishes/like/{wish.id}')
    assert response2.status_code == 400
    data2 = json.loads(response2.data)
    assert data2['success'] is False
    assert data2['already_liked'] is True

def test_like_wish_anonymous(client, db):
    # Create wish
    wish = Wish(author='Author', message='Nice birthday!')
    db.session.add(wish)
    db.session.commit()

    # Like the wish (anonymous)
    response = client.post(f'/api/wishes/like/{wish.id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['likes'] == 1

    # Try liking again (should block duplicate by IP address)
    response2 = client.post(f'/api/wishes/like/{wish.id}')
    assert response2.status_code == 400
    data2 = json.loads(response2.data)
    assert data2['success'] is False
    assert data2['already_liked'] is True

def test_like_non_existent_wish(client, db):
    response = client.post('/api/wishes/like/9999')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['success'] is False

def test_terminal_api(client):
    # Test valid command 'help'
    response = client.post('/api/terminal', json={'command': 'help'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'Comandos disponíveis' in data['response']

    # Test valid command 'poetry'
    response = client.post('/api/terminal', json={'command': 'poetry'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'pura poesia em execução' in data['response']

    # Test valid command 'clear'
    response = client.post('/api/terminal', json={'command': 'clear'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert data.get('clear') is True

    # Test unrecognized command
    response = client.post('/api/terminal', json={'command': 'unknown_cmd'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'não reconhecido' in data['response']
