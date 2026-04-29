### Criar os formulários do site ###

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from notpinterest.models import Usuario

class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Fazer Login")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if not usuario:
            raise ValidationError("Usuário inexistente, crie uma conta.")

class FormCriarConta(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    username = StringField("Nome de Usuário", validators=[DataRequired()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)]) # Senha de 6 a 20 caracteres
    confirmacao_senha = PasswordField("Confirmação de Senha", validators=[DataRequired(), EqualTo("senha")])
    botao_confirmacao = SubmitField("Criar Conta")

    # Função criada devido ao campo "email" da classe "Usuario", em "models.py", ser definido como valor único (unique=True)
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        # Se o código acima retornar um email, então já existe um usuário. Desse modo, o sistema deve
        # impedir que outro usuário com o mesmo nome seja criado. Assim, deve retornar um erro
        if usuario:
            raise ValidationError("E-mail já cadastrado, faça login para continuar.")

    # Função criada devido ao campo "username" da classe "Usuario", em "models.py", ser definido como valor único (unique=True)
#    def validate_username(self, username):
#        usuario = Usuario.query.filter_by(username=username.data).first()
#         if usuario:
#            raise ValidationError("Este nome de usuário já está em uso. Escolha outro para continuar.")

# Permite com que o usuário envie uma foto
class FormFoto(FlaskForm):
    foto = FileField("Foto", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Enviar")