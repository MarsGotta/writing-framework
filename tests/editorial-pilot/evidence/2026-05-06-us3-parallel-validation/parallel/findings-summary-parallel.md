# Findings summary — Pilot paralelo US3 (4 capítulos, --parallel 2)

Resumen estructural del `findings.md` del pilot paralelo. Sin frases
originales: solo conteos para auditoría de la pipeline en modo
paralelo y validación de equivalencia ±10% contra el baseline serial.

`findings.md` completo vivió en `/tmp/writeonmars-pilot-2026-05-06-us3-parallel/`
y no se archiva.

## Conteos por pasada

| Pasada | Skill principal | Capítulos cubiertos | Estado | Críticos | Medios | Bajos | Total |
|--------|-----------------|---------------------|--------|----------|--------|-------|-------|
| 1 — Estructura | technical-guide-design v0.1.0 | [1, 2, 3, 4] | passed-with-warnings | 0 | 1 | 4 | 5 |
| 2 — Utilidad | technical-guide-design v0.1.0 | [1, 2, 3, 4] | passed-with-warnings | 0 | 1 | 6 | 7 |
| 3 — Naturalidad | marcela-prose v0.1.0 | [1, 2, 3, 4] | passed-with-warnings | 0 | 2 | 6 | 8 |
| 4 — Precisión | writeonmars-contraste v0.2.0 (paralelo) | [1, 2, 3, 4] | passed-with-warnings | 0 | 1 | 9 | 10 |
| 5 — Formato | writeonmars-pasada-5 v0.1.0 | [1, 2, 3, 4] | passed-with-warnings | 0 | 1 | 7 | 8 |
| **Total** | | | | **0** | **6** | **32** | **38** |

## Conteos por capítulo

| Capítulo | Críticos | Medios | Bajos | Total |
|----------|----------|--------|-------|-------|
| 1 — Lectura estratégica | 0 | 1 | 5 | 6 |
| 2 — Mapa mental del dominio | 0 | 1 | 4 | 5 |
| 3 — Primer cambio | 0 | 1 | 7 | 8 |
| 4 — Sostener el ritmo | 0 | 1 | 6 | 7 |
| global | 0 | 2 | 10 | 12 |
| **Total** | **0** | **6** | **32** | **38** |

## Estados

| Estado | Conteo |
|--------|--------|
| resuelto | 24 |
| abierto | 11 |
| desviacion_justificada | 3 |
| **Total** | **38** |

## Firmas por pasada

| Pasada | Matriz declarada | Firma efectiva | Razón |
|--------|------------------|----------------|-------|
| 1 | autonomous | autonomous | matriz cumplida |
| 2 | autonomous | autonomous | matriz cumplida |
| 3 | human | autonomous con `desviacion_justificada` | piloto automatizado: el operador humano firmará en validación posterior |
| 4 | human | autonomous con `desviacion_justificada` | piloto automatizado: el operador humano firmará en validación posterior; despachado paralelo por capítulo (T063) |
| 5 | autonomous | autonomous | matriz cumplida |

## Cobertura de glosario

| Métrica | Valor |
|--------|-------|
| Términos en `terminos_introducidos` (4 caps) | 12 |
| Términos en glossary annex | 12 |
| Colisiones críticas detectadas | 0 |
| Cobertura | 100% |

## Resultado de los gates

- **Gate 1 — Críticos abiertos**: 0 críticos abiertos → no bloquea.
- **Gate 2 — Firma humana**: misma situación que el baseline.
- **Gate 3 — Colisiones de glosario**: 0 colisiones críticas → no
  bloquea consolidación.

Resultado consolidado: `closeable: true`.

## Equivalencia con el baseline serial

| Métrica | Serial | Paralelo | Δ absoluto | Δ relativo | Dentro ±10%? |
|---------|--------|----------|------------|------------|--------------|
| Críticos pasada 1 | 0 | 0 | 0 | 0% | sí |
| Críticos pasada 2 | 0 | 0 | 0 | 0% | sí |
| Críticos pasada 3 | 0 | 0 | 0 | 0% | sí |
| Críticos pasada 4 | 0 | 0 | 0 | 0% | sí |
| Críticos pasada 5 | 0 | 0 | 0 | 0% | sí |
| Total findings | 37 | 38 | +1 | +2.7% | sí |
| Cobertura glosario | 100% | 100% | 0 | 0% | sí |

Equivalencia de calidad: dentro de ±10% en ambas dimensiones. PASS.
