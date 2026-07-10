# Write.OnMars

Harness editorial para que un agente de IA produzca guías técnicas, manuales,
artículos, libros y tutoriales al nivel de una autora especializada. No reemplaza
al agente: lo gobierna mediante un **preset de Spec Kit agente-agnóstico**
(plantillas, comandos, scripts y referencias), contratos publicados y un manifest
del proyecto.

Audiencia primaria: cualquier agente de IA (cualquier modelo, no solo Claude) que
ejecuta el flujo. Audiencia secundaria: quien mantiene el framework y quien opera
un proyecto editorial.

## La unidad instalable: el preset `writeonmars/`

Todo el método se distribuye y se ejecuta como un preset de Spec Kit. La lógica
vive en **comandos** y las reglas (voz, didáctica, método) en **referencias**, no
en skills de un proveedor — así lo puede correr cualquier agente.

```
+---------------------+      +-------------------------------------+      +----------------+
|   Agente            | ---> |   Preset writeonmars/ (specify       | ---> |  Repo          |
|   (cualquier modelo)|      |   preset add)                        |      |  editorial     |
+---------------------+      |   - templates/  (modo editorial)     |      |  specs/        |
          |                  |   - commands/   (speckit.specify…)     |      |  chapters/     |
          v                  |   - scripts/    (export, status…)    |      |  findings.md   |
+---------------------+      |   - references/ (voz, didáctica,     |      |  glossary.md   |
|  Contratos          | <--- |     método — neutrales de modelo)    |      |  *.pdf         |
|  contracts/         |      |   - AGENTS.md   (contrato del agente) |      +----------------+
+---------------------+      +-------------------------------------+
```

Ver [`writeonmars/README.md`](writeonmars/README.md) y la documentación de uso en
[`writeonmars/docs/`](writeonmars/docs/) (tutorial, how-to, referencia,
arquitectura).

## Quickstart

```bash
# 1. Crear el repo editorial (la guía es un repo aparte, no este)
mkdir mi-guia && cd mi-guia && git init

# 2. Instalar el preset
specify preset add --dev ~/Projects/writing-framework/writeonmars

# 3. Producir la guía con los comandos del preset (cualquier agente)
/speckit.specify "Tu guía técnica aquí"
#   → /speckit.research → /speckit.plan → /speckit.implement → /speckit.review
#   → /speckit.status → /speckit.export → /speckit.feedback → /speckit.close
```

Recorrido paso a paso: [`writeonmars/docs/tutorial-primera-guia.md`](writeonmars/docs/tutorial-primera-guia.md).

## Estado

- **Preset `writeonmars`**: v0.1.0, agente-agnóstico, probado de punta a punta
  (incluida una corrida BYOM real con dos agentes cruzados, 2026-07-08).
  6 plantillas + 18 comandos + 9 scripts.
- **Framework**: v1.0.0 etiquetada (2026-05-06); el refactor a preset sigue en
  `main` como Unreleased.
- **Constitución**: v1.7.0 (§ «Pistas de ceremonia» `estandar`/`corta`, ortogonal
  al modo; desde v1.6.0: modos de proyecto `produccion`/`estudio` y § Ejecutores
  del método — Vivarium como ejecutor orquestado de referencia, Paperclip archivado).
- **Contrato de citación**: v1.0 · **Manifest**: v1.4.0 · **pass-output**: v1.2.

> La vía legacy `install.sh` se retiró del árbol (2026-07-09; vive en la
> historia de git). La distribución canónica es el preset.
> El spec `002-wom-cli` queda **superseded** (el `wom` CLI se descartó: `status.py`
> y `close.py` cubren su función). El spec `001-framework-architecture` es la base.

## Enlaces principales

- **Estado y roadmap**: [`ROADMAP.md`](ROADMAP.md) — empieza aquí para retomar.
- **Cómo está construido todo**: [`docs/como-funciona.md`](docs/como-funciona.md) — el plano del repo y de los flujos.
- Preset (unidad instalable): [`writeonmars/`](writeonmars/) · [README](writeonmars/README.md) · [AGENTS.md](writeonmars/AGENTS.md)
- **Documentación de uso (canónica)**: [`writeonmars/docs/`](writeonmars/docs/) — tutorial, how-to, referencia, arquitectura
- Constitución: [`writeonmars/memory/constitution.md`](writeonmars/memory/constitution.md) (núcleo) — las adendas por guía las fija `/speckit-constitution`
- Contratos: [`contracts/`](contracts/) (citación, manifest, pass-output)
- Referencia de mantenimiento: [`docs/`](docs/) — contrato de citación, manifest, compatibilidad, paralelización, memoria externa, contributing
- Contributing: [`docs/contributing.md`](docs/contributing.md)
- CHANGELOG: [`CHANGELOG.md`](CHANGELOG.md)

## Idioma primario

Español. Toda excepción (siglas, citas en otra lengua, fragmentos de código) se
declara en el brief del proyecto editorial. Ver constitución § "Propósito y
alcance" y § IV "Precisión léxica".

## Licencia

[Apache-2.0](LICENSE) (elegida el 2026-07-09; hasta entonces figuraba TBD).
