# Portfólio CV - ISSQA

Este é o meu portfólio web construído com Flask, HTML, CSS, JavaScript e Bootstrap, contendo também testes de ponta-a-ponta utilizando Playwright. A aplicação inclui suporte a internacionalização (i18n) e download de currículo ATS-friendly.

## Pré-requisitos
- **Python 3.x**
- **Node.js** (para os testes E2E com Playwright)

## 🚀 Como Executar o Projeto Localmente

### 1. Backend (Flask)
O backend da aplicação utiliza Python e Flask. Para rodar:
```bash
# Crie e ative um ambiente virtual (recomendado)
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\\Scripts\\activate

# Instale as dependências
pip install -r requirements.txt

# Inicie o servidor
python3 app.py
```
A aplicação estará disponível em `http://127.0.0.1:5000`.

### 2. Testes E2E (Playwright)
O projeto conta com testes E2E para garantir o funcionamento da troca de idiomas (i18n) e download do CV. A estrutura de testes utiliza Page Object Model (POM).

```bash
# Na raiz do projeto, instale as dependências Node (Playwright)
npm install

# Instale os navegadores do Playwright (se for a primeira vez)
npx playwright install --with-deps chromium

# Com a aplicação Flask rodando em outro terminal, execute os testes
npx playwright test
```

Os testes estão localizados na pasta `tests/`.
