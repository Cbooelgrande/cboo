#!/usr/bin/env python3
"""Cboo$$ — app de escritorio para el dashboard de finanzas.

La interfaz vive en app/web/ (lo único que se sirve, solo en 127.0.0.1).
Los datos se guardan en datos/finanzas.json (permisos 600) con respaldos diarios.
Se abre con ./iniciar.sh o desde el menú de aplicaciones.
"""
import datetime
import json
import os
import pathlib
import sys
import tempfile
import webbrowser

import webview

APP_DIR = pathlib.Path(__file__).resolve().parent
RAIZ = APP_DIR.parent
WEB = APP_DIR / 'web'
ICONO = APP_DIR / 'recursos' / 'icono.png'
DATOS = RAIZ / 'datos'
ARCHIVO = DATOS / 'finanzas.json'
RESPALDOS = DATOS / 'respaldos'
MAX_RESPALDOS = 60
MAX_BYTES = 50 * 1024 * 1024
URLS_PERMITIDAS = ('https://claude.ai/', 'https://github.com/')
# Puerto fijo: así el navegador interno recuerda la sincronización entre aperturas.
PUERTO = 48151


def _escribir_seguro(destino: pathlib.Path, texto: str) -> None:
    """Escribe a un temporal y lo reemplaza de golpe: nunca queda un archivo a medias."""
    destino.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=destino.parent, suffix='.tmp')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(texto)
            f.flush()
            os.fsync(f.fileno())
        os.chmod(tmp, 0o600)
        os.replace(tmp, destino)
    except BaseException:
        pathlib.Path(tmp).unlink(missing_ok=True)
        raise


class Api:
    """Funciones que el dashboard puede llamar. Solo estas, y con validación."""

    def load(self):
        return ARCHIVO.read_text('utf-8') if ARCHIVO.exists() else None

    def save(self, texto):
        try:
            if not isinstance(texto, str) or len(texto) > MAX_BYTES:
                return False
            datos = json.loads(texto)
            if not isinstance(datos, dict) or 'settings' not in datos:
                return False
            _escribir_seguro(ARCHIVO, texto)
            hoy = datetime.date.today().isoformat()
            _escribir_seguro(RESPALDOS / f'finanzas-{hoy}.json', texto)
            viejos = sorted(RESPALDOS.glob('finanzas-*.json'))[:-MAX_RESPALDOS]
            for v in viejos:
                v.unlink(missing_ok=True)
            return True
        except Exception as e:  # noqa: BLE001
            print('Error guardando:', e, file=sys.stderr)
            return False

    def exportar(self, texto):
        try:
            json.loads(texto)
            carpeta = next((p for p in (pathlib.Path.home() / 'Descargas', pathlib.Path.home() / 'Downloads') if p.is_dir()), pathlib.Path.home())
            destino = carpeta / f'cboo-respaldo-{datetime.date.today().isoformat()}.json'
            _escribir_seguro(destino, texto)
            return str(destino)
        except Exception:  # noqa: BLE001
            return None

    def abrir(self, url):
        if isinstance(url, str) and url.startswith(URLS_PERMITIDAS):
            webbrowser.open(url)
            return True
        return False


def main():
    # Crear la app de Qt antes que pywebview para que el sistema la reconozca como "Cboo$$"
    # (ícono y nombre propios en la barra de tareas, en vez de "python").
    from qtpy.QtWebEngineWidgets import QWebEngineView  # noqa: F401  (debe importarse antes de QApplication)
    from qtpy.QtWidgets import QApplication
    qapp = QApplication.instance() or QApplication(sys.argv)
    qapp.setApplicationName('Cboo$$')
    qapp.setDesktopFileName('cboo')

    DATOS.mkdir(mode=0o700, exist_ok=True)
    os.chmod(DATOS, 0o700)
    webview.create_window(
        'Cboo$$', str(WEB / 'index.html'), js_api=Api(),
        width=1340, height=920, min_size=(420, 600), background_color='#0d0d0d',
    )
    webview.start(gui='qt', private_mode=False, http_server=True, http_port=PUERTO, storage_path=str(DATOS / 'navegador'),
                  icon=str(ICONO), debug='--debug' in sys.argv)


if __name__ == '__main__':
    main()
