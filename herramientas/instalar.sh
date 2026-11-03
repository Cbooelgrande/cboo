#!/usr/bin/env bash
# Instala (o reinstala) Cboo$$: crea el entorno de Python y agrega la app al menú.
# No necesita sudo: todo queda dentro de ~/finanzas y ~/.local/share.
set -euo pipefail
RAIZ="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"
cd "$RAIZ"

if [ ! -x .venv/bin/python ]; then
  echo "→ Creando entorno de Python en .venv"
  if ! python3 -m venv .venv 2>/dev/null; then
    rm -rf .venv
    python3 -m venv --without-pip .venv
    .venv/bin/python /usr/lib/python3/dist-packages/pip install -q --upgrade pip setuptools wheel
  fi
fi
echo "→ Instalando dependencias"
.venv/bin/python -m pip install -q -r requirements.txt

echo "→ Agregando Cboo\$\$ al menú de aplicaciones"
mkdir -p "$HOME/.local/share/applications" "$HOME/.local/share/icons/hicolor/512x512/apps" "$HOME/.local/share/icons/hicolor/scalable/apps"
cp app/recursos/icono.png "$HOME/.local/share/icons/hicolor/512x512/apps/cboo.png"
cp app/recursos/icono.svg "$HOME/.local/share/icons/hicolor/scalable/apps/cboo.svg"
cat > "$HOME/.local/share/applications/cboo.desktop" <<DESK
[Desktop Entry]
Type=Application
Name=Cboo\$\$
Comment=Mis finanzas: sobres, gastos y coach
Exec=$RAIZ/iniciar.sh
Icon=cboo
Terminal=false
Categories=Office;Finance;
Keywords=finanzas;dinero;presupuesto;gastos;
StartupWMClass=cboo
DESK
update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true
chmod 700 datos 2>/dev/null || true
echo "✓ Listo. Busca \"Cboo\$\$\" en tus aplicaciones."
