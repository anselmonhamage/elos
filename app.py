import os
from dotenv import load_dotenv
from flask import Flask
from models.database import db, migrate, login_manager, csrf
from models.models import User, Role, UserRole, TributeContent
from controllers import register_blueprints

load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    
    db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'birthday.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    upload_folder = os.path.join(app.static_folder, 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret_key_change_me')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = upload_folder
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login_manager.init_app(app)
    login_manager.login_view = 'main.index'
    csrf.init_app(app)
    
    register_blueprints(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
        
    @app.cli.command('init-db')
    def init_db():
        """Inicializa as tabelas da base de dados, papéis, conteúdos padrão e semeia o Admin inicial vindo do .env"""
        db.create_all()

        roles_data = [
            {"name": "Administrador", "slug": "admin"},
            {"name": "Escritor", "slug": "writer"},
            {"name": "Leitor", "slug": "user"}
        ]

        for r_data in roles_data:
            existing = Role.query.filter_by(slug=r_data["slug"]).first()
            if not existing:
                db.session.add(Role(name=r_data["name"], slug=r_data["slug"]))
        db.session.commit()

        # Seed conteúdos dinâmicos das seções se não existirem
        welcome_sec = TributeContent.query.filter_by(section_key='welcome').first()
        if not welcome_sec:
            db.session.add(TributeContent(
                section_key='welcome',
                title='Festa de Aniversário Dev',
                content='Olá! Sejam bem-vindos ao espaço de comemoração do nosso dev favorito. Um cantinho preparado com muito carinho para registrar homenagens e compartilhar bons momentos.',
                image_filename='TF-home-mockup-aniversario.webp'
            ))

        msg_sec = TributeContent.query.filter_by(section_key='special_message').first()
        if not msg_sec:
            default_poetic = (
                "Muitos enxergam no código apenas sintaxe e comandos. Mas em você vemos a capacidade de transformar problemas em soluções elegantes e ideias em realidades brilhantes.\n\n"
                "Se a vida fosse um repositório, o seu commit principal seria a gentileza, a paixão por criar e a capacidade de iluminar o dia de todos ao seu redor. Você é aquela pessoa rara que consegue ser extraordinariamente brilhante com a mente e infinitamente acolhedora com o coração.\n\n"
                "Que este seu novo ciclo seja um Deploy Perfeito: sem exceções não tratadas, com latência zero para a paz de espírito e alta disponibilidade para todos os seus sonhos!"
            )
            db.session.add(TributeContent(
                section_key='special_message',
                title='As Palavras Mais Lindas do Mundo',
                content=default_poetic
            ))
        db.session.commit()

        admin_name = os.environ.get("ADMIN_NAME", "Administrador Principal")
        admin_email = os.environ.get("ADMIN_EMAIL", "admin@dev.com")
        admin_password = os.environ.get("ADMIN_PASSWORD", "AdminPass123!")

        if admin_email and admin_password:
            existing_admin = User.query.filter_by(email=admin_email).first()
            if not existing_admin:
                admin_user = User(name=admin_name, email=admin_email)
                admin_user.set_password(admin_password)
                db.session.add(admin_user)
                db.session.commit()

                admin_role = Role.query.filter_by(slug="admin").first()
                if admin_role:
                    db.session.add(UserRole(user_id=admin_user.id, role_id=admin_role.id))
                    db.session.commit()
                print(f"[SEED SUCCESS] Usuário administrador ({admin_email}) criado com sucesso!")
            else:
                print(f"[SEED INFO] Administrador ({admin_email}) já existe na base de dados.")

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
