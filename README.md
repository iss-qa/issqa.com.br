# Portfólio CV - ISSQA

Portfólio web construído com Flask, HTML, CSS, JavaScript e Bootstrap, com testes E2E em Playwright, internacionalização (i18n), download de currículo ATS-friendly e painel administrativo com MongoDB.

## Pré-requisitos
- **Python 3.9+**
- **Node.js 18+** (para os testes E2E com Playwright)
- **MongoDB** local *ou* uma connection string do **MongoDB Atlas**

## 🚀 Como Executar o Projeto Localmente

### 1. Clone e entre na pasta
```bash
git clone https://github.com/<seu-usuario>/portfolio-cv.git
cd portfolio-cv
```

### 2. Crie o arquivo `.env` na raiz
```ini
SECRET_KEY=troque-por-uma-chave-segura
EMAIL=seu.email@gmail.com
SENHA=senha-de-app-do-gmail
# Destinatários do formulário de contato (vírgula). Padrão: os dois Gmails do Isaias
CONTACT_RECIPIENTS=qa.eng.isaiasilva@gmail.com,isaiasilva.info@gmail.com
# Opcionais: MAIL_SERVER (smtp.gmail.com), MAIL_PORT (465 SSL; use 587 para STARTTLS)
# MongoDB local:
MONGO_URI=mongodb://localhost:27017
# Ou MongoDB Atlas (recomendado em produção):
# MONGO_URI=mongodb+srv://<user>:<pass>@<cluster>/portfolio_cv?retryWrites=true&w=majority
MONGO_DB=portfolio_cv
# Seed do usuário admin inicial (sem ADMIN_PASS nenhum admin é criado)
ADMIN_USER=isaias
ADMIN_PASS=troque-esta-senha
```

> `EMAIL`/`SENHA` são usados no envio SMTP do formulário de contato. O Gmail **recusa a senha normal da conta**: ative a verificação em 2 etapas e gere uma **senha de app** (16 letras) em <https://myaccount.google.com/apppasswords>. Mesmo se o e-mail falhar, a mensagem fica salva em *Admin → Contato* (marcada como "E-mail não enviado").
>
> Modelo completo em `.env.example`. **Nunca versione o `.env`.**

### 3. Backend (Flask)
```bash
# Crie e ative um ambiente virtual
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Inicie o servidor
python3 app.py
```

A aplicação sobe em `http://127.0.0.1:5000`.

> **macOS:** a porta 5000 é usada pelo *AirPlay Receiver*. Desative em *Ajustes → Geral → AirDrop & Handoff* ou rode em outra porta:
> ```bash
> python3 -c "from app import app; app.run(host='127.0.0.1', port=5001)"
> ```
> Se ainda assim a porta estiver ocupada:
> ```bash
> lsof -ti :5000 | xargs kill -9
> ```

### 4. Painel Administrativo
1. Acesse `http://127.0.0.1:5000/login`.
2. Usuário/senha iniciais vêm das variáveis `ADMIN_USER` / `ADMIN_PASS` (não há senha padrão no código).
3. No painel você pode editar: Início, Sobre, Empreendedor, Habilidades, Experiências, Formação, Portfólio e Mensagens.
4. Nas abas **Experiências** e **Formação**:
   - Arraste pelo ícone `☰` para reordenar (a ordem é persistida automaticamente).
   - Clique no cabeçalho do card para expandir/minimizar.
   - Use **Ordenar por data** para organizar automaticamente (empresas em curso no topo, depois pela data de fim e início mais recentes).

### 5. Testes E2E (Playwright)
```bash
npm install
npx playwright install --with-deps chromium

# Com o Flask rodando em outro terminal:
npx playwright test
```
Os testes ficam em `tests/` e usam Page Object Model.

## Scripts utilitários

| Comando | Descrição |
| --- | --- |
| `python3 scripts/seed_db.py --reset --samples` | Reseta e popula com dados de exemplo |
| `python3 scripts/export_db.py` | Exporta/backup do conteúdo do admin |
| `python3 scripts/create_user.py --username "email@..." --password "..."` | Cria usuário admin manualmente |
| `python3 scripts/import_from_site.py --reset` | Importa skills/currículo/portfólio do site em produção |

## Deploy

> Produção roda em **Docker no Easypanel** (VPS), usando o `Dockerfile`. Configure as variáveis do `.env.example` na aba *Ambiente* do serviço. Imagens enviadas pelo painel ficam salvas no MongoDB (coleção `uploads`, servidas em `/media/<id>`), então sobrevivem a qualquer redeploy sem precisar de volume.

### Alternativa: Vercel + MongoDB Atlas
1. Crie um cluster e um usuário no [MongoDB Atlas](https://www.mongodb.com/atlas).
2. Em *Project Settings → Environment Variables* do Vercel, configure:
   - `SECRET_KEY`, `EMAIL`, `SENHA`
   - `MONGO_URI=mongodb+srv://<user>:<pass>@<cluster>/portfolio_cv?retryWrites=true&w=majority`
   - `MONGO_DB=portfolio_cv`
3. Faça deploy (o `vercel.json` já está configurado).

> **Uploads:** imagens enviadas pelo painel (foto de perfil, fundo, portfólio) são gravadas no Mongo (coleção `uploads`), o que funciona igual em Docker e em serverless. Aceita PNG, JPG, WEBP e GIF até 8 MB (o tipo é validado pelos bytes do arquivo).
