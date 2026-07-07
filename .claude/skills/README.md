# Skills de este repo: dónde se edita cada cosa

Aviso para quien edite aquí. En esta carpeta conviven tres familias y solo una
se edita directamente:

1. **`writeonmars-*`**: copias compiladas para Claude de las referencias
   agnósticas del preset. **La fuente de verdad es
   `writeonmars/references/metodo/<mismo-nombre>/SKILL.md`**: edita allí y
   propaga aquí. Editar solo esta copia rompe el agnosticismo (los demás
   agentes leen las referencias del preset, no estas skills).
2. **`marcela-prose` y `technical-guide-design`**: skills bundled históricas de
   voz y didáctica. Su contenido agnóstico vive hoy en
   `writeonmars/references/voz/` y `writeonmars/references/didactica/`; misma
   regla, la referencia manda.
3. **`speckit-*`**: skills core de Spec Kit (y sus extensiones git). No son
   nuestras; se actualizan con Spec Kit, no a mano.

En un proyecto editorial instalado, la propagación la cubre
`/speckit-update` (smoke test: `tests/smoke/update-skill-on-installed-project.sh`).

(Nota del 2026-07-04, tras la auditoría de estructura del repo.)
