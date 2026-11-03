# 🔥 Cboo$$

App personal de finanzas: sobres con candado, quincenas, gastos con foto del comprobante y un coach que no perdona.
Todo corre en tu compu. Nada se sube a internet.

---

## 🚀 Abrir la app

- **Desde el menú de aplicaciones:** busca **Cboo$$**.
- **Desde la terminal:** `~/finanzas/iniciar.sh`

> Para fijarla en el dock: ábrela, clic derecho sobre el ícono → *Fijar / Pin*.

---

## 📁 Estructura

```
~/finanzas/
├── README.md              ← este archivo
├── iniciar.sh             ← abre la app
├── requirements.txt       ← librerías de Python (versiones fijas)
│
├── app/                   ← el programa (se puede reemplazar sin perder datos)
│   ├── main.py            ← ventana de escritorio + guardado en disco
│   ├── recursos/          ← ícono (svg y png)
│   └── web/
│       ├── index.html     ← todo el dashboard (diseño, gráficos, coach, lector)
│       └── vendor/        ← librerías locales: Chart.js y Tesseract (lector de comprobantes)
│
├── datos/                 ← 🔒 TUS DATOS (privado, solo tu usuario puede leerlo)
│   ├── finanzas.json      ← todo: salario, fijos, sobres, gastos, fotos
│   ├── respaldos/         ← copia automática diaria (se guardan los últimos 60 días)
│   └── navegador/         ← caché interna de la ventana (se puede borrar)
│
├── herramientas/
│   ├── instalar.sh        ← (re)instala la app y la agrega al menú
│   └── desinstalar.sh     ← la quita del menú (NO borra datos/)
│
├── archivo/               ← versiones viejas, solo de referencia
└── .venv/                 ← Python aislado de la app (no tocar; se recrea con instalar.sh)
```

**Regla de oro:** lo único irremplazable es `datos/`. Todo lo demás se puede reinstalar.

---

## 💡 Cómo funciona

### 1. Cada quincena (15 y último día del mes; si cae domingo, se paga el sábado)
1. **Primero se apartan los gastos fijos** (prioridad #1). Cada fijo se aparta en la 1ra, en la 2da o mitad y mitad.
2. **Lo que sobra se reparte en sobres** según tus %:

| Sobre | % por defecto | Estado |
|---|---|---|
| 🛟 Ahorro · Fondo de emergencia | 50% | 🔒 Bloqueado |
| 📈 Inversión | 30% | 🔒 Bloqueado |
| 💳 Gastos propios | 20% | Libre para gastar |

3. El día de pago tocas **🔒 Bloquear y repartir**. Desde ahí, **solo gastas de "Gastos propios"**.

> Cuando el fondo de emergencia llega a la meta (6 meses de gastos), su % se pasa solo a inversión.

### 2. Registrar gastos
- **📷 Escanear comprobante:** saca foto → la app lee total, fecha y comercio, y sugiere la categoría. **Siempre revisa antes de guardar.**
- **＋ Gasto:** a mano.
- **＋ Ingreso extra:** comisiones, se reparten solas en los sobres.
- **⇄ Mover plata:** pasar entre sobres, o meter/sacar plata (ej: ahorro que ya tenías).

### 3. 🤖 Coach (modo agresivo)
Te pone nota del 0 al 100 cada mes y te dice las cosas sin anestesia:

| Detecta | Nivel |
|---|---|
| Te pasaste del presupuesto de gastos propios | ⛔ Alerta |
| Sacaste plata de un sobre bloqueado | ⛔ Alerta |
| Vas gastando más rápido de lo que avanza el mes | ⚠️ / ⛔ |
| Más de 25% de tus gastos en salidas y compras | ⚠️ / ⛔ |
| 4 o más gastos hormiga (≤ ₡3 000) | ⚠️ / ⛔ |
| Gastaste más que el mes pasado en alguna categoría | ⚠️ Ojo |
| Quincena sin repartir (2+ días = alerta) | ⚠️ / ⛔ |
| Fijos sin pagar a final de mes | ⚠️ / ⛔ |
| Fondo de emergencia con menos de 1 mes | ⚠️ Ojo |
| Más de 70% del capital en cripto | ⚠️ Ojo |

**✨ Análisis a fondo con Claude:** copia un resumen de tu mes y abre claude.ai. Pegas con `Ctrl+V` y te da un análisis más a fondo.
⚠️ Al pegarlo, **sí compartes** ese resumen con Claude (ver Seguridad).

### 4. Editar (✏️)
Salario, valor de las criptos, meta del fondo, gastos fijos, % de cada sobre y sobres nuevos (✈️ viaje, 🚗 carro…).

---

## 💾 Respaldos

- **Automático:** cada día que usas la app se guarda una copia en `datos/respaldos/`.
- **Manual:** botón 💾 → *Descargar respaldo* → queda en `~/Downloads`.
- **Recomendado:** una vez al mes, copia `datos/` a una USB o a una nube **cifrada**.
- **Restaurar:** botón 💾 → *Importar respaldo* y elige el `.json`.

---

## 🛡️ Seguridad

**Lo que ya está protegido:**
- Los datos solo existen en `datos/`, con permisos `700/600` (otros usuarios de la compu no pueden leerlos).
- La app no se conecta a internet: los gráficos y el lector de comprobantes están en `app/web/vendor/`. Una regla de seguridad (CSP) le prohíbe a la página mandar datos a cualquier servidor.
- La ventana solo sirve la carpeta `app/web/`, en `127.0.0.1` (tu propia compu), nunca en la red.
- La app solo puede hacer 4 cosas en tu compu: cargar, guardar y exportar tus datos, y abrir `claude.ai`. Ninguna otra ruta ni página.
- Los textos que escribes se "escapan" para que no se puedan inyectar comandos.
- El archivo se guarda de forma atómica (si se va la luz, no queda a medias) y con copia diaria.

**Riesgos que quedan (y qué hacer):**

| Riesgo | Qué hacer |
|---|---|
| **Disco sin cifrar:** si te roban la compu o el disco, pueden leer `datos/`. | Usa cifrado de disco (Pop!_OS lo ofrece al instalar) y contraseña de usuario. |
| **Sesión abierta:** cualquiera que use tu compu desbloqueada puede abrir la app. | Bloquea la pantalla (`Super + Escape`) cuando te levantes. |
| **Respaldos sueltos:** el `.json` exportado trae TODO, incluidas las fotos de comprobantes. | No lo mandes por chat ni correo. Guárdalo en USB o en una nube con cifrado. |
| **"Análisis con Claude":** al pegar, tu resumen (salario, gastos, saldos) sale de tu compu. | Úsalo sabiéndolo. Si no quieres compartir montos exactos, edita el texto antes de mandarlo. |
| **Fotos de comprobantes:** pueden traer tu nombre, cédula o últimos dígitos de tarjeta. | Recórtalas si quieres, o no guardes la foto en compras sensibles. |
| **Programas maliciosos en tu usuario:** cualquier programa que corras con tu usuario puede leer tus archivos. | Instala software solo de fuentes confiables (Pop!_Shop, Flathub oficial). |
| **Actualizaciones:** las librerías de `.venv/` no se actualizan solas. | Cada tanto, sube las versiones en `requirements.txt` y corre `herramientas/instalar.sh`. |
| **El lector puede equivocarse** (ej: lee ₡46 895 en vez de ₡4 689,50). | Revisa siempre el monto antes de guardar. |

---

## 🔧 Problemas comunes

| Problema | Solución |
|---|---|
| No aparece en el menú | `~/finanzas/herramientas/instalar.sh` y cierra y vuelve a abrir sesión |
| No abre | Corre `~/finanzas/iniciar.sh` en la terminal y mira el error |
| Quiero ver la consola de desarrollo | `~/finanzas/iniciar.sh --debug` |
| Dañé los datos | Cierra la app, copia el archivo más reciente de `datos/respaldos/` a `datos/finanzas.json` |
| Moví la carpeta `finanzas` | Corre `herramientas/instalar.sh` de nuevo |

---

*Versión 3 · octubre 2026 · Moneda: colón costarricense (₡ CRC)*
