from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class WishForm(FlaskForm):
    author = StringField('Seu Nome', validators=[DataRequired(message='Informe seu nome')])
    role = StringField('Seu Cargo ou Relação (ex: Amigo Dev)')
    message = TextAreaField('Sua Mensagem Carinhosa', validators=[DataRequired(message='A mensagem não pode estar vazia')])
