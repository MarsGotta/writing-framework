# Findings summary — Baseline serial US3 (4 capítulos)

Resumen estructural del `findings.md` del baseline serial. Sin frases
originales ni texto editorial: solo conteos para auditoría de la
pipeline en modo serial.

`findings.md` completo vivió en `/tmp/writeonmars-pilot-2026-05-06-us3-baseline-serial/`
y no se archiva.

## Conteos por pasada

| Pasada | Skill principal | Capítulos cubiertos | Estado | Críticos | Medios | Bajos | Total |
|--------|-----------------|---------------------|--------|----------|--------|-------|-------|
| 1 — Estructura | technical-guide-design v0.1.0 | [1, 2, 3, 4] | passed-with-warnings | 0 | 1 | 4 | 5 |
| 2 — Utilidad | technical-guide-design v0.1.0 | [1, 2, 3, 4] | passed-with-warnings | 0 | 1 | 6 | 7 |
| 3 — Naturalidad | marcela-prose v0.1.0 | [1, 2, 3, 4] | passed-with-warnings | 0 | 2 | 5 | 7 |
| 4 — Precisión | writeonmars-contraste v0.1.0 | [1, 2, 3, 4] | passed-with-warnings | 0 | 1 | 9 | 10 |
| 5 — Formato | writeonmars-pasada-5 v0.1.0 | [1, 2, 3, 4] | passed-with-warnings | 0 | 1 | 7 | 8 |
| **Total** | | | | **0** | **6** | **31** | **37** |

## Conteos por capítulo

| Capítulo | Críticos | Medios | Bajos | Total |
|----------|----------|--------|-------|-------|
| 1 — Lectura estratégica | 0 | 1 | 5 | 6 |
| 2 — Mapa mental del dominio | 0 | 1 | 4 | 5 |
| 3 — Primer cambio | 0 | 1 | 7 | 8 |
| 4 — Sostener el ritmo | 0 | 1 | 5 | 6 |
| global | 0 | 2 | 10 | 12 |
| **Total** | **0** | **6** | **31** | **37** |

## Estados

| Estado | Conteo |
|--------|--------|
| resuelto | 24 |
| abierto | 10 |
| desviacion_justificada | 3 |
| **Total** | **37** |

## Firmas por pasada

| Pasada | Matriz declarada | Firma efectiva | Razón |
|--------|------------------|----------------|-------|
| 1 | autonomous | autonomous | matriz cumplida |
| 2 | autonomous | autonomous | matriz cumplida |
| 3 | human | autonomous con `desviacion_justificada` | piloto automatizado: el operador humano firmará en validación posterior |
| 4 | human | autonomous con `desviacion_justificada` | piloto automatizado: el operador humano firmará en validación posterior |
| 5 | autonomous | autonomous | matriz cumplida |

## Cobertura de glosario

| Métrica | Valor |
|--------|-------|
| Términos en `terminos_introducidos` (4 caps) | 12 |
| Términos en glossary annex | 12 |
| Cobertura | 100% |

## Resultado de los gates

- **Gate 1 — Críticos abiertos**: 0 críticos abiertos → no bloquea.
- **Gate 2 — Firma humana**: pasadas 3 y 4 con firma autonomous +
  `desviacion_justificada` declarada con razón explícita.

Resultado consolidado: `closeable: true`.
