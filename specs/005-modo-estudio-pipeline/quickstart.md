# Quickstart — validar el pipeline del modo estudio (005)

Recorrido de verificación por escenario, pensado para ejecutarse tras la
implementación sin conocimiento previo del repo. Todos los pasos son
verificables por script; ninguno requiere un agente LLM real (los smoke usan
stubs deterministas).

## 0. Gates (SC-006)

```bash
uvx --with pytest --with pyyaml python -m pytest tests/unit -q   # unitarios
bash tests/smoke/run-all.sh                                      # smoke (incluye estudio-e2e)
cd vivarium && cargo test --workspace && cd ..                   # ejecutor
```

## 1. Brújula consciente de modo (US1)

```bash
# Fixture: proyecto estudio con temario de 3 y 0 capítulos
python3 writeonmars/scripts/status.py --project-dir tests/fixtures/005-estudio/project --json \
  | python3 -c "import json,sys; s=json.load(sys.stdin); \
      assert s['mode']=='estudio'; assert s['next_step']=='write'; \
      assert s['pending_chapters']==[1,2,3]; print('ok write')"

# Escribir el capítulo 1 "a mano" y re-consultar
cp tests/fixtures/005-estudio/chapters/001-*.md <proyecto>/chapters/
# → next_step == 'review' (pasada 1 del capítulo 1, despachable)
```

Retrocompat (FR-011/SC-004): los fixtures de produccion existentes
(`tests/fixtures/003-factualidad/`) devuelven exactamente lo de antes; la
suite unitaria previa pasa sin editar aserciones.

## 2. Disposición humana (US2)

```bash
cd <proyecto-estudio-con-hallazgos>
python3 .specify/presets/writeonmars/scripts/dispose.py F-1.1 --aceptar        # exit 0
python3 .specify/presets/writeonmars/scripts/dispose.py F-1.2 --rechazar \
        --motivo "la frase es correcta en mi variedad dialectal"              # exit 0
python3 .specify/presets/writeonmars/scripts/dispose.py F-1.3 --aplazar        # exit 0
python3 .specify/presets/writeonmars/scripts/dispose.py F-9.9 --aceptar        # exit 1 (no existe)
python3 .specify/presets/writeonmars/scripts/dispose.py F-1.2 --aceptar        # exit 1 (ya dispuesto: desviacion_justificada)
```

Comprobar: `disposiciones.jsonl` tiene 3 líneas válidas contra
`disposition-record.schema.json`; `status.py --json` deja de listar F-1.1 y
F-1.2 en `pending_dispositions`, F-1.3 aparece en `deferred_findings`.

Atajo neutralizado (SC-005): editar a mano `findings.md` poniendo `resuelto`
a un hallazgo SIN disposición → `status.py` emite warning y el hallazgo sigue
en `pending_dispositions`.

## 3. Huella / capítulo reabierto (FR-008)

```bash
# Con el capítulo 1 aprobado (pasadas 1-4 con huellas correctas):
echo "una frase nueva" >> <proyecto>/chapters/001-*.md
python3 writeonmars/scripts/status.py --project-dir <proyecto> --json \
  | python3 -c "import json,sys; s=json.load(sys.stdin); \
      assert '1' in s['reopened_chapters']; \
      assert s['by_chapter']['1']['approved'] is False; print('ok reopen')"
```

## 4. Informe de autoría (US3)

```bash
python3 writeonmars/scripts/authorship.py --project-dir <proyecto> --json > /tmp/a1.json
python3 writeonmars/scripts/authorship.py --project-dir <proyecto> --json > /tmp/a2.json
diff /tmp/a1.json /tmp/a2.json                                    # vacío (SC-003)
```

Fixture con historia mixta (commit de agente `redactora@agents.writeonmars.invalid`
en el capítulo 1, commits humanos en el 2): veredicto cap 1 = `ia`/`mixta`,
cap 2 = `humana`, global ≠ `autoria_humana_demostrada`.

## 5. E2E con el ejecutor (SC-002) — smoke `tests/smoke/estudio-e2e.sh`

Guion del smoke (stubs deterministas, skip 99 sin cargo):

1. `vivarium new <tmp> --kind novela` → manifiesto con `mode: estudio`.
2. `vivarium run` → exit 10 (checkpoint `specify`). Escribir spec.md fixture.
3. `vivarium run` → despacha research/plan (stubs) → exit 10 con checkpoint
   `write` (faltan capítulos). **Assert**: ningún dispatch de
   `implement` en decisions.jsonl.
4. Copiar los 2 capítulos fixture (simula a la escritora) → `vivarium run` →
   despacha pasadas (stubs que emiten findings con huellas) → exit 10 con
   checkpoint `dispose`.
5. Correr `dispose.py` sobre los hallazgos accionables → `vivarium run` →
   pasada 5 → exit 10 checkpoint `intro` (humana escribe README) → escribir
   README fixture → export (stub) → exit 10 checkpoint `feedback`.
6. `feedback.md` fixture → `vivarium run` → close → exit 0. Segundo run →
   exit 0 sin despachos nuevos.
7. `authorship.py --json` → veredicto global `autoria_humana_demostrada`.
8. **Asserts globales**: en decisions.jsonl no existe ningún dispatch con
   step `implement`, `revise` ni `intro`; los checkpoints `write` y `dispose`
   constan exactamente una vez cada espera (sin duplicados).
