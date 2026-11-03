#!/usr/bin/env bash
# Quita Cboo$$ del menú y borra el entorno de Python. NO borra tus datos (carpeta datos/).
set -euo pipefail
RAIZ="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"
rm -f "$HOME/.local/share/applications/cboo.desktop" \
      "$HOME/.local/share/icons/hicolor/512x512/apps/cboo.png" \
      "$HOME/.local/share/icons/hicolor/scalable/apps/cboo.svg"
rm -rf "$RAIZ/.venv"
echo "✓ Desinstalado. Tus datos siguen en $RAIZ/datos"
