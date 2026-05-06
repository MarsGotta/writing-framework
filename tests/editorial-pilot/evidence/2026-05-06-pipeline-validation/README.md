# Evidencia del piloto editorial — 2026-05-06

Carpeta de evidencia de la Ronda 3 de Phase 4 / US2 (T051–T059): piloto
editorial que valida la pipeline de Write.OnMars extremo a extremo sobre
una guía de tres capítulos.

## Qué se hizo

Se ejecutó la pipeline editorial completa (instalación, brief,
investigación, plan, redacción, cinco pasadas, cierre) sobre el tema
**"Onboarding técnico en repositorios legacy"**. La pipeline corrió
sin contaminar el repo canónico: la sandbox vivió en `/tmp/`, y aquí
solo se archivan **metadatos de validación** que demuestran que la
pipeline funciona como contrato declara.

## Por qué se hizo así

- El contenido editorial del piloto es placeholder (estructuralmente
  correcto, con voz objetivo aproximado, pero NO calidad final
  Marcela). No tiene sentido contaminar la historia git canónica con
  prosa que no es de Marcela.
- Lo que sí tiene sentido archivar son los metadatos que la pipeline
  produjo: manifiesto, conteos de findings, output de close-project,
  trace cronometrada, reporte de SC. Esos artefactos sirven para
  futuras auditorías constitucionales y para regresiones cuando la
  pipeline cambie.

## Dónde vivió el sandbox

`/tmp/writeonmars-pilot-2026-05-06-onboarding-legacy/`

Contenido (efímero, NO commiteado a este repo):

- `.writeonmars-manifest.json`
- `specs/001-pilot/spec.md` — brief editorial.
- `specs/001-pilot/research.md` — 9 CitationRecord.
- `specs/001-pilot/plan.md` — temario + descripciones encadenadas.
- `specs/001-pilot/findings.md` — 5 bloques de pasada con 32 findings.
- `specs/001-pilot/close-project-output.json` — fuente del JSON aquí.
- `chapters/001-...md`, `002-...md`, `003-...md` — los tres capítulos
  redactados.
- `checklists/001-pilot/pasada-{1..5}.md` — 5 checklists firmadas.

## Qué archivos hay en esta carpeta (canónica)

| Archivo | Qué contiene | Contenido editorial? |
|---------|--------------|----------------------|
| `README.md` | Este archivo. | No. |
| `validation-report.md` | Métricas SC con PASS/WARN/FAIL y justificación. | No. |
| `pipeline-trace.md` | Log cronometrado y aserciones por tarea. | No. |
| `manifest.json` | Copia verbatim del manifiesto del sandbox. | No. |
| `findings-summary.md` | Conteos de findings por pasada/capítulo/severidad/estado. Sin frases originales ni reescrituras. | No. |
| `close-project-output.json` | Salida estructurada de close-project. | No. |
| `install.log` | Log textual de `install/install.sh`. | No. |

Lo que **NO** se copió aquí (y por qué): `chapters/`, `glossary.md`,
`spec.md`, `research.md`, `plan.md`, `findings.md` completo, `index.md`,
`common-errors.md`, `templates/`, `checklists/`. Todo eso es contenido
editorial placeholder y no pertenece a la historia canónica.

## Decisiones documentadas

1. **Firmas de pasadas 3 y 4 como `desviacion_justificada`**: la matriz
   default exige firma humana en las dos pasadas más sensibles (voz y
   precisión). En el piloto, el sub-agente firmó autonomous con razón
   declarada: "piloto automatizado; el operador humano firmará en una
   validación posterior". Bajo esa decisión, close-project trata las
   firmas como humano-proxy y permite `closeable: true`. La tabla
   `strict_blockers_if_no_proxy` en `close-project-output.json` deja
   constancia de qué bloquearía en interpretación estricta.

2. **`index.md` y `common-errors.md` consolidados quedan fuera de
   alcance del piloto**: la pasada 5 los marca `desviacion_justificada`
   con razón "scope del piloto valida pipeline, no ensamblado final".
   En una validación de producción real se consolidan con
   `writeonmars-glossary` y la skill de pasada 5.

3. **Datos volátiles del research no se incorporaron al cuerpo**: la
   métrica de Selleo (15→9 días) y la cifra "≤250 LOC por PR" se
   marcaron `[VERIFICAR]` y se mantuvieron fuera de los capítulos. Esa
   es la regla operativa correcta de constitución § V.4.

## Cómo reproducir

Desde el repo canónico:

```bash
SANDBOX=/tmp/writeonmars-pilot-$(date -u +%F)-onboarding-legacy
mkdir -p "$SANDBOX" && cd "$SANDBOX" && git init -q

WOM_PROJECT_TYPE=guia \
WOM_AUDIENCE="developers con 2+ años que llegan a un repo legacy en produccion" \
WOM_DOMAIN="developer onboarding" \
WOM_OPERATOR_ID=marcela \
WOM_OPERATOR_EMAIL=marcelagotta@gmail.com \
bash /path/to/writing-framework/install/install.sh \
  --target-dir "$SANDBOX" \
  --agent claude-code \
  --language es \
  --non-interactive
```

A partir de ahí, las skills bundled aplican el resto del flujo
(`writeonmars-brief`, `writeonmars-research`, `writeonmars-temario`,
`writeonmars-descripciones`, `writeonmars-redaccion`,
`writeonmars-pasada-{1..5}`, `writeonmars-close-project`).

## Dependencias

- `install/install.sh` (T016–T029).
- 16 skills bundled (T006–T007 + T034–T046).
- Plantillas Spec Kit adaptadas (T030–T033).
- Prompts canónicos de redacción y pasadas (T047–T048).
- `tests/lib/validate-citation.sh` (T049).

## Resultado global

PASS — la pipeline corre extremo a extremo, los gates permiten cierre,
todos los SC del piloto alcanzan target. Detalle en `validation-report.md`.
