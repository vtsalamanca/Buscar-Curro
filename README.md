# Buscar-Curro

> **Estado operativo desde 26/10/2026:** código, pruebas y comparación con CV privado en Debian; búsquedas diarias en GitHub Actions Linux. Windows conserva VirtualBox, pero no tiene copia operativa del proyecto. El repositorio de Debian tiene ahora `.git` propio, independiente de la migración inicial. Véase [OPERACION_DEBIAN_2026-10-26.md](OPERACION_DEBIAN_2026-10-26.md).

Búsqueda personal de empleo y autenticación verificable. La consulta pública diaria está programada mediante `.github/workflows/daily-search.yml`; el acceso privado a InfoJobs desde Debian sigue pendiente de verificación.

BT-01A dispone de una prueba manual y acotada de viabilidad de fuentes públicas. BT-01B incorpora conectores públicos, normalización, filtros, seguimiento de cambios y deduplicación; su ejecución válida está en [GitHub Actions](https://github.com/vtsalamanca/Buscar-Curro/actions/runs/39165959658). Consultar `SOURCES_STATUS.md` para la matriz, evidencias y limitaciones. **Nota histórica (BT-01B):** ese flujo específico era manual; posteriormente se incorporó el workflow diario. No se realizan candidaturas automáticas.


## Mejoras BC-04/BC-05 (fase manual y reversible)
Se han incorporado límites de consumo, control de errores parciales, snapshots
locales verificables, restauración atómica y evaluación profesional más prudente.
El nuevo \`review-provisional.json\` es una vista técnica, **no** el informe final.
Véase [IMPLEMENTACION_BC04_BC05_2026-10-25.md](IMPLEMENTACION_BC04_BC05_2026-10-25.md).

Para revisar un snapshot offline:
\`\`\`bash
python3 state_snapshot_cli.py inspect --archive copia.snapshot.zip
\`\`\`
Los datos de colas no deben subirse a repositorios públicos. La retención de
Los artefactos temporales de los workflows históricos conservan retención limitada;
el flujo diario posterior mantiene resultados mínimos versionados en la rama
`buscar-curro-resultados`. No se presentan candidaturas automáticas.
Los 80 km geográficos son en línea recta.

## BC-06: descubrimiento oficial BOE por fecha
El nuevo conector manual run_boe_discovery.py consulta hasta siete sumarios diarios
oficiales, con XML validado, enlaces originales, histórico seguro y falsos
positivos contrastados. python3 run_boe_discovery.py --days 7 no solicita
candidaturas ni activa programación. Véase IMPLEMENTACION_BC06_BOE_2026-10-25.md.

## BC-06 DOCM: última edición oficial
Nuevo conector docm_latest.py + runner manual run_docm_latest.py con validador de sumario, NID, URL y fecha. El flujo docm-latest.yml no tiene cron. Se probó con 32 disposiciones de 23/10/2026; filtros conservadores sin coincidencias. Ver IMPLEMENTACION_BC06_DOCM_2026-10-25.md.

## Evaluación contra currículo privado (Debian)

El programa admite una revisión adicional **local y confidencial**, leyendo un PDF de CV
guardado fuera del repositorio público: `~/.local/share/buscar-curro/cv_actual.pdf`.
Con Python 3 y `pdftotext` disponibles en Debian:

```sh
python3 private_cv_review.py --refresh-public
```

Obtiene únicamente el histórico público de GitHub y deja el informe en
`~/.local/share/buscar-curro/revision_privada.json`. No transfiere el CV a GitHub
ni confirma vacantes por sí mismo. Consulta los límites y la arquitectura real en
[CV_PRIVADO_Y_LINUX_2026-10-26.md](CV_PRIVADO_Y_LINUX_2026-10-26.md).

## Acceso interactivo a InfoJobs desde Debian

Hay un lanzador que abre la página **oficial** de InfoJobs en Firefox con un
perfil persistente, separado y privado para que el titular pueda guardar su
contraseña en el gestor propio del navegador y reutilizar la sesión, sin entregar
credenciales a scripts ni a ChatGPT. Los desafíos 2FA siguen sujetos a InfoJobs. Menú de aplicaciones: «Buscar Curro - acceso InfoJobs».
También se puede ejecutar `python3 infojobs_acceso_local.py --abrir`.
**No implica lectura automática del buzón privado.**
Ver [ACCESO_INFOJOBS_DEBIAN_2026-10-26.md](ACCESO_INFOJOBS_DEBIAN_2026-10-26.md).

## Revisión privada de InfoJobs desde Debian

El procedimiento BC-13 permite consultar candidaturas desde el Firefox
autorizado, con informe local privado y acceso opcional al almacén GNOME
Keyring **solo cuando el navegador requiere iniciar sesión**. No reproduce
la API HTTP anterior. Ejecutar desde Debian:

```sh
python3 infojobs_consulta_debian.py --revisar
```

La consulta y sus limitaciones de autenticación se documentan en
[INTEGRACION_INFOJOBS_LLAVERO_DEBIAN_2026-10-27.md](INTEGRACION_INFOJOBS_LLAVERO_DEBIAN_2026-10-27.md).
No confundir la revisión local con el seguimiento automático ya programado
en ChatGPT/GitHub.


## Autorización oficial InfoJobs (BC-14)

Tras comprobar la documentación del proveedor, el camino correcto para
una aplicación propia es **InfoJobs Developers + OAuth 2.0**: la aplicación no
debe recopilar la contraseña personal. El lector Firefox mantiene consulta
de sesiones ya autorizadas; si expiran, solicita autorización oficial.
Preparada una aplicación local `infojobs_oauth_oficial.py --abrir` en Debian
para registrar un cliente, abrir consentimiento en la web de InfoJobs,
guardar el token OAuth en GNOME Keyring y consultar candidaturas mediante
GET de la API, sin enviar contraseñas a ChatGPT ni a GitHub.
**El acceso OAuth real requiere todavía registrar una aplicación en el
portal de desarrolladores y obtener Client ID/Secret. No se ha autenticado
con OAuth aún.** Ver
[OAUTH_INFOJOBS_OFICIAL_2026-10-27.md](OAUTH_INFOJOBS_OFICIAL_2026-10-27.md).
