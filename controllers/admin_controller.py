from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from models.database import db
from models.models import User, Role, UserRole, TributeContent

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/toggle-role/<int:user_id>', methods=['POST'])
@login_required
def toggle_writer_role(user_id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'error': 'Acesso negado. Requer perfil de Administrador.'}), 403

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'success': False, 'error': 'Usuário não encontrado.'}), 404

    writer_role = Role.query.filter_by(slug='writer').first()
    if not writer_role:
        return jsonify({'success': False, 'error': 'Papel de escritor não encontrado.'}), 500

    if writer_role in user.roles:
        user.roles.remove(writer_role)
        db.session.commit()
        is_writer = False
        msg = f"Permissão de Escritor removida de {user.name}."
    else:
        user.roles.append(writer_role)
        db.session.commit()
        is_writer = True
        msg = f"Permissão de Escritor concedida a {user.name} com sucesso!"

    return jsonify({
        'success': True,
        'is_writer': is_writer,
        'message': msg,
        'user_id': user.id
    })

@admin_bp.route('/toggle-terminal', methods=['POST'])
@login_required
def toggle_terminal():
    if not current_user.is_admin:
        return jsonify({'success': False, 'error': 'Acesso negado. Requer perfil de Administrador.'}), 403

    sec = TributeContent.query.filter_by(section_key='terminal_setting').first()
    if not sec:
        sec = TributeContent(section_key='terminal_setting', title='Configuração do Terminal', content='true')
        db.session.add(sec)

    new_state = 'false' if sec.content == 'true' else 'true'
    sec.content = new_state
    db.session.commit()

    is_enabled = (new_state == 'true')
    msg = 'Exibição do Terminal Interativo ativada com sucesso!' if is_enabled else 'Exibição do Terminal Interativo desativada com sucesso!'

    return jsonify({
        'success': True,
        'terminal_enabled': is_enabled,
        'message': msg
    })

@admin_bp.route('/users', methods=['GET'])
@login_required
def list_users():
    if not current_user.is_admin:
        return jsonify({'success': False, 'error': 'Acesso negado. Requer perfil de Administrador.'}), 403

    users = User.query.order_by(User.created_at.desc()).all()
    users_data = []
    for u in users:
        users_data.append({
            'id': u.id,
            'name': u.name,
            'email': u.email,
            'is_admin': u.is_admin,
            'is_writer': u.is_writer
        })

    return jsonify({
        'success': True,
        'users': users_data
    })

