import argparse
from datetime import datetime
import os

from werkzeug.security import generate_password_hash

from db import get_db, init_db, seed_admin, seed_about, seed_settings


def reset_db(db):
    collections = [
        "users",
        "settings",
        "about",
        "skills",
        "experiences",
        "projects",
        "messages",
    ]
    for name in collections:
        db[name].delete_many({})


def seed_samples(db):
    if db.skills.count_documents({}) == 0:
        db.skills.insert_many(
            [
                {"name": "Automação de Testes", "level": 80, "icon": "bi bi-gear"},
                {"name": "Cypress", "level": 80, "icon": "bi bi-lightning"},
                {"name": "Postman/Insomnia", "level": 85, "icon": "bi bi-braces"},
                {"name": "Gestão de Testes", "level": 90, "icon": "bi bi-kanban"},
            ]
        )

    if db.experiences.count_documents({}) == 0:
        db.experiences.insert_many(
            [
                {
                    "kind": "work",
                    "company": "Empresa Exemplo",
                    "role": "QA Lead",
                    "start_date": "2021",
                    "end_date": "Atual",
                    "description": "Liderança de QA e automação de testes.",
                    "sort_order": 2,
                },
                {
                    "kind": "education",
                    "company": "Universidade Exemplo",
                    "role": "Sistemas de Informação",
                    "start_date": "2010",
                    "end_date": "2014",
                    "description": "Formação acadêmica em TI.",
                    "sort_order": 1,
                },
            ]
        )

    if db.projects.count_documents({}) == 0:
        db.projects.insert_many(
            [
                {
                    "title": "Projeto Portfólio",
                    "description": "Site pessoal com admin e conteúdo dinâmico.",
                    "tech": "Flask, MongoDB, Bootstrap",
                    "project_url": "https://issqa.com.br",
                    "repo_url": "",
                    "image_url": "/static/img/bannerPortifolio.png",
                    "featured": 1,
                }
            ]
        )


def main():
    parser = argparse.ArgumentParser(description="Reset e seed do MongoDB local.")
    parser.add_argument("--reset", action="store_true", help="Limpa o banco antes do seed")
    parser.add_argument("--samples", action="store_true", help="Insere dados de exemplo")
    args = parser.parse_args()

    init_db()
    db = get_db()

    if args.reset:
        reset_db(db)

    seed_settings(
        {
            "site_name": "Isaias Silva",
            "site_title": "QA Lead, Automatizador Cypress, Empreendedor",
            "profile_image": "/static/img/perfil.jpg",
            "background_image": "/static/img/bannerPortifolio.png",
            "contact_email": "qa.eng.isaiasilva@gmail.com",
            "whatsapp": "https://wa.me/5571996838735",
        }
    )
    seed_about(
        "Acredito que a educação pode mudar a vida das pessoas e sou prova disso. "
        "Sou formado em Sistemas de Informação e tenho mais de 8 anos de experiência em testes de software."
    )

    admin_user = os.getenv("ADMIN_USER", "isaias")
    admin_pass = os.getenv("ADMIN_PASS", "Is@i@s1989")
    seed_admin(admin_user, generate_password_hash(admin_pass))

    admin_email = os.getenv("ADMIN_USER_EMAIL", "qa.eng.isaiasilva@gmail.com")
    admin_email_pass = os.getenv("ADMIN_EMAIL_PASS", admin_pass)
    seed_admin(admin_email, generate_password_hash(admin_email_pass))

    if args.samples:
        seed_samples(db)

    print(f"Seed concluído em {datetime.now().isoformat()} (reset={args.reset}, samples={args.samples})")


if __name__ == "__main__":
    main()
