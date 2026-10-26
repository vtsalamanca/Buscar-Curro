# Buscar Curro — entorno operativo vigente (26/10/2026)

**Decisión del usuario:** Windows permanece como sistema operativo y anfitrión de VirtualBox. **Todo el desarrollo, las pruebas y la evaluación privada de Buscar Curro se realizan en Debian.** Los recolectores programados funcionan en runners Linux de GitHub Actions. No recrear carpetas operativas del proyecto en Windows.

## Ubicaciones verificadas

- Repositorio independiente: `/home/labgestor/proyectos/Buscar-Curro` con su propia carpeta `.git` (no enlaces a `mudanza-windows`); rama local `main` sincronizada con `origin/main`.
- Resultados Git de lectura: `/home/labgestor/proyectos/Buscar-Curro-resultados` (worktree asociado exclusivamente al Git del directorio anterior). Origen público: rama `buscar-curro-resultados` en GitHub.
- Currículo y evaluación privados: `~/.local/share/buscar-curro/cv_actual.pdf` y `revision_privada.json`, ambos permiso `600`, carpeta `700`. Nunca subirlos a GitHub.
- Uso en Debian: `cd /home/labgestor/proyectos/Buscar-Curro && python3 private_cv_review.py --refresh-public`.
- Búsqueda diaria: workflow público `.github/workflows/daily-search.yml` en GitHub Actions Linux; **no** lee el PDF privado. ChatGPT revisa Gmail y los resultados públicos mediante sus propias tareas.

## Retirada comprobada de Windows

- Eliminada la antigua carpeta `C:\Users\Usuario\Desktop\Buscar curro`, tras confirmar Git sin cambios y respaldar los 603 elementos en Debian.
- Copia ZIP/TAR antigua preservada en `/home/labgestor/proyectos/_gestion/respaldos-retirada-windows/Buscar-Curro-Windows-20261026.tar.gz`. SHA-256: `e85d04b6b32482262f0b6d025bb7611c36d9bfee5ef50cbb37c718b58eb7e913`.
- Retiradas referencias activas a Buscar Curro de `preparar_proyectos.py` y `ejecutar_pruebas.py` compartidos en Windows, sin afectar al resto.
- Reconstrucción Git: nuevo clon **sin hardlinks ni alternates** (`git clone --no-local`), HEAD y árbol comprobados, 124 pruebas Python satisfactorias y evaluación de 30 fichas desde Debian. Checkouts enlazados anteriores conservados temporalmente solo como respaldo dentro de Debian, sin participación en el repositorio actual.

## InfoJobs y aislamiento

- La sesión privada de InfoJobs validada anteriormente estaba en el navegador Chrome de Windows. **No forma parte del programa Linux**, ni está migrada. No trasladar cookies, contraseñas, perfiles ni códigos de seguridad.
- Al intentar el acceso público desde Debian el 26/10/2026, un cliente HTTP obtuvo `405` y el proxy restringido `403`. Estas respuestas **no prueban que la cuenta haya caducado**, solo que el acceso privado en Debian sigue sin verificar. No presentar la consulta de Gmail como equivalente al buzón interno de InfoJobs.
- Mantener intactos VirtualBox, las redes host-only/NAT existentes, SSH y el proxy de recuperación. La VM utiliza Windows como anfitrión, pero **el programa Buscar Curro no ejecuta código en Windows**. No se pide instalar Linux como sistema principal.
- Para usar el área privada de InfoJobs desde Linux se requiere un método legítimo de navegador y, si corresponde, un inicio de sesión interactivo del titular; no eludir CAPTCHA/2FA o restricciones de red.

## Prevalencia documental

Este archivo y la cabecera actualizada del `README.md` prevalecen sobre planes de 18–19 de octubre y apartados históricos del `ESTADO_PROYECTO.md` que mencionan el antiguo clon Windows o un cron todavía no activado. Las referencias antiguas se conservan únicamente como relato histórico y no son instrucciones vigentes.

**Presupuesto adicional autorizado:** 0 €.

## Añadido: login interactivo InfoJobs en Debian

Se incorporó `infojobs_acceso_local.py` y un lanzador local de Firefox.
Abre la web oficial en ventana privada para que el titular introduzca sus
credenciales y el código 2FA **directamente en InfoJobs**. No se recuperan
cookies ni contraseñas de Windows, ni se ha verificado acceso privado desde
Linux. Detalles y límites: [ACCESO_INFOJOBS_DEBIAN_2026-10-26.md](ACCESO_INFOJOBS_DEBIAN_2026-10-26.md).
