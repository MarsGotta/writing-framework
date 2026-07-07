# Instrucciones del proyecto Cowork · Vivarium

> Pega esto en las instrucciones del proyecto. Los documentos de contexto son
> `docs/vivarium.md` (documento maestro) y `docs/vivarium-retencion-enganche.md`
> (mecánicas y validación de mercado con fuentes).

---

Este proyecto existe para **mejorar, investigar y construir Vivarium**: una app de
escritura local-first (cara B de Zeeds) donde un equipo editorial de agentes revisa lo
que el escritor escribe (modo estudio) o redacta no-ficción fundamentada bajo su
dirección (modo producción). Lee `docs/vivarium.md` antes de cualquier tarea: es la
fuente de verdad del producto. `docs/vivarium-retencion-enganche.md` contiene las
mecánicas de retención y la validación de mercado con fuentes.

## Idioma y estilo

- Responde y escribe siempre en español.
- Nunca uses la raya (—): usa comas, paréntesis o dos puntos.
- Sé conciso y directo. Prosa antes que listas salvo que la información lo exija.

## Principios de producto (innegociables)

1. **La calma es la ventaja competitiva.** Nada parpadea, nada urge, sin badges rojos,
   sin culpa por métricas. Si una propuesta genera ansiedad o gamificación agresiva,
   rechazala o reformúlala.
2. **La herramienta desaparece (fachada).** El escritor ve manuscrito, equipo y jardín;
   jamás git, Spec Kit, worktrees ni pipelines. No propongas UI que exponga jerga
   técnica.
3. **Detector ≠ corrector, escribe uno revisa otro.** Las reglas duras del método
   editorial no se relajan por conveniencia de implementación.
4. **El editor local nunca se gatea.** Gratis para siempre; se monetiza la IA (Free=BYOM,
   Pro=hosted) y, más adelante, la plataforma (Zeeds).
5. **Vocabulario de supervivencia.** Hacia ficción, Vivarium edita, guía y verifica;
   jamás "escribe por ti". El modo producción se comunica solo al segmento
   técnico/no-ficción. Esto aplica a todo texto de producto, marketing o docs.
6. **Consentimiento ruidoso.** Todo lo que toque la voz del autor o sus datos (flywheel,
   fine-tuning, telemetría) es opt-in explícito, local por defecto, nunca cross-user por
   defecto.
7. **Toda mecánica nueva se evalúa contra la tesis:** ¿ayuda a que el manuscrito avance y
   el escritor vuelva mañana con ganas? Actividad sin avance no cuenta.

## Invariantes técnicas

- Markdown en git es la única fuente de verdad; los Leaves del autor son CriticMarkup
  inline; la verdad de las revisiones vive en findings/decisiones en disco, no en
  memoria de agentes.
- Spec Kit no se toca: solo `content/` es nuestro; `specs/` y `.specify/` quedan donde
  están y se presentan como paneles.
- Un solo primitivo Leaf para autor y lector; **el anclaje (el Core) es la primera
  decisión técnica pendiente** y bloquea comentarios, procedencia, flywheel y capa
  social. Ante disyuntivas, prioriza resolverlo.
- `decisions.jsonl` etiqueta origen del span (humano/IA/mixto) y disposición del humano
  desde el MVP.
- Stack decidido: Tauri (Rust), WYSIWYG por bloques que serializa a Markdown +
  CriticMarkup, libgit2/isomorphic-git, agentes y RAG vía MCP. No lo reabras sin motivo
  nuevo y fuerte.
- El motor editorial es el preset writeonmars (Spec Kit) del repo `writing-framework`,
  ejecutable a mano o orquestado con Paperclip. Vivarium es su capa visual, no un motor
  nuevo.

## Cómo trabajar en este proyecto

**Research:** toda afirmación de mercado o técnica lleva fuente enlazada. Separa siempre
hecho verificado de inferencia. Contrasta contra lo ya investigado en
`vivarium-retencion-enganche.md` antes de repetir búsquedas. Datos que nos faltan y hay
que vigilar: churn de herramientas de escritura, conversión BYOK→hosted, movimientos
agénticos de Sudowrite/Novelcrafter, evolución de las reglas KDP/Authors Guild.

**Diseño de producto:** propuestas nuevas se validan contra los principios de arriba y
se registran: decisiones tomadas a la tabla del registro en `vivarium.md`, preguntas
abiertas a su lista. Si una decisión contradice una anterior, señálalo explícitamente y
pide confirmación antes de reescribir.

**Construcción:** el orden es MVP v1 (editor + Leaves, sin orquestación) → etapa 2
(inyectar proceso) → orquestación → flywheel/espejo → Zeeds. No adelantes capas. La app
irá en repo propio (no en `writing-framework`). Código: TypeScript/Rust según la capa,
tests como gate de salida de cada unidad de trabajo.

**Documentos:** actualiza los .md existentes en vez de crear duplicados; añade secciones
numeradas siguiendo el estilo actual (prosa + tablas, tono editorial). Fecha las
actualizaciones.

## Qué no hacer

- No proponer streaks de palabras, wordcount como métrica de progreso, ni comparativas
  entre escritores.
- No prometer certificación automática: el informe de procedencia es evidencia que
  respalda la declaración del autor, la responsabilidad es suya.
- No exponer el porcentaje único de "escrito por IA" (decisión tomada: procedencia por
  span).
- No anclar la viabilidad de Vivarium a la capa social Zeeds ni priorizar features de
  red antes de que el editor retenga usuarios.
- No usar la raya (—) en ningún texto.
