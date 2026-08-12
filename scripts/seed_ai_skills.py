# -*- coding: utf-8 -*-
"""Adiciona as habilidades modernas de QA + IA no topo da seção Habilidades.

Uso:
    venv/bin/python scripts/seed_ai_skills.py

Idempotente — não duplica se a habilidade já existir (match por nome PT).
As habilidades existentes são deslocadas (+N no sort_order) para as novas
entrarem primeiro, já que são os diferenciais de mercado em 2026.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import get_db

NEW_SKILLS = [
    {
        "name": "IA Aplicada a Testes [ LLM-Assisted Testing, Geração de Casos, MCP ]",
        "name_en": "AI-Assisted Testing [ LLM Test Generation, MCP ]",
        "name_es": "IA Aplicada a Pruebas [ Testing asistido por LLM, Generación de Casos, MCP ]",
        "level": 90,
    },
    {
        "name": "Agentes de IA para Dev & QA [ Claude Code, GitHub Copilot, Cursor ]",
        "name_en": "AI Agents for Dev & QA [ Claude Code, GitHub Copilot, Cursor ]",
        "name_es": "Agentes de IA para Dev & QA [ Claude Code, GitHub Copilot, Cursor ]",
        "level": 88,
    },
    {
        "name": "Automação de Processos com IA [ n8n, Evolution API, Chatbots WhatsApp ]",
        "name_en": "AI-Powered Process Automation [ n8n, Evolution API, WhatsApp Chatbots ]",
        "name_es": "Automatización de Procesos con IA [ n8n, Evolution API, Chatbots de WhatsApp ]",
        "level": 85,
    },
    {
        "name": "Playwright",
        "name_en": "Playwright",
        "name_es": "Playwright",
        "level": 85,
    },
    {
        "name": "Docker & Containers [ Docker, Easypanel, VPS ]",
        "name_en": "Docker & Containers [ Docker, Easypanel, VPS ]",
        "name_es": "Docker y Contenedores [ Docker, Easypanel, VPS ]",
        "level": 80,
    },
]


def main():
    db = get_db()

    to_insert = []
    for skill in NEW_SKILLS:
        if db.skills.find_one({"name": skill["name"]}):
            print(f"  = já existe: {skill['name'][:50]}")
            continue
        to_insert.append(skill)

    if not to_insert:
        print("Nada a inserir.")
        return

    # Abre espaço no início: desloca todas as existentes
    shift = len(to_insert)
    db.skills.update_many({}, {"$inc": {"sort_order": shift}})

    for idx, skill in enumerate(to_insert, start=1):
        skill["icon"] = ""
        skill["sort_order"] = idx
        db.skills.insert_one(skill)
        print(f"  + [{idx}] {skill['level']}% {skill['name'][:60]}")

    print(f"{len(to_insert)} habilidades inseridas no topo.")


if __name__ == "__main__":
    main()
