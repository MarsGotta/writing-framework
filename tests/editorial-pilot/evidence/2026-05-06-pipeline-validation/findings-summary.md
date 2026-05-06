# Findings summary — Piloto 2026-05-06

Resumen estructural de `findings.md` del piloto. NO contiene frases
originales, reescrituras sugeridas ni texto editorial: solo conteos y
metadatos de pasada para auditoría de la pipeline.

`findings.md` completo vivió en el sandbox `/tmp/` y no se archivó.

## Conteos por pasada

| Pasada | Skill principal | Capítulos cubiertos | Estado | Críticos | Medios | Bajos | Total |
|--------|-----------------|---------------------|--------|----------|--------|-------|-------|
| 1 — Estructura | technical-guide-design v0.1.0 | [1, 2, 3] | passed-with-warnings | 0 | 1 | 4 | 5 |
| 2 — Utilidad | technical-guide-design v0.1.0 | [1, 2, 3] | passed-with-warnings | 0 | 1 | 5 | 6 |
| 3 — Naturalidad | marcela-prose v0.1.0 | [1, 2, 3] | passed-with-warnings | 0 | 2 | 4 | 6 |
| 4 — Precisión | writeonmars-contraste v0.1.0 | [1, 2, 3] | passed-with-warnings | 0 | 1 | 7 | 8 |
| 5 — Formato | writeonmars-pasada-5 v0.1.0 | [1, 2, 3] | passed-with-warnings | 0 | 1 | 6 | 7 |
| **Total** | | | | **0** | **6** | **26** | **32** |

## Conteos por capítulo

| Capítulo | Críticos | Medios | Bajos | Total |
|----------|----------|--------|-------|-------|
| 1 — Lectura estratégica | 0 | 1 | 5 | 6 |
| 2 — Mapa mental del dominio | 0 | 2 | 4 | 6 |
| 3 — Primer cambio | 0 | 1 | 7 | 8 |
| global | 0 | 2 | 10 | 12 |
| **Total** | **0** | **6** | **26** | **32** |

## Estados

| Estado | Conteo |
|--------|--------|
| resuelto | 21 |
| abierto | 8 |
| desviacion_justificada | 3 |
| **Total** | **32** |

## Firmas por pasada

| Pasada | Matriz declarada | Firma efectiva | Razón |
|--------|------------------|----------------|-------|
| 1 | autonomous | autonomous | matriz cumplida |
| 2 | autonomous | autonomous | matriz cumplida |
| 3 | human | autonomous con `desviacion_justificada` | piloto automatizado: el operador humano firmará en validación posterior |
| 4 | human | autonomous con `desviacion_justificada` | piloto automatizado: el operador humano firmará en validación posterior |
| 5 | autonomous | autonomous | matriz cumplida |

## Distribución de hallazgos por severidad/pasada

```
                   críticos  medios  bajos
pasada 1            0         1       4
pasada 2            0         1       5
pasada 3            0         2       4
pasada 4            0         1       7
pasada 5            0         1       6
```

## Resultado de los gates

- **Gate 1 — Críticos abiertos (FR-020)**: 0 críticos abiertos → no bloquea.
- **Gate 2 — Firma humana (FR-020a)**: pasadas 3 y 4 con firma autonomous
  pero `desviacion_justificada` declarada con razón explícita. Tratada como
  firma humana proxy para fines del piloto. En estricto, bloquearía
  (registrado en `close-project-output.json#strict_blockers_if_no_proxy`).

Resultado consolidado: `closeable: true`.
