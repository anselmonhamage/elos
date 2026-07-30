from flask import Blueprint, render_template, request, session
from flask_login import current_user
from models.models import Wish, User, TributeContent, WishLike
from forms import LoginForm, RegisterForm, WishForm, WelcomeSectionForm, SpecialMessageSectionForm, ProfileForm
from controllers.utils import get_or_create_section

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    wishes = Wish.query.order_by(Wish.timestamp.desc()).all()
    user_id = current_user.id if current_user.is_authenticated else None
    client_ip = request.remote_addr or '127.0.0.1'
    
    # Pre-fetch liked wishes to solve N+1 query issues
    liked_wish_ids = set()
    if wishes:
        wish_ids = [w.id for w in wishes]
        if user_id:
            likes = WishLike.query.filter(WishLike.wish_id.in_(wish_ids), WishLike.user_id == user_id).all()
        else:
            likes = WishLike.query.filter(WishLike.wish_id.in_(wish_ids), WishLike.ip_address == client_ip).all()
        liked_wish_ids = {lk.wish_id for lk in likes}

    wishes_data = [w.to_dict(liked_wish_ids=liked_wish_ids) for w in wishes]
    
    welcome_content = get_or_create_section(
        'welcome',
        'Festa de Aniversário Dev',
        'Olá! Sejam bem-vindos ao espaço de comemoração do nosso dev favorito. Um cantinho preparado com muito carinho para registrar homenagens e compartilhar bons momentos.',
        'mockup_aniversario.png'
    )
    
    default_poetic = (
        "Muitos enxergam no código apenas sintaxe e comandos. Mas em você vemos a capacidade de transformar problemas em soluções elegantes e ideias em realidades brilhantes.\n\n"
        "Se a vida fosse um repositório, o seu commit principal seria a gentileza, a paixão por criar e a capacidade de iluminar o dia de todos ao seu redor. Você é aquela pessoa rara que consegue ser extraordinariamente brilhante com a mente e infinitamente acolhedora com o coração.\n\n"
        "Que este seu novo ciclo seja um Deploy Perfeito: sem exceções não tratadas, com latência zero para a paz de espírito e alta disponibilidade para todos os seus sonhos!"
    )
    special_message_content = get_or_create_section(
        'special_message',
        'As Palavras Mais Lindas do Mundo',
        default_poetic
    )

    terminal_setting = get_or_create_section('terminal_setting', 'Configuração do Terminal', 'true')
    terminal_enabled = (terminal_setting.content == 'true')

    login_form = LoginForm()
    register_form = RegisterForm()
    wish_form = WishForm()
    profile_form = ProfileForm(name=current_user.name if current_user.is_authenticated else '')
    
    welcome_form = WelcomeSectionForm(
        title=welcome_content.title,
        content=welcome_content.content,
        image_fit=welcome_content.image_fit or 'contain'
    )
    special_msg_form = SpecialMessageSectionForm(title=special_message_content.title, content=special_message_content.content)

    users_list = []
    if current_user.is_authenticated and current_user.is_admin:
        users_list = User.query.order_by(User.created_at.desc()).all()

    active_step = 1
    if current_user.is_authenticated:
        active_step = current_user.active_step
    else:
        active_step = session.get('active_step', 1)

    return render_template(
        'index.html',
        wishes=wishes_data,
        welcome_content=welcome_content,
        special_message_content=special_message_content,
        terminal_enabled=terminal_enabled,
        login_form=login_form,
        register_form=register_form,
        wish_form=wish_form,
        profile_form=profile_form,
        welcome_form=welcome_form,
        special_msg_form=special_msg_form,
        users_list=users_list,
        active_step=active_step
    )
