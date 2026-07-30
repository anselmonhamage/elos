from flask import Blueprint, request, jsonify
from flask_login import current_user
from models.database import db
from models.models import Wish, WishLike, TributeContent

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/wishes/like/<int:wish_id>', methods=['POST'])
def like_wish(wish_id):
    wish = db.session.get(Wish, wish_id)
    if not wish:
        return jsonify({'success': False, 'error': 'Homenagem não encontrada.'}), 404

    user_id = current_user.id if current_user.is_authenticated else None
    client_ip = request.remote_addr or '127.0.0.1'

    existing_like = None
    if user_id:
        existing_like = WishLike.query.filter_by(wish_id=wish.id, user_id=user_id).first()
    else:
        existing_like = WishLike.query.filter_by(wish_id=wish.id, ip_address=client_ip).first()

    if existing_like:
        return jsonify({
            'success': False,
            'already_liked': True,
            'error': 'Você já curtiu esta homenagem!',
            'likes': wish.likes
        }), 400

    new_like = WishLike(wish_id=wish.id, user_id=user_id, ip_address=client_ip)
    wish.likes += 1
    db.session.add(new_like)
    db.session.commit()

    return jsonify({
        'success': True,
        'likes': wish.likes,
        'already_liked': True,
        'message': 'Curtida registrada com sucesso!'
    })

@api_bp.route('/terminal', methods=['POST'])
def handle_terminal():
    req = request.get_json() or {}
    cmd = req.get('command', '').strip().lower()

    if cmd == "clear":
        return jsonify({'success': True, 'response': '', 'clear': True})

    if cmd == "poetry":
        # Get poetry from special message section in DB
        special_sec = TributeContent.query.filter_by(section_key='special_message').first()
        output = special_sec.content if special_sec else "Código é lógica, mas você é pura poesia em execução. Feliz aniversário!"
    else:
        # Check DB for command response
        cmd_sec = TributeContent.query.filter_by(section_key=f"terminal_cmd_{cmd}").first()
        if cmd_sec:
            output = cmd_sec.content
        else:
            output = f"Comando '{cmd}' não reconhecido. Digite 'help' para listar os comandos."

    return jsonify({'success': True, 'response': output})

@api_bp.route('/steps/active', methods=['POST'])
def update_active_step():
    req = request.get_json() or {}
    step = req.get('step')
    if not step or not isinstance(step, int) or step < 1 or step > 4:
        return jsonify({'success': False, 'error': 'Passo inválido.'}), 400

    from flask import session
    if current_user.is_authenticated:
        user = current_user._get_current_object()
        user.active_step = step
        db.session.commit()
    else:
        session['active_step'] = step

    return jsonify({'success': True, 'step': step})
