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
# MongoDB local:
MONGO_URI=mongodb://localhost:27017
# Ou MongoDB Atlas (recomendado em produção):
# MONGO_URI=mongodb+srv://<user>:<pass>@<cluster>/portfolio_cv?retryWrites=true&w=majority
MONGO_DB=portfolio_cv
# Opcionais — usados no seed do usuário admin inicial
ADMIN_USER=isaias
ADMIN_PASS=troque-esta-senha
```

> `EMAIL`/`SENHA` são usados pelo Flask-Mail (formulário de contato). Use uma **senha de app** do Gmail, não a senha da conta.

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
2. Usuário/senha iniciais vêm das variáveis `ADMIN_USER` / `ADMIN_PASS` (padrões no `app.py`).
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

## Deploy (Vercel + MongoDB Atlas)
1. Crie um cluster e um usuário no [MongoDB Atlas](https://www.mongodb.com/atlas).
2. Em *Project Settings → Environment Variables* do Vercel, configure:
   - `SECRET_KEY`, `EMAIL`, `SENHA`
   - `MONGO_URI=mongodb+srv://<user>:<pass>@<cluster>/portfolio_cv?retryWrites=true&w=majority`
   - `MONGO_DB=portfolio_cv`
3. Faça deploy (o `vercel.json` já está configurado).

> **Uploads em serverless:** o sistema de arquivos do Vercel é somente-leitura. Imagens enviadas pelo painel (foto de perfil, fundo, portfólio) caem automaticamente em *fallback* e são armazenadas como data URI (`base64`) na coleção `settings`/`projects` do Mongo — nenhum volume externo é necessário.
