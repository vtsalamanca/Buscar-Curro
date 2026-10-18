# Buscar-Curro — Ampliación de fuentes ETT (ETT-01)

Fecha: 2026-10-18. Estado: inventario contrastado, **prueba runner y desarrollo pendientes**.

## Alcance autorizado
El usuario quiere ampliar fuentes de empleo con ETT de Toledo, especialmente Tratem y Adecco. No hay autorización para contratar servicios, iniciar sesión con datos privados, enviar candidaturas, activar programación periódica ni notificaciones.

## Fuentes
1. Tratem — https://agenciaempleo.tratem.com/ofertas/ — catálogo público con fecha, vacantes, localidad, estado y fichas.
2. Adecco — https://www.adecco.com/es-es/ofertas-trabajo/localizacion/trabajos-en-toledo — listado público; ejemplo «Coordinador/a de Transporte Escolar y Acompañantes (20h)», sin vigencia/requisitos todavía verificados.
3. Eurofirms — https://jobs.eurofirms.com/es/es/trabajo/toledo — listado provincial y filtros.
4. Randstad — https://www.randstad.es/candidatos/ofertas-empleo/p-toledo/ — localidad, fecha, sector.
5. Manpower — https://www.manpower.es/es/buscar-trabajo/ciudad/toledo/ — catálogo por localidad y fechas.
6. Gi Group — https://es.gigroup.com/ofertas-de-trabajo/castilla-la-mancha-re/toledo-pr/illescas-ci/ — ofertas por localidad.

Todas tienen **acceso a listados comprobado mediante lectura web**, no desde GitHub Actions. No declarar operativas aún.

## ETT-01A — Viabilidad técnica (Codex)
- Recuperar BT-01A/BT-01B y sus tests; conservar íntegro ATE y conectores anteriores.
- Añadir diagnóstico manual, público y acotado sobre seis fuentes con runner estándar público: respuesta real, enlazado de fichas, IDs, fechas, ubicaciones, requisitos, paginación y limitaciones JS.
- Diferenciar listado accesible de fichas realmente extraíbles; registrar 302/bloqueos de forma limpia y continuar.
- No autenticaciones, evasión de retos humanos, bucles intensivos, servicios externos tarificados ni cron.
- Pruebas/regresiones y evidencia reproducible en GitHub Actions.

## ETT-01B — Conectores viables
- Solo implementar las agencias probadas en ETT-01A, con límites de tiempo y tamaño.
- Añadir fuente/ETT/empresa contratante si identificada, ID/URL original, título, municipio, fecha, vigencia, requisitos, jornada, salario si explícito.
- Filtrar sectores activos: ATE, psicología no sanitaria, menores, discapacidad, educación e intervención social. Almacén/logística sigue suspendido; no ocultar un empleo social por palabras genéricas de menús de navegación.
- Distinguir ofertas de anuncios formativos y publicidad; respetar requisitos/habilitaciones y radio máximo 70 km desde Nambroca (no inventar distancias).
- Deduplicar entre agencias y otros portales conservando los enlaces de origen; no fusionar ofertas parecidas sin evidencia.
- Resolver previamente o en paralelo **persistencia entre ejecuciones de GitHub Actions**: BT-01B genera state.json pero su workflow manual no recupera estado anterior. Hacer pruebas de dos ejecuciones y verificar que la segunda no recuenta documentos como nuevos.
- No activar cron, notificaciones ni candidaturas; documentar rutas no viables y pendientes.

## Criterios de aceptación
- Pruebas unitarias y regresión anteriores correctas; ejecución runner válida con resultados por fuente.
- Estado anterior reproduciblemente cargado en segunda ejecución; delta real y errores diferenciados.
- Cero coste adicional, cero credenciales privadas, cero aplicaciones nuevas y ninguna candidatura.
- Actualizar ESTADO_PROYECTO.md, SOURCES_STATUS.md y PLAN_ETT_01.md; devolver commits y enlace de run.
