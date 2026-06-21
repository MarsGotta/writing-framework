# Tasks: Atribución por afirmación y gate de factualidad

**Feature**: `003-atribucion-factualidad` | **Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md) | **Data model**: [data-model.md](./data-model.md)

Convenciones: `[P]` = paralelizable (no comparte archivo con otra `[P]` de la misma fase). Cada tarea lista su(s) archivo(s), qué hacer y el criterio de aceptación (DoD). Las FR/SC entre paréntesis enlazan al spec. **Antes de empezar**: confirmar con la mantenedora la **Decisión D1** (`plan.md`) — por defecto D1-A.

---

## Fase 0 — Preparación

- **T001** — Crear la rama `003-atribucion-factualidad` y mover/copiar este folder `specs/003-atribucion-factualidad/` a su sitio definitivo (ya existe el borrador). DoD: rama creada, `spec.md`/`plan.md`/`research.md`/`data-model.md`/`contracts/claim-record.schema.json` presentes.
- **T002** — Confirmar Decisión D1 (validar vs generar la sección "Fuentes por capítulo"). DoD: decisión registrada en `plan.md` § D1 (default D1-A). Bloquea T021.

## Fase 1 — Contratos (base de todo lo demás)

- **T003** `[P]` — Publicar `claim-record.schema.json` en sus dos ubicaciones. Archivos: `contracts/claim-record.schema.json`, `writeonmars/contracts/claim-record.schema.json` (copiar de `specs/003-.../contracts/`). DoD: ambos byte-idénticos al validado; `python3 -c "import json; json.load(...)"` OK; meta-schema Draft 2020-12 OK. (FR-001)
- **T004** `[P]` — Bump `pass-output-schema.md` → v1.1 en ambas copias. Archivos: `contracts/pass-output-schema.md`, `writeonmars/contracts/pass-output-schema.md`. Añadir sección "Salida de claims (pasada 4)", trazabilidad `claim_id` en findings de pasada 4, entrada de versionado v1.1 y comentario `<!-- pass-output-schema: v1.1 -->`. NO eliminar campos v1.0. DoD: diff solo aditivo; un `findings.md` v1.0 de ejemplo sigue siendo conforme. (FR-008, FR-015)
- **T005** `[P]` — Bump `manifest-schema.json` → MINOR en ambas copias: añadir `quality_gates` (objeto opcional, `additionalProperties:false`) a `properties`; NO a `required`. Subir versión en `$id`/`$comment`/título. DoD: un manifest existente (sin `quality_gates`) valida; uno con `quality_gates` válido valida; uno con clave extra dentro de `quality_gates` falla. (FR-014, FR-015)

## Fase 2 — Núcleo de juicio (la pasada 4 produce claims.md)

- **T006** — Editar `writeonmars/references/metodo/writeonmars-contraste/SKILL.md` (núcleo). Implementar en las instrucciones: (a) persistir un `ClaimRecord` por cada afirmación verificable evaluada en `claims.md`; (b) clasificar `relacion` tras abrir la fuente y registrar `cita_fragmento_soporte`; (c) derivar `soporte` por `data-model.md` § 1.3; (d) mapear severidad por FR-009; (e) idempotencia por capítulo (reemplazo en bloque); (f) no inventar fuentes; (g) bump de versión de la skill + FR cubiertas. DoD: la skill describe sin ambigüedad cómo producir `claims.md` conforme al esquema y cómo deriva severidad. (FR-005, FR-006, FR-007, FR-009, US1, US2)
- **T007** — Actualizar el modo paralelo por capítulo de la misma skill: cada sub-agente emite su fragmento de `claims.md` (bloque del capítulo); el orquestador consolida sin race (igual que con findings). DoD: instrucciones de consolidación de `claims.md` presentes y sin escritura concurrente directa. (FR-007)
- **T008** `[P]` — Editar `writeonmars/commands/speckit.review-precision.md`: documentar la doble salida (findings + claims.md), añadir input `claim-record.schema.json`, traducir "sin web no se finge" a `soporte: pendiente`. DoD: el comando refleja la nueva salida. (FR-006)
- **T009** `[P]` — Editar `paperclip/agents/documentalista/bundle.md`: reflejar la tabla de severidad ampliada y "escribe claims.md + clasifica relación"; **no** tocar la sección de decisión del ciclo. DoD: bundle coherente con T006; sección de decisión intacta (diff no la toca). (FR-017, US4)

## Fase 3 — Núcleo de conteo (status.py determinista)

- **T010** — `status.py`: implementar `parse_claims(claims_md)` (lee bloques ```json por capítulo; tolera ausencia/JSON inválido → `unmeasured`). DoD: unit-test del parser sobre un `claims.md` de fixture devuelve la lista esperada y marca `unmeasured` correctamente. (FR-010)
- **T011** — `status.py`: implementar `compute_factuality(...)` por `data-model.md` § 3.1 (micro-promedio; excluye `pendiente` del denominador; `parcial` no soportada). DoD: para fixture 8/10 → `factuality_global == 0.8`; por-capítulo correcto; `None` cuando denominador 0. (FR-010, SC-002, SC-006)
- **T012** — `status.py`: integrar en `evaluate()` el gate g4 y los campos `--json` aditivos (`factuality_global`, `factuality_by_chapter`, `factuality_unmeasured`, `factuality_pending`, `gates.factuality`); `closeable` incorpora g4 solo en modo `blocking` con umbral presente. Añadir `warnings` si g4 rojo con `revise_pending==0`. DoD: salida JSON cumple `data-model.md` § 3.3; sin `quality_gates`, `gates.factuality==null` y `closeable` idéntico a hoy. (FR-011, FR-012, FR-013, SC-003)
- **T013** — `status.py`: dashboard (`print_dashboard`) muestra factualidad (global/por-capítulo/pendientes/no-medido) y el gate g4 solo si hay umbral; `_next_step` apunta el déficit a la vía revise existente (sin paso nuevo). DoD: dashboard legible; `_next_step` no inventa pasos. (FR-011, FR-012)

## Fase 4 — Export, gobernanza y orquestador

- **T021** — `writeonmars/scripts/export.py`: implementar D1 (por defecto D1-A: **validar** "Fuentes por capítulo" contra `claims.md`; fallar/avisar si una afirmación `sin_fuente`/`contradicho` llega al PDF sin marca o una fuente del cuerpo no está en claims). Bloqueada por T002, T006. DoD: export valida y reporta incoherencias; en D1-A no reescribe la sección. (FR-016)
- **T022** `[P]` — `writeonmars/memory/constitution.md` (+ espejo): bump MINOR. Añadir requisito de atribución por afirmación + índice de factualidad; "Fuentes por capítulo" se conserva derivada/validada; actualizar `SYNC IMPACT REPORT`. DoD: versión nueva coherente; principios IV y V actualizados sin redefinición incompatible. (FR-015)
- **T023** `[P]` — `paperclip/agents/editora-jefa/HEARTBEAT.md` § 5: añadir bullet de `gates.factuality==false` (blocking) como blocker de cierre, enrutado por la vía findings→revise. DoD: doc actualizada; lógica de heartbeat sin cambios. (US4, FR-018)

## Fase 5 — Tests y fixtures

- **T030** `[P]` — `tests/lib/validate-claim.sh` (gemelo de `validate-citation.sh`). DoD: valida un `ClaimRecord` conforme; rechaza `apoya` sin `cita_fragmento_soporte` y `verificado_en_vivo` sin `url_verificada`/`fecha_verificacion`. (FR-020)
- **T031** `[P]` — `tests/fixtures/003-factualidad/`: `findings.md` + `claims.md` + `.writeonmars-manifest.json` con factualidad conocida (8/10) y variantes (con/sin `quality_gates`, advisory/blocking, un capítulo `unmeasured`). DoD: fixtures parseables y autoconsistentes (claims↔findings coherentes). (FR-021)
- **T032** — `tests/smoke/test-factuality.sh`: corre `status.py --json` contra los fixtures y asegura: (a) retrocompat sin `quality_gates` (SC-003, idéntico al baseline); (b) blocking bajo umbral → `gates.factuality==false`, `closeable==false`, `--gate` exit 1; (c) advisory no bloquea; (d) `unmeasured` no cuenta como 0; (e) `menciona`-en-dato-duro baja el índice vs "tiene_cita/total" (SC-006). Bloqueada por T012, T031. DoD: smoke verde. (FR-021, SC-002, SC-003, SC-005, SC-006)
- **T033** — Verificación de no-regresión Paperclip (US4): correr el flujo end-to-end en el Project de prueba (`guide-nlp`) con la feature activa y comprobar SC-004 (0 tipos/estados/routines nuevos) y que la Documentalista escribe `claims.md` + decide igual. DoD: checklist de SC-004 + acceptance de US4 cumplidos. (US4, SC-004)

## Fase 6 — Cierre

- **T040** `[P]` — `docs/compatibility-matrix.md`: anotar que un MCP de contraste puede emitir `ClaimRecord` además de `CitationRecord`. DoD: matriz actualizada.
- **T041** `[P]` — `CHANGELOG.md`: entrada de la feature (contrato nuevo + v1.1 pass-output + manifest MINOR + constitución MINOR). DoD: entrada con versiones y rationale.
- **T042** — Revisión final: re-evaluar Constitution Check del `plan.md` tras la implementación; confirmar que todos los SC del spec tienen evidencia. DoD: Constitution Check re-pasado; tabla SC→evidencia completa.

---

## Grafo de dependencias (resumen)

```
T001,T002
  └─ Fase 1 (T003,T004,T005) [P entre sí]
       └─ Fase 2 (T006 → T007; T008,T009 [P])
            └─ Fase 3 (T010 → T011 → T012 → T013)
                 ├─ T021 (needs T002,T006)
                 ├─ T022,T023 [P]
                 └─ Fase 5: T030,T031 [P] → T032 (needs T012,T031) → T033
                      └─ Fase 6: T040,T041 [P] → T042
```

## Criterios de "hecho" global (Definition of Done de la feature)

- Todos los SC-001…SC-006 del spec con evidencia (T032/T033/T042).
- Retrocompatibilidad demostrada (SC-003): sin `quality_gates` ni `claims.md`, `status.py` se comporta byte-idéntico al baseline.
- Cero APIs/estados/routines nuevos de Paperclip (SC-004), verificado contra `FLOW-CONTRACT.md` §4/§5.
- Contratos versionados y espejados (raíz + `writeonmars/`).
- Juicio en la referencia agnóstica, conteo en `status.py` (Principio VI, FR-017).
