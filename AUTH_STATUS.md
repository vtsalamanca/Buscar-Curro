# Estado de autenticación

Comprobación del 18/10/2026. Repositorio público y ejecutores estándar gratuitos. Sin programación diaria activa.

| Servicio | Resultado real |
|---|---|
| ATE | Primera autenticación desde runner limpio confirmada, identidad y lectura privada verificadas. No garantiza persistencia futura. |
| InfoJobs | Adaptador implementado; página inicial devuelve HTTP 405 y señal CAPTCHA desde runner, antes de enviar credenciales. Acceso pendiente. |

Once pruebas sintéticas superadas. [Prueba conjunta](https://github.com/vtsalamanca/Buscar-Curro/actions/runs/39125415412). [Diagnóstico público sin credenciales](https://github.com/vtsalamanca/Buscar-Curro/actions/runs/39125527542).

Los valores de Secrets nunca se incluyen en el código ni resultados. No se guardan cookies, tokens, perfiles o HTML como artefactos. No se aceptan ofertas ni se envían candidaturas. Un diagnóstico que termina correctamente no demuestra acceso al servicio.

## Prueba con navegador estándar

[Chrome estándar en GitHub](https://github.com/vtsalamanca/Buscar-Curro/actions/runs/39125964900) también recibió HTTP 405. No aparecieron campos de acceso ni CAPTCHA visible. La referencia a CAPTCHA detectada anteriormente en el cuerpo HTTP no demuestra que haya un desafío visible o resoluble. Resultado: acceso no verificado; ninguna credencial de InfoJobs enviada. Sin stealth, proxies ni servicios tarificados.

## Causa del HTTP 405 identificada

[Diagnóstico del 18/10/2026](https://github.com/vtsalamanca/Buscar-Curro/actions/runs/39127957748): la respuesta pública contiene «¿Eres humano o un robot?» y explica que se ha detectado actividad poco habitual. Carga scripts de static.geetest.com. Es una verificación humana previa al acceso, no un rechazo de credenciales ni evidencia de método HTTP incorrecto. El navegador anterior no la mostró en pantalla; eso no invalida el contenido del documento recibido. No se han enviado contraseñas de InfoJobs ni resuelto desafíos.
