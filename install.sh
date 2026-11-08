#!/usr/bin/env bash
# Instala a skill omnx-social-reaproveitar-conteudo no Claude Code copiando esta pasta para ~/.claude/skills/omnx-social-reaproveitar-conteudo.
# Funciona de qualquer lugar: o script acha a própria pasta. Rodar de novo atualiza a cópia.
set -euo pipefail
NOME="omnx-social-reaproveitar-conteudo"
ORIGEM="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESTINO="$HOME/.claude/skills/$NOME"
if [ "$ORIGEM" = "$DESTINO" ]; then
  echo "Esta pasta já é a cópia instalada. Rode o install.sh da pasta original."
  exit 0
fi
mkdir -p "$HOME/.claude/skills"
[ -L "$DESTINO" ] && rm "$DESTINO"
if command -v rsync >/dev/null 2>&1; then
  rsync -a --delete --exclude='.DS_Store' --exclude='__pycache__' --exclude='install.sh' "$ORIGEM/" "$DESTINO/"
else
  mkdir -p "$DESTINO"
  cp -R "$ORIGEM/." "$DESTINO/"
  rm -f "$DESTINO/install.sh" "$DESTINO/.DS_Store"
fi
echo "Skill $NOME instalada em $DESTINO"
echo "Abra uma conversa nova no Claude Code para ela aparecer."
