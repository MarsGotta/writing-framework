---
name: technical-guide-design
description: >
  Design, review, restructure or micro-edit technical guides, manuals, tutorials,
  workshops and engineering playbooks for professional developers. Combines
  evidence-based teaching (Diátaxis, andragogy, cognitive load theory, worked
  examples) AND prose-level microstyle. Trigger for structural work: "diseña una
  guía", "revisa este temario", "mejora el material de este taller", "estructura
  este tutorial", "cómo enseñar X", "crea un workshop sobre Y". Trigger for
  microedition: "haz que suene menos robótica", "frases comprimidas", "hazlo más
  natural", "mejora la prosa de la guía", "limpia el tono plano", "frases inconexas",
  "tono de eslogan". Also when evaluating existing docs/guides for teaching
  effectiveness or operational utility.
user-invocable: true
---

# Technical Guide Design

Evidence-based playbook for designing, reviewing and restructuring technical learning material aimed at **professional developers** (not university students, not absolute beginners). Synthesizes Diátaxis, andragogy (Knowles), cognitive load theory (Sweller), worked examples (Renkl & Atkinson) and documentation style guides (Google, Write the Docs).

The skill covers two layers, in this order of impact:

1. **Structural** — modalities, cognitive load, exercises, file organization. Most of this document.
2. **Microstyle** — prose-level prose pitfalls that make a structurally sound guide feel mechanical or robotic. Catalogue with concrete before/after examples in `./references/prose-pitfalls.md`.

A guide that fails structurally will not be saved by good prose; a guide that gets the structure right will still feel artificial if the prose-level rules are ignored.

Use this skill when:

- Creating a new guide, tutorial, workshop or technical documentation set.
- Reviewing existing material for pedagogical soundness.
- Restructuring a mixed-modality document that has become hard to navigate.
- Designing the complement between a live session and async written material.
- Editing prose in a guide that is structurally sound but reads as compressed, robotic or template-driven (jump directly to `./references/prose-pitfalls.md`).

## Core principle: separate modalities (Diátaxis)

Every piece of technical learning content serves **one dominant** purpose. Mixing modalities equally in the same document is the #1 cause of poor guides.

| Modality | Orientation | Reader state | Example |
|---|---|---|---|
| **Tutorial** | Learning by doing | "I'm new, take me by the hand" | Your first test with Vitest |
| **How-to** | Task-oriented | "I have problem X, how do I solve it" | How to mock an HTTP service |
| **Reference** | Information lookup | "What's the exact syntax of X" | Table of Jasmine→Vitest equivalences |
| **Explanation** | Understanding | "Why does X work this way" | Why mutation testing vs coverage |

Two orthogonal axes underneath:

- **Practice (action) ↔ Theory (cognition)**
- **Acquisition (learning) ↔ Application (working)**

**Rule.** Label each file/section with **one dominant modality** in its frontmatter. Splitting is the default when modalities mix.

**Permitted hybrid.** A dominant modality can host a **micro-section of another modality** at the closing of the file when it directly serves the dominant one. Typical case: a chapter of *explanation* about a concept ending with a small *reference* block ("Where each tool implements this") so the reader does not have to leave context for the operational detail. Mark the micro-section visually (own H2, table, or callout) so the reader can skim or skip it.

What still does not work: equal-weight mixing (a tutorial half-built as reference table). If the file does two modalities in equal measure, split.

## Pedagogical principles for adult devs (andragogy)

Professional developers are adult learners. They:

1. **Need to know why** before what — open each section with the pain/problem, not theory.
2. **Value autonomy** — offer paths ("quick path" vs "deep dive"), never a single forced order.
3. **Bring prior experience** — reference what they already know ("if you come from Jest, vi.fn feels familiar").
4. **Are problem-centered, not subject-centered** — organize by "how do I test an async form" not by "chapter 3: matchers".
5. **Have internal motivation** — connect to real KPIs (fewer prod bugs, faster PRs, less flakiness).
6. **Learn just-in-time, not just-in-case** — content hits when they'll apply it this week.
7. **Welcome reader-orientation cues** — explicit signposts like "quédate con esta idea", "no necesitas memorizar X", "el síntoma típico es Y", "si solo lees esta sección, lee esto" lower cognitive load without being condescending. Use them at the close of dense paragraphs.

**Never do** with professionals: paternalistic tone, "what is a function", blocking solutions "so they think", emoji-rich cheer, explaining the terminal.

## Cognitive load: the three loads

- **Intrinsic**: inherent complexity — irreducible, only sequence it.
- **Extraneous**: bad design choices that add friction — minimize aggressively.
- **Germane**: the useful effort of building mental schemas — maximize via worked examples + fading.

Key effects to know:

- **Worked example effect** (Sweller & Cooper 1985): studying a fully-solved example is more efficient than solving from scratch, for novices.
- **Expertise reversal effect** (Kalyuga 2003): the SAME worked examples confuse experts. Provide "if you already know X, skip to challenge Y".
- **Backward fading** (Renkl & Atkinson 2003): step 1 complete → step 2 partial → step 3 blank. Graduate scaffolding.

## Code example design

Rules for every code snippet:

1. **MVCE** (Minimum Viable Code Example): runnable, complete, representative, nothing extra.
2. **Self-contained**: imports visible (or declared once as chapter convention). Reader should not infer >3 lines.
3. **Progressive disclosure**: first snippet trivial, add layers one at a time. Never open with the "realistic final".
4. **Single domain across the guide** (e.g. "CartApp") — reusing the domain reduces load.
5. **Real names vs placeholders**: `user/cart/order` when showing applied patterns, `foo/bar` only for pure syntax.
6. **Length**: 5–15 lines ideal, 30 max. Longer → split or link to runnable repo.
7. **Explicit over clever**: `const r = add(2,3); expect(r).toBe(5);` beats `expect(add(2,3)).toBe(5)` on first appearance.
8. **Contiguity**: explanation adjacent to code, not after. Inline comments `// ← this is the key line` beat paragraphs.
9. **Versioned**: header each chapter with stack versions + validation date ("Validated 2026-04 with Vitest 4.x").
10. **No compiling failures**: include every import. Validate snippets in CI if possible.

### Before/after pattern

Use when showing anti-patterns common in the audience:

- Mark the bad with visual flags: `// ❌ fragile` / `// ✅ resilient`.
- Never leave an anti-pattern on a page without its fix.
- Risk: familiarity effect — readers memorize the bad version. Mitigate with visual distinction.

## Durability: stable principles vs versioned facts

Technical guides age. Prices change, model versions move, command lists are rewritten between releases. The body of the guide should outlive most of those changes; the dated facts should be quarantined so they can be updated without rewriting the prose.

**Rule.** Separate stable principles from versioned facts.

- **Body of the guide.** Principles that change slowly (asymmetry of input/output cost, attention is non-uniform, memory ≠ context). These are what the reader should remember years later.
- **Versioned facts.** Specific prices, version numbers, exact command names, dates of feature releases. These belong in:
  - **Inline callouts** with a verification date: `> Verificado el 2026-05-06. Confirmar contra docs antes de publicar.`
  - **A dedicated "Sources" or "Versioned data" block at the end of each chapter**, so a future reviewer can update one block instead of hunting through prose.
  - **An anexo** for command tables and quick references.

The cost of confusing the two: a guide with concrete prices in every paragraph reads as an "informe temporal", not as a manual. A guide with no concrete data at all reads as vague. The discipline is principles inside, dated specifics flagged.

## Guide structure template

Apply to every major file:

1. **Title + one-line purpose** (who this is for, what they'll be able to do after).
2. **Prerequisites** (links to previous material or external resources).
3. **Time estimate**.
4. **Context / motivation** — why this matters (the pain without this knowledge).
5. **Body** — small sections, each with: explanation → example → micro-exercise or self-check question.
6. **Synthesis** — see "Synthesis tactics" below; pick a concrete format, not a vague summary paragraph.
7. **Consolidation exercise** — more open, applied problem.
8. **References** — deeper links, official docs.

### Optional but high-impact: appendix of reusable templates

For guides aimed at teams that will *operate* with the material (not just read it), add a final appendix collecting the templates that the body has shown in pieces:

- `AGENTS.md` / `CLAUDE.md` / config skeletons.
- _Spec_ template.
- Operational _prompts_ ready to copy.
- Review _checklists_ (PR, audit, deployment).
- Decision tables.

The appendix is the single most reused part of an operational guide. The body explains the why; the appendix provides what the team will paste into their repo on Monday.

Consistent structure across files = predictability = lower cognitive load. Combine with **varied wording** in titles and section headers (see prose-pitfalls #7) so predictable bones do not produce template skin.

## Synthesis tactics

Point 6 of the structure template ("synthesis") is too often executed as a generic summary paragraph. Pick instead one of these formats, in this order of usefulness for adult devs:

- **Decision table.** "Síntoma → causa probable → capítulo donde se trata". The single most reused piece of an operational guide.
- **Comparative table.** Option A vs B vs C, columns for "when to use", "when not to use", "what it costs". Beats discursive comparison.
- **Operational checklist.** 5-9 items. Use for "before merging a PR", "before deploying", "before publishing".
- **Self-evaluation form.** Short questions the reader answers; reveals gaps in their own understanding.

A "summary paragraph" rarely earns its place. If the synthesis can be expressed as a table or a checklist, it should be.

## Sync + async blending

When material accompanies a live session:

- **Live session**: motivation, debate, collective Q&A, shared energy. Best for *tutorial* and *explanation* modalities live.
- **Async guide**: depth, self-pace, rereading, just-in-time lookup. Best for *how-to* and *reference* modalities written.
- **Rule**: async guide must be *self-sufficient* (someone who missed the live can follow) AND *complementary* (adds what live can't deliver: depth, edge cases, reference tables).
- The live session should explicitly point to async files: "when you hit case X, go to file Y".

## Voice and prose style

**Central rule for prose-level editing:** every paragraph that explains something should follow the pattern **situation → explanation → practical consequence**. Compressed lines that fuse the three steps into a single aphorism manufacture the "internal note" feel that fails technical guides for adults. The pattern applies whether designing fresh prose or rewriting tight notes.

Style rules in technical writing are language-dependent. Apply them by audience and language, not by inertia from English style guides.

**Voice.** Pick a stable voice for the audience and the language and stay consistent.

- *English Google-style*: second person "you" reads peer-to-peer.
- *Spanish technical writing for adult devs*: plural inclusive (vía conjugation: "vemos", "tenemos", "hilamos") often reads more peer-to-peer than imperative `tú`. The plural inclusive carries author and reader together without sounding paternalistic.
- *Whatever you pick*: do not switch mid-document.

**Sentence length.** Two failure modes, opposite directions:

- *Too long*: sentences over ~25 words that mix more than two ideas should be split.
- *Too compressed*: sentences so short and aphoristic that the reader has to reconstruct intent. The remedy is **situación → explicación → consecuencia práctica**.

**Style rules to apply:**

- [ ] Task-based titles with verbs ("Configure Jest", not "Jest configuration").
- [ ] Present tense, active voice.
- [ ] Numbered steps when order matters, bullets otherwise.
- [ ] Consistent terminology — one concept = one term, always. Keep a glossary.
- [ ] Headings form a scannable outline.
- [ ] Predictable structure across files; **varied wording** in titles and section headers (so structure does not become template).
- [ ] One aphoristic phrase per chapter at most. The rest of the punchy lines turn into explanations with subject + cause.
- [ ] Pronouns (`lo / eso / esto`) only when the referent is unambiguous; replace with the noun the first time.
- [ ] One metaphor per concept, only if it clarifies. No mixed metaphors.
- [ ] Anglicisms only when canonical (`harness`, `MCP`, `tool use`, `system prompt`, `prompt`); otherwise translate.

**Concrete catalogue of prose-level pitfalls** (compressed sentences, vague pronouns, aphorism chains, mixed metaphors, unnecessary anglicisms, dry transitions, mechanical recurring titles, absolute claims) with examples and rewrite rules: `./references/prose-pitfalls.md`.

## Review checklist

When reviewing an existing guide, check each file for:

**Structure**
- [ ] Has a declared dominant modality (tutorial / how-to / reference / explanation).
- [ ] Doesn't equal-mix modalities — micro-sections of another modality only at the close, marked.
- [ ] Opens with why-this-matters, not with theory.
- [ ] Has explicit learning objectives at the top.
- [ ] Has an estimated time.

**Cognitive load**
- [ ] No section introduces more than one new concept.
- [ ] Examples use consistent domain across files.
- [ ] Code snippets are self-contained (imports visible).
- [ ] Scaffolding fades across exercises.
- [ ] Worked examples present before autonomous exercises.
- [ ] Reader-orientation cues at the close of dense paragraphs.

**Adult learner respect**
- [ ] Tone is peer-to-peer, not parental.
- [ ] References reader's prior experience.
- [ ] Offers alternative paths (fast / deep).
- [ ] Solutions available (not blocked "so they think").
- [ ] Exercises tied to real-world tasks, not toy problems.

**Code examples**
- [ ] Minimum viable, runnable, self-contained.
- [ ] Single domain across the guide.
- [ ] Real names unless pure-syntax context.
- [ ] ≤ 30 lines per snippet.
- [ ] Inline annotations over paragraph prose.
- [ ] Versions + validation date in header.
- [ ] Anti-patterns marked visually and followed by fix.

**Durability**
- [ ] Body of prose talks in stable principles.
- [ ] Dated facts (prices, versions, commands) live in callouts, sources block or appendix.
- [ ] Each versioned block has a verification date.

**Synthesis**
- [ ] Synthesis section uses a concrete format (decision table, comparative table, checklist, self-evaluation), not a generic summary paragraph.
- [ ] If the guide is operational, an appendix of reusable templates exists.

**Microstyle (prose level)**

Run the prose pitfalls catalogue (`./references/prose-pitfalls.md`) in the order recommended at the bottom of that file. Quick check:

- [ ] No vague pronouns without clear referent.
- [ ] No sentences mixing more than two ideas.
- [ ] At most one aphoristic phrase per chapter.
- [ ] Section titles vary across the guide (no five chapters with the same closing-section name).
- [ ] Entries to the recurring example vary (no five chapters opening with "Volvamos a…").
- [ ] Transitions explain why-now, not just "vamos a verlo".
- [ ] No mixed metaphors.
- [ ] Anglicisms only where canonical.

**Navigation**
- [ ] Consistent structure across files.
- [ ] Each file links to related files (tutorial → how-to for advanced, how-to → reference for details).
- [ ] Index file routes by reader intent ("I want to learn" / "I want to solve X" / "I want to look up").
- [ ] Nothing important found only by search.

## Common anti-patterns to flag

### Structural

1. **Mixed modalities** — tutorial with exhaustive reference table embedded as equal partner.
2. **Theory before pain** — 3 paragraphs defining terms before any code or example.
3. **Wall of text** — >5-line paragraphs, no H2/H3, no callouts.
4. **Frankenstein examples** — `User` test that suddenly renders `<ProductList>`.
5. **Inconsistent terminology** — "test", "spec", "case" used interchangeably.
6. **Broken code snippets** — missing imports, wrong types.
7. **Outdated versions unmarked** — no stack version header, no validation date.
8. **Blocked solutions** — exercises with no accessible answer (professional-hostile).
9. **Condescending tone** — "Let's learn together what a function is".
10. **Unlinked cross-references** — "as seen earlier" with no link.
11. **Dated data in body prose** — prices, versions, exact commands sprinkled inline instead of in callouts or appendix.
12. **Generic summary paragraphs** — synthesis sections that could be a decision table but are prose.

### Prose-level

Catalogue with examples in `./references/prose-pitfalls.md`. Headlines:

13. **Compressed sentences** — concept + metaphor + conclusion in one line.
14. **Vague pronouns** — `lo / eso / esto` without clear referent.
15. **Aphorism chains** — "no es X: es Y" repeated section after section.
16. **Mixed metaphors** — incompatible images stacked.
17. **Unnecessary anglicisms** — `mental model`, `scope`, `baseline`, `inline` where Spanish reads cleaner.
18. **Dry transitions** — "Vamos a verlo", "Quedan tres categorías" with no why-now.
19. **Mechanical recurring titles** — "La trampa común…" five chapters in a row; "Volvamos al…" as every entry to the recurring example.
20. **Absolute claims** — universal-sounding statements that a senior reader can puncture.

## Process for designing a new guide

1. **Define learning outcomes** with Bloom verbs: "By the end, you will be able to [apply/configure/migrate/evaluate] X".
2. **Identify audience state**: what they already know, their stack, their daily pain.
3. **Pick modalities**: usually tutorial + how-to + reference + explanation, each in separate files. One dominant per file.
4. **Pick a single domain** for all examples.
5. **Outline per file**: title, purpose, prerequisites, time, sections.
6. **Decide synthesis format per file** (decision table / comparative table / checklist / self-evaluation) before writing.
7. **Plan the appendix** if the guide is operational: which templates the team will copy.
8. **Design exercises with fading**: guided → semi-guided → autonomous.
9. **Write one file end-to-end first** to calibrate tone and depth.
10. **Microstyle pass** with `./references/prose-pitfalls.md` before piloting.
11. **Pilot with 2-3 real users**, collect friction points (time vs estimate, repeated doubts, frequent errors).
12. **Iterate incrementally**, don't rewrite.

## Process for reviewing existing material

1. Map each file to a dominant modality. Flag files that equal-mix more than one.
2. Check the index file: does it route by reader intent? Does it offer fast / deep paths?
3. Check durability: dated data in body or in callouts/appendix?
4. Run the structural review checklist on each file.
5. Run the prose-pitfalls catalogue on each file in the order at the bottom of `./references/prose-pitfalls.md`. Single-rule passes, not "humanize everything at once".
6. Score: how many principles does each file satisfy?
7. Prioritize fixes: structural first (modality split, missing index, dated data leaking everywhere), then synthesis format, then prose microstyle, then polish (terminology, links).
8. Produce a punch list with file + issue + proposed fix, not a full rewrite.

## Process for microediting prose only

When the user's request is microedition (the structure is sound; the prose reads compressed, robotic, template-driven, slogan-like), do not touch structure. Run only the prose pass.

Deliver three things, in this order:

1. **Diagnosis.** Which of the eight pitfalls in `./references/prose-pitfalls.md` apply, with the file/line of two or three concrete examples each. Not a generic "the prose feels off".
2. **Priorities.** Which pitfalls to fix first in this guide (typically vague pronouns first, compressed sentences second, aphorism chains third). Justify by impact on this specific text.
3. **Concrete rewrites.** Before/after for each priority, drawn from the actual file. Not generic templates.

Constraints during a microedit pass:

- **No structural changes.** Do not split files, reorder sections, or add anexos. If those are needed, flag them but do not execute them in this pass.
- **No new content.** Do not add boxes, _callouts_ or sections that were not there.
- **One rule at a time.** Each edit applies one of the eight rules. A pass that mixes "fix vague pronouns + add reader-orientation cues + translate anglicisms" loses voice; passes are sequential.
- **Preserve voice.** If the guide has a stable voice (plural inclusive in Spanish, second person in English, etc.), keep it. The microedit fixes prose, not register.

Closing of a microedit pass: list which rules were applied, on how many sentences, and which were intentionally left untouched (and why). The user should be able to validate the diff against the rule, not against taste.

## References

Full research digest with citations: `./references/research-digest.md`.

Prose-level pitfalls catalogue with examples: `./references/prose-pitfalls.md`.

Key sources:

- Diátaxis framework — https://diataxis.fr/
- Knowles, *The Adult Learner* — https://www.sciencedirect.com/book/9780128117583
- Sweller, Cognitive Load Theory — https://link.springer.com/article/10.1007/s10648-019-09465-5
- Google Developer Style — https://developers.google.com/style
- Write the Docs — https://www.writethedocs.org/guide/
- Mayer, *Multimedia Learning* — https://www.cambridge.org/core/books/multimedia-learning/
- Kent C. Dodds, *Common mistakes with React Testing Library* — https://kentcdodds.com/blog/common-mistakes-with-react-testing-library
