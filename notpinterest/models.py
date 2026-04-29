### Criar a estrutura do banco de dados ###

from notpinterest import database, login_manager
from datetime import datetime
from flask_login import UserMixin # O "UserMixin" diz qual é a classe que vai gerenciar a estrutura de logins

# Seleciona um usuário de acordo com o ID dele
@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario)) # retorna um determinado usuário

class Usuario(database.Model, UserMixin):
    # Características dos usuários
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)# unique=True
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    fotos = database.relationship("Foto", backref="usuario", lazy=True)

class Foto(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    imagem = database.Column(database.String, default="default.png") # Irá armazenar o nome que a imagem possui dentro da pasta 'static'
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
