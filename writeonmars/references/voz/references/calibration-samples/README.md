# Calibration samples — protocolo

Cuatro pares de archivos, uno por modalidad Diátaxis, para calibrar la voz de Marcela con evidencia (no solo con reglas declarativas).

## Cada par

- `<modalidad>-01-antes.md` — texto en prosa "limpia genérica humanizada". Pasa los filtros básicos (no tiene em-dash en cadena, ni regla de tres decorativa, ni "let's dive in"), pero le falta la voz autoral propia.
- `<modalidad>-01-despues.md` — el mismo texto editado por Marcela a su voz.

## Convención

- Mismo título, mismo dominio temático, mismo registro Diátaxis.
- Marcela puede crear `-despues.md` desde cero copiando el `-antes.md` y editándolo.
- Marcela puede dejar `-despues.md` con cualquier longitud (puede acortar, expandir, partir párrafos, fundir).
- Si Marcela considera que algún `-antes.md` no representa el caso límite que quería editar, puede pedir uno nuevo o reescribirlo ella.

## Cómo se procesan

Cuando los 4 pares estén completos, Claude (en una sesión nueva) hace `diff` semántico de cada par y nombra los moves recurrentes:

- Sustituciones léxicas: "X → Y" (cuando ocurre 2+ veces en distintos pares).
- Movimientos sintácticos: "rompe frase >40 palabras en 2 frases", "fusiona 3 frases cortas con punto y coma".
- Movimientos retóricos: "abre con escena, no con tesis", "cierra con pregunta abierta, no con resumen".
- Inserciones de voz: "añade paréntesis honesto", "introduce 'mi sospecha' como confesión costosa".
- Cambios de registro: "baja conector culto a casual".

Cada move recurrente entra en `references/calibration-digest.md`. Si un move solo aparece una vez, no entra (regla del PLAN: "cada delta cabe en una línea").

El digest alimenta una sección "Evidencia de voz" en `SKILL.md` (Fase 2 v2).

## Tema y alcance

Los 4 samples cubren temas cercanos al dominio actual de Marcela (IA, agentes, prompts, harness). Son cortos (300-500 palabras antes de editar) para que la edición sea rápida y honesta. Ninguno es perfecto: cada uno tiene patrones identificables que su voz tendería a tocar.
