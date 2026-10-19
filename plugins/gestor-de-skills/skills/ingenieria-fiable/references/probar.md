# Pruebas proporcionadas y reproducibles

## Ciclo de cambio
1. Identificar una conducta observable y, cuando sea viable, crear una prueba que falle por la ausencia del comportamiento requerido (**rojo**).
2. Introducir el cambio mínimo dirigido a esa conducta (**verde**); ejecutar la prueba de nuevo y, si existe, la suite general.
3. Simplificar código sin alterar el comportamiento, comprobar regresiones y conservar los registros (**refactorizar**).
4. Si no se puede ejecutar ninguna prueba real, limitar la afirmación a validación estática o propuesta; no simular ejecuciones ni resultados.

## Casos mínimos para colectores de empleo y automatizaciones
- Resultados vacíos reales frente a un fallo de acceso: no confundirlos.
- Duplicados: misma oferta con URL distinta o cambios de título, cotejar ID y empleador.
- Vigencia: distinguir publicación nueva, fecha indexada, caducidad y plazo oficial.
- Requisitos: excluir o advertir habilitaciones obligatorias no acreditadas sin inventar equivalencias.
- Ubicación: radio y distancia por carretera son magnitudes distintas.
- Autenticación: sesión expirada, CAPTCHA y denegación de acceso detienen acciones privadas sin filtrar secretos.
- Fuente caída o respuesta parcial: usar alternativa y consignar hueco de cobertura.
- Costes: si servicio/runner/API podría cobrar o su tarifa es desconocida, la ejecución se bloquea hasta aprobación explícita.
- Historial: una nueva ejecución no envía candidaturas duplicadas ni reporta anuncios conocidos como nuevos.
- Persistencia: un guardado requiere relectura o confirmación de escritura; un intento no acredita éxito.
- Entrega: generar contenido no demuestra notificación móvil recibida.

Preferir fixtures sintéticas, datos públicos estables, validadores locales y tests del propio proyecto. No usar cuentas reales ni lanzar tareas pagables para «probar por probar».
