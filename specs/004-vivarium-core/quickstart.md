# Quickstart — 004-vivarium-core (para quien implementa)

Guía operativa para implementar y verificar esta feature **sin contexto
previo**. Escrita para Codex, válida para cualquier agente o humano.

## 1. Lee, en este orden

1. `specs/004-vivarium-core/spec.md` — requisitos (FR-001..013) y criterios
   (SC-001..006). Manda sobre todo lo demás.
2. `specs/004-vivarium-core/contracts/executor-contract.md` — el contrato que
   el runner implementa (y que debes publicar en `writeonmars/contracts/`).
3. `specs/004-vivarium-core/plan.md` + `research.md` + `data-model.md` —
   stack, estructura, decisiones (R1-R11), entidades y mapa next_step→acción.
4. `specs/004-vivarium-core/contracts/` restantes — CLI, config BYOM, schema
   de decisions, extensión del manifest-schema.
5. Contexto del método (solo consulta): `paperclip/FLOW-CONTRACT.md`,
   `writeonmars/scripts/status.py`, `tools/new-guide.sh`,
   `tests/fixtures/003-factualidad-project/`.

## 2. Entorno

```bash
# Requisitos: rustup (stable ≥1.75), python3 ≥3.11, git. `specify` CLI solo
# para los tests de bootstrap reales (los unit tests lo stubbean).
cd vivarium
cargo build --workspace
cargo test  --workspace
```

Los tests de integración usan **stubs**: scripts de shell en
`vivarium/crates/vivarium-cli/tests/stubs/` que simulan agentes (escriben el
capítulo o el bloque de findings esperado) y un `specify` falso para no
depender de la herramienta real. Ningún test llama a un proveedor de IA.

## 3. Orden de implementación sugerido (una pieza verificable por paso)

1. **Workspace + esqueleto** (`Cargo.toml`, crates vacíos, CI local:
   `cargo test` verde trivial).
2. **`sidecar.rs`**: invocar `status.py --json` sobre
   `tests/fixtures/003-factualidad-project/` y deserializar los campos del
   executor-contract § 3. Unit tests con el fixture real.
3. **`manifest.rs` + extensión del schema** (contracts/manifest-mode.md):
   bump a v1.3.0, `mode`/`mode_history`, ausencia = produccion. Actualiza
   `bootstrap.py` y sus tests (`uvx --with pytest --with pyyaml python -m
   pytest tests/unit -q` debe seguir verde).
4. **`bootstrap.rs` + `vivarium new`** (FR-001/002): paridad con
   `tools/new-guide.sh`; verifica con un proyecto sintético en tmpdir
   (SC-001).
5. **`state.rs` + `dispatch.rs`** (data-model §§ 3-4): derivación de estados,
   mapa next_step→acción, reglas de relevo, guardarraíl de estudio (FR-008,
   exit 11).
6. **`decisions.rs`** (schema v1) y **`runner.rs`** (`step`/`run`, lock
   fd-lock, idempotencia FR-006, checkpoints exit 10).
7. **`vivarium mode set`** (FR-009, exit 4 sin `--yes`).
8. **Publicar el contrato** (FR-011): copiar
   `contracts/executor-contract.md` → `writeonmars/contracts/executor-contract.md`,
   dejar puntero en el borrador, actualizar CHANGELOG.
9. **Smoke e2e** `tests/smoke/vivarium-e2e.sh` (SC-002: 3 capítulos, stubs,
   kill+relaunch a mitad, 0 duplicados) e integrarlo en
   `tests/smoke/run-all.sh`.

## 4. Verificación final (gate de la feature)

```bash
cd vivarium && cargo test --workspace          # unit + integración, todo verde
cd .. && uvx --with pytest --with pyyaml python -m pytest tests/unit -q  # 131+ verdes
bash tests/smoke/run-all.sh                    # smokes existentes + vivarium-e2e
```

Cobertura de criterios: SC-001 → test de `vivarium new`; SC-002 →
`vivarium-e2e.sh`; SC-003 → test "retirar el runner" (correr a mano
`status.py` tras cada parada y comparar `next_step`); SC-004 → test del
guardarraíl estudio + inspección de `decisions.jsonl`; SC-005 → tests de
`mode set`; SC-006 → los tres comandos de arriba sin pasos manuales.

## 5. Reglas que no se negocian

- La verdad vive en archivos; el runner no computa estado editorial por su
  cuenta ni guarda estado de negocio (FR-003, `vivarium/README.md`).
- No portar los scripts Python (research.md R3).
- No parsear la salida de texto de los agentes; verificar efectos en disco
  (R6).
- El runner jamás escribe prosa del manuscrito (FR-013); en `estudio` jamás
  despacha redacción (FR-008).
- Cualquier desviación del plan se documenta en el PR/commit, no se improvisa
  en silencio.
