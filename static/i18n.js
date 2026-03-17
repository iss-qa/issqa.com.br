const translations = {
    pt: {
        // Menu
        "menu-inicio": "Inicio",
        "menu-sobre": "Sobre",
        "menu-habilidades": "Habilidades",
        "menu-curriculo": "Curriculo",
        "menu-formacao": "Formação",
        "menu-portfolio": "Portfólio",
        "menu-contato": "Contato",

        // Header
        "header-title": "Isaias Silva",
        "header-subtitle": "QA Lead, Automatizador Cypress, Empreendedor",

        // Sobre
        "sobre-title": "Sobre",
        "sobre-p1": "Acredito que a educação pode mudar a vida das pessoas e sou prova disso. Sou formado em Sistemas de Informação e tenho mais de 8 anos de experiência em testes de software, incluindo mobile, API e web. Tenho uma paixão especial por testes automatizados e de API REST e sou muito focado e profissional em entregar software de qualidade. Para contribuir com minha comunidade, dou aulas gratuitas de fundamentos de programação para jovens. Acredito que ensinar é uma forma significativa de ajudar os outros e crescer profissionalmente. Além disso, sou casado e pai de uma garotinha de 2 anos que é minha luz do dia. Sou cristão da Igreja Batista e gosto de tocar teclado e lidero o grupo de jovens na igreja e ensino na Escola Bíblica Dominical. Ser cristão e seguidor de Jesus, é algo que faço questão de estar em minha biografia.",
        "sobre-p2": "Adoro novas tecnologias e estou sempre me atualizando, além de QA, auto como desenvolvedor, onde entrego e mantenho pequenos softwares para clientes em minha comunidade. Sou um jovem bem-sucedido e acredito que minha jornada ainda está só começando. Ser orientador é minha vocação e espero influenciar e motivar muitas pessoas ao longo do caminho.",
        "sobre-emp-title": "Empreendedor",
        "sobre-emp-p1": "Atualmente venho desenvolvendo e estruturando um projeto pessoal, inclusive contratando Devs Front e Back para a implementação de uma possível solução que pode se tornar o carro chefe da minha pequena empresa. Porém isso é feito de forma bem tranquila e suave sem pressa visto que em paralelo me dedico Full Time na prestação do serviço e contrato proposto.",
        "sobre-emp-p2": "Dedico meu tempo para coordenar e gerenciar uma pequena empresa, bem como para apoiar causas sociais, como resgatar e orientar jovens da droga e da perdição para o caminho de Cristo. Gosto de fazer o bem, arrecadar alimentos e ajudar os menos afortunados. Além disso, minha família é muito importante para mim, pois tenho uma esposa amorosa que cuida de mim, uma filha adorável e um animal de estimação que completam minha vida. Apesar de ter redes sociais, sou uma pessoa discreta em relação à minha vida pessoal.",

        // Lista Sobre
        "sobre-niver": "Niver",
        "sobre-idade": "Idade",
        "sobre-cidade": "Cidade",
        "sobre-estado": "Estado",
        "sobre-estado-val": "Bahia",
        "sobre-hobby": "Hobby",
        "sobre-hobby-val": "Viajar",
        "sobre-trabalho": "Trabalho",
        "sobre-xp": "Experiência",

        // Habilidades
        "hab-title": "Habilidades",
        "hab-desc": "Em todo tempo como profissional de tecnologia eu adquiri algumas habilidades técnicas e não técnicas, a maioria delas estão aqui, de acordo com a porcentagem de conhecimento que eu acredito ter em cada uma delas.",

        "hab-t1": "Automação de Testes [ Web, Mobile, API ]",
        "hab-t2": "Postman/Insomnia",
        "hab-t3": "Pipelines CI [ Jenkins, Github Actions ]",
        "hab-t4": "Appium",
        "hab-t5": "Linguagens de Programação [ Java, Javascript, Python, Ruby ]",
        "hab-t6": "Git",
        "hab-t7": "Deploy",
        "hab-t8": "Cypress",
        "hab-t9": "Performance Testes [ k6, jmetter ]",
        "hab-t10": "Gherkin - BDD [ Cucumber ]",
        "hab-t11": "Gestão e Técnicas de Testes [ Exploratório, Regressivo, Smoke, Análise valor limite ]",
        "hab-t12": "Selenium / Selenide",
        "hab-t13": "Liderança",
        "hab-t14": "Banco de Dados [ Mysql, Sql Server, Postgree, MongoDB ]",

        "hab-s1": "Trabalho em equipe",
        "hab-s2": "Proatividade",
        "hab-s3": "Perfeccionista",
        "hab-s4": "Orientação a detalhes",
        "hab-s5": "Objetivo",
        "hab-s6": "Comunicação",
        "hab-s7": "Empatia",
        "hab-s8": "Comprometimento",
        "hab-s9": "Organizado",
        "hab-s10": "Metódico",

        // Curriculo Custom Titles
        "cv-title": "Currículo",
        "cv-formation-title": "Formação",
        "cv-f1-t": "[Acadêmica] Bacharel em Sistemas de Informação",
        "cv-f1-i": "UNIME - União Metropolitana de Educação e Cultura",
        "cv-f1-d": "Monografia: Automação de Testes Funcionais no processo de FOTA em Dispositivos Móveis",
        "cv-f2-t": "[Certificação] Tester Profissional Certified",
        "cv-f2-i": "ISTQB Certified Tester",
        "cv-f2-d": "14-CTFL-03441-BR-BSQTB",
        "cv-f3-t": "[Certificação] Scrum Foundation Professional Certification",
        "cv-f3-i": "CertiProf",
        "cv-f3-d": "Scrum Guide - SFPC - Professional Certification",
        "cv-f4-t": "[Certificação] DevOps Essentials Professional Certificate",
        "cv-f4-i": "DevOps Essentials - Credly.com",
        "cv-f4-d": "DevOps Essentials Professional Certificate",
        "cv-f5-t": "[Diploma-Curso] Cypress Discovery",
        "cv-f5-i": "Instrutor: Fernando Papito - QA Ninja",
        "cv-f5-d": "Certificamos Isaias Silva, pela conclusão de todas as aulas e atividades propostas no curso: Cypress Discovery com foco em automação de testes de aplicações web em Cypress, javascript e Node.js",
        "cv-f6-t": "[Diploma-Curso] Testando a API da Marvel em Robot Framework",
        "cv-f6-i": "Instrutor: Fernando Papito - QA Ninja",
        "cv-f6-d": "Certificamos Isaias Silva, pela conclusão de todas as aulas e atividades propostas no curso: Testando a API da Marvel em Robot Framework, com carga horária de 4 horas",
        "cv-f7-t": "[Diploma-Curso] Testes de Microservices em Node.js e MongoDB",
        "cv-f7-i": "Instrutor: Fernando Papito - QA Ninja",
        "cv-f7-d": "Certificamos Isaias Silva, pela conclusão de todas as aulas e atividades propostas no curso:Testes de Microservices em Node.js e MongoDB, com carga horária de 16 horas",
        "cv-f8-t": "[Diploma-Curso] Testes automatizados de API com HTTParty+Rspec+Ruby",
        "cv-f8-i": "Instrutor: Bruno Batista - Udemy",
        "cv-f8-d": "Certificamos Isaias Silva, pela conclusão de todas as aulas e atividades propostas no curso: Testes automatizados de API com HTTParty+Rspec+Ruby, com carga horária de 4,5 horas",
        "cv-f9-t": "[Diploma-Curso] Automação de Testes com Robot Framework Web+API - Básico",
        "cv-f9-i": "Instrutor: Mayara Fernandes - Udemy",
        "cv-f9-d": "Certificamos Isaias Silva, pela conclusão de todas as aulas e atividades propostas no curso: Automação de Testes com Robot Framework Web+API - Básico, com carga horária de 7 horas",
        "cv-f10-t": "[Diploma-Curso] Automação de Testes com Capybara, Cucumber e Ruby",
        "cv-f10-i": "Instrutor: Bruno Batista - Udemy",
        "cv-f10-d": "Certificamos Isaias Silva, pela conclusão de todas as aulas e atividades propostas no curso: Automação de Testes com Capybara, Cucumber e Ruby, com carga horária de 10 horas",
        "cv-f11-t": "[Diploma-Curso] Aprenda BDD com Cucumber e Java",
        "cv-f11-i": "Instrutor: Francisco Wagner Aquino - Udemy",
        "cv-f11-d": "Certificamos Isaias Silva, pela conclusão de todas as aulas e atividades propostas no curso: Aprenda BDD com Cucumber e Java, com carga horária de 10 horas",
        "cv-f12-t": "[Diploma-Curso] Automação de testes de API com Postman + Projeto de testes",
        "cv-f12-i": "Instrutor: Erick Valentim - Udemy",
        "cv-f12-d": "Certificamos Isaias Silva, pela conclusão de todas as aulas e atividades propostas no curso: Automação de testes de API com Postman + Projeto de testes, com carga horária de 10 horas",

        "cv-p1-t": "Analista de Automação Web (Cypress)",
        "cv-p1-i": "Foxbit Exchange",
        "cv-p1-d": "A Foxbit é uma corretora brasileira de Bitcoin e outras criptomoedas. Ela faz a intermediação de compra e venda de moedas digitais, com saques e depósitos em Reais e criptomoedas.",
        "cv-p2-t": "Analista de Testes Sr",
        "cv-p2-i": "Sinergia Studios",
        "cv-p2-d": "Startup de desenvolvimento de aplicativos e games. Atuei para implantar o setor de qualidade na organização, refizemos o GoGame 2.0 do zero e lançamos no mercado o GoGame 3.0.",
        "cv-p3-t": "Consultor - Analista de API Testes Sr",
        "cv-p3-i": "FagronTech Brasil",
        "cv-p3-d": "Phusion é um ERP Online para facilitar e potencializar o desempenho da farmácia de manipulação. Neste projeto atuei como o QA Lead.",
        "cv-p4-t": "Consultor - Analista de Testes Sr",
        "cv-p4-i": "Deal Technologies",
        "cv-p4-d": "Consultoria de tecnologia da informação e transformação digital. Alocado em projetos no ramo de fidelidade e fidelização de clientes.",
        "cv-p5-t": "Analista de Testes Pleno",
        "cv-p5-i": "Auto Avaliar",
        "cv-p5-d": "Plataforma de compra e venda de veículos. Montei junto com um consultor um framework de automação web, desenvolvi testes automatizados.",
        "cv-p6-t": "Analista de Testes Pleno",
        "cv-p6-i": "Capgemini Brasil",
        "cv-p6-d": "Atuei por um curto período automatizando um banner no aplicativo do banco Bradesco. Framework próprio do banco. Desenvolvi, Testes de API, mapa Mental e automação Mobile",
        "cv-p7-t": "Analista de Testes Pleno",
        "cv-p7-i": "Pixeon Medical System",
        "cv-p7-d": "Pixeon é um Health Tech, que possui diversas soluções para clínicas e hospitais. Atuei em diversos projetos da organização.",
        "cv-p8-t": "Analista de Testes Jr",
        "cv-p8-i": "Fraunhofer Project Center",
        "cv-p8-d": "",
        "cv-p9-t": "Analista de Testes Jr",
        "cv-p9-i": "Brisa P&D - LG Mobile",
        "cv-p9-d": "",
        "cv-p10-t": "Estagiário Testador de IDE Maker",
        "cv-p10-i": "Brisa P&D - LG Mobile",
        "cv-p10-d": "",


        // Portfolio
        "port-title": "Portfólio",
        "port-1-t": "Terminal - Foxbit Exchange",
        "port-1-d": "Projeto Privado da Foxbit, permite clientes da mesma comprar e vender Bitcoins. como QA do time, fui responsável pelas verificações e validações, garantindo assim através de testes manuais e automatizados a qualidade e o sucesso do terminal. Usando Cypress e Javascript, com pipeline montada no GitHub Actions, hoje permite o monitoramento e manutenção da aplicação",
        "port-2-t": "Gogame App - Hub de Conexão de Jogadores",
        "port-2-d": "GoGame é o app que te permite encontrar jogadores com os mesmos jogos e interesses que você, trocar dicas e combinar partidas online. Seja qual for a plataforma ou seu jogo favorito, a diversão começa aqui!. Neste projeto realizei testes manuais, automatizados e de API Rest, inclusive automatizado a API do GoGame com Robot Framework",
        "port-3-t": "Phusion Farmácia de Manipulação",
        "port-3-d": "O Phusion é um ERP Online para facilitar e potencializar o desempenho da farmácia magistral. Como QA, atuei na realização de testes manuais e automatizados nas API Rest com Postman e Newman.",
        "port-4-t": "Compra Agora/Viveo / LTM Fidelidade",
        "port-4-d": "Mais de metade dos consumidores brasileiros preferem realizar compras de marcas que oferecem um programa de fidelidade. Como QA, atuei nos diversos projetos de fidelidade.",
        "port-5-t": "Auto Avaliar Web e Mobile",
        "port-5-d": "A plataforma Auto Avaliar funciona de forma totalmente automatizada e integrada desde a identificação, avaliação e cotação do veículo usado.",
        "port-6-t": "Pixeon Health Tech",
        "port-6-d": "A Pixeon é uma importante player no desenvolvimento de sistemas de gestão para a saúde, e oferece soluções completas para suportar todas as etapas.",

        // Contato
        "contact-title": "Contato",
        "contact-loc": "Localização",
        "contact-form-name": "Nome:",
        "contact-form-name-ph": "Digite seu nome",
        "contact-form-email": "Email:",
        "contact-form-email-ph": "Digite seu email",
        "contact-form-msg": "Mensagem:",
        "contact-form-msg-ph": "Digite sua mensagem",
        "contact-form-btn": "Enviar Mensagem",
        "contact-form-loading": "Enviando, aguarde!..."
    },
    en: {
        // Menu
        "menu-inicio": "Home",
        "menu-sobre": "About",
        "menu-habilidades": "Skills",
        "menu-curriculo": "Resume",
        "menu-formacao": "Education",
        "menu-portfolio": "Portfolio",
        "menu-contato": "Contact",

        // Header
        "header-title": "Isaias Silva",
        "header-subtitle": "Senior Quality Engineering Lead | LLM-Assisted Testing | Entrepreneur",

        // Sobre
        "sobre-title": "About",
        "sobre-p1": "I believe education can change people's lives, and I am living proof of it. Holding a Bachelor's in Information Systems, I have over 10 years of experience in Quality Engineering, including Mobile Regression, RESTful APIs, and Web applications. I have a profound passion for Test Automation Architecture and am laser-focused on delivering high-quality, scalable software. To give back to my community, I teach free programming and QA fundamentals to local youth—teaching is a meaningful way to help others grow while refining my own leadership skills. Above all, I am a dedicated husband and a proud father. As a Christian, I serve by teaching Sunday School and leading young adult groups; guiding my professional and personal life with integrity.",
        "sobre-p2": "I am deeply invested in innovation, particularly in transitioning towards Generative AI (LLM-Assisted Testing) to accelerate test lifecycles and maximize business ROI. Beyond QA Strategy, I act as a full-stack developer, delivering and maintaining custom software for local businesses. As a successful entrepreneur and Lead QA, I feel my journey is just hitting its stride. Mentorship is my vocation, and I aim to inspire many along the way.",
        "sobre-emp-title": "Entrepreneurship",
        "sobre-emp-p1": "I am currently architecting a personal platform, hiring Front-end and Back-end developers to implement a solution that may become the flagship of my company. This is executed steadily and meticulously, running parallel to my full-time dedication as a Senior QA Engineering consultant.",
        "sobre-emp-p2": "I dedicate my time to leading my company and supporting social causes—mentoring youth away from drugs and toward their potential. Giving back is paramount to me. I'm protective of my family, balancing high technical output with dedicated time for my wife, daughter, and pet.",

        // Lista Sobre
        "sobre-niver": "Birthday",
        "sobre-idade": "Age",
        "sobre-cidade": "City",
        "sobre-estado": "State",
        "sobre-estado-val": "Bahia, BR",
        "sobre-hobby": "Hobby",
        "sobre-hobby-val": "Traveling",
        "sobre-trabalho": "Work",
        "sobre-xp": "Experience",

        // Habilidades
        "hab-title": "Skills",
        "hab-desc": "Throughout my career in Quality Engineering, I have mastered critical technical and leadership skills. Below is an overview of my core competencies.",

        "hab-t1": "Test Automation Architecture [ Web, Mobile Regression, API ]",
        "hab-t2": "API Validation [ Postman/Insomnia ]",
        "hab-t3": "CI/CD Pipelines [ Jenkins, Github Actions ]",
        "hab-t4": "Mobile Automation [ Appium, Maestro ]",
        "hab-t5": "Programming Languages [ JavaScript, TypeScript, Python, Ruby ]",
        "hab-t6": "Version Control [ Git ]",
        "hab-t7": "Cloud & Deployments",
        "hab-t8": "Cypress",
        "hab-t9": "Performance Testing [ k6, jMeter ]",
        "hab-t10": "Gherkin - BDD [ Cucumber ]",
        "hab-t11": "Quality Assurance & Strategy [ LLM-Assisted Testing, Exploratory, Boundary Analysis ]",
        "hab-t12": "Selenium / Playwright",
        "hab-t13": "Leadership & Mentoring",
        "hab-t14": "Databases [ MySQL, PostgreSQL, MongoDB ]",

        "hab-s1": "Cross-functional Collaboration",
        "hab-s2": "Proactivity",
        "hab-s3": "Quality-First Mindset",
        "hab-s4": "Detail-Oriented",
        "hab-s5": "Goal-Driven (ROI focused)",
        "hab-s6": "Communication & Reporting",
        "hab-s7": "Empathy",
        "hab-s8": "Commitment & Ownership",
        "hab-s9": "Organized Strategy",
        "hab-s10": "Methodical Analysis",

        // Curriculo Custom Titles
        "cv-title": "Resume",
        "cv-formation-title": "Education",
        "cv-f1-t": "[Academic] Bachelor of Information Systems",
        "cv-f1-i": "UNIME - Metropolitan Union of Education and Culture",
        "cv-f1-d": "Thesis: Functional Test Automation in Mobile Device FOTA Processes",
        "cv-f2-t": "[Certification] ISTQB Certified Tester",
        "cv-f2-i": "ISTQB Certified Tester",
        "cv-f2-d": "14-CTFL-03441-BR-BSQTB",
        "cv-f3-t": "[Certification] Scrum Foundation Professional Certification",
        "cv-f3-i": "CertiProf",
        "cv-f3-d": "Scrum Guide - SFPC - Professional Certification",
        "cv-f4-t": "[Certification] DevOps Essentials Professional Certificate",
        "cv-f4-i": "DevOps Essentials - Credly.com",
        "cv-f4-d": "DevOps Essentials Professional Certificate",
        "cv-f5-t": "[Diploma-Course] Cypress Discovery",
        "cv-f5-i": "Instructor: Fernando Papito - QA Ninja",
        "cv-f5-d": "Automation of web apps in Cypress, JavaScript, and Node.js",
        "cv-f6-t": "[Diploma-Course] Testing Marvel API with Robot Framework",
        "cv-f6-i": "Instructor: Fernando Papito - QA Ninja",
        "cv-f6-d": "Completed all proposed classes and activities in the course.",
        "cv-f7-t": "[Diploma-Course] Microservices Testing in Node.js and MongoDB",
        "cv-f7-i": "Instructor: Fernando Papito - QA Ninja",
        "cv-f7-d": "Completed all proposed classes and activities in the course.",
        "cv-f8-t": "[Diploma-Course] Automated API Testing with HTTParty+Rspec+Ruby",
        "cv-f8-i": "Instructor: Bruno Batista - Udemy",
        "cv-f8-d": "Completed all proposed classes and activities in the course.",
        "cv-f9-t": "[Diploma-Course] Test Automation with Robot Framework Web+API",
        "cv-f9-i": "Instructor: Mayara Fernandes - Udemy",
        "cv-f9-d": "Completed all proposed classes and activities in the course.",
        "cv-f10-t": "[Diploma-Course] Test Automation with Capybara, Cucumber, and Ruby",
        "cv-f10-i": "Instructor: Bruno Batista - Udemy",
        "cv-f10-d": "Completed all proposed classes and activities in the course.",
        "cv-f11-t": "[Diploma-Course] Learn BDD with Cucumber and Java",
        "cv-f11-i": "Instructor: Francisco Wagner Aquino - Udemy",
        "cv-f11-d": "Completed all proposed classes and activities in the course.",
        "cv-f12-t": "[Diploma-Course] Automated API Testing with Postman",
        "cv-f12-i": "Instructor: Erick Valentim - Udemy",
        "cv-f12-d": "Completed all proposed classes and activities in the course.",

        "cv-p1-t": "Senior Quality Engineering Lead (Cypress)",
        "cv-p1-i": "Foxbit Exchange",
        "cv-p1-d": "Foxbit is a top Brazilian cryptocurrency exchange. As Lead QA, I established the Test Automation Architecture with Cypress and Maestro.",
        "cv-p2-t": "Senior Test Analyst",
        "cv-p2-i": "Sinergia Studios",
        "cv-p2-d": "App and game development startup. Implemented the quality sector, rebuilt GoGame 2.0, and launched GoGame 3.0.",
        "cv-p3-t": "Senior API Test Consultant",
        "cv-p3-i": "FagronTech Brasil",
        "cv-p3-d": "Phusion is an online ERP to enhance compounding pharmacy performance. I acted as QA Lead working with Postman and K6.",
        "cv-p4-t": "Senior Test Consultant",
        "cv-p4-i": "Deal Technologies",
        "cv-p4-d": "IT consulting and digital transformation. Allocated to loyalty projects performing API Rest and Cypress testing.",
        "cv-p5-t": "Mid-Level Test Analyst",
        "cv-p5-i": "Auto Avaliar",
        "cv-p5-d": "Vehicle buying and selling platform. Created an automation framework with Selenium and Appium.",
        "cv-p6-t": "Mid-Level Test Analyst",
        "cv-p6-i": "Capgemini Brasil",
        "cv-p6-d": "Worked briefly automating the Bradesco bank app banner. API testing and Appium.",
        "cv-p7-t": "Mid-Level Test Analyst",
        "cv-p7-i": "Pixeon Medical System",
        "cv-p7-d": "Pixeon is a Health Tech offering solutions for clinics and hospitals. Automated validations with Selenium and Java.",
        "cv-p8-t": "Junior Test Analyst",
        "cv-p8-i": "Fraunhofer Project Center",
        "cv-p8-d": "",
        "cv-p9-t": "Junior Test Analyst",
        "cv-p9-i": "Brisa R&D - LG Mobile",
        "cv-p9-d": "",
        "cv-p10-t": "IDE Maker Tester Intern",
        "cv-p10-i": "Brisa R&D - LG Mobile",
        "cv-p10-d": "",

        // Portfolio
        "port-title": "Portfolio",
        "port-1-t": "Foxbit Exchange Trading Terminal",
        "port-1-d": "A private trading terminal allowing high-volume Bitcoin transactions. As the Lead QA, I architected the cross-browser automation suite using Cypress and JS, running directly on GitHub Actions. Ensured bulletproof reliability and zero downtime through robust regression validation and CI/CD integration.",
        "port-2-t": "Gogame App - Player Connection Hub",
        "port-2-d": "GoGame connects players worldwide based on platform and interests. I led the mobile QA rollout, engaging in rigorous manual, API, and UI automated testing using Robot Framework and Appium to guarantee an exceptional user experience on launch day.",
        "port-3-t": "Phusion Compounding Pharmacy",
        "port-3-d": "Phusion is an online ERP that optimizes pharmacy workflow. As QA, I validated API integrations using Postman and Newman, ensuring quality in bi-weekly deliveries. I also executed performance tests along critical API routes using K6.",
        "port-4-t": "Compra Agora/Viveo / LTM Loyalty",
        "port-4-d": "With over half of Brazilian consumers preferring loyalty programs, I conducted exhaustive end-to-end API validations to guarantee product stability, alongside targeted automation scripts utilizing Cypress.",
        "port-5-t": "Auto Avaliar Web & Mobile",
        "port-5-d": "The Auto Avaliar platform seamlessly automates vehicle appraisal. I rolled out a comprehensive QA process using Java, Selenium, Jenkins, and Appium for mobile automation alongside a consulting expert.",
        "port-6-t": "Pixeon Health Tech",
        "port-6-d": "Pixeon develops large-scale health management systems. In this role, I validated the SMART system and Smartweb delivery applications through manual test case design and Selenium automation.",

        // Contato
        "contact-title": "Contact",
        "contact-loc": "Location:",
        "contact-form-name": "Name:",
        "contact-form-name-ph": "Enter your name",
        "contact-form-email": "Email:",
        "contact-form-email-ph": "Enter your email",
        "contact-form-msg": "Message:",
        "contact-form-msg-ph": "Enter your message",
        "contact-form-btn": "Send Message",
        "contact-form-loading": "Sending, please wait!..."
    }
};

document.addEventListener("DOMContentLoaded", () => {
    const langToggleBtn = document.getElementById("lang-toggle");
    if (!langToggleBtn) return;

    let currentLang = localStorage.getItem("issqa-lang") || "pt";

    // Função para atualizar todos elementos com data-i18n
    const applyTranslations = (lang) => {
        document.querySelectorAll("[data-i18n]").forEach(element => {
            const key = element.getAttribute("data-i18n");

            // Tratamento especial para placeholders e val
            if (element.tagName === "INPUT" || element.tagName === "TEXTAREA") {
                if (element.placeholder) {
                    element.placeholder = translations[lang][key] || element.placeholder;
                }
            } else {
                element.innerHTML = translations[lang][key] || element.innerHTML;
            }
        });

        // Atualiza o texto do botão
        langToggleBtn.innerHTML = lang === "pt" ? "🇺🇸 English" : "🇧🇷 Português";

        // Atualiza o link do curriculo para download do PDF ATS-friendly 
        const resumeBtn = document.getElementById("download-resume-btn");
        if (resumeBtn) {
            resumeBtn.href = lang === "pt" ? "#curriculo" : "../static/Isaias_Silva_Resume.pdf";
            resumeBtn.target = lang === "pt" ? "" : "_blank";
        }
    };

    // Aplicação inicial
    applyTranslations(currentLang);

    // Listener do Botão
    langToggleBtn.addEventListener("click", () => {
        currentLang = currentLang === "pt" ? "en" : "pt";
        localStorage.setItem("issqa-lang", currentLang);
        applyTranslations(currentLang);
    });
});
