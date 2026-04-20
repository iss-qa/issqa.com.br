# v1.0.1 - Redesign & i18n Fix
import base64
import os
import re
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
    try:
        path = os.path.join(UPLOAD_DIR, filename)
        file_storage.save(path)
        return f"/static/uploads/{filename}"
    except OSError as e:
        # Read-only filesystem (Vercel/serverless). Fall back to base64 data URI.
        print(f"Filesystem write falhou ({e}); armazenando imagem como data URI.")
        try:
            file_storage.stream.seek(0)
        except Exception:
            pass
        data = file_storage.read()
        mime = file_storage.mimetype or "application/octet-stream"
        b64 = base64.b64encode(data).decode("ascii")
        return f"data:{mime};base64,{b64}"


CONTRACT_TYPES = ["CLT", "PJ", "Contrato", "Freelancer", "Estágio", "Cooperado"]


def _tab_for_kind(kind):
    return "tab-edu" if kind == "education" else "tab-exp"


_MONTH_RE = re.compile(r"^(\d{1,2})[./-](\d{4})$")
_YEAR_RE = re.compile(r"^(\d{4})$")
_CURRENT_TOKENS = {"atual", "present", "current", "agora", "hoje", "now"}


def parse_exp_date(value, is_end=False):
    """Parse date strings like '09.2024', '2014', 'Atual', or empty.

    Returns a sortable tuple (year, month). For end dates, blank or 'Atual'
    is treated as the future so currently-active experiences sort to the top.
    """
    if value is None:
        value = ""
    s = str(value).strip().lower()
    if not s:
        return (9999, 12) if is_end else (0, 0)
    if is_end and s in _CURRENT_TOKENS:
        return (9999, 12)
    m = _MONTH_RE.match(s)
    if m:
        return (int(m.group(2)), int(m.group(1)))
    m = _YEAR_RE.match(s)
    if m:
        return (int(m.group(1)), 12 if is_end else 1)
    return (0, 0)


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
            # Entrepreneur Section Basics
            "emp_title": "Empreendedor",
            "emp_desc1": "Atualmente venho desenvolvendo e estruturando um projeto pessoal, inclusive contratando Devs Front e Back para a implementação de uma possível solução que pode se tornar o carro chefe da minha pequena empresa.",
            "emp_desc2": "Dedico meu tempo para coordenar e gerenciar uma pequena empresa, bem como para apoiar causas sociais, como resgatar e orientar jovens da droga e da perdição para o caminho de Cristo.",
            "emp_niver": "14 de Setembro de 1989",
            "emp_idade": "33 anos",
            "emp_cidade": "Lauro de Freitas",
            "emp_estado": "Bahia",
            "emp_hobby": "Viajar",
            "emp_site": "links.isaiasilva",
            "emp_site_url": "https://links.isaiasilva.com.br",
            "emp_trabalho": "CEO - ISSQA",
            "emp_trabalho_url": "https://issqa.com.br",
            "emp_xp": "+10 anos",
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
    try:
        about_doc = db.about.find_one(sort=[("_id", -1)])
        skills = normalize_list(db.skills.find().sort([("sort_order", 1), ("_id", -1)]))
        experiences = normalize_list(
            db.experiences.find({"kind": "work"}).sort([("sort_order", 1), ("_id", -1)])
        )
        education = normalize_list(
            db.experiences.find({"kind": "education"}).sort([("sort_order", 1), ("_id", -1)])
        )
        projects = normalize_list(
            db.projects.find().sort([("featured", -1), ("sort_order", 1), ("_id", -1)])
        )
    except Exception as e:
        print(f"Erro ao buscar dados do banco: {e}")
        about_doc = None
        skills = []
        experiences = []
        education = []
        projects = []

    settings = {
        "site_name": get_setting("site_name", "Isaias Silva"),
        "site_title": get_setting("site_title", "QA Lead, Automatizador Cypress, Empreendedor"),
        "site_title_en": get_setting("site_title_en", ""),
        "profile_image": get_setting("profile_image", "/static/img/perfil.jpg"),
        "background_image": get_setting("background_image", "/static/img/bannerPortifolio.png"),
        "contact_email": get_setting("contact_email", "qa.eng.isaiasilva@gmail.com"),
        "whatsapp": get_setting("whatsapp", "https://wa.me/5571996838735"),
        "emp_title": get_setting("emp_title", "Empreendedor"),
        "emp_title_en": get_setting("emp_title_en", ""),
        "emp_desc1": get_setting("emp_desc1", ""),
        "emp_desc1_en": get_setting("emp_desc1_en", ""),
        "emp_desc2": get_setting("emp_desc2", ""),
        "emp_desc2_en": get_setting("emp_desc2_en", ""),
        "emp_niver": get_setting("emp_niver", "14 de Setembro de 1989"),
        "emp_niver_en": get_setting("emp_niver_en", ""),
        "emp_idade": get_setting("emp_idade", "33 anos"),
        "emp_idade_en": get_setting("emp_idade_en", ""),
        "emp_cidade": get_setting("emp_cidade", "Lauro de Freitas"),
        "emp_estado": get_setting("emp_estado", "Bahia"),
        "emp_estado_en": get_setting("emp_estado_en", ""),
        "emp_hobby": get_setting("emp_hobby", "Viajar"),
        "emp_hobby_en": get_setting("emp_hobby_en", ""),
        "emp_site": get_setting("emp_site", "links.isaiasilva"),
        "emp_site_url": get_setting("emp_site_url", "https://links.isaiasilva.com.br"),
        "emp_trabalho": get_setting("emp_trabalho", "CEO - ISSQA"),
        "emp_trabalho_en": get_setting("emp_trabalho_en", ""),
        "emp_trabalho_url": get_setting("emp_trabalho_url", "https://issqa.com.br"),
        "emp_xp": get_setting("emp_xp", "+10 anos"),
        "emp_xp_en": get_setting("emp_xp_en", ""),
    }

    return render_template(
        "index.html",
        settings=settings,
        about=about_doc["content"] if about_doc else "",
        about_en=about_doc.get("content_en", "") if about_doc else "",
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
    skills = normalize_list(db.skills.find().sort([("sort_order", 1), ("_id", -1)]))
    experiences = normalize_list(
        db.experiences.find({"kind": "work"}).sort([("sort_order", 1), ("_id", -1)])
    )
    education = normalize_list(
        db.experiences.find({"kind": "education"}).sort([("sort_order", 1), ("_id", -1)])
    )
    projects = normalize_list(db.projects.find().sort([("sort_order", 1), ("_id", -1)]))
    messages = normalize_list(db.messages.find().sort([("_id", -1)]))
    about_doc = db.about.find_one(sort=[("_id", -1)])

    settings = {
        "site_name": get_setting("site_name", ""),
        "site_title": get_setting("site_title", ""),
        "site_title_en": get_setting("site_title_en", ""),
        "profile_image": get_setting("profile_image", ""),
        "background_image": get_setting("background_image", ""),
        "contact_email": get_setting("contact_email", ""),
        "whatsapp": get_setting("whatsapp", ""),
        "emp_title": get_setting("emp_title", "Empreendedor"),
        "emp_title_en": get_setting("emp_title_en", ""),
        "emp_desc1": get_setting("emp_desc1", ""),
        "emp_desc1_en": get_setting("emp_desc1_en", ""),
        "emp_desc2": get_setting("emp_desc2", ""),
        "emp_desc2_en": get_setting("emp_desc2_en", ""),
        "emp_niver": get_setting("emp_niver", ""),
        "emp_niver_en": get_setting("emp_niver_en", ""),
        "emp_idade": get_setting("emp_idade", ""),
        "emp_idade_en": get_setting("emp_idade_en", ""),
        "emp_cidade": get_setting("emp_cidade", ""),
        "emp_estado": get_setting("emp_estado", ""),
        "emp_estado_en": get_setting("emp_estado_en", ""),
        "emp_hobby": get_setting("emp_hobby", ""),
        "emp_hobby_en": get_setting("emp_hobby_en", ""),
        "emp_site": get_setting("emp_site", ""),
        "emp_site_url": get_setting("emp_site_url", ""),
        "emp_trabalho": get_setting("emp_trabalho", ""),
        "emp_trabalho_en": get_setting("emp_trabalho_en", ""),
        "emp_trabalho_url": get_setting("emp_trabalho_url", ""),
        "emp_xp": get_setting("emp_xp", ""),
        "emp_xp_en": get_setting("emp_xp_en", ""),
    }

    return render_template(
        "admin.html",
        settings=settings,
        about=about_doc["content"] if about_doc else "",
        about_en=about_doc.get("content_en", "") if about_doc else "",
        skills=skills,
        experiences=experiences,
        education=education,
        projects=projects,
        messages=messages,
        contract_types=CONTRACT_TYPES,
    )


@app.route("/admin/profile", methods=["POST"])
@login_required
def admin_profile():
    name = request.form.get("site_name", "").strip()
    title = request.form.get("site_title", "").strip()
    title_en = request.form.get("site_title_en", "").strip()
    whatsapp = request.form.get("whatsapp", "").strip()
    contact_email = request.form.get("contact_email", "").strip()

    if name:
        set_setting("site_name", name)
    if title:
        set_setting("site_title", title)
    set_setting("site_title_en", title_en)
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
    content = request.form.get("about_content", "")
    content_en = request.form.get("about_content_en", "")
    if content:
        db = get_db()
        db.about.insert_one(
            {"content": content, "content_en": content_en, "created_at": datetime.utcnow()}
        )
        flash("Sobre atualizado.")
    return redirect(url_for("admin"))


@app.route("/admin/entrepreneur", methods=["POST"])
@login_required
def admin_entrepreneur():
    fields = [
        "emp_title",
        "emp_title_en",
        "emp_desc1",
        "emp_desc1_en",
        "emp_desc2",
        "emp_desc2_en",
        "emp_niver",
        "emp_niver_en",
        "emp_idade",
        "emp_idade_en",
        "emp_cidade",
        "emp_estado",
        "emp_estado_en",
        "emp_hobby",
        "emp_hobby_en",
        "emp_site",
        "emp_site_url",
        "emp_trabalho",
        "emp_trabalho_en",
        "emp_trabalho_url",
        "emp_xp",
        "emp_xp_en",
    ]
    for field in fields:
        val = request.form.get(field, "").strip()
        set_setting(field, val)

    flash("Seção Empreendedor atualizada.")
    return redirect(url_for("admin"))


@app.route("/admin/skills/add", methods=["POST"])
@login_required
def admin_skills_add():
    name = request.form.get("name", "").strip()
    name_en = request.form.get("name_en", "").strip()
    level = request.form.get("level", "").strip()
    icon = request.form.get("icon", "").strip()
    if name and level.isdigit():
        db = get_db()
        max_doc = db.skills.find_one(sort=[("sort_order", -1)])
        next_order = (max_doc.get("sort_order", 0) + 1) if max_doc else 1
        db.skills.insert_one(
            {
                "name": name,
                "name_en": name_en,
                "level": int(level),
                "icon": icon,
                "sort_order": next_order,
            }
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
    name_en = request.form.get("name_en", "").strip()
    level = request.form.get("level", "").strip()
    icon = request.form.get("icon", "").strip()
    if name and level.isdigit():
        db = get_db()
        db.skills.update_one(
            {"_id": ObjectId(skill_id)},
            {"$set": {"name": name, "name_en": name_en, "level": int(level), "icon": icon}},
        )
        flash("Habilidade atualizada.")
    return redirect(url_for("admin"))


@app.route("/admin/experiences/add", methods=["POST"])
@login_required
def admin_experiences_add():
    kind = request.form.get("kind", "work")
    company = request.form.get("company", "").strip()
    company_en = request.form.get("company_en", "").strip()
    role = request.form.get("role", "").strip()
    role_en = request.form.get("role_en", "").strip()
    start_date = request.form.get("start_date", "").strip()
    end_date = request.form.get("end_date", "").strip()
    description = request.form.get("description", "").strip()
    description_en = request.form.get("description_en", "").strip()
    sort_order = request.form.get("sort_order", "0").strip()
    contract_type = request.form.get("contract_type", "").strip()
    if contract_type and contract_type not in CONTRACT_TYPES:
        contract_type = ""

    if company and role:
        db = get_db()
        db.experiences.insert_one(
            {
                "kind": kind,
                "company": company,
                "company_en": company_en,
                "role": role,
                "role_en": role_en,
                "start_date": start_date,
                "end_date": end_date,
                "description": description,
                "description_en": description_en,
                "sort_order": int(sort_order or 0),
                "contract_type": contract_type,
            }
        )
        flash("Experiência adicionada.")
    return redirect(url_for("admin", _anchor=_tab_for_kind(kind)))


@app.route("/admin/experiences/<string:exp_id>/delete", methods=["POST"])
@login_required
def admin_experiences_delete(exp_id):
    db = get_db()
    doc = db.experiences.find_one({"_id": ObjectId(exp_id)}, {"kind": 1})
    db.experiences.delete_one({"_id": ObjectId(exp_id)})
    flash("Experiência removida.")
    return redirect(url_for("admin", _anchor=_tab_for_kind((doc or {}).get("kind"))))


@app.route("/admin/experiences/<string:exp_id>/update", methods=["POST"])
@login_required
def admin_experiences_update(exp_id):
    company = request.form.get("company", "").strip()
    company_en = request.form.get("company_en", "").strip()
    role = request.form.get("role", "").strip()
    role_en = request.form.get("role_en", "").strip()
    start_date = request.form.get("start_date", "").strip()
    end_date = request.form.get("end_date", "").strip()
    description = request.form.get("description", "").strip()
    description_en = request.form.get("description_en", "").strip()
    sort_order = request.form.get("sort_order", "0").strip()
    contract_type = request.form.get("contract_type", "").strip()
    if contract_type and contract_type not in CONTRACT_TYPES:
        contract_type = ""
    kind = None
    if company and role:
        db = get_db()
        existing = db.experiences.find_one({"_id": ObjectId(exp_id)}, {"kind": 1})
        kind = (existing or {}).get("kind")
        db.experiences.update_one(
            {"_id": ObjectId(exp_id)},
            {
                "$set": {
                    "company": company,
                    "company_en": company_en,
                    "role": role,
                    "role_en": role_en,
                    "start_date": start_date,
                    "end_date": end_date,
                    "description": description,
                    "description_en": description_en,
                    "sort_order": int(sort_order or 0),
                    "contract_type": contract_type,
                }
            },
        )
        flash("Experiência atualizada.")
    return redirect(url_for("admin", _anchor=_tab_for_kind(kind)))


@app.route("/admin/experiences/reorder", methods=["POST"])
@login_required
def admin_experiences_reorder():
    data = request.get_json(silent=True) or {}
    order = data.get("order") or []
    if not order:
        return {"status": "empty"}, 400
    db = get_db()
    n = len(order)
    try:
        for idx, exp_id in enumerate(order):
            db.experiences.update_one(
                {"_id": ObjectId(exp_id)},
                {"$set": {"sort_order": idx}},
            )
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500
    return {"status": "ok"}


@app.route("/admin/experiences/auto-order", methods=["POST"])
@login_required
def admin_experiences_auto_order():
    kind = request.form.get("kind", "work")
    db = get_db()
    items = list(db.experiences.find({"kind": kind}))

    def key_fn(doc):
        return (
            parse_exp_date(doc.get("end_date", ""), is_end=True),
            parse_exp_date(doc.get("start_date", ""), is_end=False),
        )

    items.sort(key=key_fn, reverse=True)
    for idx, doc in enumerate(items):
        db.experiences.update_one(
            {"_id": doc["_id"]},
            {"$set": {"sort_order": idx}},
        )
    flash("Ordenação automática aplicada pela data.")
    return redirect(url_for("admin", _anchor=_tab_for_kind(kind)))


@app.route("/admin/projects/add", methods=["POST"])
@login_required
def admin_projects_add():
    title = request.form.get("title", "").strip()
    title_en = request.form.get("title_en", "").strip()
    description = request.form.get("description", "").strip()
    description_en = request.form.get("description_en", "").strip()
    tech = request.form.get("tech", "").strip()
    tech_en = request.form.get("tech_en", "").strip()
    project_url = request.form.get("project_url", "").strip()
    repo_url = request.form.get("repo_url", "").strip()
    featured = 1 if request.form.get("featured") == "on" else 0
    image_url = request.form.get("image_url", "").strip()
    image_upload = save_upload(request.files.get("image_upload"))
    if image_upload:
        image_url = image_upload

    if title:
        db = get_db()
        max_doc = db.projects.find_one(sort=[("sort_order", -1)])
        next_order = (max_doc.get("sort_order", 0) + 1) if max_doc else 0
        db.projects.insert_one(
            {
                "title": title,
                "title_en": title_en,
                "description": description,
                "description_en": description_en,
                "tech": tech,
                "tech_en": tech_en,
                "project_url": project_url,
                "repo_url": repo_url,
                "image_url": image_url,
                "featured": featured,
                "sort_order": next_order,
            }
        )
        flash("Projeto adicionado.")
    return redirect(url_for("admin", _anchor="tab-projects"))


@app.route("/admin/projects/<string:project_id>/delete", methods=["POST"])
@login_required
def admin_projects_delete(project_id):
    db = get_db()
    db.projects.delete_one({"_id": ObjectId(project_id)})
    flash("Projeto removido.")
    return redirect(url_for("admin", _anchor="tab-projects"))


@app.route("/admin/projects/<string:project_id>/update", methods=["POST"])
@login_required
def admin_projects_update(project_id):
    title = request.form.get("title", "").strip()
    title_en = request.form.get("title_en", "").strip()
    description = request.form.get("description", "").strip()
    description_en = request.form.get("description_en", "").strip()
    tech = request.form.get("tech", "").strip()
    tech_en = request.form.get("tech_en", "").strip()
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
                    "title_en": title_en,
                    "description": description,
                    "description_en": description_en,
                    "tech": tech,
                    "tech_en": tech_en,
                    "project_url": project_url,
                    "repo_url": repo_url,
                    "image_url": image_url,
                    "featured": featured,
                }
            },
        )
        flash("Projeto atualizado.")
    return redirect(url_for("admin", _anchor="tab-projects"))


@app.route("/admin/projects/reorder", methods=["POST"])
@login_required
def admin_projects_reorder():
    data = request.get_json(silent=True) or {}
    order = data.get("order") or []
    if not order:
        return {"status": "empty"}, 400
    db = get_db()
    try:
        for idx, project_id in enumerate(order):
            db.projects.update_one(
                {"_id": ObjectId(project_id)},
                {"$set": {"sort_order": idx}},
            )
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500
    return {"status": "ok"}


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
