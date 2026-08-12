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
    featured_projects = list(
        db.projects.find({"featured": 1}).sort([("sort_order", 1), ("_id", -1)])
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
        "experience_es": get_setting("emp_xp_es", "+15 años"),
        "title_es": get_setting(
            "site_title_es",
            "QA Lead & Founder | Especialista en Automatización y Estrategia de Calidad",
        ),
        "state_es": get_setting("emp_estado_es", "Bahía, BR"),
    }
    return settings, skills, works, education, featured_projects


# Stack categorization. Usa word-boundary para evitar que "ci" case com "perfecCIonista".
# Keywords já em minúsculas; testadas contra nome PT+EN.
STACK_CATEGORIES_PT = [
    ("IA Aplicada a QA & Agentes", ["ia aplicada", "agentes de ia", "automação de processos com ia", "llm-assisted"]),
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
    ("AI-Assisted QA & Agents", ["ia aplicada", "agentes de ia", "automação de processos com ia", "llm-assisted"]),
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


STACK_CATEGORIES_ES = [
    ("IA Aplicada a QA & Agentes", ["ia aplicada", "agentes de ia", "automação de processos com ia", "llm-assisted"]),
    ("Automatización Web/API", ["automação de testes", "cypress", "selenium", "selenide", "playwright", "postman", "insomnia"]),
    ("Automatización Mobile", ["appium", "maestro"]),
    ("Rendimiento & Calidad", ["performance", "gestão e técnicas", "gherkin", "bdd"]),
    ("Lenguajes & Frameworks", ["linguagens de programação", "python", "typescript", "nestjs"]),
    ("DevOps & CI/CD", ["pipelines", "jenkins", "github actions", "ci/cd", "git", "deploy", "docker", "kubernetes"]),
    ("Bases de Datos", ["banco de dados", "mysql", "mongo", "postgres", "redis"]),
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
            name_es = (s.get("name_es") or "").strip()
            haystack = (name_pt + " " + name_en).lower()
            if any(_kw_match(haystack, kw) for kw in keywords):
                if lang == "en" and name_en:
                    raw = name_en
                elif lang == "es" and name_es:
                    raw = name_es
                else:
                    raw = name_pt
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
            "escaláveis (Cypress, Playwright, Maestro, Appium) e pipelines de CI/CD. "
            "Pioneiro em LLM-Assisted Testing e desenvolvimento com agentes de IA (Claude Code, "
            "MCP), aplicados de ponta a ponta em produtos reais. Founder da ISSQA e das startups "
            "WasteZero (CTO, Top 5 ExpoFavela Bahia 2025), Juntix (fintech de crédito colaborativo) "
            "e CRUZZO (marketplace P2P com pagamento em custódia), unindo estratégia de testes, "
            "liderança de squads ágeis e visão de produto para reduzir riscos de negócio e acelerar "
            "entregas. Experiência consolidada em testes de performance (k6, JMeter), API REST, "
            "BDD (Cucumber) e observabilidade."
        )
    if lang == "es":
        return (
            f"Ingeniero Sénior de Calidad (QA) con {settings.get('experience_es', '+15 años')} "
            "de actuación en ecosistemas financieros, health-tech y retail digital. "
            "Liderazgo técnico en Foxbit Exchange garantizando la confiabilidad de plataformas "
            "Web, Mobile y APIs de misión crítica mediante arquitecturas de automatización "
            "escalables (Cypress, Playwright, Maestro, Appium) y pipelines de CI/CD. "
            "Pionero en LLM-Assisted Testing y desarrollo con agentes de IA (Claude Code, MCP), "
            "aplicados de punta a punta en productos reales. Founder de ISSQA y de las startups "
            "WasteZero (CTO, Top 5 ExpoFavela Bahía 2025), Juntix (fintech de crédito colaborativo) "
            "y CRUZZO (marketplace P2P con pago en custodia), uniendo estrategia de pruebas, "
            "liderazgo de squads ágiles y visión de producto para reducir riesgos de negocio y "
            "acelerar entregas. Experiencia consolidada en pruebas de rendimiento (k6, JMeter), "
            "APIs REST, BDD (Cucumber) y observabilidad."
        )
    return (
        f"Senior QA Automation Engineer with {settings.get('experience_en', '15+ years')} "
        "of experience across fintech, health-tech and digital retail ecosystems. "
        "Tech lead at Foxbit Exchange safeguarding Web, Mobile and mission-critical API "
        "platforms through scalable automation architectures (Cypress, Playwright, Maestro, "
        "Appium) and CI/CD pipelines. Early adopter of LLM-Assisted Testing and AI-agent "
        "development (Claude Code, MCP), applied end-to-end in production products. Founder of "
        "ISSQA and of the startups WasteZero (CTO, Top 5 at ExpoFavela Bahia 2025), Juntix "
        "(collaborative-credit fintech) and CRUZZO (P2P marketplace with escrow payments), "
        "combining test strategy, agile squad leadership and product vision to reduce business "
        "risk and accelerate delivery. Proven expertise in performance testing (k6, JMeter), "
        "REST API testing, BDD (Cucumber) and observability."
    )


def build_stack(lang, skills, styles):
    """Stack agrupado em uma lista simples (ATS-friendly)."""
    if lang == "pt":
        categories = STACK_CATEGORIES_PT
    elif lang == "es":
        categories = STACK_CATEGORIES_ES
    else:
        categories = STACK_CATEGORIES_EN
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

CONTRACT_ES = {
    "Contrato": "Contrato",
    "Estágio": "Pasantía",
    "Cooperado": "Cooperativa",
}


def _field_for_lang(doc, field, lang):
    """Seleciona doc[field_<lang>] com fallback para o PT."""
    if lang in ("en", "es"):
        localized = doc.get(f"{field}_{lang}")
        if localized and str(localized).strip():
            return localized
    return doc.get(field) or ""


def _role_for_lang(exp, lang):
    role = _field_for_lang(exp, "role", lang)
    contract = exp.get("contract_type") or ""
    if lang == "en" and contract in CONTRACT_EN:
        contract = CONTRACT_EN[contract]
    elif lang == "es" and contract in CONTRACT_ES:
        contract = CONTRACT_ES[contract]
    return f"{role} — {contract}" if contract else role


def _company_for_lang(exp, lang):
    return _field_for_lang(exp, "company", lang)


def _desc_for_lang(exp, lang):
    return strip_html(_field_for_lang(exp, "description", lang))


def build_experience(lang, works, styles):
    flows = []
    headings = {
        "pt": "Experiência Profissional",
        "en": "Professional Experience",
        "es": "Experiencia Profesional",
    }
    heading = headings[lang]
    flows.append(Paragraph(heading, styles["h2"]))
    flows.append(hr())

    for exp in works:
        role = _role_for_lang(exp, lang)
        company = _company_for_lang(exp, lang)
        start = exp.get("start_date", "")
        current = {"pt": "Atual", "en": "Present", "es": "Actual"}
        end = exp.get("end_date") or current[lang]
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


def build_projects(lang, projects, styles):
    """Projetos em destaque (featured=1): WasteZero, Juntix, CRUZZO."""
    if not projects:
        return []
    flows = []
    headings = {
        "pt": "Projetos em Destaque (Founder)",
        "en": "Key Projects (Founder)",
        "es": "Proyectos Destacados (Founder)",
    }
    flows.append(Paragraph(headings[lang], styles["h2"]))
    flows.append(hr())

    tech_label = {"pt": "Stack", "en": "Stack", "es": "Stack"}[lang]
    for project in projects:
        title = strip_html(_field_for_lang(project, "title", lang))
        raw_desc = str(_field_for_lang(project, "description", lang) or "")
        tech = strip_html(_field_for_lang(project, "tech", lang))
        # No currículo entra só o primeiro parágrafo da descrição (split antes
        # do strip_html, que colapsa as quebras de linha)
        normalized = raw_desc.replace("\r\n", "\n")
        first_para = strip_html(normalized.split("\n\n")[0]) if normalized.strip() else ""
        block = [Paragraph(f"<b>{safe(title)}</b>", styles["job_title"])]
        if first_para:
            block.append(Paragraph(safe(first_para), styles["bullet"]))
        if tech:
            block.append(
                Paragraph(
                    f"<b>{tech_label}:</b> {safe(tech)}",
                    styles["job_meta"],
                )
            )
        block.append(Spacer(1, 3))
        flows.append(KeepTogether(block))
    return flows


def build_education(lang, education, styles):
    """Mostra apenas graduação + certificações (pula cursos Udemy para caber em 2 páginas)."""
    flows = []
    headings = {
        "pt": "Educação & Certificações",
        "en": "Education & Certifications",
        "es": "Educación & Certificaciones",
    }
    heading = headings[lang]
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
        role = strip_html(_field_for_lang(edu, "role", lang))
        inst = strip_html(_field_for_lang(edu, "company", lang))
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
    headings = {
        "pt": "Comunidade & Idiomas",
        "en": "Community & Languages",
        "es": "Comunidad & Idiomas",
    }
    heading = headings[lang]
    flows.append(Paragraph(heading, styles["h2"]))
    flows.append(hr())
    if lang == "pt":
        bullets = [
            "Fundador da <b>ISSQA</b> – consultoria de Quality Engineering e mentoria técnica.",
            "Ministra aulas gratuitas de fundamentos de QA para jovens da comunidade.",
            "Líder de grupos de jovens e professor de Escola Bíblica Dominical.",
            "<b>Idiomas:</b> Português (nativo), Inglês (profissional).",
        ]
    elif lang == "es":
        bullets = [
            "Fundador de <b>ISSQA</b> – consultora de Quality Engineering y mentoría técnica.",
            "Imparte clases gratuitas de fundamentos de QA para jóvenes de la comunidad.",
            "Líder de grupos de jóvenes y maestro de Escuela Bíblica Dominical.",
            "<b>Idiomas:</b> Portugués (nativo), Inglés (profesional).",
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


def generate_pdf(lang, settings, skills, works, education, projects, output_path):
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
    if lang == "en":
        title_text = settings["title_en"]
    elif lang == "es":
        title_text = settings["title_es"]
    else:
        title_text = settings["title_pt"]
    flows.append(Paragraph(title_text, styles["role"]))

    if lang == "en":
        state = settings["state_en"]
    elif lang == "es":
        state = settings["state_es"]
    else:
        state = settings["state"]
    location = f"{settings['city']} · {state}"
    contact_line = (
        f"{location} &nbsp;|&nbsp; "
        f"<a href='mailto:{settings['email']}'>{settings['email']}</a> &nbsp;|&nbsp; "
        "<a href='https://www.linkedin.com/in/isaiasilva/'>linkedin.com/in/isaiasilva</a> &nbsp;|&nbsp; "
        "<a href='https://github.com/isaiasilva'>github.com/isaiasilva</a>"
    )
    flows.append(Paragraph(contact_line, styles["contact"]))

    # Summary
    heading_summary = {
        "pt": "Resumo Executivo",
        "en": "Executive Summary",
        "es": "Resumen Ejecutivo",
    }[lang]
    flows.append(Paragraph(heading_summary, styles["h2"]))
    flows.append(hr())
    flows.append(Paragraph(build_summary(lang, settings), styles["body"]))

    # Stack
    heading_stack = {
        "pt": "Stack Técnica",
        "en": "Technical Stack",
        "es": "Stack Técnico",
    }[lang]
    flows.append(Paragraph(heading_stack, styles["h2"]))
    flows.append(hr())
    flows.extend(build_stack(lang, skills, styles))

    # Experience
    flows.extend(build_experience(lang, works, styles))

    # Projetos em destaque (founder)
    flows.extend(build_projects(lang, projects, styles))

    # Education
    flows.extend(build_education(lang, education, styles))

    # Community
    flows.extend(build_community(lang, styles))

    doc.build(flows)
    print(f"[OK] {lang.upper()} -> {output_path} ({os.path.getsize(output_path)} bytes)")


def main():
    settings, skills, works, education, featured_projects = fetch_data()
    os.makedirs(STATIC_DIR, exist_ok=True)
    generate_pdf(
        "pt", settings, skills, works, education, featured_projects,
        os.path.join(STATIC_DIR, "Isaias_Silva_Resume.pdf"),
    )
    generate_pdf(
        "en", settings, skills, works, education, featured_projects,
        os.path.join(STATIC_DIR, "Isaias_Silva_Resume_EN.pdf"),
    )
    generate_pdf(
        "es", settings, skills, works, education, featured_projects,
        os.path.join(STATIC_DIR, "Isaias_Silva_Resume_ES.pdf"),
    )


if __name__ == "__main__":
    main()
