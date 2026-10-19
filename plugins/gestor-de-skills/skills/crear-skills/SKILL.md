---
name: crear-skills
description: Diseña, estructura, documenta y prueba de forma estática skills propias reutilizables para tareas y proyectos; prepara SKILL.md, referencias, pruebas y control de versiones.
---
# Crear o mejorar skills propias

## Diseño
1. Extrae de la conversación el objetivo, disparadores de uso, entrada/salida, fuentes, errores anteriores y reglas de coste/privacidad. Evita preguntar lo que ya consta.
2. Comprueba skills y plugins existentes para no duplicar; diferencia entre instrucciones declarativas y capacidades reales de herramientas conectadas.
3. Genera un directorio `skills/nombre-claro/SKILL.md` con metadatos YAML válidos (`name` en minúsculas/guiones, `description` que explique cuándo usarla), pasos precisos, casos límite, condiciones de detención y salida verificable.
4. Mantén el SKILL.md breve; coloca listas de fuentes, plantillas o procedimientos largos en `references/` y menciona sus rutas desde el archivo principal.
5. Si requiere código, entrega propuesta y prueba estática primero; nunca ejecutes scripts de terceros sin autorización. Evita APIs pagadas, descargas con instalación forzada, tokens escritos en claro, claves en GitHub y tareas que puedan disparar consumo fuera de cuota.
6. Añade casos de prueba simples: caso habitual, resultado vacío, autenticación fallida, fuente inaccesible, dependencia no disponible, coste no verificable, resultados duplicados y rollback.
7. En ChatGPT/Plugin Creator, si el usuario pidió editar un plugin concreto y autorizó la modificación, conserva su identidad y actualiza archivos/versiones con comparación de publicación. En otros entornos prepara las instrucciones correspondientes, sin asumir instalación universal.
8. Verifica estructura y consistencia de fuentes; indica claramente qué pruebas se han ejecutado y cuáles quedan pendientes. Ninguna skill otorga por sí misma herramientas, credenciales ni acceso remoto.

## Reglas permanentes de coste
Presupuesto cero predeterminado. No usar funciones con tarifas por uso ni promociones consumibles sin verificar tarifa, saldo, coste estimado y autorización expresa para esa operación. Minimiza llamadas redundantes y reintentos; no sacrifiques exactitud o seguridad.

## Entrega
Propuesta, archivos o paquete autorizados, comportamiento, límites, pruebas, costes y siguiente acción concreta. Si el usuario solo pide un borrador, no instalarlo ni publicarlo.
