#!/usr/bin/env bash
# Abre la app Cboo$$. Uso: ./iniciar.sh   (agrega --debug para ver la consola de desarrollo)
cd "$(dirname "$(readlink -f "$0")")" || exit 1
exec ./.venv/bin/python app/main.py "$@"
