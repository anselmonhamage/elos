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
    cmd = req.get('command', '').strip()
    cmd_lower = cmd.lower()

    if cmd_lower == "clear":
        return jsonify({'success': True, 'response': '', 'clear': True})

    is_admin = current_user.is_authenticated and current_user.is_admin

    # Check for admin command management (add, edit, delete)
    if cmd_lower.startswith("add ") or cmd_lower.startswith("edit ") or cmd_lower.startswith("delete "):
        if not is_admin:
            return jsonify({'success': True, 'response': "Erro: Apenas administradores podem criar, editar ou deletar comandos."})

        parts = cmd.split(" ", 2)
        action = parts[0].lower()

        if action == "delete":
            if len(parts) < 2:
                return jsonify({'success': True, 'response': "Uso correto: delete <nome_do_comando>"})
            target_cmd = parts[1].strip().lower()

            if target_cmd in ["clear", "poetry", "help", "list"]:
                return jsonify({'success': True, 'response': f"Erro: O comando '{target_cmd}' é reservado pelo sistema e não pode ser deletado."})

            key = f"terminal_cmd_{target_cmd}"
            cmd_sec = TributeContent.query.filter_by(section_key=key).first()
            if not cmd_sec:
                return jsonify({'success': True, 'response': f"Erro: O comando '{target_cmd}' não existe no banco de dados."})

            db.session.delete(cmd_sec)
            db.session.commit()
            return jsonify({'success': True, 'response': f"Sucesso: Comando '{target_cmd}' removido com sucesso do banco de dados."})

        else: # add or edit
            if len(parts) < 3:
                return jsonify({'success': True, 'response': f"Uso correto: {action} <nome_do_comando> <resposta>"})

            target_cmd = parts[1].strip().lower()
            response_text = parts[2].strip()

            if target_cmd == "clear":
                return jsonify({'success': True, 'response': "Erro: O comando 'clear' é reservado e não pode ser modificado."})

            if target_cmd == "poetry":
                # Edit poetry response (which updates special_message TributeContent in DB)
                special_sec = TributeContent.query.filter_by(section_key='special_message').first()
                if special_sec:
                    special_sec.content = response_text
                    db.session.commit()
                    return jsonify({'success': True, 'response': "Sucesso: O poema de aniversário (mensagem especial) foi atualizado no banco de dados."})
                else:
                    return jsonify({'success': True, 'response': "Erro: Seção de mensagem especial não inicializada."})

            key = f"terminal_cmd_{target_cmd}"
            cmd_sec = TributeContent.query.filter_by(section_key=key).first()

            if action == "add":
                if cmd_sec or target_cmd in ["help", "list"]:
                    return jsonify({'success': True, 'response': f"Erro: O comando '{target_cmd}' já existe. Use 'edit' para alterá-lo."})
                new_sec = TributeContent(
                    section_key=key,
                    title=f"Terminal Command: {target_cmd}",
                    content=response_text
                )
                db.session.add(new_sec)
                db.session.commit()
                return jsonify({'success': True, 'response': f"Sucesso: Comando '{target_cmd}' adicionado com sucesso ao banco de dados."})

            elif action == "edit":
                if not cmd_sec:
                    return jsonify({'success': True, 'response': f"Erro: O comando '{target_cmd}' não existe. Use 'add' para criá-lo."})
                cmd_sec.content = response_text
                db.session.commit()
                return jsonify({'success': True, 'response': f"Sucesso: Resposta do comando '{target_cmd}' atualizada no banco de dados."})

    if cmd_lower == "list":
        # List all terminal commands in DB
        cmds = TributeContent.query.filter(TributeContent.section_key.like('terminal_cmd_%')).all()
        cmd_names = [c.section_key.replace('terminal_cmd_', '') for c in cmds]
        all_cmds = sorted(list(set(cmd_names + ["clear", "poetry"])))
        response_str = "Comandos cadastrados:\n" + "\n".join([f"  - {name}" for name in all_cmds])
        if is_admin:
            response_str += "\n\nComandos de administração disponíveis:\n  - add <cmd> <resp>  : Adiciona um comando\n  - edit <cmd> <resp> : Edita a resposta de um comando\n  - delete <cmd>     : Remove um comando"
        return jsonify({'success': True, 'response': response_str})

    if cmd_lower == "poetry":
        # Get poetry from special message section in DB
        special_sec = TributeContent.query.filter_by(section_key='special_message').first()
        output = special_sec.content if special_sec else "Código é lógica, mas você é pura poesia em execução. Feliz aniversário!"
    else:
        # Check DB for command response
        cmd_sec = TributeContent.query.filter_by(section_key=f"terminal_cmd_{cmd_lower}").first()
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
