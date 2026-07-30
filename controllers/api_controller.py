from flask import Blueprint, request, jsonify
from flask_login import current_user
from models.database import db
from models.models import Wish, WishLike

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

    responses = {
        "help": "Comandos disponíveis:\n  - poetry : Lê a mensagem de aniversário para o dev\n  - git log: Exibe o histórico de commits da vida\n  - status : Verifica a saúde do sistema\n  - secret : Ativa o modo de celebração\n  - clear  : Limpa a tela do terminal",
        "poetry": "Código é lógica, mas você é pura poesia em execução. Feliz aniversário!",
        "git log": "HEAD -> main: [COMMIT] Adicionado amor, inspiração e conquistas sem limites.",
        "status": "HTTP 200 OK - Estado mental: Feliz | Memória: Repleta de conquistas | Uptime: 100%",
        "secret": "Modo de comemoração ativado!"
    }

    if cmd == "clear":
        return jsonify({'success': True, 'response': '', 'clear': True})

    output = responses.get(cmd, f"Comando '{cmd}' não reconhecido. Digite 'help' para listar os comandos.")
    return jsonify({'success': True, 'response': output})
