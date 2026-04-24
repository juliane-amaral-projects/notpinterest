from flask import Flask # O Flask com 'F' maiúsculo irá criar o site
from flask_sqlalchemy import SQLAlchemy # cria o banco de dados
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

# Criação do app (aplicação), que é o site
app = Flask(__name__)

#link

# Configurar variável do APP
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config["SECRET_KEY"] = "e413aabd15f9e7cdd9afc8a234d021d6"
app.config["UPLOAD_FOLDER"] = "static/fotos_posts"

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homepage" # nome da função em "routes.py"

from fakepinterest import routes