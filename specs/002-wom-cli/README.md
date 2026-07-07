# Spec 002: `wom` CLI · SUPERSEDED, no implementar

Esta spec se **descartó** y se conserva solo como referencia histórica. El CLI
`wom` no se construye: su función la cubren los scripts deterministas del
preset (`writeonmars/scripts/status.py` y `close.py`), y la decisión de
arquitectura registrada (ver `CHANGELOG.md` § Obsoleto) fija **un único vector
de ejecución**: `specify preset add` + agente, sin CLI standalone.

Si estás buscando qué implementar, no es esto. El estado real del proyecto está
en `ROADMAP.md` y el preset vigente en `writeonmars/`.

(Banner añadido el 2026-07-04 para que el directorio completo no parezca una
feature viva.)
