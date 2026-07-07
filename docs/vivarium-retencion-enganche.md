# Vivarium · Retención y enganche: el jardín zen del escritor

> **Documento de producto** · Ideas para mejorar Vivarium (editor local-first, cara B de Zeeds)
> en tres frentes: retención, enganche y experiencia zen. Complementa el documento de diseño
> del editor. Estado: exploración. Última actualización: 2026-07-03.

## 1. Principio rector: la calma es la ventaja competitiva

Vivarium no compite en features de generación de prosa (esa batalla la tiene Sudowrite con
su modelo fine-tuneado). Compite en algo que ninguna herramienta del mercado ofrece: **un
espacio tranquilo donde el trabajo serio de escribir se siente acompañado, no vigilado**.

Esto se traduce en reglas de diseño concretas:

- **La herramienta desaparece.** La orquestación, git, Spec Kit, los agentes: todo es
  detalle de implementación (estrategia "fachada"). El escritor ve un manuscrito, un
  equipo y un jardín. Nunca un pipeline.
- **Cero ansiedad de notificación.** Nada parpadea, nada urge, nada acumula badges rojos.
  Lo que el equipo produce espera en silencio a que el escritor decida mirarlo.
- **El ritmo lo marca el escritor.** La app nunca dice "llevas 3 días sin escribir".
  Cuando vuelves, el mensaje es "tu equipo te espera", no "te has retrasado".
- **Sin culpa por métricas.** No se premia el wordcount (premiar volumen genera prosa mala
  y culpa). Se celebra el avance real: Branches que maduran, claims que se verifican,
  decisiones tomadas.

La referencia estética y emocional: la calma de una biblioteca, el cuidado de un
invernadero. De ahí el nombre.

## 2. La tesis de retención: el competidor real es el abandono

En herramientas de escritura la retención no funciona como en un SaaS normal. La mayoría
de la gente no abandona la herramienta: **abandona el libro**. Si Vivarium consigue que
más gente termine sus proyectos, la retención viene sola.

Toda mecánica de enganche de este documento se evalúa contra esa vara: ¿ayuda a que el
manuscrito avance y el escritor vuelva mañana con ganas? Si solo genera actividad
(sesiones, clicks, streaks), no nos vale.

## 3. Memoria que se acumula: la casa te conoce

La arquitectura actual ya genera retención estructural sin haberla nombrado: la
constitución, las adendas de voz, la story bible (Roots) y el log de decisiones mejoran
con cada sesión. **Hay que hacerla visible y explícita.**

- **"Tu editora te conoce desde hace 47 sesiones."** El paso del tiempo con el equipo es
  un dato emocional, no una estadística. Mostrarlo con sobriedad: en el arranque del
  proyecto, no como popup.
- **Irse debe sentirse como despedir a un equipo que ya sabe cómo escribes.** Ese es el
  switching cost honesto: no lock-in de datos (todo es markdown en git, el escritor puede
  llevárselo siempre), sino pérdida de una relación de trabajo entrenada.
- **El log de decisiones (`decisions.jsonl`) existe desde el MVP**, aunque el fine-tuning
  llegue después. Cada aceptar/rechazar/editar queda anclado desde el día uno: es la
  materia prima del flywheel (sección 14 del doc del editor) y del espejo del escritor
  (sección 7 de este documento).
- **Techo del foso: el modelo de tu voz.** El día que el usuario tenga un modelo entrenado
  con sus propias correcciones ("marcela-prose aprendida"), el coste de cambio es total y
  además es un regalo, no una jaula: el modelo es suyo, entrenado con su data local.

## 4. El ritual nocturno: deja el capítulo por la noche, las galeradas por la mañana

El pipeline peer-to-peer es asíncrono por diseño. Convertirlo en **mecánica de cita**:

1. El escritor termina su sesión y deja la Branch en revisión (un gesto, sin fricción).
2. El equipo trabaja mientras el escritor no está: pasadas de mesa, verificación contra
   Roots, findings anotados.
3. A la mañana siguiente hay galeradas esperando: Leaves priorizadas sobre el texto,
   presentadas con calma (una bandeja, no una lista de errores).

Por qué funciona:

- **Crea el hábito de volver** (el mismo mecanismo que hace irresistible el correo por la
  mañana, pero al servicio del libro).
- **Disuelve la latencia.** Las pasadas multi-agente tardan; si ocurren de noche, nadie
  mira un spinner. La lentitud del rigor se vuelve invisible.
- **Refuerza la fantasía central del producto:** tienes un equipo editorial que trabaja
  para ti mientras duermes.

Versión push, opcional y silenciosa: un **digest editorial semanal** ("esta semana: 2
Branches maduraron, 3 claims verificados, el arco del capítulo 4 tiene una tensión sin
resolver"). Tono de carta de tu editora, no de reporte de métricas.

## 5. El momento mágico llega en minutos, no tras el setup

El onboarding actual (Zeed guiado + constitución) es correcto para el proyecto serio, pero
el primer contacto debe ser inmediato:

- **Pega un texto tuyo y recibe una revisión de mesa en dos minutos**, con Leaves
  priorizadas, sin configurar nada.
- La constitución se construye después, **incremental**, a partir de lo que el escritor
  acepta y rechaza en esas primeras revisiones. La app propone adendas ("he notado que
  prefieres X, ¿lo fijamos como regla de la casa?") en lugar de pedir un formulario.
- Nadie se queda por una promesa. Se quedan porque la primera revisión les señaló algo
  **que era verdad**.

## 6. Aceptar/rechazar como interacción central, y que se note que la editora aprende

El momento de mayor valor emocional de todo el producto es revisar findings y decidir.
Merece el pulido de la interacción estrella:

- **Nivel Cursor:** por hunk, rápido, con teclado, sin modales. Aceptar, rechazar, editar
  a mano. Cada gesto alimenta `decisions.jsonl`.
- **Cerrar el loop visiblemente:** "he dejado de marcarte las oraciones largas porque las
  rechazas siempre". Este es el enganche más profundo del producto: el usuario siente que
  su inversión se acumula, que la editora de hoy es mejor que la del mes pasado **por su
  causa**.
- La evolución de la editora se comunica con discreción (una nota ocasional de la propia
  editora, en su voz), nunca como dashboard de "AI learning progress".

## 7. El espejo del escritor: autoconocimiento como feature

Del mismo log de decisiones sale un producto interior que nadie más puede ofrecer: **el
cuaderno del jardinero**, un espacio contemplativo donde el escritor se ve a sí mismo.

- **Tus patrones:** qué tipo de findings aceptas y cuáles rechazas, qué lentes te señalan
  más, en qué capítulos la voz se te escapa.
- **Tu voz, descrita:** a partir de las adendas acumuladas y las correcciones, una
  descripción viva del estilo de la casa ("frases cortas en escenas de tensión, debilidad
  por los dos puntos, adverbios solo cuando..."). Se actualiza sola; leerla es leerse.
- **Tu evolución:** cómo ha cambiado tu prosa desde el capítulo 1. No como gráfica de
  métricas, sino como observaciones ("ya casi no te marcamos transiciones; hace tres meses
  era el finding más común").
- Regla zen: el espejo **nunca prescribe ni compara con otros**. Refleja. El
  autoconocimiento es la recompensa, no un plan de mejora.

Esto convierte a Vivarium en algo que ninguna app de escritura es: no solo te ayuda a
escribir mejor, **te cuenta quién eres como escritor**. Y es inseparable del uso continuado
(el espejo sin sesiones está vacío), lo que lo hace mecánica de retención pura sin un
gramo de gamificación agresiva.

## 8. Gamificación botánica: el progreso que se contempla

La metáfora Zeed / Root / Tree / Branch / Leaf / Forest es gamificación gratis, del tipo
correcto: **progreso visible sin badges, niveles ni rachas**.

- **El árbol crece de verdad.** Una visualización viva del Tree: las Branches aprobadas
  reverdecen, las que están en revisión se distinguen con suavidad, las Leaves pueblan las
  ramas. Ver el libro crecer literalmente es potente para la gente que más sufre la
  sensación de no avanzar.
- **Estaciones, no streaks.** El proyecto tiene momentos (plantar, crecer, podar, dar
  fruto al publicar al Forest) y la interfaz los acompaña estéticamente. Si algún día hay
  rachas, miden **sesiones de trabajo con el equipo**, jamás palabras escritas.
- **Celebraciones sobrias.** Cerrar una Branch merece un momento (la rama reverdece, una
  línea de la editora), no confeti. El tono es "hoy el jardín está mejor", no "¡LEVEL UP!".
- **El fruto es publicar.** El ciclo se cierra en el Forest: el árbol da fruto, otros lo
  leen, y (ángulo Zeeds) tu Tree puede volverse Root del árbol de otra persona. Ser
  citado es el estatus más alto entre escritores y no requiere inventar ninguna moneda.

## 9. Zeeds como amplificador (no adelantarlo, pero diseñarlo en el anclaje)

La retención de largo plazo vendrá de la capa social: Leaves de lectores reales trayendo
al autor de vuelta, la conversación anclada al texto publicado, la genealogía de
Trees-que-son-Roots. Nada de esto se construye aún, pero **el anclaje pendiente (el Core)
debe diseñarse ya con este uso en mente**: si los Leaves del autor y del lector comparten
primitivo, cada lector que comenta se convierte en una razón para que el autor abra
Vivarium mañana.

## 10. Cómo se apoya en la arquitectura existente

| Mecánica | Se apoya en |
|---|---|
| Ritual nocturno / galeradas | pipeline peer-to-peer + estados por Branch (`status.py --json`) |
| Bandeja de findings | `findings.md` + Leaves CriticMarkup con prioridad |
| Aceptar/rechazar por hunk | diffs en git + anclaje (el Core, pendiente) |
| La editora aprende | `decisions.jsonl` (log de procedencia, MVP) → flywheel / fine-tuning |
| Espejo del escritor | `decisions.jsonl` + adendas de constitución + lentes |
| Árbol que crece | árbol de Branches (`content/`) + estados (drafting / in_review / approved) |
| Digest semanal | `status.py --json` (`by_branch`, gates) redactado por la Editora jefa |
| Momento mágico (paste → revisión) | pasadas de mesa sobre un `.md` suelto, sin scaffold completo |
| Fruto / publicación | export + push al Forest (capa Zeeds) |

## 11. Priorización

Si solo se construyen dos mecánicas, estas:

1. **El ritual nocturno** (hábito): es barato porque el pipeline asíncrono ya existe;
   solo hay que darle forma de cita y cuidar la bandeja de la mañana.
2. **Aceptar/rechazar que aprende visiblemente** (inversión acumulada): exige el anclaje
   y el log de decisiones, que de todas formas son foundational para el flywheel.

Después, en orden: momento mágico del onboarding (adquisición), árbol vivo (progreso
visible), espejo del escritor (diferenciación profunda), digest semanal (re-activación),
Forest/social (amplificador, fase Zeeds).

## 12. Decisiones abiertas

- Forma de la bandeja de la mañana: ¿vista propia ("galeradas") o el mismo editor con las
  Leaves desplegadas?
- ¿El espejo del escritor es un panel del proyecto o transversal a todos los Trees del
  autor?
- Tono y frecuencia del digest (¿semanal fijo, o solo cuando hay algo que decir?).
- Cuánta vida visual tiene el árbol en el MVP (¿ilustración estática por estados vs
  animación?): el riesgo es que lo contemplativo se vuelva decorativo.
- Si las "estaciones" del proyecto merecen presencia en la UI o quedan como lenguaje
  interno del equipo.

---

# Validación de mercado

> Investigación de julio de 2026 (fuentes enlazadas por afirmación). Separada de las
> mecánicas porque condiciona decisiones de posicionamiento, precio y orden de
> construcción.

## 13. Lo que juega a favor (pros)

**La línea "la IA te edita ≠ la IA escribe por ti" está institucionalizada, y Vivarium
cae del lado seguro por definición.**

- La certificación ["Human Authored" del Authors Guild](https://authorsguild.org/human-authored/faq/)
  permite explícitamente corrección, investigación y brainstorming con IA, y solo
  prohíbe la prosa generada.
- [Amazon KDP exige declarar contenido *AI-generated*](https://kdp.amazon.com/en_US/help/topic/G200672390)
  pero exime el *AI-assisted* ("editar, refinar, corregir, mejorar"). Una herramienta de
  revisión no dispara la declaración.
- La [Oficina de Copyright de EE. UU. (Parte 2, enero 2025)](https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-2-Copyrightability-Report.pdf)
  confirma que usar IA "como herramienta para editar" no afecta la copyrightabilidad de
  la obra.

**La demanda del uso que vendemos existe y está medida.** [45% de autores ya usan IA de
alguna forma (BookBub 2025, n>1.200)](https://insights.bookbub.com/how-authors-are-thinking-about-ai-survey/)
y [42% de autores de ficción la usan al menos a veces](https://www.publishersweekly.com/pw/by-topic/digital/copyright/article/99019-new-report-examines-writers-attitudes-toward-ai.html);
los usos dominantes son brainstorming, búsqueda y revisión, y **solo el 11% genera texto
publicable**. El uso mayoritario y aceptado es exactamente el que Vivarium ofrece.

**La categoría "IA como editor" crece y los incumbentes pivotan hacia ella.**
[ProWritingAid vende Manuscript Analysis y Virtual Beta Reader](https://prowritingaid.com/features/virtual-beta-reader)
como créditos premium, [AutoCrit vende AI beta readers](https://www.autocrit.com/ai-beta-reader/),
[Marlowe reclama 40k autores](https://authors.ai/). Que una empresa de gramática apueste
su revenue premium a la crítica de manuscritos valida la demanda.

**El modelo BYOM ya vende en este mercado.**
[Novelcrafter ($4-20/mes, BYOK, ~157k autores reclamados)](https://www.novelcrafter.com/pricing)
sostiene un negocio bootstrapped rentable. Nuestro free=BYOM no es una apuesta, es un
patrón probado.

**Local-first + privacidad es una posición de confianza demostrada.** Scrivener lleva
~20 años monetizando "tu obra es tuya, offline"; [Ellipsus crece con marca
anti-IA y control de versiones estilo git](https://ellipsus.com/). "Tu manuscrito nunca
entrena nada y nunca sale de tu máquina" ataca de frente los dos miedos más documentados
del colectivo: [96% exige consentimiento para entrenar con sus obras](https://authorsguild.org/news/ag-ai-survey-reveals-authors-overwhelmingly-want-consent-and-compensation-for-use-of-their-works/)
y [86% teme la imitación de su voz](https://internationalauthors.org/news/society-of-authors-ai-survey-results-published/).
[Marlowe ya vende "no entrenamos con tu manuscrito" como feature](https://authors.ai/marlowe/).

**El bundle exacto está desocupado.** Nadie combina hoy local-first + git oculto +
equipo editorial multi-agente + verificación de claims contra Roots. Sudowrite ataca
desde agentes+story bible, Ellipsus desde git+colaboración (sin IA), Novelcrafter desde
la economía BYOK; ninguno tiene las cuatro piezas.

## 14. Riesgos y debilidades (contras)

**1. Estigma: el mercado direccionable es más pequeño de lo que parece.** Entre
[58% (BookBub)](https://insights.bookbub.com/how-authors-are-thinking-about-ai-survey/) y
[67% de novelistas (Cambridge/Minderoo, 2025)](https://www.cam.ac.uk/stories/generative-ai-novelists)
no usan ninguna IA, y una parte es impersuadible por principio (ética, medio ambiente,
"AI slop"). El clima es hostil:
[agencias literarias piden evitar la IA](https://www.thebookseller.com/news/literary-agents-urge-writers-to-avoid-ai-as-they-see-change-in-nature-of-submissions),
hay editoriales que banean autores, y [una carta abierta contra libros generados juntó
1.100+ firmas en 24 horas](https://www.npr.org/2025/06/28/nx-s1-5449166/authors-publishers-ai-letter).

**2. El posicionamiento puede matar la marca (lección NaNoWriMo).**
[NaNoWriMo cerró en 2025](https://techcrunch.com/2025/04/01/nanowrimo-shut-down-after-ai-content-moderation-scandals/),
en parte por el daño reputacional de su postura percibida como pro-IA-generativa. El
mensaje es existencial, no cosmético: Vivarium debe hablar siempre vocabulario de
edición y rigor, jamás de generación. El marketing es parte del producto.

**3. Uso episódico → riesgo de churn estructural.** La revisión es por manuscrito, no
continua: entre libro y libro no hay uso. La banda de precio revelada del escritor serio
es ~$50-150/año o pagos puntuales (Scrivener $59 one-time, Atticus $147 one-time,
[informes de $30-50 por manuscrito en ProWritingAid/Marlowe](https://prowritingaid.com/pricing)).
**No existe ningún dato público de churn ni de conversión BYOK→hosted en este mercado**:
es un gap real que solo se cierra midiendo. Implicación: contemplar precio por informe o
por proyecto además de la suscripción.

**4. La economía BYOM tiene techo conocido.** Novelcrafter demuestra *lifestyle
business*, no venture scale. En coding, [Cursor tuvo que repreciar entre revueltas](https://www.finout.io/blog/what-happened-to-cursor-pricing-2026-guide-5-cost-cutting-tips)
y [Zed admitió vender tokens a pérdida](https://zed.dev/blog/not-building-ai-for-the-money):
el margen tolerado sobre inferencia hosted es +10-20%. Sudowrite genera resentimiento
constante por créditos. La lección de
[Obsidian (~$25M ARR con 7 personas monetizando sync/publish, no el editor)](https://finance.biggo.com/news/iVboYp0Bga3fZL9MJEv_):
la superficie monetizable es la red, la sincronización y la conveniencia, no el editor
ni el margen de inferencia. Refuerza la decisión "el editor local nunca se gatea" y
apunta el dinero hacia Forests/Zeeds.

**5. Los incumbentes se mueven rápido.**
[Sudowrite ya lanzó margin-notes con conciencia de story bible y workflows agénticos (junio 2026)](https://feedback.sudowrite.com/changelog),
con 16 personas y modelo propio. La ventana del feature-moat es corta (trimestres, no
años). El foso defendible no es la feature multi-agente: es la posición de confianza
local-first, el flywheel de correcciones y la profundidad del método (constitución,
pasadas, claims con veredicto).

**6. La capa social (Zeeds) es el riesgo mayor del plan.** Las redes de lectura
monetizan lectores o IP, nunca escritores:
[Wattpad ha pagado ~$3.8M en stipends en toda su historia](https://creators.wattpad.com/),
[en Royal Road solo ~0,55% de autores serializando superan $4k/mes](https://www.chapterchronicles.com/blog/royal-road-patreon-2025/),
y Medium alcanzó rentabilidad recortando payouts. A eso se suma el cold-start clásico.
El Forest solo paga si se convierte en motor de descubrimiento, territorio donde
Wattpad/Royal Road ya poseen la atención. Confirma el orden "editor primero" y aconseja
tratar Zeeds como apuesta separada con su propia validación.

**7. Riesgos técnicos y de distribución.**
[Penflip ("GitHub for writers") murió](https://alternativeto.net/software/penflip/about/)
en buena parte por exponer git a escritores: valida nuestra estrategia fachada y a la
vez advierte del coste si la abstracción se filtra. Tauri es maduro en producción, pero
la distribución indie tiene fricción real (firma y notarización macOS/Windows, updater
menos rodado que Electron).

**8. La voz y el fine-tuning son el campo minado del consentimiento.** El miedo a la
imitación de voz es el #1 documentado (86%). El flywheel debe ser ruidosamente
consentido, local y jamás cross-user (ya decidido por fases en el doc del editor:
correcto). Con BYOM, además, los términos del proveedor de API (si entrena con los
datos del usuario) se convierten en nuestra superficie de confianza: elegir y comunicar
proveedores con no-training garantizado.

## 15. Síntesis: qué cambia en el plan

1. **El vocabulario del producto es una decisión de supervivencia**, no de copy: mesa de
   edición, galeradas, rigor, verificación. Nunca "escribe por ti". Explorar la
   compatibilidad con la certificación Human Authored como ángulo de marketing.
2. **Precio**: mantener free=BYOM (validado por Novelcrafter/Raptor), pero diseñar el
   Pro pensando en uso episódico: informes por manuscrito o precio por proyecto además
   de la mensualidad. El margen hosted es conveniencia, no negocio.
3. **El dinero de plataforma vive en Forests/Zeeds, pero es una apuesta aparte** con las
   peores economías conocidas del sector: no anclar la viabilidad de Vivarium a ella.
4. **Velocidad**: la ventaja de features dura trimestres. Priorizar lo inimitable
   (flywheel con consentimiento, método, confianza local-first) sobre lo copiable
   (número de agentes, pasadas).
5. **Medir desde el día uno** lo que el mercado no publica: conversión BYOM→hosted,
   churn entre proyectos, reactivación por digest. Son nuestros datos propietarios de
   decisión.

---

# Los dos modos y la procedencia verificable

> Decisión de producto (2026-07-03): Vivarium soporta los dos sentidos del trabajo, con
> defaults por tipo de proyecto y un registro de procedencia que sustituye a la idea del
> "% escrito por IA".

## 16. Modo estudio y modo producción: dos puertas, un motor

Vivarium permite ambas direcciones, que ya existen en la arquitectura:

- **Modo estudio (el escritor escribe).** La IA guía, revisa y aprende contigo: pasadas
  de mesa, verificación, Leaves con prioridad, el espejo del escritor. Es el MVP del doc
  del editor.
- **Modo producción (la IA redacta).** Para guías técnicas, tutoriales y no-ficción
  fundamentada: la IA escribe anclada en Roots (fuentes fiables, CitationRecord) y con
  la prosa de la casa; el humano dirige validando con **Leaves CriticMarkup**
  (aceptar/corregir/comentar con prioridad), que se convierten en señal para los
  agentes vía `feedback_intake`. Es el pipeline writeonmars con la app encima. Mismo
  primitivo Leaf en ambos modos: no añade arquitectura nueva.

**Defaults opinados por tipo de proyecto, no candados:**

| Tipo de proyecto | Modo por defecto | Razón |
|---|---|---|
| Novela / relato / poesía / guion | **Estudio** (producción desactivada por defecto) | Estigma documentado + certificación Human Authored + normas de agencias/editoriales |
| Guía técnica / tutorial / documentación | **Producción** (con verificación obligatoria contra Roots) | El lector compra fiabilidad, no autoría romántica; la generación declarada es aceptada |
| Académico / ensayo | **Estudio** con lentes de verificación reforzadas | Muchas revistas y universidades prohíben también el texto generado |

Por qué defaults y no prohibición dura:

- **El género no mapea 1:1 con la norma.** Hay usos legítimos de generación alrededor de
  una novela (sinopsis, blurbs, material de marketing) y autores de no-ficción que
  quieren escribir cada palabra. El candado duro genera fricción en los bordes y
  workarounds.
- **El incentivo ya hace de policía.** Solo el modo estudio produce el informe de
  autoría humana (sección 17). Si un novelista activa producción, su registro de
  procedencia lo reflejará y perderá la evidencia certificable: no hace falta
  prohibirle nada, el sistema hace que hacer trampa no compense. Cambiar el modo de un
  proyecto de ficción pide confirmación explícita y explica exactamente qué se pierde.
- **La marca sí se segmenta duro, aunque el motor no.** Hacia ficción, el marketing solo
  habla del estudio del escritor (lección NaNoWriMo: el vocabulario es supervivencia).
  El modo producción se vende al segmento técnico/no-ficción con otro lenguaje y,
  probablemente, otra landing. Mismo motor, dos puertas.

## 17. Procedencia verificable por span (en lugar de "% escrito por IA")

**Descartado:** un porcentaje único de IA. Es crudo, gameable y reputacionalmente
peligroso (invita a comparaciones públicas absurdas). Y sobre todo, **no compra lo que
prometía**: la [certificación Human Authored](https://authorsguild.org/human-authored/faq/)
prohíbe la prosa generada por IA; un 30% generado no da "certificación al 70%",
descalifica la obra entera. En [KDP](https://kdp.amazon.com/en_US/help/topic/G200672390),
el texto generado debe declararse **aunque se haya editado a fondo después**; solo el
asistido (humano escribe, IA corrige) queda exento.

**En su lugar: registro de procedencia a nivel de span.** Git + el anclaje (el Core) +
`decisions.jsonl` ya permiten saber, párrafo a párrafo: escrito por el humano · redactado
por IA y reescrito por el humano · sugerencia de IA aceptada tal cual · redactado por IA
validado por Leaf. De ahí salen dos productos distintos según el modo:

- **Modo estudio → informe de autoría humana.** El registro *demuestra* (con el historial
  git como respaldo auditable, no como autodeclaración) que la prosa es humana y la IA
  solo editó. Vivarium se convierte en la única herramienta que genera **evidencia**
  compatible con Human Authored: argumento de venta directo para el escritor profesional
  que vive en el clima hostil documentado en la sección 14.
- **Modo producción → declaración honesta + credibilidad.** El registro alimenta la
  declaración de KDP sin dolor y, más valioso, la confianza del lector técnico: cada
  afirmación con su CitationRecord, cada párrafo con su procedencia y su verificación
  contra fuentes. En este segmento la transparencia es virtud, no estigma.

Notas de implementación:

- La procedencia cuelga del **mismo primitivo que el anclaje y el flywheel** (otra razón
  más por la que el anclaje es lo primero que hay que resolver).
- `decisions.jsonl` debe etiquetar origen del span desde el MVP (humano / IA / mixto +
  disposición del humano), aunque los informes lleguen después.
- Pregunta abierta: el umbral de "reescrito por el humano" (¿cuánta edición convierte un
  span de IA en mixto?): definir criterio propio, documentarlo y no prometer
  equivalencia legal exacta con las categorías de KDP/Authors Guild (el informe es
  evidencia, la responsabilidad de la declaración es del autor).
- Pregunta abierta: ¿informe exportable con verificación externa (hash del historial,
  estilo content credentials) o solo lectura dentro de la app?
