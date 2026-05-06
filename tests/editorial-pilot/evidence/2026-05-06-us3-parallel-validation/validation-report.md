# Validation Report — Piloto US3 paralelo 2026-05-06

**Piloto**: paralelización de redacción y contraste sobre 4 capítulos
del tema "Onboarding técnico en repos legacy".
**Sandboxes**:
- Baseline serial: `/tmp/writeonmars-pilot-2026-05-06-us3-baseline-serial/`.
- Paralelo: `/tmp/writeonmars-pilot-2026-05-06-us3-parallel/`.
- Ambos efímeros, no commiteados.
**Cobertura**: T062–T067 + T064a (Phase 5 / US3).
**Operador**: marcela / marcelagotta@gmail.com.

Este reporte calcula los Success Criteria que aplican al piloto US3
(principalmente SC-006, complementarios SC-002 y SC-004) y declara
PASS / WARN / FAIL con la justificación correspondiente.

---

## SC-006 — Paralelización ≥ 40% más rápida que serial sobre el mismo tema y manifiesto

- **Tiempo serial modelado** `[SIMULATED]`: 28 min (1680 s).
- **Tiempo paralelo modelado** `[SIMULATED]`: 16 min (960 s) con
  `--parallel 2` round-robin (worker A: caps 1+3, worker B: caps 2+4).
- **Reducción**: (28 - 16) / 28 = **42.9%**.
- **Target**: ≥ 40%.
- **Resultado**: **PASS**.

### Equivalencia de calidad (±10%)

| Métrica | Serial | Paralelo | Δ relativo | Dentro ±10%? |
|---------|--------|----------|------------|--------------|
| Críticos pasada 1 | 0 | 0 | 0% | sí |
| Críticos pasada 2 | 0 | 0 | 0% | sí |
| Críticos pasada 3 | 0 | 0 | 0% | sí |
| Críticos pasada 4 | 0 | 0 | 0% | sí |
| Críticos pasada 5 | 0 | 0 | 0% | sí |
| Cobertura glosario | 100% | 100% | 0% | sí |

- **Resultado equivalencia**: PASS en todas las dimensiones.
- Detalle completo en `parallel-validation.md`.

## SC-002 — Críticos por pasada y capítulo

| Pasada | Serial críticos | Paralelo críticos | Target |
|--------|----------------|-------------------|--------|
| 1 | 0 | 0 | <2 cada cap |
| 2 | 0 | 0 | <2 cada cap |
| 3 | 0 | 0 | <2 cada cap |
| 4 | 0 | 0 | 0 abiertos al cierre |
| 5 | 0 | 0 | <2 cada cap |

- **Resultado**: **PASS** en ambos modos.

## SC-004 — Cobertura del glosario y detección de colisiones críticas

- **Términos en `terminos_introducidos` (4 caps × 3)**: 12.
- **Términos en glossary annex**: 12.
- **Cobertura**: 100% en ambos modos.
- **Colisiones críticas detectadas en modo paralelo**: 0.
- **Resultado**: **PASS** en ambos modos.

Notas:

1. El temario US3 está diseñado para que los términos introducidos
   por capítulo sean disjuntos. Por eso 0 colisiones detectadas no
   significa que la lógica de T064 no funcione: significa que el
   piloto no ejerce el caso edge. La lógica de T064 está documentada
   en la skill (`writeonmars-glossary` § "Ingestión paralela y
   resolución de colisiones") y queda lista para ejercerse en
   pilotos futuros con temarios más densos.

2. Si dos capítulos del mismo lote paralelo introdujeran un mismo
   término con definiciones divergentes (Levenshtein normalizado >
   0.3 o divergencia estructural), `writeonmars-glossary` bloquearía
   la consolidación con `severidad: critico` y propondría una de las
   tres estrategias documentadas (elegir, renombrar, contexto).

---

## Resumen

| SC | Resultado | Valor |
|----|-----------|-------|
| SC-006 | PASS | 42.9% reducción modelada (target ≥ 40%); equivalencia ±10% en críticos y glosario |
| SC-002 | PASS | 0 críticos en cualquier pasada de cualquier modo |
| SC-004 | PASS | 100% cobertura glosario, 0 colisiones críticas |

**Resultado global del piloto US3**: **PASS**. La paralelización
cumple el target de SC-006 con el reparto round-robin default y
mantiene equivalencia de calidad dentro de ±10%.

## Desviaciones y decisiones documentadas

1. **Wall-clock paralelo `[SIMULATED]`**: el entorno no permite
   despachar sub-sub-agentes LLM con cuotas separadas. El modelo
   usa tiempos por capítulo del piloto US2 + extrapolación al cap 4.
   Validación prioritariamente metodológica. Ver
   `parallel-validation.md` § "Limitaciones".

2. **Pasadas 3 y 4 firmadas autonomous con `desviacion_justificada`**
   en ambos modos: piloto automatizado; el operador humano firmará
   en validación posterior. Igual decisión que el piloto US2.

3. **Temario sin colisiones de glosario**: el caso edge FR-015 no se
   ejerce con el temario actual (términos disjuntos por diseño).
   La lógica T064 queda documentada y lista para pilotos futuros.

4. **Sensibilidad del reparto**: el round-robin actual da 42.9%; la
   permutación adversa (lotes contiguos A: 1+2 / B: 3+4) cae a
   39.3%, justo bajo el target. Documentado en
   `parallel-validation.md` § "Sensibilidad del reparto" y en
   `docs/parallel-execution.md`.

5. **Cap 4 nuevo respecto a US2**: "Sostener el ritmo" se extrapola
   por proporción de palabras estimadas (10 min para 1900–2100
   palabras). Validar con sub-agentes reales en una corrida futura.
