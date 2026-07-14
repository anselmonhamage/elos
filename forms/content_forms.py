from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, TextAreaField, SelectField, MultipleFileField, BooleanField
from wtforms.validators import DataRequired, Optional

class WelcomeSectionForm(FlaskForm):
    title = StringField('Título de Boas-vindas', validators=[DataRequired(message='Informe o título')])
    content = TextAreaField('Mensagem de Boas-vindas', validators=[DataRequired(message='Informe a mensagem de boas-vindas')])
    images = MultipleFileField('Upload de Imagens (Selecione uma ou várias)', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png', 'webp', 'gif'], 'Apenas imagens (JPG, PNG, WEBP, GIF) são permitidas!')
    ])
    append_images = BooleanField('Adicionar novas fotos ao carrossel existente (em vez de substituir)', default=True)
    image_fit = SelectField('Ajuste Visual da Imagem', choices=[
        ('contain', 'Ajustar sem Recortes - Tamanho Natural (Contain)'),
        ('cover', 'Preencher e Recortar (Cover)'),
        ('scale-down', 'Tamanho Proporcional Reduzido (Scale-down)')
    ], default='contain')

class SpecialMessageSectionForm(FlaskForm):
    title = StringField('Título da Mensagem Especial', validators=[DataRequired(message='Informe o título')])
    content = TextAreaField('Conteúdo da Mensagem', validators=[DataRequired(message='Informe o conteúdo da mensagem')])
