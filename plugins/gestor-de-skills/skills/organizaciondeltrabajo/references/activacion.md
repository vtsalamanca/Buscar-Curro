# Activación en ChatGPT y proyectos

1. Instalar/tener disponible la skill no garantiza que el sistema la invoque en cada conversación. La descripción de la skill debe identificar tareas no triviales que la requieren, con un disparador breve.
2. Añadir a las instrucciones personalizadas una regla breve que exija considerar `organizaciondeltrabajo` antes de iniciar o retomar trabajos no triviales. Se hace desde los ajustes de ChatGPT; esta skill no puede modificarlos.
3. Añadir referencia en las instrucciones de proyectos Educamos, Buscar-Curro y Subastas cuando el usuario autorice la edición. Reusar regla breve, sin copiar todo el documento.
4. Para trabajo técnico, aplicar también `ingenieria-fiable`; evitar imponer el protocolo en preguntas simples.
5. Validar en una conversación nueva y en un cambio de fase: comprobar que se recupera estado, selecciona herramienta, evita CI innecesario y respeta presupuesto cero. Si no se activa, reconocer limitación y ajustar instrucciones.

Texto breve recomendado: «Antes de iniciar o retomar tareas no triviales, aplica la metodología organizaciondeltrabajo: revisa el contexto, archivos y skills existentes; elige la opción fiable de menor coste total y esfuerzo manual; prioriza pruebas locales agrupadas; reserva GitHub Actions para integración y automatización; presupuestos adicionales cero salvo autorización expresa. Para trabajos técnicos usa ingenieria-fiable.»
