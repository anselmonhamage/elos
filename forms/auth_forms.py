from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(message='Informe seu e-mail'), Email(message='E-mail inválido')])
    password = PasswordField('Senha', validators=[DataRequired(message='Informe sua senha')])
    remember_me = BooleanField('Lembrar-me')

class RegisterForm(FlaskForm):
    name = StringField('Nome Completo', validators=[DataRequired(message='Informe seu nome')])
    email = StringField('E-mail', validators=[DataRequired(message='Informe seu e-mail'), Email(message='E-mail inválido')])
    password = PasswordField('Senha', validators=[DataRequired(message='Informe sua senha'), Length(min=6, message='A senha deve ter no mínimo 6 caracteres')])
    confirm_password = PasswordField('Confirmar Senha', validators=[DataRequired(message='Confirme sua senha'), EqualTo('password', message='As senhas não coincidem')])
