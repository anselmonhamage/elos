import pytest
from app import create_app
from models.database import db as _db
from models.models import Role, User, UserRole

@pytest.fixture(scope='session')
def app():
    # Start the app in testing mode
    app = create_app('testing')
    with app.app_context():
        yield app

@pytest.fixture(scope='function')
def db(app):
    _db.create_all()
    
    # Seed default roles
    roles_data = [
        {"name": "Administrador", "slug": "admin"},
        {"name": "Escritor", "slug": "writer"},
        {"name": "Leitor", "slug": "user"}
    ]
    for r_data in roles_data:
        _db.session.add(Role(name=r_data["name"], slug=r_data["slug"]))
    _db.session.commit()

    yield _db
    
    _db.session.remove()
    _db.drop_all()

@pytest.fixture(scope='function')
def client(app, db):
    return app.test_client()

@pytest.fixture(scope='function')
def create_user(db):
    def _create_user(name, email, password, role_slug='user'):
        user = User(name=name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        role = Role.query.filter_by(slug=role_slug).first()
        if role:
            db.session.add(UserRole(user_id=user.id, role_id=role.id))
            db.session.commit()
        return user
    return _create_user
