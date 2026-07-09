# Comparativa: BMAD Method v6 vs Write.OnMars

**Fecha**: 2026-07-09 · **Contexto**: análisis previo a la spec 006 (pista
corta editorial) para decidir si BMAD sustituye a Spec Kit/Write.OnMars en
alguno de los dos ejes del proyecto — construir el framework/Vivarium y
generar los escritos — y qué adoptar de él. Fuentes: repo y docs oficiales
([bmad-code-org/bmad-method](https://github.com/bmad-code-org/bmad-method),
[docs.bmad-method.org](https://docs.bmad-method.org/)), módulo
[CIS](https://github.com/bmad-code-org/bmad-module-creative-intelligence-suite),
y análisis independientes ([BMAD vs Spec Kit](https://medium.com/@mariussabaliauskas/a-comparative-analysis-of-ai-agentic-frameworks-bmad-method-vs-github-spec-kit-edd8a9c65c5e),
[crítica de Santos](https://adsantos.medium.com/you-should-bmad-part-2-a007d28a084b),
[perfil de Ry Walker](https://rywalker.com/research/bmad-method),
[v4→v6 de Trần](https://medium.com/@hieutrantrung.it/from-token-hell-to-90-savings-how-bmad-v6-revolutionized-ai-assisted-development-09c175013085)).
Informe completo del análisis en el chat de Cowork del 2026-07-09.

## Los dos en una frase

- **BMAD Method** (v6.7.1 estable, ~49k estrellas, MIT): un equipo ágil
  simulado por personas-agente (analista, PM, arquitecto, dev, UX, tech
  writer) con cuatro fases condicionales, **ceremonia adaptativa a escala**
  (Quick Flow / Method / Enterprise), ciclo de implementación por story files
  autocontenidos y carga just-in-time por step-files. Método de *personas*:
  la calidad vive en el prompt del rol.
- **Write.OnMars**: método de *estado* — la verdad vive en archivos, la
  computa un script (`status.py`), y las garantías son código: gates g1-g4,
  huellas sha256, exit codes contratados, `effect_satisfied` que re-lee el
  disco y jamás cree el stdout del agente.

## Qué valida BMAD de nuestro diseño (no cambiar)

1. **Verificación dura frente a gates instruccionales.** La crítica
   independiente documenta pipelines BMAD que marcaron "completa" una feature
   rota: sus gates son prompt. Nuestro `effect_satisfied` + gates
   deterministas son exactamente la vacuna contra ese modo de fallo; el
   contraste lo confirma como diferencial, no como sobre-ingeniería.
2. **Orquestación por código, no por conversación.** BMAD exige al humano
   cambiar de persona (o Party Mode, que sigue siendo chat); no tiene runner
   desatendido. Vivarium (runner por estados, BYOM, reconciliación,
   checkpoints con exit 10/11) está un paso por delante en el eje que a este
   proyecto le importa.
3. **Un sustrato para dos oficios.** Nuestras plantillas duales
   (editorial/software) hacen que el mismo Spec Kit construya el software y
   los libros. BMAD nos partiría en dos mundos con dos toolchains.
4. **Dominio editorial en serio.** El módulo "creativo" de BMAD (CIS v0.2.0)
   es ideación y se autodeclara tech demo; la "escritura creativa" es
   categoría de marketing de la era v4. No existe allí pipeline de
   manuscrito con voz calibrada, factualidad, procedencia ni español: en
   este dominio Write.OnMars no tiene sustituto.

## Qué adoptamos YA (spec 006)

1. **Ceremonia adaptativa a escala** (la mejor idea de BMAD v6): pistas de
   rito según tamaño, con **escalado que arrastra el trabajo hecho** (su
   tech-spec alimenta el PRD al subir de pista). Traducción nuestra: campo
   `track` (`estandar`/`corta`) en el manifiesto, temario degenerado de una
   fila, revisión en dos relevos (combinada 1·2·3·5 + precisión 4), intro
   omitido, escalado corta→estandar que conserva brief, pieza, findings y
   claims. Spec: `specs/006-pista-corta-editorial/`.

## Qué va al ROADMAP (buenas ideas, otra feature)

1. **Carga just-in-time por step-files** (v6: 74-90% menos tokens que v4
   fragmentando workflows y cargando solo el paso actual). Aplicable a
   nuestras referencias: la pasada de voz carga hoy `references/voz/SKILL.md`
   entero (~42k) en cada ejecución; trocearlo por modalidad/paso ahorraría
   tokens por pasada sin cambiar el método.
2. **ux-spec como artefacto de primera clase + story files autocontenidos**
   para la fase de interfaz Tauri de Vivarium: nuestro plan-template es flaco
   en diseño de UI; un `ux-spec.md` antes de la spec de la interfaz, y tareas
   de frontend que empaqueten su contexto (patrón story file), reducen la
   ambigüedad justo donde nuestra ceremonia actual es más débil.
3. **Testing basado en riesgo (módulo TEA)** como enfoque para la capa GUI,
   donde la suite actual (unitarios de scripts + smokes con stubs) no llega.
4. **Ideación estructurada opcional pre-brief** (workflows CIS, Party Mode):
   capa de acompañamiento para la captura del Zeed y el modo estudio en
   Vivarium — como referencia opcional, nunca paso obligatorio.
5. **Detección de escala con alertas** (scope alerts que sugieren escalar de
   pista cuando la pieza pide ser guía): complemento futuro del escalado
   manual de la 006.
6. **Port de Write.OnMars como módulo BMAD (vía BMad Builder)** como canal de
   distribución hacia su comunidad (~49k estrellas): personas-agente como
   fachada, la verdad sigue en nuestros archivos y scripts (Principio VI lo
   permite: prohíbe acoplar el método a un ejecutor, no tener fachadas).
   Después de licencia ✓, publicación del preset y obra producida.

## Trampas ajenas que evitamos por diseño

- **Ceremonia fija para todo tamaño** — la nuestra hasta la 006: el mismo
  rito para artículo y libro. BMAD lo resolvió con pistas; lo adoptamos con
  contratos intactos en vez de heredar su costumbre de PRD para todo.
- **Curva y toolchain**: BMAD pide Node+Python+uv, `.bmad/`, semanas de
  curva y 6-12 personas-agente; su propio ecosistema lo desaconseja para
  desarrolladores en solitario. Nuestro coste de entrada ya está amortizado
  (5 specs entregadas con Spec Kit).
- **Tiempo-hasta-entrega**: en la evaluación independiente de abril de 2026
  BMAD quedó el mejor en refinamiento iterativo y el peor en time-to-PR
  (~6 días y ~200$ donde los spec-driven tardaron 1-2). Para una persona con
  agentes, ese perfil es el equivocado.
- **Gates de prompt**: historias marcadas "done" con la feature rota. Regla
  de la casa reafirmada: ningún gate sin verificación por efecto en disco.
