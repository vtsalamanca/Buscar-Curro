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
