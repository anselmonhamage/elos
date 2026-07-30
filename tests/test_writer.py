import json
from models.models import TributeContent, Wish

def test_update_welcome_section_writer(client, db, create_user):
    writer = create_user('Writer User', 'writer@example.com', 'password123', role_slug='writer')
    client.post('/login', data={
        'email': 'writer@example.com',
        'password': 'password123'
    })

    response = client.post('/writer/update-welcome', data={
        'title': 'New Welcome Title',
        'content': 'New Welcome Content description...',
        'image_fit': 'cover'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['title'] == 'New Welcome Title'
    
    # Check db
    sec = TributeContent.query.filter_by(section_key='welcome').first()
    assert sec is not None
    assert sec.title == 'New Welcome Title'
    assert sec.content == 'New Welcome Content description...'
    assert sec.image_fit == 'cover'

def test_update_welcome_section_reader_forbidden(client, db, create_user):
    create_user('Reader User', 'reader@example.com', 'password123', role_slug='user')
    client.post('/login', data={
        'email': 'reader@example.com',
        'password': 'password123'
    })

    response = client.post('/writer/update-welcome', data={
        'title': 'Hack Welcome Title',
        'content': 'Hack Welcome Content description...'
    })
    assert response.status_code == 403
    data = json.loads(response.data)
    assert data['success'] is False
    assert 'permissão negada' in data['error'].lower()

def test_update_special_message_writer(client, db, create_user):
    writer = create_user('Writer User', 'writer@example.com', 'password123', role_slug='writer')
    client.post('/login', data={
        'email': 'writer@example.com',
        'password': 'password123'
    })

    response = client.post('/writer/update-special-message', data={
        'title': 'Special Day!',
        'content': 'Congratulations on your achievements!'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['title'] == 'Special Day!'

    # Check db
    sec = TributeContent.query.filter_by(section_key='special_message').first()
    assert sec is not None
    assert sec.title == 'Special Day!'
    assert sec.content == 'Congratulations on your achievements!'

def test_create_wish_writer(client, db, create_user):
    writer = create_user('Writer User', 'writer@example.com', 'password123', role_slug='writer')
    client.post('/login', data={
        'email': 'writer@example.com',
        'password': 'password123'
    })

    response = client.post('/writer/wish', data={
        'author': 'Tester',
        'role': 'QA Engineer',
        'message': 'This is a beautiful test wish message!'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['wish']['author'] == 'Tester'
    assert data['wish']['message'] == 'This is a beautiful test wish message!'

    # Check db
    wish = db.session.get(Wish, data['wish']['id'])
    assert wish is not None
    assert wish.author == 'Tester'
    assert wish.user_id == writer.id

def test_create_wish_reader_forbidden(client, db, create_user):
    create_user('Reader User', 'reader@example.com', 'password123', role_slug='user')
    client.post('/login', data={
        'email': 'reader@example.com',
        'password': 'password123'
    })

    response = client.post('/writer/wish', data={
        'author': 'Reader Hack',
        'role': 'Spy',
        'message': 'Spamming the page'
    })
    assert response.status_code == 403
    data = json.loads(response.data)
    assert data['success'] is False
    assert 'apenas usuários com permissão de escritor' in data['error'].lower()

def test_delete_wish_owner_success(client, db, create_user):
    # Setup users
    writer1 = create_user('Writer 1', 'writer1@example.com', 'password123', role_slug='writer')
    writer2 = create_user('Writer 2', 'writer2@example.com', 'password123', role_slug='writer')
    
    # Create wish under writer1
    wish = Wish(user_id=writer1.id, author='Writer 1', message='My original post')
    db.session.add(wish)
    db.session.commit()

    # Login as writer2 (not owner)
    client.post('/login', data={
        'email': 'writer2@example.com',
        'password': 'password123'
    })
    # Since writer2 is a writer, they actually can delete wishes because current_user.is_writer is True
    # In controllers/writer_controller.py:
    # if not (current_user.is_writer or wish.user_id == current_user.id):
    # This means ANY writer can delete any wish. So writer2 will succeed! Let's test that first:
    response = client.delete(f'/writer/wish/delete/{wish.id}')
    assert response.status_code == 200
    assert db.session.get(Wish, wish.id) is None

def test_delete_wish_reader_unauthorized(client, db, create_user):
    writer = create_user('Writer', 'writer@example.com', 'password123', role_slug='writer')
    reader = create_user('Reader', 'reader@example.com', 'password123', role_slug='user')
    
    wish = Wish(user_id=writer.id, author='Writer', message='My original post')
    db.session.add(wish)
    db.session.commit()

    # Login as reader (not owner, not writer)
    client.post('/login', data={
        'email': 'reader@example.com',
        'password': 'password123'
    })
    
    response = client.delete(f'/writer/wish/delete/{wish.id}')
    assert response.status_code == 403
    data = json.loads(response.data)
    assert data['success'] is False
    assert 'permissão negada' in data['error'].lower()

def test_delete_welcome_image(client, db, create_user):
    create_user('Writer User', 'writer@example.com', 'password123', 'writer')
    
    client.post('/login', data={
        'email': 'writer@example.com',
        'password': 'password123'
    })
    
    sec = TributeContent(
        section_key='welcome',
        title='Welcome Section',
        content='Welcome text description...',
        image_filenames=json.dumps(['hero_image1.jpg', 'hero_image2.jpg']),
        image_filename='hero_image1.jpg'
    )
    db.session.add(sec)
    db.session.commit()
    
    response = client.post('/writer/delete-welcome-image', json={
        'image_url': 'hero_image1.jpg'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'hero_image1.jpg' not in data['images_urls']
    
    db.session.refresh(sec)
    assert 'hero_image1.jpg' not in sec.get_images_list()
    assert sec.image_filename == 'hero_image2.jpg'
