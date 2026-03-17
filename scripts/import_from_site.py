import argparse
import os
import re
import sys
import urllib.request
from html import unescape

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from db import get_db, init_db


def strip_tags(text):
    return re.sub(r"<[^>]+>", "", text).strip()


def fetch_html(url):
    with urllib.request.urlopen(url) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def extract_section(html, start_marker, end_marker):
    start = html.find(start_marker)
    end = html.find(end_marker, start)
    if start == -1 or end == -1:
        return ""
    return html[start:end]


def parse_skills(section):
    names = re.findall(
        r'<p[^>]*class=[\'"][^\'"]*mt-3[^\'"]*[\'"][^>]*>(.*?)</p>',
        section,
        re.S,
    )
    levels = re.findall(r'aria-valuenow="(\d+)"', section)
    if not levels:
        levels = re.findall(r'aria-valuenow="([0-9]+)"', section)
    skills = []
    for name, level in zip(names, levels):
        skills.append(
            {
                "name": strip_tags(unescape(name)),
                "level": int(level),
                "icon": "",
            }
        )
    return skills


def parse_cv_items(column_html):
    item_pattern = re.compile(
        r"<div class=[\"']cv-item[\"'][^>]*>.*?<h5[^>]*>(.*?)</h5>.*?<h6>(.*?)</h6>.*?<p><em[^>]*>(.*?)</em></p>(?:.*?<p[^>]*>(.*?)</p>)?",
        re.S,
    )
    items = []
    for role, period, company, description in item_pattern.findall(column_html):
        items.append(
            {
                "role": strip_tags(unescape(role)),
                "period": strip_tags(unescape(period)),
                "company": strip_tags(unescape(company)),
                "description": strip_tags(unescape(description)) if description else "",
            }
        )
    return items


def parse_curriculo(section):
    parts = section.split('<div class="col-md-6">')
    if len(parts) < 3:
        return [], []
    formacao_html = parts[1]
    profissional_html = parts[2]
    formation = parse_cv_items(formacao_html)
    professional = parse_cv_items(profissional_html)
    return formation, professional


def parse_portfolio(section):
    cards = []
    card_pattern = re.compile(
        r'<div class="card[^"]*">.*?<div class="card-body">.*?</div>\s*</div>',
        re.S,
    )
    for card_html in card_pattern.findall(section):
        img_match = re.search(r'<img[^>]*src="([^"]+)"', card_html)
        title_match = re.search(r'<h5 class="card-title"[^>]*>(.*?)</h5>', card_html, re.S)
        desc_match = re.search(r'<p class="card-text"[^>]*>(.*?)</p>', card_html, re.S)
        links = re.findall(r'<a href="([^"]+)"', card_html)

        image_url = img_match.group(1).strip() if img_match else ""
        if image_url.startswith("../static/"):
            image_url = image_url.replace("../static", "/static")

        title = strip_tags(unescape(title_match.group(1))) if title_match else ""
        desc = strip_tags(unescape(desc_match.group(1))) if desc_match else ""

        project_url = links[0] if len(links) > 0 else ""
        repo_url = links[1] if len(links) > 1 else ""

        cards.append(
            {
                "title": title,
                "description": desc,
                "tech": "",
                "project_url": project_url,
                "repo_url": repo_url,
                "image_url": image_url,
                "featured": 0,
            }
        )
    return cards


def main():
    parser = argparse.ArgumentParser(description="Importa dados do site em produção para o MongoDB.")
    parser.add_argument("--url", default="https://www.issqa.com.br/", help="URL do site")
    parser.add_argument("--reset", action="store_true", help="Limpa skills/experiences/projects antes de importar")
    args = parser.parse_args()

    html = fetch_html(args.url)

    skills_section = extract_section(
        html,
        '<section class="mt-5 section-bg" id="habilidades">',
        "<!-- Seção Curriculo -->",
    )
    curriculo_section = extract_section(
        html,
        "<!-- Seção Curriculo -->",
        "<!-- Seção Portfólio",
    )
    portfolio_section = extract_section(
        html,
        "<!-- Seção Portfólio",
        "<!-- Seção Contato -->",
    )

    skills = parse_skills(skills_section)
    formation, professional = parse_curriculo(curriculo_section)
    projects = parse_portfolio(portfolio_section)

    init_db()
    db = get_db()

    if args.reset:
        db.skills.delete_many({})
        db.experiences.delete_many({})
        db.projects.delete_many({})

    # Skills with sort_order (top items higher)
    total = len(skills)
    for idx, skill in enumerate(skills):
        skill["sort_order"] = total - idx
    if skills:
        db.skills.insert_many(skills)

    # Curriculo
    total_edu = len(formation)
    for idx, item in enumerate(formation):
        db.experiences.insert_one(
            {
                "kind": "education",
                "company": item["company"],
                "role": item["role"],
                "start_date": item["period"],
                "end_date": "",
                "description": item["description"],
                "sort_order": total_edu - idx,
            }
        )

    total_work = len(professional)
    for idx, item in enumerate(professional):
        db.experiences.insert_one(
            {
                "kind": "work",
                "company": item["company"],
                "role": item["role"],
                "start_date": item["period"],
                "end_date": "",
                "description": item["description"],
                "sort_order": total_work - idx,
            }
        )

    # Projects
    if projects:
        db.projects.insert_many(projects)

    print(f"Import concluído: {len(skills)} skills, {len(formation)} formação, {len(professional)} experiências, {len(projects)} projetos")


if __name__ == "__main__":
    main()
