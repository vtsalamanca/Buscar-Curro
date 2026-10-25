# BC-06 ampliación DOCM — Implementación (25/10/2026)

**Resultado:** Nuevo conector del **último sumario del DOCM**, mantenido separado de las búsquedas históricas oficiales previas.

## Mecánica sin servicios de pago
- URL oficial `https://docm.jccm.es/docm/`; una petición HTTP/HTML permitida por ejecución, con HTTPS y host fijo, límite 1 MiB y 15 segundos.
- Se capturan `p.sumario`, texto del anuncio, NID y enlace PDF **realmente presente** en la página, validando fecha, ruta e identificador. Si cambió la estructura, fecha es futura, página tiene más de 10 días o mezcla fechas, se devuelve fallo explícito.
- Filtro conservador por ámbito profesional y actos de empleo; no trata premios o subvenciones como vacantes, ni presume que una mención a discapacidad implique un trabajo de atención personal.
- Los documentos son **candidatos por título**, no ofertas confirmadas. No se descargan PDF ni se infieren requisitos, plazos ni kilometraje.
- Nuevo programa `run_docm_latest.py` con histórico/delta local y enlace del NID; workflow `.github/workflows/docm-latest.yml` exclusivamente `workflow_dispatch`, 12 min estándar, permisos de lectura, grupo compartido con otros flujos, continuidad mediante artefacto 30 días, diagnóstico 7 días. Sin calendario ni candidaturas.
- Salidas `docm-output*/` excluidas del repositorio público.

## Prueba real y límites
- Fuente DOCM accesible desde Debian: HTTP 200, HTML ~73.888 bytes. Última publicación visible: **23/10/2026**.
- Parser validó **32 disposiciones**, 0 NID inválidos, **0 candidatos** tras el filtro profesional. No es una comprobación de días anteriores, ni prueba ausencia de vacantes; para vigilar períodos sin perder publicaciones falta barrido por fecha y persistencia que no caduque.
- 10 pruebas nuevas del DOCM y sus pipelines, hasta **102/102** pruebas de toda la suite locales superadas. Sintaxis Python y `git diff --check` correctos.
- Documento base oficial del diario: https://docm.jccm.es/docm/
- No se ha verificado ejecución remota en GitHub Actions de este nuevo flujo. Mantener manual.

## Próximas dependencias
Restan BOP Toledo, Empleo CLM y otras entidades, más el detalle documental de convocatoria, informes finales a consensuar, persistencia duradera >30 días, permisos y facturación antes del cron diario. **No activar automatización de calendario ni pagos.**
