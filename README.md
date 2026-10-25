# Buscar-Curro
Búsqueda personal de empleo y autenticación verificable. Sin ejecuciones programadas activas.

BT-01A dispone de una prueba manual y acotada de viabilidad de fuentes públicas. BT-01B incorpora conectores públicos, normalización, filtros, seguimiento de cambios y deduplicación; su ejecución válida está en [GitHub Actions](https://github.com/vtsalamanca/Buscar-Curro/actions/runs/39165959658). Consultar `SOURCES_STATUS.md` para la matriz, evidencias y limitaciones. El flujo sigue siendo exclusivamente manual: no hay cron, candidaturas, autenticación privada ni notificaciones.


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
GitHub Actions sigue limitada a 30 días y no se ha activado ejecución diaria,
avisos ni candidaturas automáticas. Los 80 km geográficos son en línea recta.

## BC-06: descubrimiento oficial BOE por fecha
El nuevo conector manual run_boe_discovery.py consulta hasta siete sumarios diarios
oficiales, con XML validado, enlaces originales, histórico seguro y falsos
positivos contrastados. python3 run_boe_discovery.py --days 7 no solicita
candidaturas ni activa programación. Véase IMPLEMENTACION_BC06_BOE_2026-10-25.md.

## BC-06 DOCM: última edición oficial
Nuevo conector docm_latest.py + runner manual run_docm_latest.py con validador de sumario, NID, URL y fecha. El flujo docm-latest.yml no tiene cron. Se probó con 32 disposiciones de 23/10/2026; filtros conservadores sin coincidencias. Ver IMPLEMENTACION_BC06_DOCM_2026-10-25.md.
