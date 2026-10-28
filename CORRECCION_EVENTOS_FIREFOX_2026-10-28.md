# BC-17 — Corregir eventos de entrada en formularios Firefox (28/10/2026)

## Fallo reproducido

En el laboratorio Debian, `Atspi.EditableText.set_text_contents(...)`
devolvía una respuesta positiva, pero una página HTML local no recibía
los eventos de entrada esperados (`input`/`change`); en pruebas posteriores
se observó incluso que el texto no siempre aparecía en el campo. Por tanto,
no era válido interpretar el éxito de la llamada AT-SPI como acreditación de
que una web hubiera recibido los datos de un formulario.

Los intentos anteriores de rellenar InfoJobs desde el llavero y pulsar
«Iniciar sesión» quedaron sin autenticación confirmada. La causa exacta del
fallo real no está demostrada; el defecto de la escritura AT-SPI **sí**.

## Solución implementada

`input_eventos_firefox.py` introduce un controlador local de eventos
**X11/XTest** para Firefox, sin geckodriver, Selenium, WebDriver BiDi,
navegador modificado, copias de cookies, portapapeles ni servicios pagados.
No accede por sí mismo a ningún llavero.

La función `focus_and_fill(field, value, keyboard, window_id, x, y)`:

1. Comprueba rol de campo editable y que el valor sea válido.
2. Resuelve **antes de escribir** el mapa de caracteres del teclado X11.
   Por ahora solo admite ASCII imprimible compatible con el teclado activo;
   si encuentra otro carácter, falla antes de escribir datos reales.
3. Activa la ventana y pulsa la coordenada visible del campo identificada
   previamente por el cliente y sus comprobaciones de origen.
4. Escribe el carácter de prueba inocuo `z` y **verifica que aumentó
   el número de caracteres precisamente en ese campo**. Si no, aborta.
5. Selecciona y borra el contenido del campo mediante teclas normales;
   verifica que está vacío.
6. Teclea el valor mediante eventos nativos y comprueba longitud final.
   No pulsa «Iniciar sesión» ni transmite nada por red por sí misma.

La rutina no confía en el estado AT-SPI `FOCUSED` sin prueba de teclado,
porque en Firefox apareció incoherente con el caret visual. La validación
por cambio en el campo impide continuar si se ha seleccionado otro control.

## Verificación ejecutada

- 6 pruebas unitarias: valor sintético, centinela, abortar ante destino
  incorrecto, carácter incompatible, campos no permitidos y geometría.
- **Una prueba de integración con Firefox ESR 153.5.0esr real** en Debian,
  página HTML de origen `file://` con perfil temporal y texto ficticio.
  El campo terminó con la longitud correcta y su modelo de prueba reportó
  coincidencia **exacta del contenido**; se observaron `len(valor)+2`
  eventos `input`: centinela, borrado y caracteres finales.
- 169 pruebas Python del repositorio, correctas (1 test gráfico omitido
  por defecto y ejecutado expresamente por separado).
- 7 pruebas JavaScript correctas. `git diff --check` limpio.
- Sin contraseñas reales ni conexiones a InfoJobs durante la comprobación
  sintética. Firefox temporal se cerró en el `finally` de cada test.

Comando explícito para repetir la prueba gráfica en la sesión Debian:

```bash
cd /home/labgestor/proyectos/Buscar-Curro
BC_FIREFOX_X11_SMOKE=1 python3 -m unittest test_input_eventos_firefox_integration -q
```

No se ejecuta este test en los runners públicos de GitHub porque necesita
Firefox, X11 y el escritorio del propietario. La importación de `gi` se
mantiene dentro de la prueba gráfica y no se exige al ejecutar las pruebas
unitarias en un runner estándar.

## Límites y siguiente comprobación

- **Arreglado y comprobado:** los eventos de escritura de la entrada sintética
  que antes fallaban con `set_text_contents`. El código es reutilizable.
- **No conectado al login de producción:** el lector de candidaturas BC-16
  sigue siendo exclusivamente de lectura y no cambia. La rutina no decide
  coordenadas ni verifica URL por cuenta del cliente: esos controles deben
  formar parte de cualquier futura integración por portal.
- **Inicio de sesión real con llavero: pendiente.** Se intentó una única
  llamada para la prueba en un Firefox aislado de InfoJobs, pero los
  controles de seguridad de la herramienta la rechazaron antes de ejecutarse.
  **No se enviaron credenciales**, y no se debe eludir ese bloqueo.
- El modo headless ya se había comprobado como capacidad técnica, pero no
  resuelve por sí mismo el problema de eventos; no se instalaron geckodriver,
  Selenium ni navegadores «undetected».

Coste adicional **0 €**. No se han escrito contraseñas, datos de candidaturas,
cookies ni tokens en el repositorio.
