# Reloj de Ayuno

App web instalable (PWA) para hacer ayuno intermitente: temporizador, planes (16:8, 18:6, 20:4, OMAD…), historial editable, estadísticas con gráficas, registro de peso y sincronización opcional entre dispositivos con JSONBin.

- Se publica con GitHub Pages desde la rama `main` (carpeta raíz).
- El código fuente está en `src/app.html`. Tras editarlo, ejecuta `python3 src/build.py` para regenerar `index.html` y los iconos.
- La clave de JSONBin no está en el código: cada dispositivo la pide una vez en Ajustes y la guarda solo en ese navegador.
