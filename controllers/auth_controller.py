import base64
from flask import Blueprint, request, jsonify, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from models.database import db
from models.models import User, Role, UserRole
from forms import LoginForm, RegisterForm, ProfileForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip().lower()).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return jsonify({'success': True, 'message': f'Bem-vindo de volta, {user.name}!'})
        return jsonify({'success': False, 'error': 'E-mail ou senha incorretos.'}), 400
    
    errors = [err for field_errors in form.errors.values() for err in field_errors]
    return jsonify({'success': False, 'error': errors[0] if errors else 'Dados de login inválidos.'}), 400

@auth_bp.route('/register', methods=['POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        if User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'error': 'Este e-mail já está cadastrado.'}), 400
        
        user = User(name=form.name.data.strip(), email=email)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        user_role = Role.query.filter_by(slug='user').first()
        if user_role:
            db.session.add(UserRole(user_id=user.id, role_id=user_role.id))
            db.session.commit()

        login_user(user)
        return jsonify({'success': True, 'message': 'Conta criada com sucesso!'})

    errors = [err for field_errors in form.errors.values() for err in field_errors]
    return jsonify({'success': False, 'error': errors[0] if errors else 'Dados de cadastro inválidos.'}), 400

@auth_bp.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data.strip()

        if form.profile_image.data:
            file = form.profile_image.data
            from services.storage_service import get_storage_provider
            provider = get_storage_provider()
            url = provider.upload_file(file, unique_prefix="profile_")
            current_user.profile_image = url

        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Perfil atualizado com sucesso!',
            'name': current_user.name,
            'profile_image': current_user.profile_image
        })

    errors = [err for field_errors in form.errors.values() for err in field_errors]
    return jsonify({'success': False, 'error': errors[0] if errors else 'Erro ao atualizar perfil.'}), 400

@auth_bp.route('/profile/delete', methods=['POST'])
@login_required
def delete_account():
    user = current_user._get_current_object()
    logout_user()
    db.session.delete(user)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Sua conta foi excluída com sucesso.'})

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
