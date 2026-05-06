# Write.OnMars

Harness editorial para que agentes de IA produzcan guías técnicas de
calidad de autora.

## Estado

Pre-release. La feature activa es `001-framework-architecture` y todavía
no hay tag `v1.0.0` publicado. La estructura, los contratos y la
constitución están consolidados; las skills `writeonmars-*` y los
scripts de instalación se desarrollan en las fases descritas en
`specs/001-framework-architecture/tasks.md`.

## Enlaces rápidos

- Constitución: [`.specify/memory/constitution.md`](.specify/memory/constitution.md)
- Spec activa: [`specs/001-framework-architecture/spec.md`](specs/001-framework-architecture/spec.md)
- Plan: [`specs/001-framework-architecture/plan.md`](specs/001-framework-architecture/plan.md)
- Tareas: [`specs/001-framework-architecture/tasks.md`](specs/001-framework-architecture/tasks.md)
- Quickstart: [`specs/001-framework-architecture/quickstart.md`](specs/001-framework-architecture/quickstart.md)
- Documentación: [`docs/`](docs/)

## Arquitectura en una pantalla

- **Skills + MCP opcional + plantillas Spec Kit adaptadas**: el framework
  se distribuye como un conjunto de skills bundled en `.claude/skills/`,
  un módulo MCP opcional en `mcp/writeonmars-research/` para investigación
  con contrato de citación y plantillas de Spec Kit reescritas para
  producción editorial.
- **Distribución por instalación**: `install/install.sh` copia los
  assets sobre un repositorio Git existente, registra los hooks de Spec
  Kit y emite el manifiesto del proyecto (`.writeonmars-manifest.json`)
  con las versiones de cada componente.
- **Agnosticismo de agente**: las skills nucleares y los contratos
  publicados en `contracts/` no asumen un agente concreto. La
  prioridad v1 es Claude Code; los adaptadores para Codex u otros
  agentes residirán en `agents/<nombre>/` cuando estén soportados.

## Idioma primario

Español. El idioma se declara en el brief de cada proyecto editorial y
puede sobreescribirse por excepción (ver constitución § "Propósito y
alcance" y § IV "Precisión léxica").

## Licencia

TBD (pendiente de elegir antes de la release v1.0.0).
