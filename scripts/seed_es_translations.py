# -*- coding: utf-8 -*-
"""Seed profissional do conteúdo em Espanhol (es-419 neutro) para todo o site.

Uso:
    venv/bin/python scripts/seed_es_translations.py

Idempotente — só preenche campos vazios (`*_es`), preservando qualquer tradução
já preenchida manualmente pelo painel admin. Use --force para sobrescrever.

Também corrige um bug de dados antigo: o projeto GoGame estava com o
título/descrição EN do projeto "Bíblica Israel" (traduções trocadas).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import get_db, get_setting, set_setting

FORCE = "--force" in sys.argv


# ----------------------------- SETTINGS --------------------------------

SETTINGS_ES = {
    "site_title_es": "QA Lead & Founder | Especialista en Automatización y Estrategia de Calidad",
    "emp_title_es": "Emprendedor",
    "emp_niver_es": "14 de septiembre de 1989",
    "emp_idade_es": "36 años",
    "emp_estado_es": "Bahía, BR",
    "emp_hobby_es": "Viajar",
    "emp_trabalho_es": "CEO - ISSQA",
    "emp_xp_es": "+15 años",
    "emp_desc1_es": (
        '<p>En los últimos 6 años he prestado servicios de tecnología a diferentes organizaciones, '
        'acumulando experiencias que moldearon mi visión del mundo y de los negocios. En los últimos '
        '2 años di un paso aún mayor al fundar y liderar iniciativas que resuelven problemas '
        'estructurales de nuestra sociedad.</p><p>Mi trayectoria como founder se consolidó sobre dos '
        'pilares principales:</p><ul><li><strong>WasteZero:</strong> Una startup con la misión de '
        'combatir el desperdicio en el comercio minorista — transformando lo que sería pérdida en '
        'oportunidad de liquidez para las empresas e impacto social directo para el consumidor.</li>'
        '<li><strong>Juntix:</strong> Una fintech que moderniza la economía colaborativa, '
        'transformando la tradicional "caja de ahorro entre amigos" en una plataforma digital segura, '
        'transparente y eficiente, democratizando el acceso al crédito sin la burocracia de los bancos '
        'tradicionales.</li></ul><p>En este camino presenté <strong>pitch decks</strong>, participé en '
        'mentorías de alto nivel, viajé a grandes eventos de innovación y pasé por ciclos de '
        'aceleración y rondas de negocios. Fueron 2 años de una verdadera "universidad del '
        'emprendimiento" en la práctica — viviendo intensamente el aprendizaje acelerado, la '
        'resiliencia frente a la incertidumbre y la construcción de productos que generan valor '
        'real.</p><p>Hoy esa experiencia me permite transitar entre la arquitectura técnica de '
        'software y la visión estratégica de mercado, siempre enfocado en escalar soluciones que unen '
        'tecnología, finanzas y sostenibilidad.</p>'
    ),
    "emp_desc2_es": (
        '<p>Todo esto en paralelo a una de las mayores responsabilidades de la vida: criar a dos '
        'hijos pequeños — una de 4 años y otro de un año y medio. ¿Desafiante? Sin duda. Pero también '
        'profundamente transformador.</p><p>Al mismo tiempo, sigo creando proyectos, atendiendo '
        'clientes y manteniendo mi actuación como <strong>QA Engineer Sénior</strong> — equilibrando '
        'el rigor técnico de la ingeniería de software con el pensamiento estratégico del '
        'emprendedor.</p><p>Esta combinación de experiencias me ha hecho un profesional más completo, '
        'humano y determinado.</p><p>Además de todo esto, dedico parte de mi tiempo a coordinar y '
        'gestionar una pequeña empresa, así como a apoyar causas sociales que llevo en el corazón. '
        'Una de ellas es el trabajo de rescatar y orientar a jóvenes que se perdieron en las drogas y '
        'la marginalidad, mostrándoles un nuevo camino — el camino de Cristo.</p>'
        '<p><strong>Creo que transformar vidas va mucho más allá del código y de los negocios. '
        'Es un llamado</strong>.</p>'
    ),
}

ABOUT_ES = (
    "Creo profundamente que la educación tiene el poder de transformar vidas — y soy prueba viva de "
    "ello. Soy graduado en Sistemas de Información y tengo más de 15 años de experiencia en pruebas e "
    "ingeniería de software, habiendo trabajado en proyectos de gran escala para empresas destacadas "
    "del mercado.\n\n"
    "Pero más allá del lado técnico, soy un entusiasta de la educación. Enseñar es parte de quien "
    "soy. Tengo el orgullo de haber enseñado a leer a mi hija con apenas 4 años — uno de los logros "
    "que más me ha marcado en la vida — y eso me recuerda constantemente el impacto que una buena "
    "enseñanza puede tener en el desarrollo de una persona.\n\n"
    "Me gusta enseñar programación y creo que el conocimiento tecnológico es una de las herramientas "
    "más poderosas de transformación social hoy en día. Por eso, me dedico a incentivar a los "
    "jóvenes a dar sus primeros pasos en el mundo de la tecnología, mostrándoles que este camino es "
    "accesible y puede cambiar trayectorias de vida. La educación no es solo transmisión de "
    "contenido — es despertar potencial. Y eso es lo que me mueve."
)


# --------------------------- EXPERIÊNCIAS ------------------------------
# Chave de casamento: trecho único do campo "company" no banco (case-insensitive).

WORK_ES = [
    {
        "match": "iss software",
        "company_es": "ISS Software Quality Solutions",
        "role_es": "Socio Fundador · Consultoría de QA y Desarrollo",
        "description_es": (
            "ISS Software Quality Solutions es mi consultora propia (empresa registrada) "
            "especializada en Calidad de Software y Desarrollo. Como socio fundador, actúo desde la "
            "concepción de la arquitectura hasta la entrega, aplicando un framework riguroso de "
            "pruebas — automatización, rendimiento y confiabilidad — en cada proyecto. Bajo ISSQA "
            "nacen y crecen productos propios como WasteZero y Juntix, además de la consultoría "
            "especializada en QA e ingeniería de software para instituciones como el IBBI. Sea en "
            "producto propio o consultoría externa, el compromiso es entregar soluciones seguras, "
            "escalables y con excelencia técnica orientada a pruebas."
        ),
    },
    {
        "match": "juntix",
        "company_es": "Juntix",
        "role_es": "Socio Fundador & Líder de Tecnología (Full-Stack, IA e Infra)",
        "description_es": (
            "Plataforma SaaS incubada en ISSQA. Como socio fundador y líder de tecnología, concebí y "
            "ejecuté toda la arquitectura bajo la premisa de máxima eficiencia, con Inteligencia "
            "Artificial en todas las etapas del ciclo de desarrollo. Destacados — Arquitectura e IA: "
            "flujo de desarrollo pionero en el que el 100% de la aplicación (back-end y front-end) "
            "fue construida con apoyo de agentes de IA, acelerando la entrega sin renunciar a la "
            "calidad; Full-Stack: liderazgo técnico de back-end y front-end, entregando un SaaS "
            "escalable, responsivo y centrado en el usuario; Infra & DevOps: gestión de contenedores "
            "y despliegue continuo (EasyPanel + Hostinger) con alta disponibilidad y bajo costo; "
            "QA & Calidad: estándares rigurosos de automatización y pruebas E2E para garantizar la "
            "integridad de las transacciones y la seguridad de los datos; Negocio: roadmap de "
            "producto, integración de pasarelas de pago y cumplimiento regulatorio."
        ),
    },
    {
        "match": "wastezero",
        "company_es": "WasteZero",
        "role_es": "Socio Fundador & CTO",
        "description_es": (
            "Startup de economía circular incubada en ISSQA. Como socio fundador y CTO, lideré la "
            "estrategia tecnológica y el desarrollo de punta a punta de la plataforma — de la "
            "infraestructura al lanzamiento a escala. Trabajé hands-on en un ecosistema robusto, con "
            "API escalable y apps en Flutter para los entornos corporativo y del cliente, "
            "conduciendo todo el ciclo de vida del software con CI/CD y despliegue continuo. Además "
            "del liderazgo técnico y la gestión del equipo, representé a la startup en escenarios de "
            "innovación y rondas de inversión: Top 5 de ExpoFavela Bahía 2025 (representando al "
            "estado en la etapa nacional en São Paulo), NEON 2025 (Arena Web Summit) y BTX25 — "
            "articulando alianzas y defendiendo el modelo de negocio ante paneles de inversores."
        ),
    },
    {
        "match": "foxbit",
        "company_es": "Foxbit Exchange",
        "role_es": "Senior QA Automation Engineer (Web y Mobile)",
        "description_es": (
            "Senior QA Automation Engineer con sólida trayectoria en el mercado de activos digitales "
            "(Foxbit), especializado en el aseguramiento de calidad de ecosistemas financieros "
            "complejos (Web, Mobile y APIs). Especialista en automatización mobile con Maestro "
            "Studio y automatización web con Cypress y Playwright, garantizando cobertura total de "
            "punta a punta. Experiencia estructurando escenarios de prueba complejos y liderando "
            "ceremonias ágiles, utilizando Jira para la gestión de defectos y el control de riesgos. "
            "Fuerte dominio de lógica de programación y arquitectura de pruebas, actuando de forma "
            "estratégica para elevar la confiabilidad de productos financieros, con foco en "
            "rendimiento, estabilidad de lanzamientos e integración entre equipos multifuncionales."
        ),
    },
    {
        "match": "casas bahia",
        "company_es": "Grupo Casas Bahia",
        "role_es": "Analista de Pruebas Sénior",
        "description_es": (
            "Actuación estratégica como Analista de Pruebas Sénior en el aseguramiento de calidad de "
            "ecosistemas críticos de alta escala, con foco en aplicaciones Web, Mobile y "
            "arquitecturas de APIs (microservicios). Responsable del ciclo completo de QA, desde la "
            "definición de planes de prueba y criterios de aceptación hasta la implementación y el "
            "mantenimiento de frameworks robustos de automatización, buscando acelerar el pipeline "
            "de entrega y la confiabilidad de las versiones. Especialista en sustentación de "
            "software, actuando directamente en el análisis de causa raíz y la mitigación de "
            "incidentes en producción, integrando prácticas de pruebas continuas a la cultura ágil "
            "de los squads para asegurar la mejor experiencia de compra y la estabilidad funcional "
            "de plataformas líderes del retail."
        ),
    },
    {
        "match": "sinergia",
        "company_es": "Sinergia Studios",
        "role_es": "Analista de Pruebas Sénior",
        "description_es": (
            "Responsable de la implantación del área de Quality Assurance en la startup, "
            "estructurando desde cero todos los procesos y estándares de calidad de la organización. "
            "Lideré la estrategia de pruebas durante la reformulación completa de GoGame 2.0 y el "
            "lanzamiento estratégico de la versión 3.0, siendo el principal responsable de "
            "garantizar la integridad del ciclo de vida del software. Implementé automatización "
            "mobile con Robot Framework, Appium y TestProject, combinándolos con pruebas manuales "
            "rigurosas y gestión de defectos vía Jira, asegurando un producto estable y de alto "
            "rendimiento para el mercado."
        ),
    },
    {
        "match": "fagron",
        "company_es": "FagronTech Brasil",
        "role_es": "Consultor - Analista Sénior de Pruebas de API",
        "description_es": (
            "Como consultor sénior en FagronTech — un ERP especializado para farmacias magistrales — "
            "lideré la estrategia de calidad en un entorno de alta complejidad regulatoria y de "
            "datos. Fui responsable de la validación de APIs con Postman, Newman y Swagger, además "
            "de implementar la cultura de pruebas de rendimiento con k6. Actué directamente en la "
            "sustentabilidad del sistema mediante el monitoreo de mensajería con RabbitMQ y la "
            "gestión de pipelines de CI/CD en entornos de staging y producción, garantizando "
            "despliegues seguros y la integridad de integraciones críticas del ecosistema."
        ),
    },
    {
        "match": "deal",
        "company_es": "Deal Technologies",
        "role_es": "Consultor - Analista de Pruebas Sénior",
        "description_es": (
            "Actué como consultor en proyectos estratégicos de transformación digital para los "
            "sectores de fidelización y marketplace (Compra Agora y LTM Fidelidade). Con foco en "
            "arquitecturas de microservicios, lideré el aseguramiento de calidad mediante pruebas "
            "rigurosas de APIs REST, utilizando un stack moderno compuesto por Cypress, Postman y "
            "Newman. Gestioné todo el ciclo de vida de las pruebas y la integración continua dentro "
            "del ecosistema Azure DevOps, asegurando entregas ágiles y la estabilidad de plataformas "
            "de alto volumen de transacciones."
        ),
    },
    {
        "match": "auto avaliar",
        "company_es": "Auto Avaliar",
        "role_es": "Analista de Pruebas Semi Sénior",
        "description_es": (
            "Participé en la estructuración estratégica del ecosistema de calidad de la plataforma, "
            "colaborando en la arquitectura de un framework robusto de automatización web. "
            "Desarrollé suites de pruebas automatizadas con Selenium y Selenide, integrándolas a "
            "pipelines de Integración Continua (CI) vía Jenkins con reportes personalizados de punta "
            "a punta. En el segmento mobile, lideré la automatización de la aplicación de tasación "
            "vehicular con Appium y Cucumber, aplicando prácticas de BDD para garantizar la "
            "confiabilidad de los procesos de inspección y compraventa de vehículos."
        ),
    },
    {
        "match": "capgemini",
        "company_es": "Capgemini Brasil",
        "role_es": "Analista de Pruebas Semi Sénior",
        "description_es": (
            "Actué en un proyecto estratégico para la aplicación del Banco Bradesco, enfocado en el "
            "aseguramiento de calidad de componentes de alta visibilidad. Utilicé el framework "
            "propietario de la institución para el desarrollo de automatización mobile (Appium + "
            "Java) y pruebas de API. Responsable del mapeo de escenarios complejos mediante mapas "
            "mentales y de la gestión del ciclo de vida de pruebas vía ALM Octane y Jira. "
            "Experiencia en un entorno de desarrollo robusto con Bitbucket, Bamboo para integración "
            "continua y Mobile Center para pruebas en dispositivos reales."
        ),
    },
    {
        "match": "pixeon",
        "company_es": "Pixeon Medical System",
        "role_es": "Analista de Pruebas Semi Sénior",
        "description_es": (
            "Actué como Analista de QA en Pixeon, referente en HealthTech, garantizando la calidad "
            "de sistemas críticos para hospitales y clínicas. Destaco la automatización end-to-end "
            "de aplicaciones Web y Desktop, utilizando Java y Selenium para validar el flujo de "
            "entrega de resultados de exámenes en SmartWeb. Fui responsable de la mitigación de "
            "riesgos mediante pruebas manuales rigurosas y la resolución de tickets complejos, "
            "utilizando Jira para la gestión de defectos y asegurando la confiabilidad de soluciones "
            "que impactan directamente el cuidado del paciente."
        ),
    },
    {
        "match": "fraunhofer",
        "company_es": "Fraunhofer Project Center",
        "role_es": "Analista de Pruebas Jr",
        "description_es": (
            "Actué como Analista de QA en el Fraunhofer Project Center, asignado al proyecto del "
            "Sistema Nacional de Trasplantes (SNT) en el Parque Tecnológico de Bahía. Fui "
            "responsable del aseguramiento de calidad de flujos críticos de donación de órganos, "
            "donde la precisión y la disponibilidad del sistema son vitales. En colaboración directa "
            "con el equipo de ingeniería, realicé el levantamiento y la gestión de bugs vía Mantis, "
            "basando la estrategia de pruebas en requisitos complejos y reglas de negocio rigurosas "
            "para asegurar la integridad de una de las plataformas de salud más esenciales del país."
        ),
    },
    {
        "match": "brisa",
        "company_es": "Brisa I+D – LG Mobile",
        "role_es": "Analista de Pruebas Jr",
        "description_es": (
            "Trabajé en Brisa I+D en la validación de dispositivos móviles de LG en fase de "
            "prelanzamiento (líneas K, Q, V y Stylo). Fui responsable de asegurar la calidad de "
            "hardware y software mediante pruebas rigurosas de rendimiento, interfaz (UI) y "
            "funcionalidad de aplicaciones nativas. Mi actuación fue decisiva para garantizar la "
            "conformidad de los dispositivos antes de la producción a escala. Además, me especialicé "
            "en protocolos de actualización vía FOTA (Firmware Over the Air), tema que profundicé "
            "técnicamente en mi tesis de grado, consolidando una base sólida en ciclo de vida de "
            "dispositivos y conectividad."
        ),
    },
    {
        "match": "softwell",
        "company_es": "Softwell Solutions Ltda.",
        "role_es": "Analista de Pruebas Jr.",
        "description_es": (
            "Desarrollo, mantenimiento y prueba de proyectos y sistemas en MAKER ALL. Pruebas de la "
            "plataforma MAKER ALL EXTREME 3.0 y de MAKER MOBILE (iOS y Android), WebRun Java y "
            "WebRun .Net. Gestión, análisis, creación de casos de estudio y checklists, registro y "
            "seguimiento de bugs y soporte al usuario."
        ),
        # EN estava vazio no banco — completa junto
        "description_en": (
            "Development, maintenance and testing of projects and systems on MAKER ALL. Tested the "
            "MAKER ALL EXTREME 3.0 platform and MAKER MOBILE (iOS and Android), WebRun Java and "
            "WebRun .Net. Managed analysis, case studies, checklists, bug tracking and user support."
        ),
    },
    {
        "match": ".compos",
        "company_es": ".COMPOS",
        "role_es": "Programador CakePHP",
        "description_es": (
            "Desarrollo de proyectos (cronograma, requisitos, gestión, plazos) con el framework "
            "CakePHP 2.0 y base de datos PostgreSQL 9, JavaScript, jQuery, AJAX, XML y HTML. "
            "Desarrollo de pruebas de software (caja blanca/negra, regresión, etc.) con PHPUnit/PEAR "
            "y desarrollo con PSP."
        ),
        "description_en": (
            "Project development (schedule, requirements, management, deadlines) using the CakePHP "
            "2.0 framework with PostgreSQL 9, JavaScript, jQuery, AJAX, XML and HTML. Software "
            "testing (white/black box, regression) with PHPUnit/PEAR and PSP-based development."
        ),
    },
    {
        "match": "caixa econ",
        "company_es": "Caixa Econômica Federal",
        "role_es": "Programador PHP",
        "description_es": (
            "Desarrollo de sistemas en PHP según la demanda de la empresa. Configuración y "
            "mantenimiento de servidores. Documentación y actualización de los programas existentes "
            "para la plataforma web, utilizando las bases de datos SQL Server y Microsoft Access."
        ),
        "description_en": (
            "Developed PHP systems on demand. Configured and maintained servers. Documented and "
            "migrated existing programs to the web platform using SQL Server and Microsoft Access "
            "databases."
        ),
    },
]


# ----------------------------- FORMAÇÃO --------------------------------
# Chave de casamento: trecho único do campo "role" (PT) no banco.

EDU_ES = [
    {
        "match": "tester profissional",
        "company_es": "ISTQB",
        "role_es": "[Certificación] ISTQB Certified Tester – Foundation Level (CTFL)",
        "description_es": "ID de credencial: 14-CTFL-03441-BR-BSQTB.",
    },
    {
        "match": "scrum foundation",
        "company_es": "CertiProf",
        "role_es": "[Certificación] Scrum Foundation Professional Certification (SFPC)",
        "description_es": "Certificación profesional alineada a la Guía Scrum.",
    },
    {
        "match": "devops essentials",
        "company_es": "DevOps Essentials – Credly.com",
        "role_es": "[Certificación] DevOps Essentials Professional Certificate",
        "description_es": "Fundamentos de la cultura DevOps y prácticas de ingeniería.",
    },
    {
        "match": "postman + projeto",
        "company_es": "Instructor: Erick Valentim – Udemy",
        "role_es": "[Diploma-Curso] Automatización de pruebas de API con Postman + Proyecto de pruebas",
        "description_es": "Curso completado con todas las clases y actividades (10 horas).",
    },
    {
        "match": "cypress discovery",
        "company_es": "Instructor: Fernando Papito – QA Ninja",
        "role_es": "[Diploma-Curso] Cypress Discovery",
        "description_es": (
            "Automatización de pruebas de aplicaciones web con Cypress, JavaScript y Node.js "
            "(20 horas)."
        ),
    },
    {
        "match": "api da marvel",
        "company_es": "Instructor: Fernando Papito – QA Ninja",
        "role_es": "[Diploma-Curso] Probando la API de Marvel con Robot Framework",
        "description_es": "Curso completado con todas las clases y actividades (4 horas).",
    },
    {
        "match": "microservices em node",
        "company_es": "Instructor: Fernando Papito – QA Ninja",
        "role_es": "[Diploma-Curso] Pruebas de Microservicios en Node.js y MongoDB",
        "description_es": "Curso completado con todas las clases y actividades (16 horas).",
    },
    {
        "match": "httparty",
        "company_es": "Instructor: Bruno Batista – Udemy",
        "role_es": "[Diploma-Curso] Pruebas automatizadas de API con HTTParty + RSpec + Ruby",
        "description_es": "Curso completado con todas las clases y actividades (4,5 horas).",
    },
    {
        "match": "robot framework web+api",
        "company_es": "Instructora: Mayara Fernandes – Udemy",
        "role_es": "[Diploma-Curso] Automatización de Pruebas con Robot Framework Web + API (Básico)",
        "description_es": "Curso completado con todas las clases y actividades (7 horas).",
    },
    {
        "match": "capybara",
        "company_es": "Instructor: Bruno Batista – Udemy",
        "role_es": "[Diploma-Curso] Automatización de Pruebas con Capybara, Cucumber y Ruby",
        "description_es": "Curso completado con todas las clases y actividades (10 horas).",
    },
    {
        "match": "bdd com cucumber",
        "company_es": "Instructor: Francisco Wagner Aquino – Udemy",
        "role_es": "[Diploma-Curso] Aprende BDD con Cucumber y Java",
        "description_es": "Curso completado con todas las clases y actividades (10 horas).",
    },
    {
        "match": "bacharel em sistemas",
        "company_es": "UNIME – Unión Metropolitana de Educación y Cultura",
        "role_es": "[Académica] Licenciatura en Sistemas de Información",
        "description_es": (
            "Tesis: Automatización de Pruebas Funcionales en el proceso FOTA de Dispositivos "
            "Móviles."
        ),
    },
]


# ----------------------------- PROJETOS --------------------------------
# Chave de casamento: trecho único do campo "title" (PT) no banco.

PROJECTS_ES = [
    {
        "match": "wastezero",
        "title_es": (
            "WasteZero: el marketplace vía WhatsApp que transforma el desperdicio en oportunidad a "
            "través de la economía circular."
        ),
        "tech_es": (
            "Next.js 14, React, TypeScript, Tailwind CSS, Node.js, Fastify, MongoDB, "
            "Google Gemini (IA), Cloudflare R2, Mercado Pago, Instagram Graph API, Playwright"
        ),
        "description_es": (
            "Plataforma que convierte el excedente de stock y los productos próximos a vencer en "
            "ventas: el comerciante fotografía el artículo, la IA (Google Gemini) genera título, "
            "descripción, categoría y precio, y la oferta se publica en una tienda online propia con "
            "descuento progresivo y bolsas sorpresa. Automatiza la difusión en Instagram y WhatsApp, "
            "alertas de venta en tiempo real, PIX confirmado vía Mercado Pago Connect y analítica de "
            "embudo. Monorepo pnpm con Next.js 14, Fastify y MongoDB, multi-tenant y trilingüe."
        ),
    },
    {
        "match": "juntix",
        "title_es": "Juntix - Fintech de gestión de crédito colaborativo",
        "tech_es": (
            "React, TypeScript, Vite, TailwindCSS, NestJS, Node.js, MongoDB, Mongoose, Redis, "
            "BullMQ, Docker, JWT, Pix (Lytex/Woovi), Stripe, WhatsApp API, Claude AI, Tesseract OCR, "
            "Cloudflare R2, Jest, Playwright, GitHub Actions"
        ),
        "description_es": (
            "Plataforma SaaS que organiza y automatiza cajas de ahorro colaborativas — grupos en los "
            "que los participantes aportan mensualmente y, cada mes, uno de ellos recibe el monto "
            "reunido. Juntix no custodia fondos: actúa como capa de intermediación y automatización, "
            "con todo el flujo financiero liquidado por PSPs regulados por el BACEN (Lytex y Woovi), "
            "incluyendo split automático entre participante, administrador y plataforma.\n\n"
            "Backend en NestJS + MongoDB con colas BullMQ para cobro recurrente, conciliación de "
            "webhooks y facturación electrónica; frontend en React + TypeScript. Construí el motor "
            "de split y el ledger financiero, el score de triaje antifraude, agentes de IA (Claude) "
            "para reclutamiento y onboarding, comunicación multicanal (WhatsApp vía Evolution API + "
            "correo transaccional) y un panel administrativo con auditoría y rutinas de protección "
            "de datos (LGPD).\n\n"
            "Seguridad tratada como requisito de producto, no como capa final: control de acceso por "
            "roles, reCAPTCHA v3, rate limiting, cifrado de campos sensibles (documento, clave Pix, "
            "datos bancarios) y validación documental con OCR."
        ),
    },
    {
        "match": "cruzzo",
        "title_es": "CRUZZO - Marketplace P2P de mentorías y tareas de campo con pago en custodia",
        "tech_es": (
            "Next.js 14 (App Router), React 18, TypeScript, Tailwind CSS, Node.js, MongoDB Atlas, "
            "Mongoose, JWT (jose), WebRTC, Cloudflare R2, Docker, Monorepo (npm workspaces), Didit "
            "(KYC), Google OAuth 2.0 / OpenID Connect, reCAPTCHA v3, Recharts, i18n (pt-BR/es/en)"
        ),
        "description_es": (
            "Marketplace P2P que conecta a quienes están migrando (Cruzzers) con residentes locales "
            "verificados (Landers): mentorías por video y tareas de campo pagadas, con el valor "
            "retenido en custodia hasta que la entrega sea aprobada. Piloto en Ciudad del Este, "
            "Paraguay.\n\n"
            "Proyecto concebido y construido por mí de punta a punta — modelado de dominio, "
            "back-end, front-end, infraestructura y despliegue. El núcleo es la malla financiera: "
            "ledger de doble entrada, custodia liberada por la aprobación del contratante o por "
            "plazo automático, disputas en las que el veredicto de culpa dirige el reembolso, y "
            "reconciliación entre ledger y saldo validada por smoke tests que corren contra base de "
            "datos real.\n\n"
            "El USD es la unidad de cuenta; BRL, PYG y EUR son solo visualización, convertidos con "
            "cotización en vivo. También implementé verificación de identidad (KYC) integrada a "
            "Didit por webhook con firma verificada, sello Verificado derivado del resultado del "
            "KYC, sala de video WebRTC punta a punta sin SDK de terceros, enmascaramiento de "
            "contacto antes de la contratación (anti-fuga), autenticación JWT en cookies HttpOnly "
            "con login social, reputación por puntualidad, tres idiomas garantizados en tiempo de "
            "compilación y cumplimiento de la LGPD y el Marco Civil — anonimización en lugar de "
            "eliminación y registro de accesos con expiración automática.\n\n"
            "Infraestructura en monorepo npm workspaces, imagen Docker multi-stage, MongoDB Atlas y "
            "Cloudflare R2, publicada en un VPS con Easypanel. El riel de pago con PSP es el próximo "
            "paso: la contabilidad ya está lista y probada para recibirlo."
        ),
    },
    {
        "match": "pixeon",
        "title_es": "Pixeon Health Tech",
        "tech_es": "Java, Selenium, Jira, Jenkins",
        "description_es": (
            "Pixeon es un actor importante en el desarrollo de sistemas de gestión para la salud "
            "(hospitales, clínicas y laboratorios), y ofrece soluciones completas para soportar "
            "todas las etapas de la prestación de servicios. Como QA, actué en la validación y "
            "verificación del sistema SMART y del sistema de entrega de resultados SmartWeb, "
            "utilizando pruebas manuales y automatizadas con Selenium, Selenide y Java."
        ),
    },
    {
        "match": "auto avaliar",
        "title_es": "Auto Avaliar Web y Mobile",
        "tech_es": "Selenium, Selenide, Appium, Cucumber, Jenkins",
        "description_es": (
            "La plataforma Auto Avaliar funciona de forma totalmente automatizada e integrada desde "
            "la identificación, evaluación y cotización del vehículo usado. Como QA realicé pruebas "
            "manuales y automatizadas en las principales herramientas de la organización y, junto a "
            "un consultor, montamos y automatizamos la aplicación móvil de Auto Avaliar. Utilizamos "
            "Java, Selenium, Jenkins y Appium."
        ),
    },
    {
        "match": "compra agora",
        "title_es": "Compra Agora / Viveo / LTM Fidelidad",
        "tech_es": "Cypress, Postman, Newman, Azure DevOps",
        "description_es": (
            "Más de la mitad de los consumidores brasileños prefieren comprar a marcas que ofrecen "
            "un programa de fidelización. Como QA, actué en diversos proyectos de fidelización "
            "realizando pruebas manuales y de API REST para garantizar la calidad del producto. En "
            "algunos proyectos también realicé pruebas automatizadas con Cypress."
        ),
    },
    {
        "match": "phusion",
        "title_es": "Phusion – ERP para Farmacia Magistral",
        "tech_es": "Postman, Newman, Swagger, k6, RabbitMQ",
        "description_es": (
            "Phusion es un ERP online para facilitar y potenciar el desempeño de la farmacia "
            "magistral. Como QA, realicé pruebas manuales y automatizadas de las APIs REST con "
            "Postman y Newman, garantizando la calidad de las entregas quincenales del squad. "
            "También realicé pruebas de rendimiento con k6 en las principales rutas de la API."
        ),
    },
    {
        "match": "gogame",
        "title_es": "GoGame App - Hub de conexión de jugadores",
        "tech_es": "Robot Framework, Appium, REST API",
        "description_es": (
            "GoGame es la app que te permite encontrar jugadores con los mismos juegos e intereses "
            "que tú, intercambiar consejos y coordinar partidas online. Sea cual sea la plataforma o "
            "tu juego favorito, ¡la diversión empieza aquí! En este proyecto realicé pruebas "
            "manuales, automatizadas y de API REST, incluyendo la automatización de la API de GoGame "
            "con Robot Framework."
        ),
        # Correção do bug de dados: EN do GoGame estava com o conteúdo do Bíblica Israel
        "fix_en": {
            "title_en": "GoGame App – Player Connection Hub",
            "tech_en": "Robot Framework, Appium, REST API",
            "description_en": (
                "GoGame connects players worldwide based on platform and interests. I led the "
                "mobile QA rollout, engaging in rigorous manual, API and UI automated testing using "
                "Robot Framework and Appium to guarantee an exceptional user experience on launch "
                "day."
            ),
        },
    },
    {
        "match": "terminal",
        "title_es": "Terminal – Foxbit Exchange",
        "tech_es": "Cypress, JavaScript, GitHub Actions",
        "description_es": (
            "Proyecto privado de Foxbit que permite a sus clientes comprar y vender Bitcoin. Como "
            "QA del equipo, fui responsable de las verificaciones y validaciones, garantizando "
            "mediante pruebas manuales y automatizadas la calidad y el éxito del terminal. Con "
            "Cypress y JavaScript, y una pipeline montada en GitHub Actions, hoy permite el "
            "monitoreo y mantenimiento de la aplicación."
        ),
    },
    {
        "match": "bíblica israel",
        "title_es": "Bíblica Israel – Proyecto Amigo",
        "tech_es": "MongoDB, Vite, Next.js",
        "description_es": (
            "Responsable de la arquitectura y el desarrollo del Proyecto Amigo, una solución "
            "digital enfocada en la experiencia de integración y retención de miembros. La "
            "plataforma gestiona la asignación de actividades de acogida para visitantes y nuevos "
            "integrantes, utilizando datos para potenciar el crecimiento institucional y la "
            "fidelización. Implementé una interfaz ágil con Vite, rutas dinámicas con Next.js y un "
            "backend escalable con MongoDB, con foco en una experiencia de usuario fluida e "
            "intuitiva."
        ),
        # EN estava vazio no banco
        "fix_en": {
            "title_en": "Bíblica Israel – Friend Project",
            "tech_en": "MongoDB, Vite, Next.js",
            "description_en": (
                "Owned the architecture and development of Projeto Amigo, a digital solution "
                "focused on member onboarding and retention. The platform manages welcome "
                "activities for visitors and new members, using data to boost institutional growth "
                "and loyalty. Built a fast Vite interface, dynamic routing with Next.js and a "
                "scalable MongoDB backend, focused on a fluid, intuitive UX."
            ),
        },
    },
]


# --------------------------- HABILIDADES -------------------------------
# Chave: trecho único do campo "name" (PT) no banco -> name_es.

SKILLS_ES = {
    "metódico": "Metódico",
    "organizado": "Organizado",
    "comprometimento": "Compromiso",
    "empatia": "Empatía",
    "comunicação": "Comunicación",
    "objetivo": "Orientado a objetivos",
    "orientação a detalhes": "Atención al detalle",
    "perfeccionista": "Perfeccionista",
    "proatividade": "Proactividad",
    "trabalho em equipe": "Trabajo en equipo",
    "banco de dados": "Bases de Datos [ MySQL, SQL Server, PostgreSQL, MongoDB ]",
    "liderança": "Liderazgo y Mentoría",
    "selenium": "Selenium / Selenide",
    "gestão e técnicas": (
        "Gestión y Técnicas de Pruebas [ Exploratorias, Regresión, Smoke, Valores límite ]"
    ),
    "gherkin": "Gherkin - BDD [ Cucumber ]",
    "performance": "Pruebas de Rendimiento [ k6, JMeter ]",
    "cypress": "Cypress",
    "deploy": "Cloud y Despliegues",
    "git": "Control de Versiones (Git)",
    "linguagens de programação": "Lenguajes de Programación [ Java, JavaScript, Python, Ruby ]",
    "appium": "Automatización Mobile [ Appium, Maestro ]",
    "pipelines": "Pipelines CI/CD [ Jenkins, GitHub Actions ]",
    "postman": "Postman / Insomnia",
    "automação de testes": "Automatización de Pruebas [ Web, Mobile, API ]",
}


def set_if_empty(doc, updates):
    """Retorna dict apenas com campos vazios no doc (ou tudo, com --force)."""
    out = {}
    for key, value in updates.items():
        if FORCE or not (doc.get(key) or "").strip():
            out[key] = value
    return out


def main():
    db = get_db()

    # Settings
    n = 0
    for key, value in SETTINGS_ES.items():
        if FORCE or not (get_setting(key, "") or "").strip():
            set_setting(key, value)
            n += 1
    print(f"[settings] {n} chaves ES gravadas")

    # About (documento mais recente)
    about = db.about.find_one(sort=[("_id", -1)])
    if about and (FORCE or not (about.get("content_es") or "").strip()):
        db.about.update_one({"_id": about["_id"]}, {"$set": {"content_es": ABOUT_ES}})
        print("[about] content_es gravado")

    # Experiências (work)
    n = 0
    for item in WORK_ES:
        match = item["match"]
        doc = db.experiences.find_one(
            {"kind": "work", "company": {"$regex": match, "$options": "i"}}
        )
        if not doc:
            print(f"  !! work não encontrado: {match!r}")
            continue
        updates = set_if_empty(
            doc,
            {k: v for k, v in item.items() if k not in ("match",)},
        )
        if updates:
            db.experiences.update_one({"_id": doc["_id"]}, {"$set": updates})
            n += 1
    print(f"[work] {n} experiências atualizadas")

    # Formação
    n = 0
    for item in EDU_ES:
        match = item["match"]
        doc = db.experiences.find_one(
            {"kind": "education", "role": {"$regex": match, "$options": "i"}}
        )
        if not doc:
            print(f"  !! education não encontrado: {match!r}")
            continue
        updates = set_if_empty(doc, {k: v for k, v in item.items() if k != "match"})
        if updates:
            db.experiences.update_one({"_id": doc["_id"]}, {"$set": updates})
            n += 1
    print(f"[education] {n} itens atualizados")

    # Projetos
    n = 0
    for item in PROJECTS_ES:
        match = item["match"]
        doc = db.projects.find_one({"title": {"$regex": match, "$options": "i"}})
        if not doc:
            print(f"  !! projeto não encontrado: {match!r}")
            continue
        updates = set_if_empty(
            doc, {k: v for k, v in item.items() if k not in ("match", "fix_en")}
        )
        # Correções EN forçadas (bug de traduções trocadas / EN faltando)
        if "fix_en" in item:
            updates.update(item["fix_en"])
        if updates:
            db.projects.update_one({"_id": doc["_id"]}, {"$set": updates})
            n += 1
    print(f"[projects] {n} projetos atualizados")

    # Habilidades
    n = 0
    for match, name_es in SKILLS_ES.items():
        doc = db.skills.find_one({"name": {"$regex": match, "$options": "i"}})
        if not doc:
            print(f"  !! skill não encontrada: {match!r}")
            continue
        if FORCE or not (doc.get("name_es") or "").strip():
            db.skills.update_one({"_id": doc["_id"]}, {"$set": {"name_es": name_es}})
            n += 1
    print(f"[skills] {n} habilidades com name_es")

    print("Concluído.")


if __name__ == "__main__":
    main()
