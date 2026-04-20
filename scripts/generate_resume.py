"""Gera PDFs de currículo (PT e EN) a partir dos dados do MongoDB.

Uso:
    venv/bin/python scripts/generate_resume.py

Saída:
    static/Isaias_Silva_Resume.pdf     (Português)
    static/Isaias_Silva_Resume_EN.pdf  (English)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    HRFlowable,
    ListFlowable,
    ListItem,
    KeepTogether,
)

from db import get_db, get_setting


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")

PRIMARY = HexColor("#021124")
ACCENT = HexColor("#149ddd")
MUTED = HexColor("#555555")


# ----------------------- Data helpers ---------------------------------


def fetch_data():
    db = get_db()
    skills = list(db.skills.find().sort([("sort_order", 1), ("_id", -1)]))
    works = list(
        db.experiences.find({"kind": "work"}).sort([("sort_order", 1), ("_id", -1)])
    )
    education = list(
        db.experiences.find({"kind": "education"}).sort(
            [("sort_order", 1), ("_id", -1)]
        )
    )
    settings = {
        "name": get_setting("site_name", "Isaias Silva"),
        "title_pt": get_setting(
            "site_title", "Senior QA Automation Engineer | Software Developer"
        ),
        "title_en": get_setting(
            "site_title_en", "Senior QA Automation Engineer | Software Developer"
        ),
        "email": get_setting("contact_email", "qa.eng.isaiasilva@gmail.com"),
        "city": get_setting("emp_cidade", "Lauro de Freitas"),
        "state": get_setting("emp_estado", "Bahia"),
        "state_en": get_setting("emp_estado_en", "Bahia, BR"),
        "experience": get_setting("emp_xp", "+15 anos"),
        "experience_en": get_setting("emp_xp_en", "15+ years"),
    }
    return settings, skills, works, education


# Stack categorization. Usa word-boundary para evitar que "ci" case com "perfecCIonista".
# Keywords já em minúsculas; testadas contra nome PT+EN.
STACK_CATEGORIES_PT = [
    ("Automação Web/API", ["automação de testes", "cypress", "selenium", "selenide", "playwright", "postman", "insomnia"]),
    ("Automação Mobile", ["appium", "maestro"]),
    ("Performance & Qualidade", ["performance", "gestão e técnicas", "gherkin", "bdd"]),
    ("Linguagens & Frameworks", ["linguagens de programação", "python", "typescript", "nestjs"]),
    ("DevOps & CI/CD", ["pipelines", "jenkins", "github actions", "ci/cd", "git", "deploy", "docker", "kubernetes"]),
    ("Bancos de Dados", ["banco de dados", "mysql", "mongo", "postgres", "redis"]),
    ("Soft Skills", [
        "liderança", "comunicação", "empatia", "proatividade",
        "trabalho em equipe", "comprometimento", "organizado", "metódico",
        "objetivo", "orientação a detalhes", "perfeccionista",
    ]),
]

STACK_CATEGORIES_EN = [
    ("Web/API Automation", ["automação de testes", "cypress", "selenium", "selenide", "playwright", "postman", "insomnia"]),
    ("Mobile Automation", ["appium", "maestro"]),
    ("Performance & QA Strategy", ["performance", "gestão e técnicas", "gherkin", "bdd"]),
    ("Languages & Frameworks", ["linguagens de programação", "python", "typescript", "nestjs"]),
    ("DevOps & CI/CD", ["pipelines", "jenkins", "github actions", "ci/cd", "git", "deploy", "docker", "kubernetes"]),
    ("Databases", ["banco de dados", "mysql", "mongo", "postgres", "redis"]),
    ("Soft Skills", [
        "liderança", "comunicação", "empatia", "proatividade",
        "trabalho em equipe", "comprometimento", "organizado", "metódico",
        "objetivo", "orientação a detalhes", "perfeccionista",
    ]),
]


def _kw_match(haystack, kw):
    """Match por palavra (ou token delimitado) para evitar colisões como 'ci' em 'perfeccionista'."""
    pattern = r"(?:^|[^a-záéíóúãõâêô])" + re.escape(kw) + r"(?:$|[^a-záéíóúãõâêô])"
    return re.search(pattern, haystack, flags=re.IGNORECASE) is not None


def _display_skill(name):
    """Para ATS, mantém a lista de tecnologias dentro dos colchetes quando existir."""
    if not name:
        return ""
    # Normaliza espaços/quebras de linha para permitir match de nomes multi-linha no DB.
    normalized = re.sub(r"\s+", " ", str(name)).strip()
    m = re.match(r"^(.+?)\s*\[\s*(.+?)\s*\]\s*$", normalized)
    if m:
        label = m.group(1).strip(" -—|·")
        techs = re.sub(r"\s+", " ", m.group(2)).strip()
        return f"{label} ({techs})" if label else techs
    return normalized.strip(" -—|·")


def categorize_skills(skills, categories, lang):
    grouped = {label: [] for label, _ in categories}
    used = set()
    for label, keywords in categories:
        for s in skills:
            if s.get("_id") in used:
                continue
            name_pt = (s.get("name") or "").strip()
            name_en = (s.get("name_en") or "").strip()
            haystack = (name_pt + " " + name_en).lower()
            if any(_kw_match(haystack, kw) for kw in keywords):
                raw = name_en if (lang == "en" and name_en) else name_pt
                display = _display_skill(raw)
                if display:
                    grouped[label].append(display)
                used.add(s.get("_id"))
    return [(label, items) for label, items in grouped.items() if items]


def strip_html(s):
    if not s:
        return ""
    text = re.sub(r"<[^>]+>", " ", str(s))
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def safe(s):
    """Escape caracteres que ReportLab interpreta como mini-HTML (<, >, &)."""
    if s is None:
        return ""
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


# ----------------------- Rendering ------------------------------------


def build_styles():
    base = getSampleStyleSheet()
    return {
        "name": ParagraphStyle(
            "Name", parent=base["Title"], fontName="Helvetica-Bold",
            fontSize=22, leading=26, textColor=PRIMARY, spaceAfter=2,
        ),
        "role": ParagraphStyle(
            "Role", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=11, leading=14, textColor=ACCENT, spaceAfter=2,
        ),
        "contact": ParagraphStyle(
            "Contact", parent=base["Normal"], fontName="Helvetica",
            fontSize=9.2, leading=12, textColor=MUTED, spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "H2", parent=base["Heading2"], fontName="Helvetica-Bold",
            fontSize=12, leading=14, textColor=PRIMARY, spaceBefore=10,
            spaceAfter=4, keepWithNext=1,
        ),
        "body": ParagraphStyle(
            "Body", parent=base["Normal"], fontName="Helvetica",
            fontSize=9.5, leading=13, textColor=HexColor("#222222"),
            alignment=TA_JUSTIFY, spaceAfter=3,
        ),
        "job_title": ParagraphStyle(
            "JobTitle", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=10.5, leading=13, textColor=PRIMARY, spaceAfter=1,
            keepWithNext=1,
        ),
        "job_meta": ParagraphStyle(
            "JobMeta", parent=base["Normal"], fontName="Helvetica-Oblique",
            fontSize=9, leading=12, textColor=MUTED, spaceAfter=3,
            keepWithNext=1,
        ),
        "stack_cat": ParagraphStyle(
            "StackCat", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=9.5, leading=12, textColor=PRIMARY, spaceAfter=1,
        ),
        "stack_items": ParagraphStyle(
            "StackItems", parent=base["Normal"], fontName="Helvetica",
            fontSize=9.2, leading=12, textColor=HexColor("#222222"),
            spaceAfter=4,
        ),
        "bullet": ParagraphStyle(
            "Bullet", parent=base["Normal"], fontName="Helvetica",
            fontSize=9.3, leading=12.5, textColor=HexColor("#222222"),
            alignment=TA_JUSTIFY, spaceAfter=2,
        ),
    }


def hr():
    return HRFlowable(
        width="100%", thickness=0.6, color=ACCENT, spaceBefore=2, spaceAfter=2
    )


# ----------------------- Content blocks -------------------------------


def build_summary(lang, settings):
    if lang == "pt":
        return (
            f"Engenheiro Sênior de Qualidade (QA) com {settings.get('experience', '+15 anos')} "
            "de atuação em ecossistemas financeiros, health-tech e varejo digital. "
            "Liderança técnica na Foxbit Exchange garantindo a confiabilidade de plataformas Web, "
            "Mobile e APIs de missão crítica por meio de arquiteturas de automação "
            "escaláveis (Cypress, Playwright, Maestro, Appium) e pipelines de CI/CD em Kubernetes. "
            "Founder da ISSQA e CTO da WasteZero, une estratégia de testes, liderança de squads "
            "ágeis e visão de produto para reduzir riscos de negócio e acelerar entregas. "
            "Experiência consolidada em testes de performance (k6, JMeter), API REST, BDD "
            "(Cucumber), observabilidade e práticas de LLM-Assisted Testing."
        )
    return (
        f"Senior QA Automation Engineer with {settings.get('experience_en', '15+ years')} "
        "of experience across fintech, health-tech and digital retail ecosystems. "
        "Tech lead at Foxbit Exchange safeguarding Web, Mobile and mission-critical API "
        "platforms through scalable automation architectures (Cypress, Playwright, Maestro, "
        "Appium) and Kubernetes-based CI/CD pipelines. Founder of ISSQA and CTO at WasteZero, "
        "combining test strategy, agile squad leadership and product vision to reduce business "
        "risk and accelerate delivery. Proven expertise in performance testing (k6, JMeter), "
        "REST API testing, BDD (Cucumber), observability and LLM-Assisted Testing practices."
    )


def build_stack(lang, skills, styles):
    """Stack agrupado em uma lista simples (ATS-friendly)."""
    categories = STACK_CATEGORIES_PT if lang == "pt" else STACK_CATEGORIES_EN
    grouped = categorize_skills(skills, categories, lang)

    flows = []
    for label, items in grouped:
        safe_items = ", ".join(safe(i) for i in items)
        flows.append(Paragraph(f"<b>{safe(label)}:</b> {safe_items}.", styles["stack_items"]))
    return flows


CONTRACT_EN = {
    "Contrato": "Contract",
    "Estágio": "Internship",
    "Cooperado": "Cooperative",
    # CLT, PJ, Freelancer ficam como estão (usados internacionalmente ou específicos BR)
}


def _role_for_lang(exp, lang):
    role = (exp.get("role_en") if lang == "en" else None) or exp.get("role") or ""
    contract = exp.get("contract_type") or ""
    if lang == "en" and contract in CONTRACT_EN:
        contract = CONTRACT_EN[contract]
    return f"{role} — {contract}" if contract else role


def _company_for_lang(exp, lang):
    return (exp.get("company_en") if lang == "en" else None) or exp.get("company") or ""


def _desc_for_lang(exp, lang):
    desc = (exp.get("description_en") if lang == "en" else None) or exp.get("description") or ""
    return strip_html(desc)


def build_experience(lang, works, styles):
    flows = []
    heading = "Experiência Profissional" if lang == "pt" else "Professional Experience"
    flows.append(Paragraph(heading, styles["h2"]))
    flows.append(hr())

    for exp in works:
        role = _role_for_lang(exp, lang)
        company = _company_for_lang(exp, lang)
        start = exp.get("start_date", "")
        end = exp.get("end_date") or ("Present" if lang == "en" else "Atual")
        block = [
            Paragraph(f"{safe(role)} — <b>{safe(company)}</b>", styles["job_title"]),
            Paragraph(f"{safe(start)} · {safe(end)}", styles["job_meta"]),
        ]
        desc = _desc_for_lang(exp, lang)
        if desc:
            block.append(Paragraph(safe(desc), styles["bullet"]))
        block.append(Spacer(1, 3))
        flows.append(KeepTogether(block))
    return flows


def build_education(lang, education, styles):
    """Mostra apenas graduação + certificações (pula cursos Udemy para caber em 2 páginas)."""
    flows = []
    heading = "Educação & Certificações" if lang == "pt" else "Education & Certifications"
    flows.append(Paragraph(heading, styles["h2"]))
    flows.append(hr())

    def is_relevant(edu):
        role = (edu.get("role") or "").lower()
        company = (edu.get("company") or "").lower()
        if "diploma-curso" in role or "udemy" in company:
            return False
        return True

    relevant = [e for e in education if is_relevant(e)]
    if not relevant:
        relevant = education[:4]

    items = []
    for edu in relevant:
        role = (edu.get("role_en") if lang == "en" else None) or edu.get("role") or ""
        inst = (edu.get("company_en") if lang == "en" else None) or edu.get("company") or ""
        start = edu.get("start_date", "")
        end = edu.get("end_date") or ""
        period = f"{start} – {end}" if start or end else ""
        line = f"<b>{safe(role)}</b> — {safe(inst)}"
        if period:
            line += f" <font color='#777777'>({safe(period)})</font>"
        items.append(ListItem(Paragraph(line, styles["bullet"]), leftIndent=10))

    flows.append(ListFlowable(items, bulletType="bullet", start="•", leftIndent=10))
    return flows


def build_community(lang, styles):
    flows = []
    heading = "Comunidade & Idiomas" if lang == "pt" else "Community & Languages"
    flows.append(Paragraph(heading, styles["h2"]))
    flows.append(hr())
    if lang == "pt":
        bullets = [
            "Fundador da <b>ISSQA</b> – consultoria de Quality Engineering e mentoria técnica.",
            "Ministra aulas gratuitas de fundamentos de QA para jovens da comunidade.",
            "Líder de grupos de jovens e professor de Escola Bíblica Dominical.",
            "<b>Idiomas:</b> Português (nativo), Inglês (profissional).",
        ]
    else:
        bullets = [
            "Founder of <b>ISSQA</b> – Quality Engineering consultancy and technical mentoring.",
            "Delivers free QA fundamentals classes to youth in the local community.",
            "Youth group leader and Sunday-school teacher.",
            "<b>Languages:</b> Portuguese (native), English (professional).",
        ]
    items = [ListItem(Paragraph(b, styles["bullet"]), leftIndent=10) for b in bullets]
    flows.append(ListFlowable(items, bulletType="bullet", start="•", leftIndent=10))
    return flows


# ----------------------- Document -------------------------------------


def generate_pdf(lang, settings, skills, works, education, output_path):
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=15 * mm, rightMargin=15 * mm,
        topMargin=14 * mm, bottomMargin=14 * mm,
        title=f"Isaias Silva — Resume ({lang.upper()})",
        author="Isaias Silva",
    )
    styles = build_styles()
    flows = []

    # Header
    flows.append(Paragraph(settings["name"], styles["name"]))
    title_text = settings["title_en"] if lang == "en" else settings["title_pt"]
    flows.append(Paragraph(title_text, styles["role"]))

    location = (
        f"{settings['city']} · {settings['state_en'] if lang == 'en' else settings['state']}"
    )
    contact_line = (
        f"{location} &nbsp;|&nbsp; "
        f"<a href='mailto:{settings['email']}'>{settings['email']}</a> &nbsp;|&nbsp; "
        "<a href='https://www.linkedin.com/in/isaiasilva/'>linkedin.com/in/isaiasilva</a> &nbsp;|&nbsp; "
        "<a href='https://github.com/isaiasilva'>github.com/isaiasilva</a>"
    )
    flows.append(Paragraph(contact_line, styles["contact"]))

    # Summary
    heading_summary = "Resumo Executivo" if lang == "pt" else "Executive Summary"
    flows.append(Paragraph(heading_summary, styles["h2"]))
    flows.append(hr())
    flows.append(Paragraph(build_summary(lang, settings), styles["body"]))

    # Stack
    heading_stack = "Stack Técnica" if lang == "pt" else "Technical Stack"
    flows.append(Paragraph(heading_stack, styles["h2"]))
    flows.append(hr())
    flows.extend(build_stack(lang, skills, styles))

    # Experience
    flows.extend(build_experience(lang, works, styles))

    # Education
    flows.extend(build_education(lang, education, styles))

    # Community
    flows.extend(build_community(lang, styles))

    doc.build(flows)
    print(f"[OK] {lang.upper()} -> {output_path} ({os.path.getsize(output_path)} bytes)")


def main():
    settings, skills, works, education = fetch_data()
    os.makedirs(STATIC_DIR, exist_ok=True)
    generate_pdf(
        "pt", settings, skills, works, education,
        os.path.join(STATIC_DIR, "Isaias_Silva_Resume.pdf"),
    )
    generate_pdf(
        "en", settings, skills, works, education,
        os.path.join(STATIC_DIR, "Isaias_Silva_Resume_EN.pdf"),
    )


if __name__ == "__main__":
    main()
