# Quickstart: primer uso de Write.OnMars

**Feature**: 001-framework-architecture | **Date**: 2026-05-06

Recorrido de extremo a extremo desde un repositorio Git vacío hasta producir el primer capítulo. Sirve a (a) operadores nuevos que instalan el framework por primera vez, (b) mantenedores que validan US1 y US2 manualmente y (c) la guía piloto editorial declarada en `research.md` § R6.

---

## Prerrequisitos

- Git ≥ 2.30
- Bash 5+
- Un agente compatible (v1: Claude Code)
- Acceso al repositorio canónico de Write.OnMars (clonado o disponible localmente)

Opcional para modo `bundled` (FR-009b):

- Python 3.11+ y dependencias declaradas en `mcp/writeonmars-research/pyproject.toml`

---

## Paso 1 — Crear el repositorio editorial

```bash
mkdir guia-onboarding-developers
cd guia-onboarding-developers
git init
```

Acceptance scenario cubierto: US1 §AC1 (precondición).

---

## Paso 2 — Instalar Write.OnMars

Desde el repositorio canónico del framework (asumiendo clone en `~/repos/writing-framework`):

```bash
bash ~/repos/writing-framework/install/install.sh \
  --target-dir "$(pwd)" \
  --agent claude-code \
  --language es
```

El instalador (FR-001):

1. Detecta si ya existe Spec Kit en el destino (FR-003); si existe, fusiona sin sobreescribir.
2. Copia las plantillas de Spec Kit (`.specify/templates/`) y la constitución actual (`.specify/memory/constitution.md`).
3. Copia las skills bundled a `.claude/skills/`: `marcela-prose`, `technical-guide-design`, `writeonmars-*`. Use `--symlink` si quieres enlaces para desarrollo local (R2).
4. Registra los hooks Git de Spec Kit (`before_specify`, `after_constitution`, etc.).
5. Lanza el cuestionario interactivo (FR-002):

   ```text
   Tipo de proyecto editorial: [guía | manual | libro | artículo]
   Agente prioritario: [claude-code | codex | cursor | other]
   Idioma primario: [es | en | other]
   Audiencia general (1 línea):
   Dominio técnico:
   ```

6. Genera `CLAUDE.md`/`AGENTS.md` con la audiencia, dominio y reglas microestilísticas heredadas (FR-007).
7. Crea `.writeonmars-manifest.json` validado contra `contracts/manifest-schema.json` con default v1 (`signing_matrix`: pasadas 1, 2, 5 autónomas; pasadas 3, 4 humanas).

Acceptance scenarios cubiertos: US1 §AC1, US1 §AC2, US1 §AC3.

**Tiempo objetivo**: < 5 minutos (SC-001).

---

## Paso 3 — Verificar la instalación

```bash
ls .claude/skills/                # debería listar marcela-prose, technical-guide-design, writeonmars-*
cat .writeonmars-manifest.json    # validar contra el schema
git status                        # detectar cambios sin commitear
```

Validar el manifiesto contra el JSON Schema (opcional pero recomendado):

```bash
ajv validate \
  -s ~/repos/writing-framework/contracts/manifest-schema.json \
  -d .writeonmars-manifest.json
```

---

## Paso 4 — Iniciar el primer proyecto editorial

```bash
/speckit-specify "Guía sobre onboarding técnico de developers en proyectos legacy"
```

La skill `writeonmars-brief` (envuelta en `/speckit-specify`) despliega el cuestionario del brief obligatorio (FR-005) cubriendo los nueve campos del Principio III. La spec se guarda en `specs/001-onboarding-developers/spec.md`.

Si quedan campos críticos con `[NEEDS CLARIFICATION]`, el sistema bloquea el avance (FR-006). Resolver con `/speckit-clarify`.

---

## Paso 5 — Investigación con fuentes

```bash
/speckit-plan
```

`writeonmars-research` (FR-008) orquesta sobre los MCPs disponibles según `manifest.research_mode`:

- `byom` (default): consulta los MCPs externos compatibles con el contrato de citación (`context7` para docs, web search, `fetch`). Cada cita registrada cumple `contracts/citation-contract.md` v1.0.
- `bundled`: usa `mcp/writeonmars-research/` como motor único.

Salida: `specs/001-onboarding-developers/research.md` con ≥ 1 fuente fechada por concepto obligatorio (SC-009).

---

## Paso 6 — Temario y descripciones encadenadas

Mismo `/speckit-plan` invoca `writeonmars-temario` (envuelve `/technical-guide-design`) y `writeonmars-descripciones`. Resultado: secciones "Temario" y "Descripciones encadenadas" añadidas a `plan.md` (FR-010).

Cada descripción declara: promesa, conexión con capítulo anterior, conexión con siguiente, ejemplo recurrente aplicado y conceptos del glosario que introduce.

---

## Paso 7 — Tareas

```bash
/speckit-tasks
```

`writeonmars-tasks` (futuro; v1 reutiliza `/speckit-tasks` con plantilla adaptada) descompone la producción en tareas alineadas con la estructura didáctica del Principio II (FR-012). Cada pasada del Principio V aparece como una tarea independiente y secuencialmente ordenada (FR-013).

---

## Paso 8 — Redacción capítulo a capítulo

```bash
/speckit-implement
```

Para cada capítulo del temario:

1. `writeonmars-redaccion` despacha un sub-agente (Agent tool de Claude Code) con: brief, temario, descripción del capítulo objetivo, descripciones contiguas, ejemplo recurrente y glosario consolidado (FR-014).
2. El sub-agente invoca `/technical-guide-design` para arquitectura del capítulo y `/marcela-prose` para voz y microestilo.
3. La salida llega como `chapters/[###]-titulo.md` con front-matter YAML según `data-model.md` § 7.
4. Términos nuevos se devuelven en un anexo y se consolidan en `glossary.md` (FR-015), detectando colisiones léxicas.

Acceptance scenario cubierto: US2 §AC1, §AC3.

---

## Paso 9 — Cinco pasadas de revisión

Para cada capítulo redactado, en orden estricto:

| Pasada | Skill | Sub-agente fresco | Firma default v1 |
|--------|-------|-------------------|------------------|
| 1 — Estructura | `/technical-guide-design` | sí | autónoma |
| 2 — Utilidad | `/technical-guide-design` | sí | autónoma |
| 3 — Naturalidad | `/marcela-prose` | sí | **humana** |
| 4 — Precisión | `writeonmars-contraste` | sí | **humana** |
| 5 — Formato | `writeonmars-pasada-5` | sí | autónoma |

Cada pasada produce un bloque en `findings.md` conforme al `pass-output-schema.md` v1.0 y una checklist firmable en `checklists/[###-feature]/pasada-N.md`.

Las pasadas 3 y 4 quedan en estado `blocked` hasta que un operador humano del manifiesto firme. Ningún hallazgo `critico` puede quedar `abierto` para cerrar el proyecto (FR-020 + FR-020a).

Acceptance scenarios cubiertos: US2 §AC4, §AC5, §AC6.

---

## Paso 10 — Cierre y publicación

Cuando todos los capítulos pasaron las cinco pasadas y `findings.md` está limpio, el operador genera los artefactos finales:

- `index.md` — ruta de lectura ordenada con enlaces (FR-029).
- `glossary.md` proyecto-wide.
- `common-errors.md` agregado.
- `templates/` con plantillas reutilizables extraídas durante la redacción.

```bash
git add chapters/ index.md glossary.md common-errors.md templates/ specs/001-onboarding-developers/
git commit -m "guide: onboarding-developers v1.0.0 — 5 pasadas firmadas"
```

v1 termina en markdown. Compilación a PDF/web/ePub queda fuera de scope (decisión Q5 → opción A).

---

## Validación de éxito (mapeo a Success Criteria)

| Criterio | Cómo se valida |
|----------|----------------|
| SC-001 (instalación <5 min) | Cronometrar pasos 1–3. |
| SC-002 (≤2 hallazgos críticos por capítulo en pasada 3, 0 en pasada 4) | Inspeccionar `findings.md`. |
| SC-003 (estructura didáctica 100% capítulos) | Verificar 9 secciones en cada `chapters/[###]-titulo.md`. |
| SC-004 (glosario 100% términos) | Diff de términos técnicos del cuerpo vs `glossary.md`. |
| SC-005 (ejemplo recurrente ≥80% capítulos) | Búsqueda del ejemplo en cada capítulo. |
| SC-009 (research.md fuente por concepto) | Cross-check `research.md` vs `conceptos_obligatorios` del brief. |

SC-006 (paralelización ≥40%) y SC-007 (portabilidad entre agentes) se validan en US3 y en una feature posterior, no en este quickstart.

---

## Resolución de problemas frecuentes

- **El manifiesto falla validación**: ejecutar `ajv validate` para localizar el campo. Comparar contra `contracts/manifest-schema.json`.
- **Una pasada queda en `blocked` por hallazgo crítico**: revisar `findings.md`, aplicar reescritura sugerida o documentar `desviacion_justificada` con firma humana.
- **Colisión léxica entre capítulos paralelos**: `writeonmars-glossary` reporta el conflicto en consola; reconciliar el término antes de cerrar.
- **MCP de investigación no compatible**: revisar `docs/compatibility-matrix.md`. Si tu MCP no aparece, verificar contra `contracts/citation-contract.md` y proponer entrada via PR.
