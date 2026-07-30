import os
import uuid
from flask import Blueprint, jsonify, url_for, current_app, request
from flask_login import login_required, current_user
from models.database import db
from models.models import Wish, TributeContent
from forms.forms import WishForm, WelcomeSectionForm, SpecialMessageSectionForm

writer_bp = Blueprint('writer', __name__, url_prefix='/writer')

import json

@writer_bp.route('/update-welcome', methods=['POST'])
@login_required
def update_welcome_section():
    if not current_user.is_writer:
        return jsonify({'success': False, 'error': 'Permissão negada. Apenas Escritores podem editar esta seção.'}), 403

    form = WelcomeSectionForm()
    if form.validate_on_submit():
        sec = TributeContent.query.filter_by(section_key='welcome').first()
        if not sec:
            sec = TributeContent(section_key='welcome', title='', content='')
            db.session.add(sec)

        sec.title = form.title.data.strip()
        sec.content = form.content.data.strip()
        if form.image_fit.data:
            sec.image_fit = form.image_fit.data
        sec.updated_by_id = current_user.id

        uploaded_files = request.files.getlist('images')
        if not uploaded_files or not any(f.filename for f in uploaded_files):
            if form.images.data:
                uploaded_files = form.images.data if isinstance(form.images.data, list) else [form.images.data]

        valid_files = [f for f in uploaded_files if f and f.filename]
        MAX_SIZE_BYTES = 1 * 1024 * 1024 # 1MB Máximo

        # Validação do Tamanho Máximo de 1MB por Imagem
        for file in valid_files:
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)

            if file_size > MAX_SIZE_BYTES:
                size_mb = round(file_size / (1024 * 1024), 2)
                return jsonify({
                    'success': False,
                    'error': f"A imagem '{file.filename}' possui {size_mb}MB. Cada foto de boas-vindas deve ter até no máximo 1MB!"
                }), 400

        from services.storage_service import get_storage_provider
        provider = get_storage_provider()

        saved_urls = []
        for file in valid_files:
            url = provider.upload_file(file, unique_prefix="hero_")
            saved_urls.append(url)

        if saved_urls:
            if form.append_images.data:
                existing = sec.get_images_list()
                combined = []
                for img in existing:
                    if img not in combined and img not in saved_urls:
                        combined.append(img)
                for img in saved_urls:
                    if img not in combined:
                        combined.append(img)
            else:
                combined = []
                for img in saved_urls:
                    if img not in combined:
                        combined.append(img)

            sec.image_filenames = json.dumps(combined)
            sec.image_filename = combined[0]

        db.session.commit()

        images_urls = []
        for fn in sec.get_images_list():
            if fn.startswith('http://') or fn.startswith('https://') or fn.startswith('/'):
                images_urls.append(fn)
            elif os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], fn)):
                images_urls.append(url_for('static', filename='uploads/' + fn))
            else:
                images_urls.append(url_for('static', filename='images/' + fn))

        return jsonify({
            'success': True,
            'title': sec.title,
            'content': sec.content,
            'images_urls': images_urls,
            'image_fit': sec.image_fit or 'cover',
            'message': 'Tela de boas-vindas atualizada com sucesso!'
        })

    errors = [err for field_errors in form.errors.values() for err in field_errors]
    return jsonify({'success': False, 'error': errors[0] if errors else 'Dados inválidos.'}), 400

@writer_bp.route('/update-special-message', methods=['POST'])
@login_required
def update_special_message_section():
    if not current_user.is_writer:
        return jsonify({'success': False, 'error': 'Permissão negada. Apenas Escritores podem editar a mensagem.'}), 403

    form = SpecialMessageSectionForm()
    if form.validate_on_submit():
        sec = TributeContent.query.filter_by(section_key='special_message').first()
        if not sec:
            sec = TributeContent(section_key='special_message', title='', content='')
            db.session.add(sec)

        sec.title = form.title.data.strip()
        sec.content = form.content.data.strip()
        sec.updated_by_id = current_user.id
        db.session.commit()

        return jsonify({
            'success': True,
            'title': sec.title,
            'content': sec.content,
            'message': 'Mensagem especial atualizada com sucesso!'
        })

    errors = [err for field_errors in form.errors.values() for err in field_errors]
    return jsonify({'success': False, 'error': errors[0] if errors else 'Dados inválidos.'}), 400

@writer_bp.route('/wish', methods=['POST'])
@login_required
def create_wish():
    if not current_user.is_writer:
        return jsonify({'success': False, 'error': 'Apenas usuários com permissão de Escritor podem publicar recados.'}), 403

    form = WishForm()
    if form.validate_on_submit():
        author = form.author.data.strip() or current_user.name
        role_text = form.role.data.strip() or "Escritor Convidado"
        message = form.message.data.strip()

        new_wish = Wish(
            user_id=current_user.id,
            author=author,
            role=role_text,
            message=message
        )
        db.session.add(new_wish)
        db.session.commit()

        return jsonify({'success': True, 'wish': new_wish.to_dict()})

    errors = [err for field_errors in form.errors.values() for err in field_errors]
    return jsonify({'success': False, 'error': errors[0] if errors else 'Erro na mensagem.'}), 400

@writer_bp.route('/wish/delete/<int:wish_id>', methods=['POST', 'DELETE'])
@login_required
def delete_wish(wish_id):
    wish = db.session.get(Wish, wish_id)
    if not wish:
        return jsonify({'success': False, 'error': 'Recado não encontrado.'}), 404

    # Permissão: Administrador, Escritor ou autor do recado
    if not (current_user.is_writer or wish.user_id == current_user.id):
        return jsonify({'success': False, 'error': 'Permissão negada para excluir este recado.'}), 403

    db.session.delete(wish)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Recado excluído com sucesso!'})
