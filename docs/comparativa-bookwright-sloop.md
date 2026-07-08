# Comparativa: Bookwright y S|Loop vs Write.OnMars

**Fecha**: 2026-07-08 · **Contexto**: análisis previo a la implementación de la
feature 005 (pipeline del modo estudio) para contrastar dos proyectos hermanos
y decidir qué adoptar. Análisis completo con agentes sobre el código real:
Bookwright `51d5a7b` (github.com/jmorenobl/bookwright) y S|Loop v0.10.0
(`~/Projects/sngular-loop`). Ambos son del mismo autor (Jorge Moreno) y
comparten ADN con Write.OnMars: Spec Kit, verdad en archivos, scripts
deterministas como árbitro, agente-agnosticismo.

## Los tres proyectos en una frase

- **Bookwright**: Write.OnMars con el género cambiado — ficción/memoria en vez
  de guía técnica, grafo RDF (GOLEM/CIDOC-CRM) en vez de claims.md, un solo
  agente sin relevos. CLI Python en PyPI, 2 libros reales publicados con él.
- **S|Loop**: el problema inverso al nuestro — construcción de *software*
  desatendida por IA (bucle de ~6h sin humano), donde nosotros hacemos
  *escritura* con checkpoints humanos obligatorios. Motor Python que usa el
  workflow runner de spec-kit como runtime.
- **Write.OnMars**: pipeline editorial con dos modos (producción/estudio),
  relevos escribe-uno-revisa-otro entre agentes distintos, checkpoints humanos
  por diseño, y ledger versionado (`decisions.jsonl` + `findings.md`).

## Qué validan de nuestro diseño (no cambiar)

1. **El ledger de disposiciones de la 005 es ventaja diferencial.** Bookwright
   no tiene disposición de hallazgos (los reportes de continuidad son prosa
   efímera en el chat) ni atribución de autoría por pasaje. Nuestro
   `dispose.py` + `disposiciones.jsonl` + `authorship.py` no tienen
   equivalente en ninguno de los dos.
2. **La huella de contenido (R4) es el guardarraíl que a Bookwright le
   falta.** Su "actualización in situ respeta la prosa humana" descansa 100%
   en la obediencia del prompt, sin verificación mecánica. Nuestra huella
   sha256 por pasada es exactamente el guardarraíl determinista que su propio
   análisis pide.
3. **Frontera por archivos, no por stdout.** S|Loop rasca JSON del stdout de
   `specify` y lo reconoce como su frontera más frágil. Vivarium ↔ preset por
   archivos + exit codes es la decisión correcta; mantenerla dura.
4. **Auditoría versionada.** El rastro de S|Loop (ledger, veredictos,
   métricas) vive en `.run/` gitignored: no sobrevive a un clean ni viaja con
   el repo. Nuestro `decisions.jsonl`/`findings.md` versionados sí.
5. **Relevos escribe-uno-revisa-otro.** Bookwright: el mismo modelo redacta y
   se auto-revisa en la misma sesión. Nuestra regla dura de voz ≠ precisión no
   tiene equivalente y es defendible como diferencial.
6. **Verificación por efecto en disco.** El "veredicto efectivo = PASS del
   agente AND arnés verde" de S|Loop es la versión endurecida de lo que
   Vivarium ya hace (`effect_satisfied` re-corre `status.py` tras cada
   despacho y jamás cree el stdout del agente).

## Qué adoptamos YA en la 005 (enmiendas aplicadas)

1. **"No evaluado ≠ verde" (Bookwright, validación tri-valuada).** Su lección
   más cara: un validador que no puede mirar debe decir "no pude mirar y por
   qué" en su propio canal, no devolver lista vacía (= falso verde). Aplicado:
   - En estudio, **huella ausente ⇒ la pasada NO cuenta** para ese capítulo
     (denegar el verde). No existen proyectos estudio legacy, así que la
     permisividad "cuenta con warning" era un falso-verde gratuito; un
     proyecto convertido re-pasa sus capítulos, que es barato y honesto.
   - La pasada 4 en estudio con `roots/` vacío debe declarar "no evaluable
     contra fuentes" en su bloque, no emitir 0 hallazgos como si hubiera
     verificado.
2. **Heurísticos lingüísticos fuera del gate (Bookwright, "move 3").** Su
   dogfooding midió que las reglas regex sobre prosa real eran 100% ruido y
   tardó ~10 iteraciones en digerirlo. Nuestra 005 ya está del lado correcto
   (el estado deriva de archivos y tablas, no de análisis de prosa); queda
   codificado aquí como regla de la casa: **ningún heurístico sobre prosa
   entra en un gate sin medirlo antes sobre prosa real**.

## Qué va al ROADMAP (buenas ideas, otra feature)

1. **Firma de fallo repetida como clasificador transitorio/determinista**
   (S|Loop): normalizar stderr (fuera UUIDs/rutas/timestamps) y abortar el
   reintento cuando dos fallos consecutivos firman igual. Aplicable al runner
   de Vivarium para no quemar despachos en fallos reproducibles.
2. **Late binding de prompts con ledger** (S|Loop): el plan emite intenciones
   (metaprompts); el prompt concreto se sintetiza al abrir cada tarea contra
   el estado real + decisiones previas. Aplicable a `implement` en producción:
   el prompt del capítulo N se sintetizaría con los capítulos 1..N-1 ya
   escritos y las decisiones del proyecto, en vez de fijarse en el temario.
3. **Protocolo `[PENDING]` de tres sistemas** (Bookwright): un token único que
   las pasadas estampan (marcar-vs-preguntar según si el dato es estructural),
   los validadores tratan como "no decidido" (apagándose con no-evaluado) y un
   comando enumera. Candidato para adendas/claims.
4. **Hallazgo vs ancla con umbral de fiabilidad** (Bookwright): separar "cita
   registrada" de "restricción que ancla y bloquea", con promoción solo si la
   fuente supera un umbral declarado en el manifiesto. Refinaría el índice de
   factualidad (003) en una iteración futura.
5. **Fichas de personaje con "diálogo de muestra" y "lenguaje corporal"**
   (Bookwright): plantillas de `roots/` para narrativa cuando el modo estudio
   se use con novela — estabilizan la voz al revisar consistencia.
6. **`next_detail` con prompt listo-para-usar** (Bookwright: `next_actions =
   {skill, prompt, reason}`): status.py podría emitir junto al paso el prompt
   sintetizado, cerrando el bucle sin que el ejecutor lo componga.

## Trampas ajenas que evitamos por diseño

- **Grafo RDF académico** (Bookwright): GOLEM+CIDOC-CRM+SPARQL es un coste
  enorme para validadores que en la práctica leen frontmatter; nuestros
  archivos planos computables llegan igual de lejos para el caso de uso.
- **Invariante predicado pero no cableado** (S|Loop: "mismo comando en
  pre-commit, arnés y CI" sin CI ni pre-commit): un invariante que solo vive
  en prosa se degrada. Los nuestros (gates de CLAUDE.md) se ejecutan en cada
  feature; mantener esa disciplina.
- **Superficie CLI dual** (S|Loop: typer+argparse en paralelo): nunca duplicar
  superficie de comando.
