# Modo paralelo de Write.OnMars

Documentación operativa del modo paralelo en redacción y contraste.
Cubre cuándo usarlo, cómo invocarlo, manejo de colisiones de glosario
y limitaciones conocidas.

Skills involucradas (todas v0.2.0-mvp-2026-05-06 o superior):

- `writeonmars-redaccion` — bandera `--parallel N`.
- `writeonmars-contraste` — dispatch paralelo por capítulo.
- `writeonmars-glossary` — ingestión paralela y resolución de
  colisiones críticas.

Audiencia: operadores humanos y agentes que orquestan la pipeline.

---

## 1. Cuándo usar paralelo

Tres criterios objetivos para que el modo paralelo compense el
overhead de dispatch:

1. **≥ 4 capítulos**. Por debajo de 4, el overhead de despacho
   suele igualar o superar la ganancia. Para 3 capítulos exactos,
   el modo serial es la opción default.
2. **Capítulos no fuertemente acoplados**. Las descripciones
   encadenadas (cap N → cap N+1) deben ser suaves: cada capítulo
   trae su propia promesa, ejemplo y checklist sin depender de
   artefactos generados en otro capítulo del mismo lote.
3. **Recursos disponibles**: cuotas, latencia y costo del modelo
   objetivo permiten N invocaciones concurrentes sin contención
   significativa.

Casos paradigmáticos donde paralelo gana:

- Guías de 6–10 capítulos cubriendo facetas independientes de un
  mismo dominio (cada cap = una faceta).
- Manuales con un patrón de capítulo idéntico (mismo molde
  pedagógico) repetido sobre diferentes objetos del dominio.
- Reediciones donde solo cambian los capítulos de la mitad final y
  se quiere paralelizar la nueva tanda contra la cuota de modelo.

## 2. Cuándo evitarlo

- **Bibliografía pequeña** (≤ 3 capítulos). Overhead > ganancia.
- **Dependencia secuencial fuerte**. Si el cap 3 referencia
  artefactos producidos en el cap 2 (por ejemplo, "como vimos en el
  ejemplo del checkout que cerró el capítulo anterior"), el modo
  paralelo introduce incoherencias. Solución: rediseñar las
  descripciones encadenadas para que la dependencia sea informativa
  (mencionar) y no estructural (depender de un artefacto generado).
- **Operador con control fino capítulo a capítulo**. Cuando se
  requiere revisión humana intermedia entre capítulos para corregir
  rumbo (capítulo 1 falla → no escribir cap 2 hasta arreglar), el
  serial es obligatorio.
- **Cuotas de modelo limitadas**. Si la cuota concurrente del
  modelo objetivo es 1, paralelo no aporta nada (los sub-agentes
  hacen cola).
- **Latencia anómala del modelo**. Si el wall-clock del modelo es
  altamente variable (algunos capítulos terminan en 5 min, otros
  en 25 min), el `max(T_caps_per_worker)` puede no compensar.

## 3. Cómo invocar

### Redacción paralela

```bash
# Default: serial.
writeonmars-redaccion redacta el capitulo 1

# Paralelo con 2 sub-agentes, todos los pendientes.
writeonmars-redaccion redacta los capitulos pendientes --parallel 2

# Paralelo con 4 sub-agentes (típico para guías de 8 caps).
writeonmars-redaccion redacta los capitulos pendientes --parallel 4
```

`N` debe estar entre 2 y 8. Sin la bandera, el modo serial se
preserva por compatibilidad histórica.

Mecánica del despacho:

1. Identifica los capítulos pendientes (sin archivo en `chapters/`).
2. Decide reparto round-robin: si pendientes ≤ N, cada sub-agente
   toma 1 capítulo; si pendientes > N, lotes secuenciales.
3. Despacha N sub-agentes en una única llamada concurrente
   (Claude Code Agent tool, varias invocaciones en un mensaje).
4. Cada sub-agente recibe el mismo prompt canónico
   (`agents/claude/prompts/redaccion.md`) y el mismo contexto
   compartido del lote. Solo el capítulo objetivo cambia.
5. Cada sub-agente escribe a su archivo `chapters/[###]-<slug>.md`.
   No hay shared writes ni mutación concurrente del glosario.

### Contraste paralelo (pasada 4)

`writeonmars-contraste` paraleliza por defecto cuando hay ≥ 4
capítulos. Para forzar serial:

```bash
writeonmars-contraste pasada 4 --serial
```

Mecánica:

1. Un sub-agente de contraste por capítulo.
2. Despacho concurrente en una llamada.
3. Cada sub-agente devuelve un fragmento del bloque "Pasada 4 —
   Capítulo N".
4. El orquestador concatena los fragmentos en `findings.md`,
   ordenados por número de capítulo.
5. Si dos capítulos citan la misma fuente (`citation_id` idéntico)
   con interpretaciones divergentes, surface una nota consolidada
   "Pasada 4 — global" con `severidad: medio` para que el operador
   humano decida en la firma.

## 4. Manejo de colisiones de glosario

`writeonmars-glossary` detecta colisiones cuando dos capítulos
introducen el mismo término con definiciones divergentes. Es el
caso edge declarado en FR-015 del spec.

### Detección

- Comparación lex de definiciones: Levenshtein normalizado por
  longitud máxima.
- Umbral default: `0.3`. Distancia > 0.3 marca colisión crítica.
- También se dispara colisión si difiere `categoria`,
  `anglicismo_admitido` u otros campos estructurales del anexo.

### Bloqueo

La consolidación se suspende. La skill NO escribe `glossary.md`
(ni feature ni proyecto) hasta que el operador resuelva.

### Resolución asistida (tres estrategias)

1. **Elegir una definición** (preferida; preserva univocidad).
   La skill propone retirar la definición perdedora del anexo del
   capítulo perdedor y reescribir la mención en cuerpo si fuese
   necesario.

2. **Renombrar uno de los términos** (cuando son conceptos
   genuinamente distintos que casualmente comparten nombre).
   La skill propone un calificador para uno de los dos.

3. **Nota de "sentido en contexto X / sentido en contexto Y"**
   (último recurso; viola univocidad estricta). Solo admisible si:
   - El operador humano firma el finding crítico.
   - Se registra como `desviacion_justificada`.
   - El glosario lleva ambas entradas con su contexto declarado.

Para cualquiera de las tres, la skill ofrece un patch sugerido
(diff) que el operador acepta o rechaza. Sin aceptación explícita,
la consolidación queda bloqueada.

### Ejemplo

Capítulo 2 introduce `mapa_mental_dominio` como "diagrama operativo
del flujo de negocio". Capítulo 5 introduce `mapa_mental_dominio`
como "checklist de los 12 conceptos del dominio". Levenshtein
normalizado entre las definiciones = 0.62 (> 0.3). Colisión
crítica. La skill bloquea, propone:

a) Elegir la definición de cap 2 (más alineada con event-storming);
   reescribir cap 5 para usar `checklist_dominio`.
b) Renombrar el de cap 5 a `checklist_dominio_corto`.
c) Anotar "sentido cap 2 (visual) / sentido cap 5 (auditoría)"
   con firma humana.

El operador elige (a). La skill aplica el patch y reanuda la
consolidación.

## 5. Limitaciones conocidas

1. **Variabilidad LLM**: dos invocaciones del mismo prompt al
   mismo modelo pueden producir capítulos con diferente número de
   findings por pasada. La equivalencia ±10% del SC-006 se
   considera el rango operativo aceptable; valores fuera del
   rango ameritan investigación.

2. **Overhead de dispatch**: el setup de N sub-agentes paralelos
   (envío de contexto, espera al primer token) tiene un costo
   fijo. Para capítulos cortos (< 5 min de generación), ese
   overhead puede empatar la ganancia. Threshold operativo:
   capítulos ≥ 10 min compensan claramente.

3. **Permutación de reparto**: round-robin default (caps
   intercalados entre workers) suele dar buenos resultados, pero
   permutaciones adversas (lotes contiguos cuando los caps
   tardíos son los más largos) reducen la ganancia. Si tienes
   visibilidad sobre tiempos por capítulo, fuerza reparto manual.

4. **Glosario consolidado entre lotes, no dentro**: los
   capítulos del mismo lote no ven los términos que introducen
   sus pares del mismo lote. La detección de colisiones se
   difiere a `writeonmars-glossary` tras el cierre del lote
   (FR-015 cubierto, pero con latencia). En guías densas en
   terminología compartida, considera `--parallel 2` (lotes
   pequeños) en lugar de `--parallel 4` (más colisiones
   posibles por lote).

5. **No hay paralelismo en pasadas 1, 2, 3, 5**: solo redacción y
   pasada 4 paralelizan. Las otras pasadas son rápidas y la
   coherencia global de la guía conviene revisarla en serie.

6. **Validación con sub-agentes reales pendiente**: la
   validación SC-006 actual usa modelado de wall-clock con
   tiempos derivados del piloto US2. Una validación con
   sub-agentes reales (con cuotas separadas) debería confirmar
   que el target del 40% se cumple en producción.

## 6. Referencia a evidencia

La validación de SC-006 vive en
`tests/editorial-pilot/evidence/2026-05-06-us3-parallel-validation/parallel-validation.md`.

Resultado: PASS — 42.9% reducción modelada (target ≥ 40%),
equivalencia ±10% en hallazgos críticos por pasada y cobertura de
glosario.

Ver también:

- `validation-report.md` (resumen SC).
- `pipeline-trace.md` (cronograma de alto nivel).
- `baseline-serial/` y `parallel/` (detalle por modo).
