# Importar os módulos necessários
from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

# Criar uma instância da aplicação flask
app = Flask(__name__)

# Definir uma chave secreta para a sessão
app.secret_key = "copilot"

# Definir a string de conexão com o banco de dados sqlite
# Você deve substituir o caminho_do_arquivo.db pelo seu
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'

# Criar uma instância do SQLAlchemy
db = SQLAlchemy(app)

# Criar uma instância do LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Definir a classe do modelo de usuário
class User(UserMixin, db.Model):
    # Definir o nome da tabela
    __tablename__ = "users"

    # Definir os campos da tabela
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    accesslevel = db.Column(db.Integer, nullable=False)

    # Definir o método de representação do objeto
    def __repr__(self):
        return f"<User {self.username}>"

# Definir uma função que carrega um usuário pelo seu id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Definir uma rota para a página de cadastro
@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    return render_template("cadastrar.html")

# Definir uma rota para a página de registro
@app.route("/register", methods=["GET", "POST"])
def register():
    # Verificar se o método da requisição é POST
    if request.method == "POST":
        # Obter os dados do formulário
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        accesslevel = request.form.get("accesslevel")

        # Gerar um hash da senha
        secure_password = generate_password_hash(password)

        # Verificar se o nome de usuário já existe no banco de dados
        user = User.query.filter_by(username=username).first()

        # Se o nome de usuário não existe e as senhas são iguais
        if user is None and password == confirm:
            # Criar um novo objeto de usuário
            new_user = User(name=name, username=username, password=secure_password,accesslevel=accesslevel)

            # Adicionar o usuário ao banco de dados
            db.session.add(new_user)
            db.session.commit()

            # Redirecionar para a página de login com uma mensagem de sucesso
            flash("Você se registrou com sucesso. Agora você pode fazer o login.", "success")
            return redirect(url_for("login"))
        else:
            # Retornar uma mensagem de erro
            flash("O nome de usuário já existe ou as senhas não são iguais.", "danger")
            return render_template("register.html")
    else:
        # Retornar um template de registro
        return render_template("register.html")

@app.route("/alterar_senha", methods=["GET", "POST"])
@login_required
def alterar_senha():
    return render_template("profile.html",alterar_senha=True,user=current_user)

@app.route("/salvar_nova_senha", methods=["GET", "POST"])
def salvar_nova_senha():
    id = request.form.get("id")
    password_old = request.form.get("password_old")
    password_new = request.form.get("password_new")
    confirm = request.form.get("confirm")

    # Verificar se o nome de usuário já existe no banco de dados
    user = User.query.filter_by(id=id).first()
    # Se o nome de usuário não existe e as senhas são iguais
    if user and check_password_hash(user.password, password_old):
        if password_new == confirm:
            user.name = user.name
            user.password = generate_password_hash(password_new)
            user.accesslevel = user.accesslevel
            # Adicionar o usuário ao banco de dados
            #db.session.add(new_user)
            db.session.commit()
            flash("Senha alterada com sucesso.", "success")
            return render_template("profile.html", user=current_user)
        else:
            flash("Erro ao alterar senha. As senhas novas não conferem.", "danger")
            return render_template("profile.html", user=current_user)
    else:
        flash("Erro ao alterar senha. Senha antiga está incorreta.", "danger")
        return render_template("profile.html", user=current_user)

# Definir uma rota para a página de login
@app.route("/login", methods=["GET", "POST"])
def login():
    # Verificar se o método da requisição é POST
    if request.method == "POST":
        # Obter os dados do formulário
        username = request.form.get("username")
        password = request.form.get("password")
        remember = request.form.get("remember")

        # Buscar o usuário pelo nome de usuário no banco de dados
        user = User.query.filter_by(username=username).first()

        # Se o usuário existe e a senha está correta
        if user and check_password_hash(user.password, password):
            # Fazer o login do usuário
            login_user(user, remember=remember)

            # Redirecionar para a página inicial com uma mensagem de sucesso
            flash("Você fez o login com sucesso.", "success")
            return redirect(url_for("home"))
        else:
            # Retornar uma mensagem de erro
            flash("Nome de usuário ou senha inválidos.", "danger")
            return render_template("login.html")
    else:
        # Retornar um template de login
        return render_template("login.html")

# Definir uma rota para a página de logout
@app.route("/logout")
@login_required
def logout():
    # Fazer o logout do usuário
    logout_user()

    # Redirecionar para a página inicial com uma mensagem de sucesso
    flash("Você saiu da sua conta.", "success")
    return redirect(url_for("index"))

# Definir uma rota para a página inicial
@app.route("/")
def index():
    # Retornar um template de index
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("home.html")

# Definir uma rota para a página de perfil
@app.route("/profile")
@login_required
def profile():
    # Retornar um template de perfil com os dados do usuário atual
    return render_template("profile.html", user=current_user)

# Definir uma função que é executada antes de cada requisição
@app.before_request
def make_session_permanent():
    # Definir a sessão como permanente
    session.permanent = True

    # Definir o tempo de vida da sessão como 30 minutos
    app.permanent_session_lifetime = timedelta(minutes=30)

# Executar a aplicação
if __name__ == "__main__":
    app.run()
