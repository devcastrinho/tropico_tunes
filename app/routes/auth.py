from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.extensions import db
from app.models import Address, User


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/cadastro", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("shop.home"))
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if len(name) < 2 or "@" not in email or len(password) < 8:
            flash("Preencha nome, e-mail válido e uma senha de ao menos 8 caracteres.", "error")
        elif User.query.filter_by(email=email).first():
            flash("Este e-mail já está cadastrado.", "error")
        else:
            user = User(name=name, email=email, phone=request.form.get("phone", "").strip())
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash("Bem-vindo à TRÓPICO!", "success")
            return redirect(url_for("shop.home"))
    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("shop.home"))
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(request.form.get("password", "")):
            login_user(user, remember=bool(request.form.get("remember")))
            return redirect(request.args.get("next") or url_for("shop.home"))
        flash("E-mail ou senha inválidos.", "error")
    return render_template("auth/login.html")


@auth_bp.post("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("shop.home"))


@auth_bp.route("/recuperar-senha", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        flash("Se o e-mail estiver cadastrado, enviaremos as instruções de recuperação.", "info")
        return redirect(url_for("auth.login"))
    return render_template("auth/forgot.html")


@auth_bp.route("/perfil", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        current_user.name = request.form.get("name", "").strip() or current_user.name
        current_user.phone = request.form.get("phone", "").strip()
        db.session.commit()
        flash("Perfil atualizado.", "success")
        return redirect(url_for("auth.profile"))
    return render_template("auth/profile.html")


@auth_bp.post("/perfil/endereco")
@login_required
def add_address():
    required = ["street", "number", "neighborhood", "city", "state", "zip_code"]
    if any(not request.form.get(field, "").strip() for field in required):
        flash("Preencha todos os campos obrigatórios do endereço.", "error")
    else:
        address = Address(user_id=current_user.id, **{field: request.form.get(field, "").strip() for field in required}, complement=request.form.get("complement", "").strip())
        db.session.add(address)
        db.session.commit()
        flash("Endereço adicionado.", "success")
    return redirect(url_for("auth.profile"))

