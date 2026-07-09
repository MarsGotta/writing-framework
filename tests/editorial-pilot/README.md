# Piloto editorial de Write.OnMars

> **Nota (2026-07-09)**: este README describe el arnés de los pilotos de mayo
> de 2026, que instalaban con el `install.sh` legacy (retirado del árbol; vive
> en la historia de git). Un piloto nuevo se monta con `specify preset add`
> o `tools/new-guide.sh`. La evidencia archivada en `evidence/` no se toca.

## Propósito

Este directorio aloja el piloto editorial que valida manualmente la User
Story 2 (`US2 — Producción de una guía completa siguiendo el flujo
editorial`) de la feature `001-framework-architecture`. La validación
manual se eligió de forma deliberada conforme a `research.md` § R6: la
calidad editorial no se puede afirmar con un test de Bash, requiere una
producción real que se inspeccione contra los criterios de éxito (SC) de
la spec.

El piloto cumple dos funciones simultáneas:

1. Sirve como **prueba de aceptación end-to-end** del framework: instala,
   ejecuta el ciclo de ocho etapas y produce una guía técnica firmada con
   las cinco pasadas.
2. Genera **evidencia archivada** que la persona mantenedora consulta
   cuando la constitución cambia, cuando aparecen regresiones o cuando un
   PR propone modificar una skill nuclear.

## Alcance del primer piloto

El primer piloto está acotado a **3 capítulos sobre un tema cerrado**.
Tema sugerido por defecto: *"Onboarding técnico en repositorios legacy"*.
Es un tema acotado, con audiencia clara (personas técnicas que llegan a
un proyecto que no escribieron) y se presta a un ejemplo recurrente único
sin necesidad de citas externas masivas.

El piloto MUST partir de un brief generado por `writeonmars-brief` que
cubra los nueve campos exigidos por **FR-005** de la spec. Si el brief
deja `[NEEDS CLARIFICATION]` en cualquier campo crítico, el piloto se
detiene hasta resolverlo (regla heredada de la constitución § III).

Los criterios de validación obligatorios para declarar el piloto exitoso
son:

- **SC-002**: el cierre del proyecto (`writeonmars-close-project`)
  reporta `closeable: true` sin hallazgos críticos abiertos.
- **SC-003**: el 100 % de los capítulos respeta la plantilla de nueve
  secciones didácticas (Problema real → Idea clave → Por qué importa →
  Cómo funciona → Ejemplo → Error frecuente → Qué hacer en la práctica →
  Checklist → Puente).
- **SC-004**: el glosario consolidado cubre el 100 % de los términos
  técnicos usados en el cuerpo expositivo. No quedan términos huérfanos.
- **SC-005**: el ejemplo recurrente declarado en el brief aparece como
  hilo conductor en al menos el 80 % de los capítulos.
- **SC-009**: cada concepto obligatorio del brief queda respaldado por al
  menos un registro de citación válido contra
  `contracts/citation-record.schema.json`.

## Estructura del directorio

```text
tests/editorial-pilot/
├── README.md         # Este archivo.
├── sandbox/          # Repo editorial generado por T051 (no se commitea,
│                     # listado en .gitignore). El operador del piloto
│                     # ejecuta install/install.sh apuntando aquí dentro
│                     # y trabaja contra ese sandbox sin contaminar el
│                     # repo canónico.
└── evidence/         # Evidencia archivada. Sí se commitea.
    └── <YYYY-MM-DD>-<topic>/
        ├── spec.md
        ├── research.md
        ├── plan.md
        ├── chapters/
        ├── findings.md
        ├── checklists/
        ├── manifest.json
        └── validation-report.md
```

Cada ejecución del piloto crea **un nuevo directorio** dentro de
`evidence/` con la fecha y el tema. Nunca se reescribe ni se mueve un
piloto pasado.

## Mapeo a Success Criteria

La tabla siguiente conecta cada SC de la spec con el artefacto del
piloto que lo valida y la skill responsable de generarlo. Sirve como
guía operativa al revisar la evidencia.

| SC      | Métrica                                                                    | Artefacto del piloto que lo valida                                       | Skill responsable             |
|---------|----------------------------------------------------------------------------|---------------------------------------------------------------------------|-------------------------------|
| SC-001  | Instalación inicial completada en menos de 5 minutos.                      | `evidence/<...>/install-log.txt` con timestamp inicio/fin.                | `writeonmars-install`         |
| SC-002  | Cierre del proyecto sin hallazgos críticos abiertos.                       | `evidence/<...>/findings.md` y reporte de `writeonmars-close-project`.    | `writeonmars-close-project`   |
| SC-003  | 100 % de capítulos con las nueve secciones didácticas.                     | Inspección de `evidence/<...>/chapters/*.md` + `validation-report.md`.    | `writeonmars-redaccion`       |
| SC-004  | Glosario consolidado cubre el 100 % de términos técnicos.                  | `evidence/<...>/glossary.md` cruzado contra cuerpo de capítulos.          | `writeonmars-glossary`        |
| SC-005  | Ejemplo recurrente presente en ≥ 80 % de capítulos.                        | Búsqueda del nombre del ejemplo recurrente en `evidence/<...>/chapters/`. | `writeonmars-redaccion`       |
| SC-006  | Reducción ≥ 40 % del tiempo total por paralelización.                      | Comparación de cronómetros baseline (T064a) vs paralelo (T065).           | `writeonmars-redaccion --parallel` |
| SC-007  | Skills nucleares portables a otros agentes (scaffolding listo en v1).      | Existencia de `agents/<otro-agente>/prompts/` poblado.                    | n/a (cross-cutting)           |
| SC-008  | Actualización trazable de skill bundled en menos de 15 minutos.            | Registro temporal en `docs/maintenance/skill-update-procedure.md`.        | `writeonmars-update`          |
| SC-009  | Al menos un registro de citación válido por concepto obligatorio.          | `evidence/<...>/research.md` validado con `tests/lib/validate-citation.sh`. | `writeonmars-research`        |

## Reglas de no-borrado

La evidencia de pilotos pasados es material de auditoría:

- MUST conservarse íntegra. No se reescribe, no se reorganiza ni se
  reemplaza por una versión "mejorada".
- Si un piloto encuentra un defecto del framework, se documenta en
  `validation-report.md` y se abre una nueva iteración en otro
  directorio. La evidencia original permanece como registro del fallo
  detectado y resuelto.
- Las correcciones tipográficas a un `validation-report.md` están
  permitidas siempre que se registren en el propio archivo con fecha y
  motivo. Ninguna corrección puede cambiar la conclusión del piloto.
- `sandbox/` es desechable: solo el contenido de `evidence/` cuenta como
  registro canónico.
