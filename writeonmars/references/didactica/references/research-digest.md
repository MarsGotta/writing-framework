# Research Digest

> **Nota (2026-07-04)**: este documento se conserva en inglés a propósito. Es
> material de consulta con las fuentes originales, no una referencia operativa
> del pipeline: la skill (`../SKILL.md`) y el catálogo de defectos
> (`prose-pitfalls.md`) ya están en español y son lo que los agentes cargan al
> redactar y revisar.

Full research synthesis behind the `technical-guide-design` skill. Based on 3 Opus research reports + a Perplexity base report on e-learning best practices.

---

## 1. Diátaxis Framework (Daniele Procida)

**Canonical current system** for structuring technical docs. Defines 4 mutually exclusive modalities by user need.

| Modality | Orientation | Objective | Analogy |
|---|---|---|---|
| **Tutorial** | Learning | Acquire minimum competence | Teaching a child to cook |
| **How-to guide** | Task | Solve concrete problem | Cooking recipe |
| **Reference** | Information | Describe the machine | Encyclopedia / API docs |
| **Explanation** | Understanding | Illuminate the "why" | Magazine article |

### Critical distinctions

- **Tutorial**: author guarantees success; reader makes no decisions. For absolute beginners in the task.
- **How-to**: assumes competence; tackles real user problem with their own variables.
- **Reference**: dry, precise, consultable. Doesn't teach or explain — describes.
- **Explanation**: discursive, allows opinions, historical context, discarded alternatives.

### The two orthogonal axes

```
                  PRACTICE              THEORY
  LEARNING     |  Tutorial          |  Explanation
  APPLICATION  |  How-to guide      |  Reference
```

Axis 1: action (practice) vs cognition (theory).
Axis 2: study (acquire skill) vs work (apply skill).

Each quadrant serves a distinct mental state — mixing confuses the reader.

### Common error

Mixing all 4 in one document. A tutorial that digresses into architecture breaks learning flow; a how-to with philosophy loses the in-a-hurry reader; a reference with tutorials becomes unconsultable.

### Diátaxis vs Divio (predecessor)

Procida published Divio version ~2017. Diátaxis (2021+) refined it:
- Clearer terminology ("topic guide" → "explanation").
- Articulates the 2 orthogonal axes explicitly.
- Separation is structural across the whole project, not per-page.
- More principle-based than prescriptive folder structure.

Sources:
- https://diataxis.fr/
- https://diataxis.fr/theory/
- https://documentation.divio.com/ (predecessor)

---

## 2. Google Developer Documentation Style Guide

Applicable principles for learning material:

- **Task-based writing**: verbal titles ("Configure Jest" not "Jest configuration").
- **Present tense, active voice**: "The function returns X" not "X will be returned".
- **Second person ("you")**: engages reader. Avoid "we" (ambiguous about who acts).
- **Numbered steps** only when order matters; bullets otherwise.
- **Consistent terminology**: one concept = one term, always. Glossary required.
- **Short sentences** (< 25 words), paragraphs < 5 sentences.
- **Code samples** self-contained, copyable, working in isolation.

Source: https://developers.google.com/style

---

## 3. Write the Docs

Professional community of technical writers. Principles:

- **Docs as code**: docs live in the repo, reviewed in PRs, with CI, versioned with code.
- **Minimal viable docs**: publishing incomplete beats not publishing. Iterate.
- **Progressive disclosure**: simple first, advanced details after. Avoid overwhelm.
- **Content reuse / single source of truth**: shared snippets (includes), not copy-paste.
- **Reader-oriented architecture**, not system-oriented.

Source: https://www.writethedocs.org/guide/

---

## 4. Andragogy (Malcolm Knowles) — adult learners

The 6 principles and operational translation:

1. **Need to know**: open each section with "why this matters" (e.g. "without this pattern your test breaks whenever the DOM changes"). No theory before the pain.
2. **Autonomy / self-concept**: guide allows skipping sections, choosing path (happy path vs deep dive), self-pacing. Never "do it in this order or you won't understand".
3. **Prior experience as resource**: reference what they already know ("if you come from Jest, RTL feels familiar except in X"). Invite comparison with their current stack.
4. **Problem-centered**: organize by problem ("how to test a form with async validation"), not by subject ("chapter 3: matchers"). Each exercise solves a real case.
5. **Internal motivation**: connect to KPIs they already care about (fewer prod bugs, faster PRs, less "works on my machine").
6. **Readiness**: content enters when they'll apply it this week. Just-in-time, not just-in-case.

Reference: Knowles, M. S. (1984). *The Adult Learner: A Neglected Species*.

---

## 5. Active learning (qualitative principle, not Dale's Cone)

Active engagement with material outperforms passive consumption. This is the empirically validated principle, confirmed by Freeman et al. (2014), a meta-analysis of 225 studies on STEM higher education: https://www.pnas.org/doi/10.1073/pnas.1319030111

**Do not use** the "Dale's Cone of Experience" retention percentages (~10% reading / ~75% doing / ~90% teaching). Those numbers are widely cited but are a fabrication: Edgar Dale never published them, and the data behind them does not exist. Treating them as evidence undermines the rest of the digest.

**Do use** the qualitative implication for guide design:

- Each concept followed by an action (exercise, prompt, decision the reader has to take), not just a paragraph.
- Include moments where the reader has to articulate the concept ("explain to your pair why this test fails", "predict the output before running the snippet"), since articulation reveals gaps.
- Worked examples (section 6 of this digest) are the workhorse for moving novices from passive reading to active schema-building.

The proportion between hands-on and reading is a context decision (audience, time available, format), not a rule with fixed percentages.

---

## 6. Cognitive Load Theory (Sweller) applied to code

### Three loads

- **Intrinsic**: inherent to the concept (async testing with `waitFor` is intrinsically more complex than a sync assert). Not reducible, only sequenceable.
- **Extraneous**: hidden imports, unshown setup, `foo/bar` names, examples with 3 new concepts simultaneously. This kills learning. Solution: self-contained snippets, one new concept at a time.
- **Germane**: useful effort of building mental schemas. Enhanced with worked examples + fading.

### Key effects

- **Worked-example effect** (Sweller & Cooper 1985): showing complete resolved solutions helps juniors (lower load).
- **Expertise reversal effect** (Kalyuga 2003): the SAME worked examples **confuse seniors** — they already have the schema, reading step-by-step generates extraneous load.
- **Solution for mixed audience**: worked example + "if you already know this, skip to challenge X".

References:
- Sweller, J. (2011). *Cognitive Load Theory*. https://doi.org/10.1016/B978-0-12-387691-1.00002-8
- Kalyuga expertise reversal: https://doi.org/10.1207/S15326985EP3801_4

---

## 7. ZPD (Vygotsky) and scaffolding with fading

Recommended graduation:

- **Exercise 1 guided**: code 80% written, complete the assert.
- **Exercise 2 semi-guided**: hints, hints about what to test.
- **Exercise 3 autonomous**: only requirement "test this component".

Scaffolding must disappear. Explicit fading: "in the next section I won't give you the `describe` structure anymore".

Source: Vygotsky, *Mind in Society* (1978), Harvard University Press.

---

## 8. Deliberate practice (Anders Ericsson)

Requirements:

- Specific objective
- **Immediate feedback**
- Outside comfort zone
- Repetition with variation

Applied: each exercise has verifiable success criterion (test passes/fails), progressive variation of the same pattern (test 3 different forms, not 1), and explicit reflection ("what changed between exercise A and B?").

Reference: Ericsson, K. A. (1993). *The Role of Deliberate Practice*. https://doi.org/10.1037/0033-295X.100.3.363

---

## 9. Motivation of adult professional developer

### Works

- Real problems from their stack
- Ownership of pace
- Recognizing expertise ("you know what a mock is, but let's see why `vi.spyOn` differs")
- Results applicable to current sprint

### Doesn't work

- Abstract theory in isolation
- Tone "let's learn together what a function is"
- Generic TODO-list examples
- Omniscient narrator explaining the obvious

**Senior devs abandon in 3 minutes if they detect condescension.**

---

## 10. Microlearning and spaced repetition

Blocks of 10-20 min respect adult attention window (Bradbury, 2016) and allow integration between short real-work sessions.

Spaced repetition (Cepeda et al., 2006): revisiting concepts on days 1, 3, 7 consolidates better than one 2h session.

Structure: modules < 20 min, each module with a "recall" of the previous.

Source: https://doi.org/10.1037/0033-2909.132.3.354

---

## 11. Blended learning (sync + async)

**Sync contributes**: social motivation, unblocking doubts, collective energy, accountability.

**Async contributes**: depth, own pace, rereading, deferred application.

The written guide must be **self-sufficient** (someone who missed live can follow) but **complementary** (the live session resolves what text can't: debate, real-time Q&A, live pairing).

---

## 12. Code example design — detailed

### MVCE (Minimum Viable Code Example)

Stack Overflow principle, derived from SSCCE (Yoakum-Stover):
- **M**inimum — remove anything not contributing to the point.
- **V**iable — compiles and runs.
- **C**omplete — nothing hidden.
- **E**xample — representative.

For a testing guide: cut accessory business logic, keep imports explicit, eliminate mocks not relevant to the concept.

### Progressive disclosure (Nielsen)

First: trivial test (`expect(2+2).toBe(4)` with Vitest).
Then: add layer by layer — a `describe`, then `beforeEach`, then mocks, then `TestBed` of Angular.

Never show the "realistic final example" at once.

Source: https://www.nngroup.com/articles/progressive-disclosure/

### Runnable vs snippet

- **Runnable** (StackBlitz/repo): for first example of each chapter and the "guiding project".
- **Snippet inline**: for illustrating a specific concept.
- Rule: if reader must infer > 3 lines (imports, setup), make it runnable.

### Self-contained

Each didactic snippet must include relevant imports. Omitting `import { describe, it, expect } from 'vitest'` is acceptable only if declared once at chapter start as convention.

### Worked examples (educational research)

**Sweller & Cooper (1985)** demonstrated: students who study worked examples solve subsequent problems faster and with fewer errors than those solving from scratch — reduce **extraneous cognitive load**.

**Backward fading** (Renkl & Atkinson, 2003): step 1 complete, step 2 to complete, step 3 to complete. In Testing Library: first example with `render`+`getByRole`+`expect` complete; second, reader writes the `expect`; third, writes `getByRole`+`expect`.

**Self-explanation prompts** (Chi et al., 1989): embedded questions like "why do we use `findBy` and not `getBy` here?" before showing the answer.

### Naming

**Real domain names** (`user`, `cart`, `order`, `product`) when the example teaches an applied pattern. **Placeholders** (`foo`, `bar`) only when concept is purely syntactic (e.g. structure of `describe`/`it`). Avoid mixing.

**Consistency**: choose ONE simple domain for the whole guide (e.g. "TodoApp" or "CartApp") and reuse in Angular and Vue. Reduces cognitive load. Avoid **Frankenstein examples**: a `User` test that suddenly renders `<ProductList>`.

### Before/after

Show "bad" code first only when it's a common anti-pattern the reader probably already writes (fragile tests with excessive `getByTestId`). Use diff syntax or comments `// ❌ fragile` vs `// ✅ resilient`.

**Risk** (familiarity effect, Anderson): mark anti-pattern visually (strikethrough, red, `BAD:` label) to reduce incorrect memorization. Never leave anti-pattern without correction on same page.

### Annotations

- Inline comments `// <-- here the service is mocked` are more effective than separate prose (contiguity principle).
- Numbered callouts (①②③) with explanation below work well for long snippets.

### Length

- 5–15 lines optimal.
- 30 max.
- Snippets > 30 lines should be divided or linked to runnable repo.

### Code golf vs readability

Always choose the **explicit** version over the elegant in didactic context:
- `const result = add(2, 3); expect(result).toBe(5);` over `expect(add(2,3)).toBe(5)` the first time.
- Once taught, can collapse.

Avoid aggressive destructuring, chained nullish operators, one-liners in new-concept examples.

### Tests as examples

- **AAA** explicit with `// Arrange / // Act / // Assert` comments in first examples; can omit when reader has internalized.
- **Test language**: choose ONE (Spanish `it('debería sumar...')` or English `it('should add...')`) and keep across all files — language switching distracts. For Spanish-speaking audience learning Vitest, Spanish is more accessible.
- **One concept per test**: one main assert per `it` in didactic context (production code can have more).

### Common errors

- `expect(1+1).toBe(2)` without real context.
- "Realistic" example with 200 lines of setup hiding the technique.
- Abrupt Angular↔Vue switch without transition — use clear headings, maintain parallelism.
- Snippets that don't compile: missing `import`, implicit types. Validate in CI.
- Outdated versions: mark each chapter with Vitest/Stryker/Angular/Vue version + validation date.

### Contiguity principle (Mayer)

Text explanation adjacent to code, not at the end. Use numbered legends when more than one point to explain.

Source: Mayer, *Multimedia Learning* (Cambridge): https://www.cambridge.org/core/books/multimedia-learning/

### Code first vs concept first

- **Concept first**: for abstract concepts (what is a mutation in Stryker).
- **Code first**: for syntactic patterns (how to write a spy with `vi.fn()`).
- Alternate deliberately by case.

---

## 13. Guide structure (e-learning template)

A typical effective guide includes:

1. Context and objectives (what you'll learn and why it matters).
2. Prerequisites and needed resources (with links and downloadable files).
3. Time estimate per section.
4. "Warm-up" or activation (short questions, diagnostic challenge).
5. Step-by-step development: small sections, each with brief explanation, example, guided mini-task.
6. Final synthesis (visual or textual summary, checklist).
7. Open consolidation activity (mini-project or example variation).
8. Self-evaluation with simple rubric.
9. Additional resources and optional readings.

Universities publishing guides for online content insist on maintaining this structure **predictably between units** to reduce cognitive load.

---

## 14. Iteration and continuous improvement

Design is iterative. After piloting a guide:

- Collect data on friction points (real vs estimated times, recurring doubts, frequent errors).
- Document and version guides.
- Incorporate small changes between editions rather than complete redesigns.
- Maintain proposed improvements list based on usage evidence.

---

## 15. Full source list

### Frameworks and style guides
- Diátaxis: https://diataxis.fr/
- Grand Unified Theory: https://diataxis.fr/theory/
- Divio (predecessor): https://documentation.divio.com/
- Google Developer Style: https://developers.google.com/style
- Google Code samples: https://developers.google.com/style/code-samples
- Microsoft Style Guide: https://learn.microsoft.com/en-us/style-guide/developer-content/code-examples
- Write the Docs: https://www.writethedocs.org/guide/
- Docs as code: https://www.writethedocs.org/guide/docs-as-code/

### Cognitive & learning science
- Knowles, *The Adult Learner*: https://www.sciencedirect.com/book/9780128117583
- Sweller CLT: https://link.springer.com/article/10.1007/s10648-019-09465-5
- Sweller & Cooper (1985) worked examples: https://onlinelibrary.wiley.com/doi/10.1207/s1532690xci0201_3
- Kalyuga expertise reversal: https://doi.org/10.1207/S15326985EP3801_4
- Renkl & Atkinson (2003) backward fading: https://psycnet.apa.org/record/2003-01403-003
- Chi et al. (1989) self-explanation: https://onlinelibrary.wiley.com/doi/10.1207/s15516709cog1302_1
- Mayer, *Multimedia Learning*: https://www.cambridge.org/core/books/multimedia-learning/
- Ericsson deliberate practice: https://doi.org/10.1037/0033-295X.100.3.363
- Cepeda spaced practice: https://doi.org/10.1037/0033-2909.132.3.354
- Freeman active learning meta-analysis: https://www.pnas.org/doi/10.1073/pnas.1319030111

### Practical / industry
- Nielsen Progressive Disclosure: https://www.nngroup.com/articles/progressive-disclosure/
- Stack Overflow MCVE: https://stackoverflow.com/help/minimal-reproducible-example
- Kent C. Dodds, *Common mistakes with React Testing Library*: https://kentcdodds.com/blog/common-mistakes-with-react-testing-library
- Stryker Mutator docs: https://stryker-mutator.io/docs/
