### Criar as rotas do site (os links) ###

from flask import render_template, url_for, redirect
from fakepinterest import app, database, bcrypt
from fakepinterest.models import Usuario, Foto
from flask_login import login_required, login_user, logout_user, current_user
from fakepinterest.forms import FormLogin, FormCriarConta, FormFoto
import os
from werkzeug.utils import secure_filename

# Criar uma rota para colocar o site no ar (disponível somente na rede privada do computador)
@app.route("/", methods=["GET", "POST"])
def homepage():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        # Se encontrou algum usuário e a senha digitada equivale a senha do usuário, faça login do usuário
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("homepage.html", form=form_login)

# Tela de "criar conta"
@app.route("/criarconta", methods=["GET", "POST"])
def criar_conta():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha)

        # Adicionar usuário no banco de dados
        database.session.add(usuario)
        database.session.commit()

        # Login do usuário antes de redirecioná-lo para o perfil dele
        login_user(usuario, remember=True) # para o sistema lembrar que o usuário está logado

        # Após a submissão do formulário, o usuário será direcionado para o perfil dele
        return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("criarconta.html", form=form_criarconta)

@app.route("/perfil/<id_usuario>", methods=["GET", "POST"])
@login_required # Faz com que a função "perfil(usuario)" só poderá ser acessada quando o usuário estiver logado
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
        # O usuário está vendo o perfil dele
        form_foto = FormFoto()
        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            # Salvar o arquivo na pasta fotos_posts
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                              app.config["UPLOAD_FOLDER"], nome_seguro)
            arquivo.save(caminho)
            # Criar foto e registrá-la no banco de dados
            foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit() # salva a modificação no banco de dados
        return render_template("perfil.html", usuario=current_user, form=form_foto)
    else:
        # O usuário está vendo o perfil de outro usuário
        usuario = Usuario.query.get(int(id_usuario))
        return render_template("perfil.html", usuario=usuario, form=None)

# Rota para a página de logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))

# Rota para o feed
@app.route("/feed")
@login_required
def feed():
    fotos= Foto.query.order_by(Foto.data_criacao.desc()).all()
    return render_template("feed.html", fotos=fotos)