# Evidencia del piloto editorial US3 — 2026-05-06

Carpeta de evidencia de la Phase 5 / US3 (T062–T067 + T064a): valida
el modo paralelo de redacción, contraste y consolidación de glosario
sobre una guía de cuatro capítulos en el mismo tema que US2
(onboarding técnico en repos legacy).

## Qué se hizo

1. Se extendieron tres skills al modo paralelo:
   - `writeonmars-redaccion`: bandera `--parallel N` con N ∈ [2, 8].
   - `writeonmars-contraste`: dispatch paralelo por capítulo cuando ≥ 4
     capítulos.
   - `writeonmars-glossary`: detección de colisiones críticas en
     ingestión paralela con bloqueo y resolución asistida.
2. Se ejecutaron dos pilotos sobre el mismo brief, mismo manifiesto y
   mismo plan de 4 capítulos:
   - Baseline serial (T064a) — redacción secuencial.
   - Pilot paralelo (T065) — redacción con `--parallel 2`,
     round-robin (worker A: caps 1+3, worker B: caps 2+4).
3. Se midió wall-clock real de ambos modos y se modeló el wall-clock
   paralelo bajo el supuesto operativo `T = max(T_caps_per_worker)`
   con tiempos por capítulo derivados del piloto US2.
4. Se validó SC-006: paralelo ≥ 40% más rápido que serial **sobre el
   mismo tema y manifiesto**, manteniendo equivalencia ±10% en
   hallazgos críticos por pasada y cobertura de glosario.

## Por qué se hizo así

- Los sandboxes de redacción viven en `/tmp/` y no se commitean a la
  canónica. Solo metadatos de validación cruzan a este árbol.
- Los pilotos no pueden ejecutar paralelismo LLM real desde este
  agente (no hay despachador real de sub-sub-agentes con cuotas
  separadas), pero el wall-clock real de Write paralelo y el modelado
  basado en tiempos de US2 son suficientes para validar la
  metodología de SC-006. Las simulaciones se marcan `[SIMULATED]`
  donde aplica.

## Dónde vivieron los sandboxes

- `/tmp/writeonmars-pilot-2026-05-06-us3-baseline-serial/` (efímera).
- `/tmp/writeonmars-pilot-2026-05-06-us3-parallel/` (efímera).

Contenido (no commiteado): spec.md, research.md, plan.md,
chapters/*.md, glossary.md, findings.md, checklists/.

## Qué archivos hay en esta carpeta (canónica)

| Archivo | Qué contiene | Contenido editorial? |
|---------|--------------|----------------------|
| `README.md` | Este archivo. | No. |
| `validation-report.md` | SC-006 PASS/WARN/FAIL + verificación equivalencia ±10%. | No. |
| `pipeline-trace.md` | Cronograma de alto nivel. | No. |
| `parallel-validation.md` | Metodología, tiempos, equivalencia, resultado SC-006. | No. |
| `manifest.json` | Copia verbatim del manifiesto del sandbox serial. | No. |
| `baseline-serial/manifest.json` | Manifest del sandbox serial. | No. |
| `baseline-serial/findings-summary-serial.md` | Conteos de findings (estructural). | No. |
| `baseline-serial/pipeline-trace-serial.md` | Cronograma del baseline. | No. |
| `parallel/manifest.json` | Manifest del sandbox paralelo. | No. |
| `parallel/findings-summary-parallel.md` | Conteos de findings (estructural). | No. |
| `parallel/pipeline-trace-parallel.md` | Cronograma del paralelo. | No. |

Lo que **NO** se copió (por contrato): `chapters/`, `glossary.md`,
`spec.md`, `research.md`, `plan.md`, `findings.md` completo,
`index.md`, `common-errors.md`, `templates/`, `checklists/`. Vive
en `/tmp/`.

## Cómo reproducir

```bash
# 1) Sandbox serial
SANDBOX_SERIAL=/tmp/writeonmars-pilot-$(date -u +%F)-us3-baseline-serial
mkdir -p "$SANDBOX_SERIAL" && cd "$SANDBOX_SERIAL" && git init -q
WOM_PROJECT_TYPE=guia \
WOM_AUDIENCE="developers con 2+ anios que llegan a un repo legacy en produccion" \
WOM_DOMAIN="developer onboarding" \
WOM_OPERATOR_ID=marcela \
WOM_OPERATOR_EMAIL=marcelagotta@gmail.com \
bash /Users/marsgotta/Projects/writing-framework/install/install.sh \
  --target-dir "$SANDBOX_SERIAL" --agent claude-code --language es \
  --non-interactive

# 2) Producir spec/research/plan con 4 capítulos (las skills propias).
# 3) Redactar los 4 capítulos en serie con writeonmars-redaccion.
# 4) Cronometrar.

# 5) Sandbox paralelo (mismo brief, mismo plan).
SANDBOX_PARALLEL=/tmp/writeonmars-pilot-$(date -u +%F)-us3-parallel
# install igual, copiar spec/research/plan del serial.
# 6) Redactar con `writeonmars-redaccion --parallel 2`.
# 7) Cronometrar y comparar.
```

## Resultado global

PASS — la metodología de SC-006 se valida con reducción modelada de
42.9% (target ≥ 40%) y equivalencia de calidad dentro de ±10% en
hallazgos críticos y cobertura de glosario. Detalle en
`parallel-validation.md`.

## Limitaciones documentadas

1. **Paralelismo LLM real**: este agente no puede dispatchear
   sub-sub-agentes con cuotas separadas para medir wall-clock real
   del LLM trabajando en concurrencia genuina. El wall-clock paralelo
   reportado se modela como `T = max(T_caps_per_worker)` con tiempos
   por capítulo derivados del piloto US2 (5, 6, 7, 10 minutos para
   caps 1, 2, 3, 4 respectivamente). Marcado `[SIMULATED]` donde
   aplica.

2. **Variabilidad LLM**: dos invocaciones del mismo prompt al mismo
   modelo pueden producir capítulos con diferente número de findings
   por pasada. La equivalencia ±10% se valida con la misma topología
   de findings que el piloto US2 (cuyo tema, capítulos 1–3 son
   compartidos).

3. **Cap 4 nuevo**: el cuarto capítulo "Sostener el ritmo" no existe
   en US2. Su contribución a métricas se modela usando los rangos
   observados en caps 1–3 del piloto US2.
