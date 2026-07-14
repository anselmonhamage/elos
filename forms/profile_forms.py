from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField
from wtforms.validators import DataRequired, Optional

class ProfileForm(FlaskForm):
    name = StringField('Seu Nome Completo', validators=[DataRequired(message='Informe seu nome')])
    profile_image = FileField('Foto de Perfil (Base64)', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png', 'webp', 'gif'], 'Apenas arquivos de imagem (JPG, PNG, WEBP, GIF) são permitidos!')
    ])
