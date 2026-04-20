"""Seed profissional do conteúdo em Inglês para experiências, formação e projetos.

Uso:
    venv/bin/python scripts/seed_en_translations.py

Idempotente — só atualiza campos vazios (`*_en`), preservando qualquer tradução
já preenchida manualmente pelo painel admin.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import get_db


# Chave de casamento: trecho único do campo "company" no banco (case-insensitive).
WORK_EXPERIENCES = [
    {
        "match": "foxbit",
        "company_en": "Foxbit Exchange",
        "role_en": "Senior QA Automation Engineer (Web & Mobile)",
        "description_en": (
            "Senior QA Automation Engineer with a strong track record in the digital-asset market at Foxbit, "
            "specialising in quality assurance for complex financial ecosystems (Web, Mobile, APIs). "
            "Drive mobile automation with Maestro Studio and web automation with Cypress and Playwright, "
            "delivering full end-to-end coverage. Design advanced test scenarios and lead agile ceremonies, "
            "using Jira for defect management and risk control. Combine deep programming expertise and test "
            "architecture knowledge to raise the reliability of financial products, with focus on performance, "
            "release stability and cross-functional collaboration."
        ),
    },
    {
        "match": "iss sofware",  # typo intencional: nome original no banco
        "company_en": "ISS Software Quality Solutions",
        "role_en": "Founding Partner & Tech Lead",
        "description_en": (
            "As tech lead and co-founder of ISS Software Quality Solutions, I design and deliver digital products "
            "where Software Quality is the core development pillar. Built complex platforms such as WasteZero "
            "(Circular Economy) and Juntix (Credit Fintech), applying a rigorous testing framework from day one "
            "of the architecture. Beyond developing robust ecosystems for IBBI and other institutions, I provide "
            "specialised QA consulting — establishing automation strategies, performance testing and release "
            "stability. Every deliverable from ISS, whether in-house product or external consulting, meets the "
            "highest standards of reliability, security and technical excellence through a fully test-driven "
            "software lifecycle."
        ),
    },
    {
        "match": "wastezero",
        "company_en": "WasteZero",
        "role_en": "Co-Founder & CTO",
        "description_en": (
            "As Co-Founder and CTO of WasteZero, I led the technology strategy and the end-to-end development of "
            "the platform — from infrastructure design to scale launch. Hands-on delivery of a robust ecosystem "
            "including a scalable API and Flutter interfaces for both corporate and consumer environments, "
            "owning the full software lifecycle including CI/CD and production releases. Beyond technical "
            "leadership and team management, I represented the startup at strategic innovation events and "
            "investor pitches, positioning WasteZero among the Top 5 startups of ExpoFavela Bahia 2025 and "
            "representing the state at the national edition in São Paulo. Also featured in events such as NEON "
            "2025 (Arena Web Summit) and BTX25, building partnerships and defending the business model before "
            "investor panels."
        ),
    },
    {
        "match": "casas bahia",
        "company_en": "Grupo Casas Bahia",
        "role_en": "Senior QA Engineer",
        "description_en": (
            "Strategic role as Senior QA Engineer ensuring quality across high-scale critical ecosystems, focused "
            "on Web, Mobile and API microservices architectures. Owned the full QA cycle, from test plans and "
            "acceptance criteria to implementation and maintenance of robust automation frameworks, accelerating "
            "the delivery pipeline and release reliability. Specialist in software sustaining engineering, acting "
            "directly on root-cause analysis and incident mitigation in production, embedding continuous testing "
            "into the agile squads culture to safeguard the shopping experience and functional stability of "
            "leading retail platforms."
        ),
    },
    {
        "match": "sinergia",
        "company_en": "Sinergia Studios",
        "role_en": "Senior QA Engineer",
        "description_en": (
            "Responsible for establishing the Quality Assurance function at the startup, structuring from scratch "
            "every process and standard. Led the testing strategy during the full rebuild of GoGame 2.0 and the "
            "strategic launch of GoGame 3.0, as the main owner of software-lifecycle integrity. Implemented "
            "mobile automation with Robot Framework, Appium and TestProject, combined with rigorous manual "
            "testing and defect management via Jira — delivering a stable, high-performance product to market."
        ),
    },
    {
        "match": "fagron",
        "company_en": "FagronTech Brasil",
        "role_en": "Senior API Test Consultant",
        "description_en": (
            "As Senior Consultant at FagronTech — an ERP specialised in compounding pharmacies — led the quality "
            "strategy in a highly regulated, data-intensive environment. Owned API validation with Postman, "
            "Newman and Swagger, and implemented a performance-testing culture using k6. Acted directly on "
            "system sustainability through message-broker monitoring (RabbitMQ) and management of CI/CD pipelines "
            "across staging and production, ensuring safe deployments and integrity of critical ecosystem "
            "integrations."
        ),
    },
    {
        "match": "deal technologies",
        "company_en": "Deal Technologies",
        "role_en": "Senior Test Consultant",
        "description_en": (
            "Consulting role on strategic digital-transformation projects for the loyalty and marketplace sectors "
            "(Compra Agora and LTM Fidelidade). Focused on microservices architectures, led quality assurance "
            "through rigorous REST API testing with a modern stack (Cypress, Postman, Newman). Owned the full "
            "testing lifecycle and continuous integration inside the Azure DevOps ecosystem, enabling agile "
            "delivery and the stability of high-throughput transactional platforms."
        ),
    },
    {
        "match": "auto avaliar",
        "company_en": "Auto Avaliar",
        "role_en": "Mid-Level QA Engineer",
        "description_en": (
            "Acted on the strategic structuring of the platform's quality ecosystem, co-architecting a robust "
            "web automation framework. Developed automated test suites with Selenium and Selenide, integrating "
            "them into Jenkins Continuous Integration pipelines with end-to-end custom reporting. On the mobile "
            "side, led automation of the vehicle-appraisal app using Appium and Cucumber, applying BDD practices "
            "to guarantee the reliability of inspection, buying and selling flows."
        ),
    },
    {
        "match": "capgemini",
        "company_en": "Capgemini Brasil",
        "role_en": "Mid-Level QA Engineer",
        "description_en": (
            "Worked on a strategic project for the Banco Bradesco mobile app, focused on quality of high-visibility "
            "components. Used the bank's proprietary framework for mobile automation (Appium + Java) and API "
            "testing. Owned complex scenario mapping through mind maps and managed the test lifecycle in ALM "
            "Octane and Jira. Operated a robust development environment using Bitbucket, Bamboo (CI) and Mobile "
            "Center for testing on real devices."
        ),
    },
    {
        "match": "pixeon",
        "company_en": "Pixeon Medical System",
        "role_en": "Mid-Level QA Engineer",
        "description_en": (
            "QA Engineer at Pixeon, a HealthTech reference, ensuring quality of mission-critical systems for "
            "hospitals and clinics. Led end-to-end automation of Web and Desktop applications using Java and "
            "Selenium to validate the exam-results delivery flow in SmartWeb. Mitigated risk through rigorous "
            "manual testing and complex ticket resolution, using Jira for defect management and safeguarding "
            "the reliability of solutions that directly impact patient care."
        ),
    },
    {
        "match": "fraunhofer",
        "company_en": "Fraunhofer Project Center",
        "role_en": "Junior QA Engineer",
        "description_en": (
            "QA Engineer at Fraunhofer Project Center, assigned to the Brazilian National Transplant System (SNT) "
            "project at the Bahia Technology Park. Owned quality assurance of critical organ-donation flows, where "
            "precision and system availability are vital. Working in close collaboration with the engineering "
            "team, managed bug triage and lifecycle via Mantis, basing test strategy on complex requirements and "
            "strict business rules to safeguard the integrity of one of Brazil's most essential healthcare "
            "platforms."
        ),
    },
    {
        "match": "brisa",
        "company_en": "Brisa R&D – LG Mobile",
        "role_en": "Junior QA Engineer",
        "description_en": (
            "Worked at Brisa R&D validating LG mobile devices in pre-launch stage (K, Q, V and Stylo product "
            "lines). Ensured hardware and software quality through rigorous performance, UI and native-app "
            "functional testing. Contribution was decisive to certify device compliance before large-scale "
            "production. Also specialised in FOTA (Firmware Over the Air) update protocols — topic deepened "
            "in the undergraduate thesis — building a strong foundation on device lifecycle and connectivity."
        ),
    },
]


EDUCATION = [
    {
        "match": "unime",
        "company_en": "UNIME – Metropolitan Union of Education and Culture",
        "role_en": "[Academic] Bachelor of Information Systems",
        "description_en": (
            "Thesis: Functional Test Automation in Mobile Device FOTA (Firmware Over the Air) Processes."
        ),
    },
    {
        "match": "istqb",
        "company_en": "ISTQB",
        "role_en": "[Certification] ISTQB Certified Tester – Foundation Level (CTFL)",
        "description_en": "Credential ID: 14-CTFL-03441-BR-BSQTB.",
    },
    {
        "match": "certiprof",
        "company_en": "CertiProf",
        "role_en": "[Certification] Scrum Foundation Professional Certification (SFPC)",
        "description_en": "Scrum Guide aligned – Professional Certification.",
    },
    {
        "match": "devops essentials",
        "company_en": "DevOps Essentials – Credly.com",
        "role_en": "[Certification] DevOps Essentials Professional Certificate",
        "description_en": "Fundamentals of the DevOps culture and engineering practices.",
    },
]


# Cursos (Diploma-Curso) — casamento pelo texto único em `role`
COURSES = [
    {
        "role_match": "Cypress Discovery",
        "company_en": "Instructor: Fernando Papito – QA Ninja",
        "role_en": "[Diploma-Course] Cypress Discovery",
        "description_en": (
            "Completed all classes and activities of the course Cypress Discovery, focused on web "
            "application test automation with Cypress, JavaScript and Node.js."
        ),
    },
    {
        "role_match": "API da Marvel",
        "company_en": "Instructor: Fernando Papito – QA Ninja",
        "role_en": "[Diploma-Course] Testing the Marvel API with Robot Framework",
        "description_en": (
            "Completed all classes and activities of the course Testing the Marvel API with Robot "
            "Framework (4-hour course)."
        ),
    },
    {
        "role_match": "Microservices em Node.js",
        "company_en": "Instructor: Fernando Papito – QA Ninja",
        "role_en": "[Diploma-Course] Microservices Testing in Node.js and MongoDB",
        "description_en": (
            "Completed all classes and activities of the course Microservices Testing in Node.js and "
            "MongoDB (16-hour course)."
        ),
    },
    {
        "role_match": "HTTParty+Rspec+Ruby",
        "company_en": "Instructor: Bruno Batista – Udemy",
        "role_en": "[Diploma-Course] Automated API Testing with HTTParty + RSpec + Ruby",
        "description_en": (
            "Completed all classes and activities of the course Automated API Testing with HTTParty + "
            "RSpec + Ruby (4.5-hour course)."
        ),
    },
    {
        "role_match": "Robot Framework Web+API",
        "company_en": "Instructor: Mayara Fernandes – Udemy",
        "role_en": "[Diploma-Course] Test Automation with Robot Framework Web + API (Basic)",
        "description_en": (
            "Completed all classes and activities of the course Test Automation with Robot Framework "
            "Web + API (7-hour course)."
        ),
    },
    {
        "role_match": "Capybara, Cucumber e Ruby",
        "company_en": "Instructor: Bruno Batista – Udemy",
        "role_en": "[Diploma-Course] Test Automation with Capybara, Cucumber and Ruby",
        "description_en": (
            "Completed all classes and activities of the course Test Automation with Capybara, "
            "Cucumber and Ruby (10-hour course)."
        ),
    },
    {
        "role_match": "BDD com Cucumber e Java",
        "company_en": "Instructor: Francisco Wagner Aquino – Udemy",
        "role_en": "[Diploma-Course] Learn BDD with Cucumber and Java",
        "description_en": (
            "Completed all classes and activities of the course Learn BDD with Cucumber and Java "
            "(10-hour course)."
        ),
    },
    {
        "role_match": "API com Postman",
        "company_en": "Instructor: Erick Valentim – Udemy",
        "role_en": "[Diploma-Course] Automated API Testing with Postman + Testing Project",
        "description_en": (
            "Completed all classes and activities of the course Automated API Testing with Postman + "
            "Testing Project (10-hour course)."
        ),
    },
]


# Conteúdos de settings (strings simples, HTML permitido)
SETTINGS_EN = {
    "emp_niver_en": "September 14, 1989",
    "emp_title_en": "Entrepreneurship",
    "emp_desc1_en": (
        "<p>Over the past 6 years, I have been providing technology services to a range of "
        "organisations, accumulating experiences that shaped my worldview and business mindset. "
        "In the last 2 years, I took an even bigger step: I founded <strong>WasteZero</strong>, "
        "a startup on a mission to fight food waste in retail — a real-world problem with direct "
        "social and environmental impact.</p>"
        "<p>On this journey, I've delivered pitch decks, taken part in mentoring programmes, "
        "travelled to startup and entrepreneurship events, went through acceleration cycles and "
        "investor rounds. Two years that have been a real-world MBA in entrepreneurship — with "
        "everything that comes with it: accelerated learning, resilience, uncertainty and a lot of "
        "growth.</p>"
    ),
    "emp_desc2_en": (
        "<p>All of this in parallel with one of life's greatest responsibilities: raising two young "
        "children — a 4-year-old and a 1-and-a-half-year-old. Challenging? Without a doubt. But "
        "also deeply transformative.</p>"
        "<p>At the same time, I keep building projects, serving clients and performing as a "
        "<strong>Senior QA Engineer</strong> — balancing the technical rigour of software "
        "engineering with the strategic mindset of an entrepreneur.</p>"
        "<p>This combination of experiences has made me a more complete, humane and determined "
        "professional.</p>"
        "<p>Beyond all that, I dedicate part of my time to running a small company and supporting "
        "social causes I carry in my heart. One of them is rescuing and mentoring young people "
        "who have lost their way to drugs and marginalisation, showing them a new path — the path "
        "of Christ.</p>"
        "<p><strong>I believe that transforming lives goes far beyond code and business. It is a "
        "calling.</strong></p>"
    ),
}


ABOUT_EN = (
    "I deeply believe that education has the power to transform lives — and I am living proof of "
    "it. I hold a Bachelor's degree in Information Systems and have over 15 years of experience "
    "in software testing and engineering, having worked on large-scale projects for leading "
    "companies in the market.\n\n"
    "Beyond the technical side, I am an education enthusiast. Teaching is part of who I am. I am "
    "proud to have taught my daughter to read at just 4 years old — one of the most meaningful "
    "achievements of my life — and it constantly reminds me of the impact that good teaching can "
    "have on a person's development.\n\n"
    "I love teaching programming and I believe technological knowledge is one of the most powerful "
    "tools for social transformation today. That is why I dedicate myself to encouraging young "
    "people to take their first steps in technology, showing them that this path is accessible and "
    "can change life trajectories. Education is not only about passing on content — it's about "
    "awakening potential. And that is what drives me."
)


PROJECTS = [
    {
        "match": "wastezero",
        "title_en": "WasteZero",
        "tech_en": "Flutter, Node.js, Vite, REST API, GCP",
        "description_en": (
            "Circular-economy platform connecting retailers to consumers for the sale of surplus items or products "
            "close to expiration. Originally focused on reducing food waste in supermarkets, it has expanded into "
            "a broader sustainability ecosystem. As co-founder and CTO, I led the architecture, scalable API and "
            "Flutter apps for both corporate and consumer experiences, plus the full CI/CD and production cycle."
        ),
    },
    {
        "match": "b",  # Bíblica Israel
        "title_en": "Bíblica Israel – Projeto Amigo",
        "tech_en": "MongoDB, Next.js, Vite, TypeScript",
        "description_en": (
            "Owned the architecture and development of Projeto Amigo, a digital solution focused on membership "
            "onboarding and retention experience. The platform integrates community-management features, "
            "engagement tracking and automated communications to keep members active and connected.",
        ),
    },
    {
        "match": "pixeon",
        "title_en": "Pixeon Health Tech",
        "tech_en": "Java, Selenium, Jira, Jenkins",
        "description_en": (
            "Pixeon is a major player in healthcare management systems for hospitals, clinics and laboratories, "
            "offering end-to-end solutions across the patient journey. As QA Engineer, I led the automation of "
            "critical Web/Desktop flows using Java and Selenium and drove rigorous manual validation in close "
            "partnership with engineering teams."
        ),
    },
    {
        "match": "auto avaliar",
        "title_en": "Auto Avaliar Web & Mobile",
        "tech_en": "Selenium, Selenide, Appium, Cucumber, Jenkins",
        "description_en": (
            "The Auto Avaliar platform automates vehicle appraisal end-to-end — from identification and valuation "
            "to used-car quoting. I helped architect the web automation framework using Selenium/Selenide "
            "integrated into Jenkins CI, and led mobile automation with Appium and Cucumber (BDD)."
        ),
    },
    {
        "match": "compra agora",
        "title_en": "Compra Agora / Viveo / LTM Loyalty",
        "tech_en": "Cypress, Postman, Newman, Azure DevOps",
        "description_en": (
            "More than half of Brazilian consumers prefer to buy from brands with loyalty programmes. Led QA on "
            "loyalty and marketplace projects, running extensive REST API validation (Cypress, Postman, Newman) "
            "and CI/CD pipelines in Azure DevOps to ensure stability across high-transaction platforms."
        ),
    },
    {
        "match": "phusion",
        "title_en": "Phusion – Compounding Pharmacy ERP",
        "tech_en": "Postman, Newman, Swagger, k6, RabbitMQ",
        "description_en": (
            "Phusion is an online ERP that streamlines compounding-pharmacy operations. As QA Lead, I owned REST "
            "API validation with Postman and Newman, implemented performance tests with k6 and monitored message "
            "brokering with RabbitMQ to guarantee delivery quality and system reliability."
        ),
    },
    {
        "match": "gogame",
        "title_en": "GoGame App – Players Connection Hub",
        "tech_en": "Appium, Robot Framework, TestProject, Jira",
        "description_en": (
            "GoGame connects players who share the same games and interests, enabling chat, tips and online "
            "matchmaking across any platform. I performed manual, mobile-automation and REST API testing — "
            "including automating the GoGame API with Robot Framework."
        ),
    },
    {
        "match": "terminal - foxbit",
        "title_en": "Terminal – Foxbit Exchange",
        "tech_en": "Cypress, JavaScript, GitHub Actions",
        "description_en": (
            "Private Foxbit project allowing customers to buy and sell cryptocurrencies. As QA on the team, I owned "
            "end-to-end verification and validation, combining manual and automated testing with Cypress and "
            "JavaScript to guarantee terminal reliability. Pipelines in GitHub Actions enable continuous "
            "monitoring and safe evolution of the application."
        ),
    },
]


def _match_doc(text, needle):
    return needle.lower() in (text or "").lower()


def update_only_empty(collection, query, updates):
    """Atualiza apenas campos que estão vazios — preserva o que o usuário já editou."""
    existing = collection.find_one(query)
    if not existing:
        return False
    patch = {}
    for key, value in updates.items():
        if not existing.get(key):
            patch[key] = value
    if patch:
        collection.update_one({"_id": existing["_id"]}, {"$set": patch})
    return len(patch)


def main():
    db = get_db()

    # Work experiences
    print("\n=== Work experiences ===")
    for entry in WORK_EXPERIENCES:
        query = {"kind": "work", "company": {"$regex": entry["match"], "$options": "i"}}
        updated = update_only_empty(db.experiences, query, {
            "company_en": entry["company_en"],
            "role_en": entry["role_en"],
            "description_en": entry["description_en"],
        })
        print(f"  [{updated or 'skip'}] {entry['company_en']}")

    # Education (relevante)
    print("\n=== Education ===")
    for entry in EDUCATION:
        query = {"kind": "education", "company": {"$regex": entry["match"], "$options": "i"}}
        updated = update_only_empty(db.experiences, query, {
            "company_en": entry["company_en"],
            "role_en": entry["role_en"],
            "description_en": entry["description_en"],
        })
        print(f"  [{updated or 'skip'}] {entry['company_en']}")

    # Courses (Diploma-Curso) — casados pelo `role`
    print("\n=== Courses ===")
    for entry in COURSES:
        query = {"kind": "education", "role": {"$regex": re.escape(entry["role_match"]), "$options": "i"}}
        updated = update_only_empty(db.experiences, query, {
            "company_en": entry["company_en"],
            "role_en": entry["role_en"],
            "description_en": entry["description_en"],
        })
        print(f"  [{updated or 'skip'}] {entry['role_en']}")

    # Projects
    print("\n=== Projects ===")
    for entry in PROJECTS:
        query = {"title": {"$regex": re.escape(entry["match"]), "$options": "i"}}
        desc = entry["description_en"]
        if isinstance(desc, tuple):
            desc = desc[0]
        updated = update_only_empty(db.projects, query, {
            "title_en": entry["title_en"],
            "tech_en": entry["tech_en"],
            "description_en": desc,
        })
        print(f"  [{updated or 'skip'}] {entry['title_en']}")

    # Settings EN (seções Sobre/Empreendedor)
    print("\n=== Settings (About / Entrepreneur EN) ===")
    for key, value in SETTINGS_EN.items():
        existing = db.settings.find_one({"key": key})
        if existing and (existing.get("value") or "").strip():
            print(f"  [skip] {key}")
            continue
        db.settings.update_one(
            {"key": key}, {"$set": {"key": key, "value": value}}, upsert=True
        )
        print(f"  [set] {key}")

    # About EN — atualiza o documento mais recente em `about`
    print("\n=== About EN ===")
    latest = db.about.find_one(sort=[("_id", -1)])
    if latest and not (latest.get("content_en") or "").strip():
        db.about.update_one({"_id": latest["_id"]}, {"$set": {"content_en": ABOUT_EN}})
        print("  [set] about.content_en")
    else:
        print("  [skip] about.content_en")

    print("\n[OK] done.")


if __name__ == "__main__":
    main()
