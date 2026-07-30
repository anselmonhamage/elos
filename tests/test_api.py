import json
from models.models import Wish, WishLike, User

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

def test_active_step_api(client, db, create_user):
    # Test active step update as anonymous guest (should save in session)
    response = client.post('/api/steps/active', json={'step': 2})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['step'] == 2

    # Test active step update as authenticated user (should save in DB)
    user = create_user('Step User', 'step@example.com', 'password123')
    client.post('/login', data={
        'email': 'step@example.com',
        'password': 'password123'
    })

    response2 = client.post('/api/steps/active', json={'step': 4})
    assert response2.status_code == 200
    data2 = json.loads(response2.data)
    assert data2['success'] is True
    assert data2['step'] == 4

    # Verify db
    updated_user = db.session.get(User, user.id)
    assert updated_user.active_step == 4

    # Test invalid step validation
    response3 = client.post('/api/steps/active', json={'step': 99})
    assert response3.status_code == 400

def test_terminal_admin_commands(client, db, create_user):
    # Test admin commands as anonymous guest (should fail)
    response = client.post('/api/terminal', json={'command': 'add testcmd customresponse'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'Apenas administradores' in data['response']

    # Login as admin
    create_user('Admin', 'admin@dev.com', 'AdminPass123!', role_slug='admin')
    client.post('/login', data={
        'email': 'admin@dev.com',
        'password': 'AdminPass123!'
    })

    # Test list command
    response_list = client.post('/api/terminal', json={'command': 'list'})
    assert response_list.status_code == 200
    data_list = json.loads(response_list.data)
    assert 'Comandos de administração disponíveis' in data_list['response']

    # Add command
    response_add = client.post('/api/terminal', json={'command': 'add testcmd This is a custom test response'})
    assert response_add.status_code == 200
    data_add = json.loads(response_add.data)
    assert 'adicionado com sucesso' in data_add['response']

    # Execute added command
    response_exec = client.post('/api/terminal', json={'command': 'testcmd'})
    assert response_exec.status_code == 200
    data_exec = json.loads(response_exec.data)
    assert data_exec['response'] == 'This is a custom test response'

    # Edit command
    response_edit = client.post('/api/terminal', json={'command': 'edit testcmd Modified response!'})
    assert response_edit.status_code == 200
    data_edit = json.loads(response_edit.data)
    assert 'atualizada' in data_edit['response']

    # Execute edited command
    response_exec2 = client.post('/api/terminal', json={'command': 'testcmd'})
    assert response_exec2.status_code == 200
    data_exec2 = json.loads(response_exec2.data)
    assert data_exec2['response'] == 'Modified response!'

    # Delete command
    response_del = client.post('/api/terminal', json={'command': 'delete testcmd'})
    assert response_del.status_code == 200
    data_del = json.loads(response_del.data)
    assert 'removido com sucesso' in data_del['response']

    # Execute deleted command (should not recognize)
    response_exec3 = client.post('/api/terminal', json={'command': 'testcmd'})
    assert response_exec3.status_code == 200
    data_exec3 = json.loads(response_exec3.data)
    assert 'não reconhecido' in data_exec3['response']
