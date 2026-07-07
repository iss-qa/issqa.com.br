#!/usr/bin/env bash
#
# run_local.sh — sobe o portfólio localmente para visualizar as mudanças.
#
# Uso:
#   ./run_local.sh                # porta 5057 (procura a próxima livre se ocupada)
#   PORT=8000 ./run_local.sh      # tenta a partir da porta 8000
#   FLASK_DEBUG=0 ./run_local.sh  # desliga o auto-reload
#   NO_BROWSER=1 ./run_local.sh   # não abre o navegador automaticamente
#
# Ctrl+C para parar o servidor.
#
set -uo pipefail

# --- diretório do projeto (onde este script está) ---
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

HOST="${HOST:-127.0.0.1}"
WANT_PORT="${PORT:-5057}"
export FLASK_DEBUG="${FLASK_DEBUG:-1}"

# --- escolhe o Python (usa o venv do projeto se existir) ---
if [ -x "$PROJECT_DIR/venv/bin/python" ]; then
  PY="$PROJECT_DIR/venv/bin/python"
else
  PY="$(command -v python3 || command -v python || true)"
  if [ -z "$PY" ]; then
    echo "❌ Python não encontrado. Instale o Python 3 ou crie a venv: python3 -m venv venv"
    exit 1
  fi
  echo "⚠️  venv não encontrada; usando: $PY"
fi

# --- garante dependências instaladas ---
if ! "$PY" -c "import flask, pymongo, dotenv" >/dev/null 2>&1; then
  echo "📦 Instalando dependências (requirements.txt)..."
  "$PY" -m pip install -r requirements.txt || { echo "❌ Falha ao instalar dependências."; exit 1; }
fi

# --- acha uma porta livre a partir de WANT_PORT ---
port_in_use() { lsof -nP -iTCP:"$1" -sTCP:LISTEN >/dev/null 2>&1; }
PORT="$WANT_PORT"
for _ in $(seq 0 25); do
  port_in_use "$PORT" || break
  echo "⚠️  Porta $PORT ocupada, tentando $((PORT+1))..."
  PORT=$((PORT+1))
done
export HOST PORT
URL="http://$HOST:$PORT/#curriculo"

# --- avisos úteis ---
[ -f "$PROJECT_DIR/.env" ] || echo "⚠️  .env não encontrado — usará mongodb://localhost:27017 por padrão."

# --- abre o navegador só DEPOIS que o servidor responder de fato ---
if [ "${NO_BROWSER:-0}" != "1" ]; then
  (
    for _ in $(seq 1 60); do
      if curl -s -o /dev/null "http://$HOST:$PORT/" 2>/dev/null; then
        echo ""
        echo "✅ Servidor pronto! Abrindo o navegador em: $URL"
        if command -v open >/dev/null 2>&1; then open "$URL"
        elif command -v xdg-open >/dev/null 2>&1; then xdg-open "$URL"
        fi
        break
      fi
      sleep 0.5
    done
  ) &
fi

echo ""
echo "🚀 Subindo o portfólio (Ctrl+C para parar)"
echo "   Público:   http://$HOST:$PORT/"
echo "   Admin:     http://$HOST:$PORT/admin   (usuário: isaias)"
echo "   Currículo: $URL"
echo ""
echo "   Se o navegador mostrar 'conexão recusada', aguarde 1-2s e dê refresh (Cmd+R)."
echo ""

# --- sobe o servidor em primeiro plano ---
exec "$PY" app.py
