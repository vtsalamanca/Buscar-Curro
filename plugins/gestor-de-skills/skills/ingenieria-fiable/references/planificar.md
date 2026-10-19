# Planificar un cambio técnico sin burocracia innecesaria

1. Extraer objetivo, plataforma, fuentes existentes y preferencias confirmadas; recuperar versiones, pruebas anteriores y fallos antes de proponer algo nuevo.
2. Separar requisitos esenciales, exclusiones expresas, límites (coste 0 €, acceso, permisos, tiempo, datos) y hechos aún no verificados.
3. Definir criterios de aceptación observables. Ejemplos: «10 ofertas de prueba -> 8 únicas con el identificador correcto», «un portal inaccesible queda PARCIAL y se consulta la alternativa», «ninguna ejecución programada se activa sin autorización y revisión de facturación».
4. Seleccionar arquitectura mínima y reversible; evitar instalar nuevas dependencias si las capacidades existentes bastan. En GitHub Actions, el workflow, el script, el histórico y la entrega son piezas separadas; no prometer que un SKILL.md sustituye un workflow.
5. Ordenar entregables en bloques cortos: primero lectura y diseño, luego pruebas controladas, cambio mínimo, verificación y, si está autorizado, publicación.
6. Para cada bloque registrar entrada, resultado esperado, evidencia de aprobación y recuperación ante fallo. No delegar en subagentes por defecto; usarlos solo si están disponibles, encajan y no tienen coste no autorizado.
7. Ante ambigüedad no esencial, adoptar una opción segura y reversible, identificándola como decisión técnica; pedir aprobación solamente en los límites de autorización que lo requieran.

Mini ficha: Objetivo | Situación previa | Alcance | No hacer | Criterios de aceptación | Dependencias/permisos | Coste y cuota | Pruebas | Reversión.
