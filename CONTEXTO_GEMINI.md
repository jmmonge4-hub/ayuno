# Reloj de Ayuno: contexto completo del proyecto

> Documento autocontenido para que otro asistente de IA (p. ej. Gemini) pueda continuar el desarrollo sin más información. Refleja el estado del repositorio `jmmonge4-hub/ayuno` a 28 de noviembre de 2026 (último commit en `main`: `b87cc1d`).

---

## 1. Qué es

**Reloj de Ayuno** es una aplicación web instalable (PWA) en español para seguir el **ayuno intermitente**. Es de uso personal: la usa su autor (médico de familia en España) en el móvil y en el ordenador, con los datos sincronizados entre ambos.

- **En producción:** https://jmmonge4-hub.github.io/ayuno/ (GitHub Pages, rama `main`, carpeta raíz).
- **Sin backend propio, sin framework, sin dependencias de npm.** Todo es HTML + CSS + JavaScript vanilla en un único archivo.
- **Funciona sin conexión** gracias a un service worker.
- **Datos locales** en `localStorage`; sincronización **opcional** a través de **JSONBin.io** (API v3).
- Sección de **peso cifrada** con contraseña (Web Crypto: PBKDF2 + AES-GCM).

---

## 2. Funcionalidades

La interfaz tiene 4 pestañas (barra superior en escritorio, barra inferior en móvil ≤ 860 px).

### 2.1 Pestaña «Ayuno» (temporizador)
- **Anillo SVG** de progreso: azul (`--fast`) mientras se ayuna, verde (`--ok`) al cumplir el objetivo, ámbar (`--eat`) en la ventana de comida. Marcas en el anillo para las horas de cada etapa metabólica que caen antes del objetivo.
- Centro del anillo: tiempo transcurrido `hh:mm:ss`, porcentaje, «Faltan X» o «+X extra».
- Botón principal: **Empezar ayuno** / **Terminar ayuno**.
- Cajas de hora: **Inicio** (editable: se puede corregir la hora de inicio, no en el futuro) y **Objetivo** (editable: cambia las horas objetivo del ayuno en curso).
- Sin ayuno activo: muestra el tiempo desde el último ayuno, la ventana de comida restante (24 − horas del plan) y la hora sugerida del próximo ayuno.
- **Terminar ayuno** abre un modal con hora de fin editable, nota opcional (máx. 300 caracteres), y botones *Guardar*, *Seguir ayunando* y *Descartar*.
- **Planes** (botones): `13:11` Suave, `14:10` Inicio, `16:8` Clásico, `18:6` Avanzado, `20:4` Guerrero, `OMAD` (23 h) 1 comida, `36h` Monje, `libre` (horas personalizadas en Ajustes, 1–168 h).
- **Esta semana**: 7 casillas L–D, rellenas si se cumplió el objetivo ese día, semirrellenas si hubo ayuno sin llegar. Racha actual.
- **Qué pasa en tu cuerpo**: etapas orientativas (0 h digestión, 4 h bajada de azúcar, 12 h quema de grasa, 16 h cetosis ligera, 18 h cetosis, 24 h autofagia, 48 h hormona de crecimiento), con la etapa actual marcada «Ahora». Incluye aviso de que es orientativo y de consultar al médico.
- **Peso** (tarjeta al final de esta pestaña, protegida con contraseña). Ver sección 6.

### 2.2 Pestaña «Estadísticas»
- Selector de periodo: 7 días, 30 días, 90 días, 1 año.
- 8 tarjetas: nº de ayunos en el periodo, duración media, % objetivos cumplidos, ayuno más largo, racha actual, mejor racha, horas totales, nº total de ayunos.
- **Gráfica de barras** (SVG propio) de horas de ayuno por día, con línea discontinua del objetivo del plan actual. Tocar una barra muestra el detalle del día.
- **Media por día de la semana** (mini barras L–D).
- Regla: **las horas cuentan para el día en que termina el ayuno**. Un día está «cumplido» si algún ayuno que terminó ese día alcanzó su objetivo.
- Racha: días consecutivos cumplidos; si hoy aún no se ha cumplido, la racha sigue viva desde ayer.

### 2.3 Pestaña «Historial»
- Lista de ayunos agrupada por mes, de más reciente a más antiguo: fecha/hora inicio → fin, nota, insignia de objetivo (✓ si cumplido), duración en horas.
- **+ Añadir ayuno** manual (inicio, fin, objetivo, nota). Validaciones: fin > inicio, máximo 14 días, fin no en el futuro.
- Tocar un ayuno abre **Editar** (y **Eliminar**, con confirmación).

### 2.4 Pestaña «Ajustes»
- **Tema**: Auto / Claro / Oscuro.
- **Avisos**: notificación al alcanzar el objetivo (Notification API; usa `registration.showNotification` del service worker si existe) + vibración + toast.
- **Objetivo personalizado** (horas del plan «Libre»).
- **Tus datos**: exportar copia `.json` (descarga o copiar al portapapeles), importar copia (reemplaza los datos), borrar todo.
- **Sincronizar móvil y ordenador** (JSONBin): tipo de clave (Access Key o Master Key), clave, ID del bin; conectar, sincronizar ahora, copiar ID, desconectar.
- **Instalar en el móvil**: instrucciones para Android/iPhone y botón «Instalar ahora» si el navegador emite `beforeinstallprompt`. La tarjeta se oculta si la app ya está instalada (`display-mode: standalone`).

### 2.5 Otros detalles
- **Datos de ejemplo**: en la primera apertura se generan ~6 semanas de ayunos de demostración (marcados `demo: true`, generador pseudoaleatorio con semilla fija). Un banner avisa; se borran solos al empezar el primer ayuno real, al conectar la sincronización o con el botón «Borrar ejemplos».
- **Indicador de sincronización** en la barra superior (punto de color + texto: Sin sincronizar / Conectando / Sincronizando / Pendiente / Sincronizado / Sin subir / Sin conexión). Al tocarlo va a Ajustes y sincroniza.
- Se recuerda la última pestaña abierta (`localStorage['reloj-ayuno.v1.tab']`). También se puede abrir una pestaña con `#timer`, `#stats`, `#history`, `#settings`.
- Accesibilidad: roles `tablist`/`tab`/`tabpanel`, `aria-pressed` en segmentados, `aria-live` en el toast, foco visible, `prefers-reduced-motion`.

---

## 3. Arquitectura y estructura de archivos

```
ayuno/                      (repo GitHub, servido tal cual por GitHub Pages)
├── index.html              ← GENERADO por build.py (no editar a mano)
├── manifest.webmanifest    ← GENERADO por build.py
├── icon-192.png            ← GENERADO (PIL)
├── icon-512.png            ← GENERADO
├── icon-maskable-512.png   ← GENERADO
├── apple-touch-icon.png    ← GENERADO (180×180)
├── sw.js                   ← service worker (escrito a mano, NO lo genera build.py)
├── .nojekyll               ← evita el procesado Jekyll de Pages
├── README.md
├── CONTEXTO_GEMINI.md      ← este documento
└── src/
    ├── app.html            ← CÓDIGO FUENTE ÚNICO (~1250 líneas: <title>, fuentes, <style>, HTML del body y <script>)
    └── build.py            ← script de construcción
```

Existe además una copia de trabajo en la carpeta compartida del proyecto (`ayuno-app/src/`, `ayuno-app/dist/`, `ayuno-app/reloj-ayuno.zip`); el **repositorio es la fuente de verdad**.

### 3.1 `src/app.html`
Es un **fragmento**, no un documento completo. Contiene en este orden:
1. `<title>` y `<link>` a Google Fonts: **Bricolage Grotesque** (títulos), **Atkinson Hyperlegible** (texto), **DM Mono** (números).
2. Un `<style>` con todo el CSS (tokens en `:root`, modo oscuro por `prefers-color-scheme` y por `data-theme`).
3. El marcado del body: `header.topbar`, `main` con 4 `section.view`, `#modal-root`, `#toast`.
4. Un único `<script>` en IIFE con `'use strict'`.

### 3.2 `src/build.py` (Python 3 + Pillow)
- Lee `src/app.html`.
- Escribe en `dist/` si existe esa carpeta; si no, **en la raíz del repo** (que es el caso del repo).
- Genera `index.html` = cabecera fija (`<!doctype>`, `lang="es"`, metas viewport/`theme-color`/apple-mobile-web-app, `<link rel="manifest">`, iconos, un pequeño CSS de safe-area) + `app.html` partido: todo hasta `</style>` va en `<head>`, el resto en `<body>`.
- Genera `manifest.webmanifest`: `name` «Reloj de Ayuno», `short_name` «Ayuno», `lang` es, `start_url`/`scope` `./`, `display` standalone, `orientation` portrait, `background_color` `#eef1f6`, `theme_color` `#3346c9`, iconos 192, 512 y 512 maskable.
- Dibuja los iconos con PIL (fondo azul noche `#141b2d`, anillo con arco lila `#8d9bff` y punto ámbar central `#f2a650`), con superresolución ×4 y reducción LANCZOS.

Uso: `python3 src/build.py` desde la raíz del repo. (Regenerar los PNG puede cambiar bytes según la versión de Pillow aunque se vean iguales; no hace falta subirlos si no cambia el diseño.)

### 3.3 `sw.js` (service worker)
- Caché `reloj-ayuno-v2` con el «shell»: `./`, `index.html`, `manifest.webmanifest`, iconos.
- `install`: precarga el shell + `skipWaiting()`. `activate`: borra cachés antiguas + `clients.claim()`.
- `fetch` (solo GET):
  - Navegación: **red primero** (y actualiza `index.html` en caché), caché si no hay conexión. Así las actualizaciones llegan al abrir la app con conexión.
  - Resto del mismo origen: **caché primero**, red como respaldo (y se guarda).
  - Google Fonts: caché primero; si falla, respuesta vacía 504.
  - Las llamadas a JSONBin **no** pasan por la caché.
- `notificationclick`: enfoca una ventana abierta o abre `./`.
- Si se cambian archivos del shell distintos de `index.html` (iconos, manifest), conviene **subir la versión de `CACHE`** (`reloj-ayuno-v3`…).
- Se registra desde la app solo en `http(s)` (`navigator.serviceWorker.register('sw.js')`).

---

## 4. Lógica principal (JavaScript)

Todo dentro de una IIFE. Constantes: `KEY = 'reloj-ayuno.v1'`, `H` (ms por hora), `MIN`, `DAY`, `PLANS`, `STAGES`.

| Bloque | Funciones clave | Qué hace |
|---|---|---|
| Almacenamiento | `defaults()`, `load()`, `save(local)`, `tomb(id)`, `uid()` | Estado global `S`. `save()` escribe en localStorage y, salvo `save(true)`, llama a `Sync.schedule()` para subir cambios. `tomb` marca un id como borrado (lápida con timestamp). |
| Demo | `seedDemo()`, `hasDemo()`, `clearDemo()` | Datos de ejemplo. |
| Utilidades | `$`, `pad`, `ymd`, `dayStart`, `hms`, `dur`, `hShort`, `relDay`, `toLocalInput`/`fromLocalInput`, `esc`, `planHours`, `toast`, `fasts()` | Formato con `Intl.DateTimeFormat('es-ES')`. `esc` escapa HTML (las notas del usuario se escapan siempre). |
| Tema | `applyTheme()` | `data-theme` en `<html>` y actualiza `meta[name=theme-color]`. |
| Navegación | `show(v)`, `render()` | Muestra la vista y re-renderiza solo la visible. |
| Temporizador | `ringSVG()`, `renderTimer()` | Se repinta cada segundo con `setInterval` si la vista está activa. Lanza el aviso al cumplir el objetivo (`cur.notified`). |
| Estadísticas | `dayMap()`, `streaks()`, `renderStats()`, `drawDays()`, `capDay()` | Gráficas SVG generadas a mano, responsivas (se recalculan en `resize`). |
| Historial | `renderHistory()`, `editFast(f)` | Alta/edición/borrado. |
| Modales | `modal(html, onMount)`, `confirmBox()`, `goalOptions()` | Modal genérico con cierre por Escape, clic fuera o `[data-close]`. |
| Ayuno | `startFast()`, `editStart()`, `editGoal()`, `endFast()` | Cada cambio en el ayuno actual actualiza `S.curU`. |
| Avisos | `askNotif()`, `notifyGoal()` | |
| Copias | `exportData()`, `importData(text)` | Import valida y limpia; marca como borrados los ids antiguos que no vienen en la copia (para que la sincronización no los resucite). |
| Peso | módulo `Weight` | Ver sección 6. |
| Sincronización | módulo `Sync` | Ver sección 7. |
| Eventos | `bind()` | Todos los manejadores. |

Arranque: `load(); save(true); applyTheme(); bind(); show(pestaña); Weight.render(); Sync.run();` + temporizador de 1 s + registro del SW + escucha de cambio de esquema de color.

---

## 5. Modelo de datos

### 5.1 `localStorage`
| Clave | Contenido |
|---|---|
| `reloj-ayuno.v1` | Estado principal `S` (JSON). |
| `reloj-ayuno.v1.tab` | Última pestaña. |
| `reloj-ayuno.v1.sync` | Configuración de JSONBin `{ktype, key, bin}`. **Solo en ese dispositivo; nunca se exporta ni se sube.** |
| `reloj-ayuno.v1.dirty` | Timestamp de cambios locales pendientes de confirmar en el bin (0/ausente = nada pendiente). |

### 5.2 Estado `S`
```js
{
  v: 1,
  plan: '16:8',          // id de PLANS
  customH: 16,           // horas del plan 'libre'
  current: null | { start: <ms>, goal: <horas>, notified: <bool> },  // ayuno en curso
  curU: 0,               // timestamp de última modificación de `current` (LWW)
  prefsU: 0,             // timestamp de última modificación de plan/customH (LWW)
  deleted: { [id]: <ms> },   // lápidas de borrado (se purgan a los 365 días al sincronizar)
  fasts: [ { id, start, end, goal, note, u, demo? } ],  // ms epoch; goal en horas; u = última modificación
  weights: [],           // LEGADO: pesos en claro de versiones antiguas; se migran a wvault al crear contraseña
  wvault: null | { v:1, alg:'PBKDF2-SHA256/AES-GCM', iter:310000, salt:<b64>, iv:<b64>, ct:<b64> },
  wvaultU: 0,            // timestamp de la última escritura del vault (LWW)
  theme: 'auto' | 'light' | 'dark',   // NO se sincroniza
  notify: false,         // NO se sincroniza
  seeded: false
}
```

### 5.3 Contenido descifrado del vault de peso
```js
{ entries: [ { id, date: 'YYYY-MM-DD', kg: <número, 1 decimal>, u } ],
  deleted: { [id]: <ms> },
  heightCm: null | número, goalKg: null | número, prefU: <ms> }
```
Un registro por fecha (guardar otro el mismo día sustituye al anterior).

### 5.4 Copia de seguridad (exportación)
`{ app: 'reloj-ayuno', exportedAt: ISO, ...S }`. Incluye `wvault` cifrado (no la contraseña) y **nunca** la clave de JSONBin.

---

## 6. Sección de peso cifrada (módulo `Weight`)

- Al principio: «Protege tu peso con una contraseña» (mín. 4 caracteres, dos veces). Se genera `salt` aleatoria de 16 bytes, se deriva una clave AES-GCM 256 con **PBKDF2-SHA-256, 310 000 iteraciones**. Cada guardado cifra todo el objeto con un IV nuevo de 12 bytes.
- La **contraseña nunca se guarda**; la clave derivada vive solo en memoria mientras está desbloqueado. **Bloqueo automático** si la app pasa más de 5 min en segundo plano; botón «Bloquear».
- **Si se olvida la contraseña, los datos de peso se pierden** (botón «He olvidado la contraseña» borra el vault en todos los dispositivos).
- Desbloqueado muestra: peso actual, cambio total, últimos 30 días, ritmo (regresión lineal de las últimas 4 semanas, kg/semana), **IMC** con categoría (bajo peso < 18,5; normal < 25; sobrepeso < 30; obesidad), progreso hacia el peso objetivo con estimación de semanas.
- Gráfica de evolución (puntos + **media móvil de 7 días** + línea de objetivo) con rangos 1 mes, 3 meses, 1 año, todo.
- Lista de registros (6 últimos, ampliable) con diferencia respecto al anterior y borrado.
- «Altura y objetivo · Contraseña»: altura (cm), peso objetivo (kg), cambiar contraseña (genera nueva salt y recifra; el resto de dispositivos tendrán que desbloquear con la nueva).
- Sincronización: el vault viaja cifrado como un bloque con LWW por `wvaultU`. Si llega uno remoto más nuevo y este dispositivo está desbloqueado, `Weight.remoteChanged()` lo descifra y hace **merge por entrada** (`u` + lápidas), re-cifrando si el resultado difiere. Si no se puede descifrar (contraseña cambiada en otro dispositivo), se bloquea y se avisa.
- Requiere `crypto.subtle` (solo en contexto seguro https).

---

## 7. Sincronización con JSONBin (módulo `Sync`)

- API: `https://api.jsonbin.io/v3/b`. Cabecera `X-Access-Key` o `X-Master-Key` según el tipo elegido. Lecturas con `X-Bin-Meta: false`, `cache: 'no-store'`.
- **Conectar**: si el ID del bin está vacío, se crea un bin privado (`POST`, `X-Bin-Private: true`, `X-Bin-Name: reloj-ayuno`); si no, se valida que el bin existe y contiene datos de esta app. El campo del ID del bin viene **prerrellenado** en el HTML con el bin del autor.
- **Enlace de configuración**: abrir la app con `#k=CLAVE&b=BIN` (opcional `&t=master`) configura el dispositivo sin teclear y limpia el hash de la URL. El autor configura sus dispositivos con un enlace privado; **la clave nunca se incluye en el repositorio**.
- **Carga útil subida**: `{ app, v, savedAt, plan, customH, prefsU, current, curU, deleted, fasts (sin demo, ordenados por id), weights (vacío si hay vault), wvault, wvaultU }`.
- **Algoritmo de `run()`**: `GET latest` → `merge(remote)` → si el resultado canónico (sin `savedAt`, claves ordenadas) difiere del remoto → `PUT`. Tras un `PUT` se programa una **lectura de verificación a los 5 s**.
- **Reglas de merge**:
  - `fasts` (y `weights` legado): por `id`, gana el de mayor `u`; se descartan los que tengan lápida `deleted[id] >= u`.
  - `deleted`: unión, máximo por id; purga de lápidas de más de 365 días.
  - `current` (por `curU`), `plan`/`customH` (por `prefsU`), `wvault` (por `wvaultU`): **último que escribe gana**.
- **Cambios pendientes persistentes** (desde el PR #1, 24-11-2026): cada `save()` marca `dirty` en localStorage y programa subida a los **0,3 s**. `dirty` solo se limpia cuando una lectura posterior confirma que el bin coincide (JSONBin no tiene escrituras condicionales, así que otro dispositivo podría pisar una subida simultánea).
- **Disparadores**: cada 20 s con la app visible; `focus`, `online`, `pageshow` (bfcache), volver a primer plano. Al ocultar/cerrar (`visibilitychange` hidden, `pagehide`), si hay algo pendiente se sube con `fetch(..., {keepalive: true})` (límite ~64 KB). Antirrebote de 3 s para lecturas duplicadas. Reintento a los 30 s si falla.
- Errores traducidos: 401/403 clave inválida, 404 bin inexistente, 429 límite de peticiones, sin conexión.

---

## 8. Diseño visual

- Concepto: el anillo es el «cielo nocturno» del ayuno (azul índigo) y el ámbar marca la ventana de comida.
- Tokens CSS en `:root`: `--bg #eef1f6`, `--surface #fff`, `--ink #141b2d`, `--muted`, `--line`, `--fast #3346c9`, `--eat #c46f14`, `--ok #1d7f53`, `--danger #b42318` y variantes `-soft`; versiones oscuras (`--bg #0c111e`, `--fast #8d9bff`, `--eat #f2a650`…).
- Tema oscuro: automático con `@media (prefers-color-scheme: dark)` sobre `:root:not([data-theme="light"])`, y forzado con `:root[data-theme="dark"]`.
- Responsive: dos columnas en escritorio (máx. 1120 px); una columna y barra de pestañas fija inferior en ≤ 860 px; ajustes extra en ≤ 560 y ≤ 400 px. Respeta `safe-area-inset` (iPhone).
- Componentes: `.card`, `.tile`, `.btn` (`primary`, `eat`, `big`, `danger`, `ghost`, `sm`), `.seg`, `.badge`, `.plan`, `.stage`, `.overlay/.sheet` (modal), `.toast`.
- Sin librerías de gráficos: todos los gráficos son SVG generados con template strings.

---

## 9. Decisiones de diseño (y por qué)

1. **Un solo archivo HTML sin dependencias**: fácil de mantener, de desplegar en GitHub Pages y de previsualizar; carga rápida y funciona offline.
2. **localStorage primero**: la app funciona sin cuenta ni red; la sincronización es opcional.
3. **JSONBin** como «backend» gratuito y sin servidor propio. Al no tener escrituras condicionales, se compensa con merge por elemento, lápidas, LWW para campos escalares, verificación tras subir y la marca `dirty` persistente.
4. **La clave de JSONBin nunca está en el código ni en la copia de seguridad**: el repo es público.
5. **Peso cifrado de extremo a extremo**: es un dato de salud; ni JSONBin ni el repositorio pueden leerlo. Coste aceptado: si se olvida la contraseña, se pierde.
6. **Las horas cuentan el día en que termina el ayuno** (para gráficas, semana y rachas).
7. **Datos de ejemplo** para que la app no se vea vacía la primera vez; se eliminan solos.
8. **Texto sanitario prudente**: etapas metabólicas «orientativas» y recomendación de consultar al médico; ayunos ≥ 48 h «con supervisión».
9. Tema y avisos son preferencias **por dispositivo** (no se sincronizan).

---

## 10. Flujo de trabajo para hacer cambios

1. Editar **solo** `src/app.html` (y `sw.js` o `build.py` si procede).
2. Ejecutar `python3 src/build.py` en la raíz para regenerar `index.html` y `manifest.webmanifest`.
3. Probar localmente sirviendo la carpeta por http (p. ej. `python3 -m http.server`) para que funcione el service worker; `crypto.subtle` funciona en `localhost`.
4. Si cambian recursos del shell que no sean `index.html`, subir la versión de `CACHE` en `sw.js`.
5. Cambios a `main` mediante **pull request** (squash merge); GitHub Pages despliega automáticamente desde `main` (raíz).
6. Mantener la interfaz y los textos **en español** (es-ES).
7. **Nunca** escribir la clave de JSONBin en código, commits, issues ni documentación.
8. Mantener la compatibilidad del formato de datos (`v: 1`): los usuarios tienen datos guardados y sincronizados; cualquier campo nuevo debe tener valor por defecto en `defaults()` y tolerar su ausencia en el merge y en la importación.

---

## 11. Historial y estado actual

| Commit | Cambio |
|---|---|
| `b546c6f` | Primera versión: PWA de ayuno (temporizador, planes, historial, estadísticas, peso, export/import, JSONBin). |
| `389f0bd` | Luz verde de sincronización en la barra superior y enlace de configuración `#k=…&b=…`. |
| `e853a8d` | ID del bin prerrellenado. |
| `9ecd27d` | Sección de peso protegida con contraseña y cifrada; la tarjeta de peso sale de Estadísticas y pasa al final de la pestaña Ayuno. |
| `b87cc1d` (PR #1, 24-11-2026) | Sincronización fiable: cambios pendientes persistentes, verificación tras subir, subida a 0,3 s, flush con keepalive, sondeo cada 20 s, comparación canónica. |

**Estado:** estable y en uso en producción. No hay PR abiertos ni tareas a medias conocidas.

### Ideas o pendientes posibles (no comprometidos)
- Notificaciones con la app cerrada (hoy el aviso depende de que la app esté abierta o en segundo plano; haría falta Push API con servidor, o Notification Triggers, poco soportado).
- Recordatorio de inicio de ayuno / fin de ventana de comida.
- Exportar estadísticas o historial a CSV.
- Gráfica combinada ayuno + peso.
- Pruebas automáticas (hoy no hay tests; la lógica de `merge`, `streaks` y `dayMap` sería la primera candidata).
- Si el vault de peso crece mucho, `keepalive` deja de aplicarse por el límite de ~64 KB (ya contemplado en el código: hace la petición normal).

---

## 12. Cómo pedirle cambios a un asistente

Al pedir un cambio, conviene indicar: qué pestaña o función, el comportamiento deseado, y recordar las restricciones: **archivo único `src/app.html`, sin dependencias externas salvo Google Fonts, textos en español, no romper el formato de datos ni la sincronización, no exponer la clave de JSONBin, regenerar con `build.py`**.
