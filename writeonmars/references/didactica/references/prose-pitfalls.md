# Prose-level pitfalls in technical guides

Microstyle catalogue for technical writing aimed at professional developers. Companion to `SKILL.md`. Use it when reviewing prose that is structurally sound but reads as compressed, mechanical or robotic.

The general diagnosis behind every entry below: a prose problem usually does not come from lack of information. It comes from **excess compression**. The writer summarized their own notes instead of guiding the reader.

The remedy pattern, applicable to all entries below:

> **situación → explicación → consecuencia práctica**

A reader should not have to reconstruct intention from a tight phrase. A guide that earns its name guides.

Eight pitfalls follow, each with the pattern, why it fails, examples, and the rewrite rule.

---

## 1. Compressed sentences (concept + metaphor + conclusion in one line)

**Symptom.** A single sentence trying to deliver three things at once: define, illustrate and conclude.

**Why it fails.** The reader has to unpack the sentence in their head. The text reads like internal author notes, not like an explanation written for someone else.

**Example — bad:**

> Cabe en la cabeza, deja sitio para que cada concepto técnico aterrice en algo reconocible y evita el bullet hipotético del tipo "imaginemos un sistema X".

(Three ideas, two metaphors, one English term, one nested example. The reader has to map all of them.)

**Example — better:**

> El ejemplo es pequeño a propósito. Una API REST de tareas es fácil de seguir y es suficiente para hablar de validación, tests, contexto, memoria, herramientas y revisión de PRs sin cambiar de escenario en cada capítulo.

**Rewrite rule.** If a sentence contains *concept + metaphor + conclusion*, split it. Two clear sentences beat one clever one.

---

## 2. Vague pronouns ("lo", "eso", "esto", "aquello")

**Symptom.** A pronoun is doing work the noun should be doing.

**Why it fails.** The reader has to scroll back to figure out what the pronoun refers to. Even if the referent is technically deducible, the cognitive cost is real and the prose feels disjointed.

**Examples — bad:**

> Eso cambia la forma de revisar.
>
> Desarrolladores que sienten que "lo aceptan a ciegas" cuando el agente entrega un PR y quieren cambiar eso.

**Examples — better:**

> Tener una _spec_ cambia la revisión: ya no preguntamos si el código "parece bien", preguntamos si cumple lo acordado.
>
> Personas que ya reciben PRs generados por agentes y sienten que a veces aprueban cambios que no entienden del todo.

**Rewrite rule.** Replace `lo / eso / esto` with the concrete subject the first time it appears. The second mention can pronominalize without ambiguity.

---

## 3. Aphorism chains ("no es X: es Y" repeated)

**Symptom.** Section after section closing with a sentencious "no es X: es Y", "no se hace A: se hace B", or similar negation-affirmation pair.

**Why it fails.** Individually these phrases land. Stacked, they manufacture a slogan tone and the text starts to feel like a manifesto written for posters.

**Examples — bad (cluster):**

> La economía no es opcional: es estructural.
>
> Cuando el presupuesto importa, no se estima: se mide.
>
> Delegar lo que no podemos juzgar es no delegar: es aceptar a ciegas.

**Examples — better:**

> El coste forma parte del diseño del agente. Cada archivo leído, cada resultado de herramienta y cada respuesta generada vuelve a ocupar contexto y presupuesto.
>
> Si el coste importa, mide una sesión real. Las estimaciones a ojo suelen fallar porque el gasto depende del historial, las herramientas, las iteraciones y la salida generada.

**Rewrite rule.** Maximum **one aphoristic phrase per chapter**, and only when it earns its place. The rest of the punchy lines turn into explanations with subject + cause.

---

## 4. Mixed metaphors

**Symptom.** Two or more incompatible images in the same sentence (spatial + landing + "in the hand" + "moves the needle").

**Why it fails.** The reader has to reconcile images that don't belong together, which costs more than the metaphor saves.

**Examples — bad:**

> deja sitio para que cada concepto técnico aterrice en algo reconocible
>
> Modelos parecidos, montados en harnesses distintos, dan agentes que se sienten radicalmente distintos en la mano.

**Examples — better:**

> permite explicar cada concepto con el mismo ejemplo
>
> El mismo modelo puede comportarse de forma muy distinta según el harness que lo rodee.

**Rewrite rule.** One metaphor per concept, and only if it clarifies. If the metaphor obliges reinterpretation, drop it. Domestic and mechanical metaphors over cosmic or sensorial.

---

## 5. Anglicisms that don't add precision

**Symptom.** English terms peppered through Spanish prose where a clean Spanish word exists and is unambiguous.

**Whitelist (keep in English):** `harness`, `MCP`, `tool use`, `system prompt`, `context window`, `prompt`, `skill`, `spec`, `output`/`input` only when discussing pricing.

**To translate by default:**

| English          | Better in Spanish                              |
| ---------------- | ---------------------------------------------- |
| mental model     | modelo mental                                  |
| scope            | alcance                                        |
| baseline         | línea base / punto de partida                  |
| inline           | dentro del propio código / mezclada en lógica  |
| datasource       | fuente de datos                                |
| built-in         | nativa / integrada                             |
| bullet           | viñeta / lista                                 |
| fork             | duplicación de mantenimiento (cuando es figurado) |

**Rule.** Use English only when the term is the canonical one in the discipline or when translating creates ambiguity. Inertia is not a reason.

---

## 6. Dry transitions ("Vamos a verlo", "Quedan tres categorías")

**Symptom.** Bare connector at the start of a paragraph or after a list, with no explanation of why we're moving from idea A to idea B.

**Why it fails.** The text reads like an outline, not a finished document. The reader senses the seams.

**Examples — bad:**

> Vamos a ese tema.
>
> Quedan tres categorías:
>
> Vamos a verlo.

**Examples — better:**

> Ese presupuesto nos lleva al siguiente problema: los tokens.
>
> Con esa distinción podemos separar tres casos:
>
> Para entender por qué ocurre, hay que mirar qué entra realmente en el contexto.

**Rewrite rule.** Every transition should answer **why now**: why this idea follows that one, why this list of three appears here.

---

## 7. Mechanical repetition of section titles and entries

**Symptom A.** Every chapter closes with a section called the same: "## La trampa común" five chapters in a row. Every chapter enters the recurring example with "Volvamos a…".

**Why it fails.** Predictable bones lower cognitive load. Predictable *skin* manufactures template feel.

**Mechanical (bad):**

```
## La trampa común: confundir A con B
## La trampa común: confundir C con D
## La trampa común: confundir E con F
```

**Varied (better):**

```
## A no es B
## Dónde se suele escapar el coste
## Lo que una ventana grande no soluciona
```

**Symptom B.** Every entry to the recurring domain example uses "Volvamos al ejemplo de…".

**Varied (better):**

> En la API de tareas, esto aparece de forma concreta cuando…
>
> El mismo problema se ve en el _endpoint_ POST /tasks.
>
> Pensemos en la paginación de GET /tasks.

**Rewrite rule.** Same structure across files; varied wording in titles and entries. Three alternative phrasings per recurring block beats one fixed phrasing.

---

## 8. Absolute claims that the audience can puncture

**Symptom.** A sentence sounds clean and quotable, but a senior developer reading it knows the edge case that breaks it.

**Why it fails.** Loss of trust. The reader stops reading the sentence and starts arguing with it.

**Examples — bad:**

> Si algo no está en el contexto, para el modelo no existe.
>
> El agente no recibió un script.

**Examples — better:**

> Si algo no está en el contexto ni puede recuperarse mediante una herramienta, el modelo no puede usarlo de forma fiable en esa llamada.
>
> En esta sesión, el agente no recibió un script: decidió cada paso a partir del estado del repositorio.

**Rewrite rule.** Add scope words when the universal version overshoots: *en una sesión típica, normalmente, en muchos `harnesses`, en este ejemplo*. Precision earns more trust than slogan.

---

## Bonus: reader-orientation cues

Not a pitfall, a tactic. The opposite move of compression. Periodic phrases that lower the reader's cognitive load by signalling what to retain and what to skim.

Examples that work in technical Spanish:

- **"Quédate con esta idea."** — when one paragraph carries the whole point.
- **"No necesitas memorizar X."** — when a detail is shown for completeness.
- **"En la práctica esto significa…"** — bridging concept to action.
- **"El síntoma típico es…"** — anchoring abstraction to a recognizable case.
- **"Si solo lees esta sección, lee esto."** — explicit fast path.

A guide aimed at adult professionals respects their attention more by signalling what matters than by being uniformly dense.

---

## Microedit pass — the order to apply the rules

When auditing prose that is structurally sound but reads off, run in this order:

1. **Vague pronouns** (entry #2). The cheapest fix and the one with most impact on readability.
2. **Compressed sentences** (entry #1). Split anything that mixes more than two ideas.
3. **Aphorism chains** (entry #3). Keep one per chapter at most.
4. **Mechanical repetition** (entry #7). Vary titles and entries.
5. **Dry transitions** (entry #6). Add a "why now" to every connector.
6. **Mixed metaphors** (entry #4). Demote or remove.
7. **Unnecessary anglicisms** (entry #5).
8. **Absolute claims** (entry #8).

Do not run them all in one pass with the goal of "humanize". Run each pass with a single rule in mind. The text will keep its voice and lose the friction.
