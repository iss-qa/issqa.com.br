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

## Banco e Admin (MongoDB)

### Variáveis de ambiente
- `SECRET_KEY`
- `EMAIL` (SMTP)
- `SENHA` (SMTP)
- `MONGO_URI` (ex: `mongodb://localhost:27017`)
- `MONGO_DB` (ex: `portfolio_cv`)

### Seed/reset do banco
```bash
python3 scripts/seed_db.py --reset --samples
```

### Export/backup do conteúdo do admin
```bash
python3 scripts/export_db.py
```

### Criar usuário admin manualmente
```bash
python3 scripts/create_user.py --username "qa.eng.isaiasilva@gmail.com" --password "Is@i@s1989"
```

### Importar dados do site em produção (skills/currículo/portfólio)
```bash
python3 scripts/import_from_site.py --reset
```

## Produção com MongoDB Atlas
1. Crie um cluster no Atlas e um usuário de banco.
2. Copie a connection string e configure:
   - `MONGO_URI=mongodb+srv://<user>:<pass>@<cluster>/<db>?retryWrites=true&w=majority`
   - `MONGO_DB=<db>`
3. No Vercel, adicione essas variáveis em `Project Settings -> Environment Variables`.


lsof -ti :5000 | xargs kill -9
