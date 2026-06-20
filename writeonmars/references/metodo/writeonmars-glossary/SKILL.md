---
name: writeonmars-glossary
description: Consolida el glosario del proyecto, detecta colisiones de definición y términos huérfanos. Trigger cuando la persona diga "consolida el glosario", "detecta términos huérfanos", "actualiza glossary.md", "valida la cobertura de glosario".
allowed-tools: Bash, Read, Write, Edit
---

# writeonmars-glossary

Skill que materializa FR-015, FR-021 y SC-004. Consume los anexos de
glosario emitidos por cada capítulo (bloque
`<!-- glossary-annex START/END -->`) y los `conceptos_introducidos` del
plan, los consolida en `specs/[###-feature]/glossary.md` (feature) y
`glossary.md` (proyecto-wide), detecta colisiones de definición entre
capítulos y términos huérfanos (técnicos en cuerpo expositivo sin entrada
en glosario).

## Cuándo dispararse

- "consolida el glosario"
- "detecta términos huérfanos"
- "actualiza glossary.md"
- "valida la cobertura de glosario"
- Tras cada redacción de capítulo, antes de la pasada 1.
- Antes de cerrar el proyecto (validación SC-004).

## Qué hace

1. Carga los `chapters/*.md` redactados y extrae:
   - El front-matter YAML (`terminos_introducidos`).
   - El bloque `<!-- glossary-annex START -->` …
     `<!-- glossary-annex END -->`.
2. Carga los `conceptos_introducidos` declarados en
   `## Descripciones encadenadas` del plan.
3. Compara términos entre capítulos:
   - Si el mismo término aparece con definiciones distintas en dos
     capítulos, marca colisión `severidad: critico` (FR-015).
   - Si un término del cuerpo aparece sin entrada en el anexo de
     glosario, marca como huérfano (`severidad: medio`, fix de SC-004).
4. Detecta anglicismos: si un término es marcado `anglicismo_admitido:
   true`, exige `justificacion` (constitución § IV).
5. Renderiza `specs/[###-feature]/glossary.md` siguiendo data-model.md §6
   y propaga al `glossary.md` raíz cuando la guía supera tres capítulos
   (estándar editorial de la constitución).
6. Emite reporte de colisiones, huérfanos y anglicismos sin justificar
   para que la pasada 1 o 5 los aborde.

## Inputs

- `chapters/[###]-titulo.md` (todos los capítulos disponibles).
- `specs/[###-feature]/plan.md` — descripciones encadenadas.
- `.specify/memory/constitution.md` — § IV.

## Outputs

- `specs/[###-feature]/glossary.md` (feature-scope).
- `glossary.md` (project-wide), si ≥ 4 capítulos.
- Reporte con colisiones, términos huérfanos y anglicismos sin
  justificar.

## Procedimiento

1. Recopilar todos los anexos `<!-- glossary-annex -->` de los
   capítulos. Indexar por término.
2. Para cada término con múltiples definiciones, comparar texto y
   reportar colisión cuando difieran semánticamente. Solicitar
   resolución antes de persistir.
3. Para cada capítulo, escanear cuerpo expositivo y comparar contra el
   glosario consolidado. Si encuentra un término técnico (heurística:
   sustantivo capitalizado o término que aparece en
   `conceptos_obligatorios` del brief) sin entrada en el glosario,
   emitir warning de huérfano.
4. Validar que cada `anglicismo_admitido: true` tenga `justificacion`
   apuntando a constitución § IV.
5. Renderizar el glosario consolidado en orden alfabético, con
   `capitulo_origen` indicado.
6. Si el proyecto tiene ≥ 4 capítulos, escribir también `glossary.md`
   en la raíz como vista de proyecto.

## Errores comunes

- Anexo de glosario malformado: la skill lo reporta y deja el término
  fuera del consolidado hasta que el operador lo corrija.
- Colisiones sin resolver: bloquean cierre vía
  `writeonmars-close-project` cuando el finding queda crítico abierto.
- Términos huérfanos: warning, no bloqueante por sí solo, pero la pasada
  5 lo escala.
- Anglicismos sin justificar: warning, exigir justificación en el
  glosario antes de pasada 5.

## Ingestión paralela y resolución de colisiones

Cuando `writeonmars-redaccion --parallel N` despacha varios capítulos
en simultáneo, los anexos `<!-- glossary-annex -->` aterrizan al mismo
tiempo. Esta sección describe cómo ingerir esos anexos y resolver las
colisiones que surjan, materializando el edge case de FR-015 declarado
en el spec.

### Detección

1. Indexa todos los anexos por término (case-fold + normalización
   básica de acentos para comparar formas equivalentes).
2. Para cada término con ≥ 2 definiciones (es decir, presente en ≥ 2
   capítulos), calcula la distancia léxica entre las definiciones:
   - Métrica: Levenshtein normalizado por longitud máxima.
   - Umbral por defecto: `0.3`. Distancia normalizada > 0.3 marca el
     término como `colision_critica`.
   - Distancia ≤ 0.3 se trata como variación menor (la skill consolida
     usando la primera definición y emite warning de bajo nivel para
     que el operador revise el matiz).
3. Verifica también divergencias estructurales (diferentes
   `categoria`, diferentes `anglicismo_admitido`, diferente
   `capitulo_origen` declarado): cualquiera marca colisión incluso si
   la distancia léxica es baja.

### Bloqueo

Las colisiones críticas suspenden la consolidación: la skill NO
escribe `glossary.md` (ni feature ni proyecto) hasta que el operador
resuelva. Esto cumple FR-015 (edge case "dos capítulos definen el
mismo término distinto en paralelo") declarado en el spec § Edge
Cases. Si la skill se invoca después de un piloto paralelo y detecta
colisiones, devuelve estado `bloqueado_por_colisiones` con la lista
detallada y aborta la escritura.

### Output

Cada colisión se registra como entrada en el bloque "Pasada 1 —
colisiones de glosario" en `findings.md`, con `severidad: critico` y
los siguientes campos:

- `termino`: forma canónica.
- `capitulo_origen_1`, `definicion_1`: capítulo y texto literal de la
  primera definición conflictiva.
- `capitulo_origen_2`, `definicion_2`: ídem segunda definición.
- `distancia_levenshtein`: valor normalizado calculado.
- `divergencias_estructurales`: lista de campos con valor distinto
  (`categoria`, `anglicismo_admitido`, etc.).
- `sugerencia_resolucion`: una de las cuatro estrategias de la
  siguiente subsección.

### Resolución asistida

La skill propone tres estrategias al operador, en este orden de
preferencia (siguiendo constitución § IV: univocidad del término):

a) **Elegir una definición**: marcar una como canónica, retirar la
otra del anexo del capítulo perdedor y reescribir la mención en cuerpo
si fuese necesario. Preserva univocidad. Default sugerido cuando la
definición canónica del proyecto está clara.

b) **Renombrar uno de los términos**: si los dos capítulos están
introduciendo conceptos genuinamente distintos que casualmente
comparten nombre, renombrar uno (p. ej. añadir calificador) y
documentar la decisión en `findings.md`. Preserva univocidad después
del renombre.

c) **Nota de "sentido en contexto X / sentido en contexto Y"**: último
recurso. Viola la regla de univocidad pero a veces es la única opción
honesta cuando el dominio impone homonimia. Se admite SOLO si:
- La colisión está auditada por el operador humano (firma humana
  obligatoria en el finding).
- Se registra como `desviacion_justificada` en el finding crítico.
- El glosario consolidado lleva ambas entradas explícitamente
  marcadas con su contexto.

Para cualquiera de las tres, la skill ofrece un patch sugerido
(diff) que el operador acepta o rechaza. Sin aceptación explícita, la
consolidación queda bloqueada.

### Reentry tras resolución

Una vez resuelto el conflicto (la entrada del finding pasa a
`resuelto` o `desviacion_justificada` con firma humana), invocar de
nuevo `writeonmars-glossary` reanuda la consolidación normalmente. Si
quedan colisiones críticas abiertas, sigue bloqueada.

## FR cubierta

- FR-015 (consolidación y detección de colisiones, incluido el edge
  case de ingestión paralela).
- FR-021 (estándar editorial de glosario obligatorio).
- SC-004 (cobertura del glosario y detección de huérfanos).
- Constitución § IV (anglicismos admitidos con justificación;
  univocidad del término).

## Versión

v0.2.0-mvp-2026-05-06 — añade ingestión paralela y resolución de
colisiones críticas (T064).
v0.1.0-mvp — 2026-05-06.
