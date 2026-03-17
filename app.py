# v1.0.1 - Redesign & i18n Fix
import os
from datetime import datetime, timedelta

import jwt
from bson import ObjectId
from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_mail import Mail, Message
from markupsafe import Markup, escape
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from db import (
    get_db,
    init_db,
    seed_admin,
    seed_about,
    seed_settings,
    get_setting,
    set_setting,
)

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev")

mail_settings = {
    "MAIL_SERVER": "smtp.gmail.com",
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.getenv("EMAIL"),
    "MAIL_PASSWORD": os.getenv("SENHA"),
}

app.config.update(mail_settings)
mail = Mail(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "static", "uploads")
try:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
except Exception as e:
    print(f"Erro ao criar diretório de uploads (comum em Vercel/Serverless): {e}")


def nl2br(value):
    if value is None:
        return ""
    return Markup("<br>".join(escape(value).splitlines()))


app.jinja_env.filters["nl2br"] = nl2br


def create_token(username):
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(hours=8),
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, app.secret_key, algorithm="HS256")


def decode_token(token):
    return jwt.decode(token, app.secret_key, algorithms=["HS256"])


def login_required(view):
    def wrapped(*args, **kwargs):
        token = request.cookies.get("auth_token")
        if not token:
            return redirect(url_for("login"))
        try:
            decode_token(token)
        except jwt.PyJWTError:
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    wrapped.__name__ = view.__name__
    return wrapped


def save_upload(file_storage):
    if not file_storage or not file_storage.filename:
        return ""
    filename = secure_filename(file_storage.filename)
    if not filename:
        return ""
    path = os.path.join(UPLOAD_DIR, filename)
    file_storage.save(path)
    return f"/static/uploads/{filename}"


def normalize_doc(doc):
    if not doc:
        return None
    doc["id"] = str(doc["_id"])
    return doc


def normalize_list(cursor):
    return [normalize_doc(doc) for doc in cursor]


def init_app_data():
    init_db()
    seed_settings(
        {
            "site_name": "Isaias Silva",
            "site_title": "QA Lead, Automatizador Cypress, Empreendedor",
            "profile_image": "/static/img/isa-perfil.jpg",
            "background_image": "/static/img/bannerPortifolio.png",
            "contact_email": "qa.eng.isaiasilva@gmail.com",
            "whatsapp": "https://wa.me/5571996838735",
        }
    )
    seed_about(
        "Acredito que a educação pode mudar a vida das pessoas e sou prova disso. "
        "Sou formado em Sistemas de Informação e tenho mais de 8 anos de experiência em testes de software."
    )
    default_pass = os.getenv("ADMIN_PASS", "Is@i@s1989")
    seed_admin(os.getenv("ADMIN_USER", "isaias"), generate_password_hash(default_pass))
    seed_admin(
        os.getenv("ADMIN_USER_EMAIL", "qa.eng.isaiasilva@gmail.com"),
        generate_password_hash(os.getenv("ADMIN_EMAIL_PASS", default_pass)),
    )


try:
    init_app_data()
except Exception as e:
    print(f"Erro ao inicializar dados do app (provável timeout no MongoDB): {e}")


@app.route("/")
def index():
    db = get_db()
    about_doc = db.about.find_one(sort=[("_id", -1)])
    skills = normalize_list(db.skills.find().sort([("sort_order", -1), ("_id", -1)]))
    experiences = normalize_list(
        db.experiences.find({"kind": "work"}).sort([("sort_order", -1), ("_id", -1)])
    )
    education = normalize_list(
        db.experiences.find({"kind": "education"}).sort([("sort_order", -1), ("_id", -1)])
    )
    projects = normalize_list(
        db.projects.find().sort([("featured", -1), ("_id", -1)])
    )

    settings = {
        "site_name": get_setting("site_name", "Isaias Silva"),
        "site_title": get_setting("site_title", "QA Lead, Automatizador Cypress, Empreendedor"),
        "profile_image": get_setting("profile_image", "/static/img/perfil.jpg"),
        "background_image": get_setting("background_image", "/static/img/bannerPortifolio.png"),
        "contact_email": get_setting("contact_email", "qa.eng.isaiasilva@gmail.com"),
        "whatsapp": get_setting("whatsapp", "https://wa.me/5571996838735"),
    }

    return render_template(
        "index.html",
        settings=settings,
        about=about_doc["content"] if about_doc else "",
        skills=skills,
        experiences=experiences,
        education=education,
        projects=projects,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        db = get_db()
        user = db.users.find_one({"username": username})
        if user and check_password_hash(user["password_hash"], password):
            token = create_token(username)
            resp = make_response(redirect(url_for("admin")))
            resp.set_cookie("auth_token", token, httponly=True, samesite="Lax")
            return resp
        flash("Usuário ou senha inválidos.")
    return render_template("login.html")


@app.route("/logout")
def logout():
    resp = make_response(redirect(url_for("login")))
    resp.set_cookie("auth_token", "", expires=0)
    return resp


@app.route("/admin")
@login_required
def admin():
    db = get_db()
    skills = normalize_list(db.skills.find().sort([("sort_order", -1), ("_id", -1)]))
    experiences = normalize_list(
        db.experiences.find({"kind": "work"}).sort([("sort_order", -1), ("_id", -1)])
    )
    education = normalize_list(
        db.experiences.find({"kind": "education"}).sort([("sort_order", -1), ("_id", -1)])
    )
    projects = normalize_list(db.projects.find().sort([("_id", -1)]))
    messages = normalize_list(db.messages.find().sort([("_id", -1)]))
    about_doc = db.about.find_one(sort=[("_id", -1)])

    settings = {
        "site_name": get_setting("site_name", ""),
        "site_title": get_setting("site_title", ""),
        "profile_image": get_setting("profile_image", ""),
        "background_image": get_setting("background_image", ""),
        "contact_email": get_setting("contact_email", ""),
        "whatsapp": get_setting("whatsapp", ""),
    }

    return render_template(
        "admin.html",
        settings=settings,
        about=about_doc["content"] if about_doc else "",
        skills=skills,
        experiences=experiences,
        education=education,
        projects=projects,
        messages=messages,
    )


@app.route("/admin/profile", methods=["POST"])
@login_required
def admin_profile():
    name = request.form.get("site_name", "").strip()
    title = request.form.get("site_title", "").strip()
    whatsapp = request.form.get("whatsapp", "").strip()
    contact_email = request.form.get("contact_email", "").strip()

    if name:
        set_setting("site_name", name)
    if title:
        set_setting("site_title", title)
    if whatsapp:
        set_setting("whatsapp", whatsapp)
    if contact_email:
        set_setting("contact_email", contact_email)

    profile_image = save_upload(request.files.get("profile_image"))
    background_image = save_upload(request.files.get("background_image"))
    if profile_image:
        set_setting("profile_image", profile_image)
    if background_image:
        set_setting("background_image", background_image)

    flash("Perfil atualizado.")
    return redirect(url_for("admin"))


@app.route("/admin/about", methods=["POST"])
@login_required
def admin_about():
    content = request.form.get("about_content", "").strip()
    if content:
        db = get_db()
        db.about.insert_one({"content": content, "created_at": datetime.utcnow()})
        flash("Sobre atualizado.")
    return redirect(url_for("admin"))


@app.route("/admin/skills/add", methods=["POST"])
@login_required
def admin_skills_add():
    name = request.form.get("name", "").strip()
    level = request.form.get("level", "").strip()
    icon = request.form.get("icon", "").strip()
    if name and level.isdigit():
        db = get_db()
        max_doc = db.skills.find_one(sort=[("sort_order", -1)])
        next_order = (max_doc.get("sort_order", 0) + 1) if max_doc else 1
        db.skills.insert_one(
            {"name": name, "level": int(level), "icon": icon, "sort_order": next_order}
        )
        flash("Habilidade adicionada.")
    return redirect(url_for("admin"))


@app.route("/admin/skills/<string:skill_id>/delete", methods=["POST"])
@login_required
def admin_skills_delete(skill_id):
    db = get_db()
    db.skills.delete_one({"_id": ObjectId(skill_id)})
    flash("Habilidade removida.")
    return redirect(url_for("admin"))


@app.route("/admin/skills/<string:skill_id>/update", methods=["POST"])
@login_required
def admin_skills_update(skill_id):
    name = request.form.get("name", "").strip()
    level = request.form.get("level", "").strip()
    icon = request.form.get("icon", "").strip()
    if name and level.isdigit():
        db = get_db()
        db.skills.update_one(
            {"_id": ObjectId(skill_id)},
            {"$set": {"name": name, "level": int(level), "icon": icon}},
        )
        flash("Habilidade atualizada.")
    return redirect(url_for("admin"))


@app.route("/admin/experiences/add", methods=["POST"])
@login_required
def admin_experiences_add():
    kind = request.form.get("kind", "work")
    company = request.form.get("company", "").strip()
    role = request.form.get("role", "").strip()
    start_date = request.form.get("start_date", "").strip()
    end_date = request.form.get("end_date", "").strip()
    description = request.form.get("description", "").strip()
    sort_order = request.form.get("sort_order", "0").strip()

    if company and role:
        db = get_db()
        db.experiences.insert_one(
            {
                "kind": kind,
                "company": company,
                "role": role,
                "start_date": start_date,
                "end_date": end_date,
                "description": description,
                "sort_order": int(sort_order or 0),
            }
        )
        flash("Experiência adicionada.")
    return redirect(url_for("admin"))


@app.route("/admin/experiences/<string:exp_id>/delete", methods=["POST"])
@login_required
def admin_experiences_delete(exp_id):
    db = get_db()
    db.experiences.delete_one({"_id": ObjectId(exp_id)})
    flash("Experiência removida.")
    return redirect(url_for("admin"))


@app.route("/admin/experiences/<string:exp_id>/update", methods=["POST"])
@login_required
def admin_experiences_update(exp_id):
    company = request.form.get("company", "").strip()
    role = request.form.get("role", "").strip()
    start_date = request.form.get("start_date", "").strip()
    end_date = request.form.get("end_date", "").strip()
    description = request.form.get("description", "").strip()
    sort_order = request.form.get("sort_order", "0").strip()
    if company and role:
        db = get_db()
        db.experiences.update_one(
            {"_id": ObjectId(exp_id)},
            {
                "$set": {
                    "company": company,
                    "role": role,
                    "start_date": start_date,
                    "end_date": end_date,
                    "description": description,
                    "sort_order": int(sort_order or 0),
                }
            },
        )
        flash("Experiência atualizada.")
    return redirect(url_for("admin"))


@app.route("/admin/projects/add", methods=["POST"])
@login_required
def admin_projects_add():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    tech = request.form.get("tech", "").strip()
    project_url = request.form.get("project_url", "").strip()
    repo_url = request.form.get("repo_url", "").strip()
    featured = 1 if request.form.get("featured") == "on" else 0
    image_url = request.form.get("image_url", "").strip()
    image_upload = save_upload(request.files.get("image_upload"))
    if image_upload:
        image_url = image_upload

    if title:
        db = get_db()
        db.projects.insert_one(
            {
                "title": title,
                "description": description,
                "tech": tech,
                "project_url": project_url,
                "repo_url": repo_url,
                "image_url": image_url,
                "featured": featured,
            }
        )
        flash("Projeto adicionado.")
    return redirect(url_for("admin"))


@app.route("/admin/projects/<string:project_id>/delete", methods=["POST"])
@login_required
def admin_projects_delete(project_id):
    db = get_db()
    db.projects.delete_one({"_id": ObjectId(project_id)})
    flash("Projeto removido.")
    return redirect(url_for("admin"))


@app.route("/admin/projects/<string:project_id>/update", methods=["POST"])
@login_required
def admin_projects_update(project_id):
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    tech = request.form.get("tech", "").strip()
    project_url = request.form.get("project_url", "").strip()
    repo_url = request.form.get("repo_url", "").strip()
    featured = 1 if request.form.get("featured") == "on" else 0
    image_url = request.form.get("image_url", "").strip()
    image_upload = save_upload(request.files.get("image_upload"))
    if image_upload:
        image_url = image_upload
    if title:
        db = get_db()
        db.projects.update_one(
            {"_id": ObjectId(project_id)},
            {
                "$set": {
                    "title": title,
                    "description": description,
                    "tech": tech,
                    "project_url": project_url,
                    "repo_url": repo_url,
                    "image_url": image_url,
                    "featured": featured,
                }
            },
        )
        flash("Projeto atualizado.")
    return redirect(url_for("admin"))


@app.route("/admin/messages/<string:message_id>/delete", methods=["POST"])
@login_required
def admin_messages_delete(message_id):
    db = get_db()
    db.messages.delete_one({"_id": ObjectId(message_id)})
    flash("Mensagem removida.")
    return redirect(url_for("admin"))


@app.route("/send", methods=["POST"])
def send():
    name = request.form.get("nome", "").strip()
    email = request.form.get("email", "").strip()
    subject = request.form.get("assunto", "").strip()
    message_text = request.form.get("mensagem", "").strip()

    if not name or not email or not message_text:
        flash("Preencha todos os campos obrigatórios.")
        return redirect(url_for("index"))

    db = get_db()
    db.messages.insert_one(
        {
            "name": name,
            "email": email,
            "subject": subject,
            "message": message_text,
            "created_at": datetime.utcnow(),
        }
    )

    recipient = get_setting("contact_email", "qa.eng.isaiasilva@gmail.com")
    msg = Message(
        subject=subject or f"{name} enviou uma mensagem pelo site",
        sender=app.config.get("MAIL_USERNAME"),
        recipients=[recipient],
        body=f"{name} ({email}) enviou:\n\n{message_text}",
    )
    mail.send(msg)
    flash("Mensagem enviada com sucesso!")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
