# BC-06 — descubrimiento oficial BOE por fechas (25/10/2026)

**Estado:** implementación local verificada. Sin ejecución programada, autenticación, candidaturas ni APIs de pago.

## Funcionalidad
- Nueva vía independiente con **API oficial BOE** de datos abiertos: `GET https://www.boe.es/datosabiertos/api/boe/sumario/{YYYYMMDD}`, XML. No se incorpora captura de navegador, reintentos masivos ni inferencias de IA.
- `boe_discovery.py` filtra y valida URI oficial, esquema HTTPS y host, ID BOE y URL del documento, día real del sumario, tipo XML, hasta 1 MiB por día, timeout 15s, máximo 7 días por ejecución, rechazo de XML con DTD. Un HTTP404 queda separado de error de conectividad y no se interpreta automáticamente como ausencia de ofertas.
- Se consultan anuncios del sumario, sin descargar sus fichas completas; relevancia **preliminar por título y señales de convocatoria**. Reglas adversariales descartan premios, nombramientos, oposiciones universitarias genéricas y referencias de zonas remotas explícitas; no equivalen a análisis exhaustivo ni revisión de requisitos.
- `run_boe_discovery.py` guarda estado, delta, notas por día, lista y enlaces de documentos candidatos y vista provisional; distingue cambios en ejecuciones consecutivas con histórico válido.
- `.github/workflows/boe-discovery.yml`: **solo manual** mediante workflow_dispatch, estándar ubuntu-24.04, 12 minutos, lectura mínima, un único grupo compartido con otras búsquedas públicas, estado técnico 30 días, diagnósticos 7 días. Se restaura estado previo con validación; si caduca, se detiene sin simular «todos nuevos».
- Salida local excluida mediante `.gitignore`. Los archivos de resultados no se publican en el repositorio.

## Validación local y consulta real
- Suite completa sin red externa para pruebas unitarias: **92/92** correcta. Incluye BOE con títulos maliciosos, XML con DTD, fecha errónea, API fallida, 404, 7 días máximo y dos ejecuciones idénticas sin falsos nuevos.
- Acceso real BOE 24/10/2026: HTTP200, 193.408 bytes XML, 326 anuncios. Una primera versión del filtro incorporó erróneamente una plaza de cuerpos docentes universitarios en Jaén; se detectó, corrigió y agregó regresión.
- Semana 18–24/10/2026: seis ediciones consultadas (19–24), domingo 18 sin edición (404), **1.539 títulos examinados**. Filtro inicial generó siete títulos irrelevantes (nombramientos, premios, universidad Valladolid, otras comunidades); depurado antes de cierre. La segunda consulta real con filtro mejorado devolvió **0 candidatos por título**, 0 errores y sin falsos positivos observados en el informe. Esto NO demuestra ausencia de ofertas reales ni cobertura completa.
- `python3 -m compileall -q .` y `git diff --check` correctos en las pruebas de cierre.
- Fuentes oficial OpenAI no aplican; documentación BOE: https://www.boe.es/datosabiertos/api/api.php?lang=es.

## Límites pendientes
El sumario BOE es una **nueva fuente incremental**, NO sustituye el catálogo DOCM/BOP/JCCM ni el seguimiento ATE. No hay búsqueda por texto íntegro del BOE, extracción de requisitos/plazos a partir de las fichas, ni ampliación a otras fuentes BC-06. La comparación por fechas exige que se repita dentro de la ventana (7 días) y estado persistente adecuado. No está programada ninguna frecuencia. La selección de fuentes todavía es conservadora y puede descartar vacantes cuyo título no exprese claramente el rol; guardar pruebas adversariales y auditar resultados. Persistencia remota mayor a 30 días, facturación y formato del informe final siguen pendientes antes de BC-08.
