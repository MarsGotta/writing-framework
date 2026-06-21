# Research (Phase 0) — Métodos en producción para generación long-form con citas

**Feature**: `003-atribucion-factualidad`
**Fecha de consulta**: 2026-06-21
**Alcance**: contrastar cómo se resuelve hoy, en producción y en la literatura reciente, la generación de texto largo fundamentado en fuentes, para fundamentar las decisiones de diseño de esta feature. No es un `research.md` editorial (no produce `CitationRecord` para una guía); es el research de ingeniería de la feature.

> Nota de método: las fuentes web se recogieron con búsqueda en junio 2026. Donde una afirmación es volátil (precios, versiones, números reportados por una empresa), se marca y se atribuye a su fuente; no se trata como verdad atemporal.

---

## 1. El patrón que se impuso en producción

La conclusión transversal de todas las fuentes es que la generación long-form "de una pasada" falla en factualidad, y que el patrón que funciona separa cuatro fases: **investigar → fundamentar (grounding) → escribir → verificar**. Write.OnMars ya implementa ese spine (`research` que bloquea el `plan` → `implement` → pasada 4 que verifica en vivo). La feature no cambia el patrón; cierra la brecha de **grano** (de capítulo a afirmación) y de **medición** (de "contar críticos" a "índice de factualidad").

---

## 2. Sistemas y técnicas contrastados

### 2.1 STORM / Co-STORM (Stanford OVAL)

Sistema que genera artículos largos tipo Wikipedia con citas, en dos etapas: pre-escritura (recolecta referencias + outline mediante *perspective-guided question asking* y *simulated conversation*) y escritura con citas. Publicado en NAACL 2024.

- **Hallazgo clave reutilizable**: las referencias se recogen **durante** la investigación y se mantiene un grafo de citación fundamentado; citar *durante* (no post-hoc) mejora drásticamente la precisión de las citas. → Valida el `research`-gated de Write.OnMars y refuerza persistir el vínculo afirmación↔fuente como artefacto (US1), en lugar de reconstruirlo al final.
- **Co-STORM** añade humano-en-el-bucle (interrumpir, dirigir) y un mapa mental dinámico. → Consistente con los dos checkpoints humanos del método.
- **Brecha que NO copiamos en v1**: la generación sistemática de amplitud (perspectivas) en la fase de research. Se anota como posible mejora futura del `research`, fuera del alcance de esta feature.

Fuentes: STORM (GitHub) — https://github.com/stanford-oval/storm · Proyecto STORM (Stanford) — https://storm-project.stanford.edu/research/storm/ · Co-STORM (cobertura) — https://www.edtechinnovationhub.com/news/pn7fo3f7xehe5gfj24mcjuntt7ormz

### 2.2 "Attribute First, then Generate" (locally-attributable grounded text generation)

Invierte el orden clásico: **content selection → sentence planning → generación condicionada al fragmento fuente**, de modo que la atribución es fina (a nivel de frase) **por construcción**, no por matching posterior. Reportan citas más concisas y mejor o igual calidad, reduciendo el tiempo de verificación humana, frente a enfoques post-hoc (que tienden a citar documentos/párrafos enteros y cargan al lector con la verificación).

- **Implicación de diseño**: el ideal es atribución a nivel de frase. v1 de la feature adopta la **mitad barata** (atribuir-y-persistir tras escribir, en `claims.md`) y deja el "attribute first" real (la Redactora selecciona fuente antes de escribir) como extensión, por su impacto en la voz/didáctica. La estructura `cita_fragmento_soporte` del `ClaimRecord` es justamente el fragmento fuente que este enfoque exige.

Fuentes: ACL 2024 — https://aclanthology.org/2024.acl-long.182/ · arXiv — https://arxiv.org/abs/2403.17104

### 2.3 Anthropic Citations API (productización del grounding a nivel de frase)

Funcionalidad de la API que chunkea los documentos fuente en frases y hace que el modelo cite la frase exacta que respalda cada afirmación de la salida. Disponible en la API de Anthropic, Vertex AI y Amazon Bedrock.

- **Dato de producción (volátil, atribuido)**: un cliente (Endex) reportó que las alucinaciones de fuente cayeron del 10% al 0% y las referencias por respuesta subieron ~20% tras integrar Citations. → Evidencia de que el grano de frase reduce alucinación medible.
- **Relación con la feature**: es la versión "infra" de lo que la pasada 4 hace por método. No la adoptamos como dependencia (rompería la neutralidad de modelo del Principio VI), pero confirma el objetivo: vínculo afirmación↔frase-fuente, no afirmación↔documento.

Fuentes: Anuncio — https://www.anthropic.com/news/introducing-citations-api · Docs — https://platform.claude.com/docs/en/build-with-claude/citations · Análisis (S. Willison) — https://simonwillison.net/2025/Jan/24/anthropics-new-citations-api/ · Bedrock — https://aws.amazon.com/about-aws/whats-new/2025/06/citations-api-pdf-claude-models-amazon-bedrock/

### 2.4 Evaluación de factualidad: FActScore, VeriScore, RARR

- **FActScore** (EMNLP 2023): descompone el texto largo en **afirmaciones atómicas** y verifica cada una contra una fuente (humano o modelo NLI). Métrica = afirmaciones soportadas / total. → Es exactamente el molde del índice de factualidad de US3. v1 usa el grano de afirmación que la pasada 4 ya produce (no descomposición sub-oracional pura); el refinamiento atómico es v2.
- **VeriScore**: evalúa la factualidad de afirmaciones **verificables** en texto largo, asumiendo que no todo es verificable (corrige el sesgo de SAFE, que extrae todo y penaliza de más). → Justifica que el denominador del índice sean solo las **afirmaciones verificables**, no toda frase (coherente con la heurística existente de `writeonmars-contraste` y con el edge case "afirmación no verificable").
- **RARR**: verificación posterior + **revisión automática** del texto cuando la fuente lo contradice. → Es conceptualmente lo que ya hace el bucle pasada 4 → `findings.md` → `revise`. La feature lo hace más fino (clasifica la relación) pero respeta el mismo "detector ≠ corrector".

Fuentes: FActScore (GitHub) — https://github.com/shmsw25/factscore · VeriScore — https://arxiv.org/html/2406.19276 · Survey de generación basada en evidencia (atribución/cita/quotation) — https://arxiv.org/html/2508.15396v1

### 2.5 Scite "smart citations" (relación de la cita)

Scite clasifica el contexto de cada cita en **supporting / contrasting / mentioning**, en lugar de tratar toda cita como equivalente. → Es el fundamento de US2: la `relacion` (`apoya`/`matiza`/`contradice`/`menciona`) es propiedad de la **arista** afirmación↔fuente, contextual, no de la fuente. Una fuente puede apoyar una afirmación y solo mencionar otra. Por eso el veredicto vive en `evidencia[]` del `ClaimRecord` y NO en el `CitationRecord`.

Fuente: comparativa de herramientas de investigación 2026 (incluye Scite smart citations) — https://www.iatrox.com/blog/best-ai-tools-medical-research-2026-elicit-consensus-semantic-scholar-perplexity

### 2.6 Tooling de usuario final (contexto, no dependencia)

Perplexity Pages, NotebookLM, Elicit y Scite forman el ecosistema de "informe largo con fuentes". NotebookLM **fundamenta solo en el corpus subido** (cero web abierta) → menos alucinación a costa de cobertura. Write.OnMars usa web abierta + `resources/` con contrato de citación: más flexible, más arriesgado **sin** grano fino — exactamente el riesgo que esta feature mitiga. No se adopta ninguna de estas herramientas como dependencia; se citan como evidencia de la dirección del mercado.

Fuente: ver 2.5.

### 2.7 Spec-driven development (contexto del harness)

GitHub Spec Kit (sobre el que corre Write.OnMars) es la herramienta spec-driven más adoptada en 2026, pero pensada para **código**. Extender spec-driven a producción **editorial** con contratos de citación y estado determinista en `scripts/` es lo distintivo de Write.OnMars; esta feature sigue esa misma filosofía (contrato nuevo + script determinista, no lógica acoplada al orquestador).

Fuentes: Spec Kit (GitHub) — https://github.com/github/spec-kit · Martin Fowler, comparativa SDD (Kiro/Spec Kit/Tessl) — https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html

---

## 3. Mapeo investigación → decisión de diseño

| Hallazgo (fuente) | Decisión en esta feature |
|---|---|
| Citar durante la investigación, no post-hoc (STORM) | Persistir el vínculo afirmación↔fuente como artefacto durable `claims.md` (US1), no reconstruirlo al export. |
| Atribución a nivel de frase reduce alucinación y coste de verificación (Attribute First; Citations API) | `ClaimRecord` por afirmación con `cita_fragmento_soporte` (frase exacta de la fuente). v1 atribuye tras escribir; inline-anchor queda como extensión. |
| Factualidad = soportadas / verificables (FActScore, VeriScore) | Índice de factualidad determinista en `status.py` (US3); denominador = afirmaciones verificables; `pendiente` no cuenta como soportada. |
| Verificación + revisión automática (RARR) | Reusar el bucle existente pasada 4 → `findings.md` → `revise`; no crear vía nueva (preserva "detector ≠ corrector"). |
| El valor de la cita depende de la relación, no de su presencia (Scite) | Enum `relacion` por arista en `evidencia[]`; gobierna la severidad (US2/FR-009). |
| Spec-driven determinista, no acoplado al orquestador (Spec Kit) | Juicio en la referencia agnóstica; conteo en `status.py`; cero APIs nuevas de Paperclip (US4). |

---

## 4. Dónde Write.OnMars ya iba por delante (y se conserva)

- **Voz y didáctica como ciudadanos de primera clase**: ninguno de los sistemas anteriores produce una voz de autora ni diseño de carga cognitiva (STORM = tono Wikipedia neutro; las APIs = respuestas fundamentadas). La feature NO toca esto.
- **Escribe-uno-revisa-otro con cross-model**: la separación Redactora ≠ revisores y voz ≠ precisión es más rigurosa que los pipelines de generación-con-citas revisados. Se preserva intacta.
- **Reproducibilidad por contrato + script determinista + constitución versionada**: la feature se suma a esta disciplina (nuevo contrato versionado + cómputo determinista), no la rompe.

## 5. Qué queda fuera (y por qué)

- **Attribute-First real** (selección de fuente previa a escribir): mayor cambio, riesgo para el diferencial de voz/didáctica. v2.
- **Descomposición atómica sub-oracional pura** (FActScore estricto): el grano de afirmación actual de `writeonmars-contraste` es suficiente para v1; atomizar es refinamiento posterior.
- **Clasificador NLI dedicado**: la relación la juzga el modelo de la pasada 4 (ya cross-model, con web), no un modelo clasificador separado; añadirlo es complejidad de infraestructura no justificada en v1.
- **Adoptar Citations API / NotebookLM como dependencia**: rompería la neutralidad de modelo (Principio VI). Se usan como evidencia de dirección, no como implementación.

---

## Fuentes

- Stanford STORM — https://github.com/stanford-oval/storm · https://storm-project.stanford.edu/research/storm/
- Co-STORM (cobertura) — https://www.edtechinnovationhub.com/news/pn7fo3f7xehe5gfj24mcjuntt7ormz
- Attribute First, then Generate (ACL 2024) — https://aclanthology.org/2024.acl-long.182/ · https://arxiv.org/abs/2403.17104
- Anthropic Citations API — https://www.anthropic.com/news/introducing-citations-api · https://platform.claude.com/docs/en/build-with-claude/citations · https://simonwillison.net/2025/Jan/24/anthropics-new-citations-api/ · https://aws.amazon.com/about-aws/whats-new/2025/06/citations-api-pdf-claude-models-amazon-bedrock/
- FActScore — https://github.com/shmsw25/factscore
- VeriScore — https://arxiv.org/html/2406.19276
- Survey de generación basada en evidencia — https://arxiv.org/html/2508.15396v1
- Tooling de investigación 2026 (Elicit/Consensus/Scite/Perplexity) — https://www.iatrox.com/blog/best-ai-tools-medical-research-2026-elicit-consensus-semantic-scholar-perplexity
- GitHub Spec Kit — https://github.com/github/spec-kit
- Martin Fowler, comparativa SDD — https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html
