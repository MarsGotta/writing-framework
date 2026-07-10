# Pista corta

La pista corta dimensiona la ceremonia del método para una **pieza única**: un
artículo, un post, un tutorial breve o un ensayo corto. Mantiene las garantías de
la casa —voz calibrada, factualidad, revisión— pero paga menos rito: temario de
una fila, revisión en dos relevos y sin README de presentación. La pista es
ortogonal al modo (`produccion` / `estudio`): puedes combinarla con cualquiera de
los dos.

## Cuándo elegirla

Elige pista corta cuando el proyecto es **una sola pieza** que cabe en un
capítulo. Un repositorio contiene una sola pieza, igual que en pista estándar
contiene una sola guía.

Si el proyecto va a tener varios capítulos —una guía, un manual, un libro—, usa la
pista estándar, que es el default. El multi-pieza (un blog o una columna con varios
artículos en el mismo repositorio) queda fuera de alcance: no lo modela ninguna de
las dos pistas. Ante la duda, empieza en corta: escalar a estándar conserva todo el
trabajo (lo verás en «Escalar a pista estándar»), mientras que arrancar en estándar
por precaución te cobra el rito completo desde el primer día.

## Declarar la pista

La pista se fija **al crear el proyecto** y no se edita a mano en el manifiesto: la
escriben `bootstrap.py` al crear y `track.py` al escalar, nunca tú. Con el bootstrap
directo:

```bash
python3 writeonmars/scripts/bootstrap.py --track corta --sector tecnologia
```

El `--sector tecnologia` fija el sector, deja el registro (`tecnico-divulgativo`) y
materializa las adendas del sector **por referencia** en la constitución del
proyecto. Con el sector ya fijado, el ciclo se salta el paso `constitution`.

Cuando el proyecto lo crea el ejecutor (`vivarium new`), declara la pista por
variables de entorno, que viajan al bootstrap sin necesidad de argumentos nuevos:

```bash
WRITEONMARS_TRACK=corta WRITEONMARS_SECTOR=tecnologia \
  vivarium new mi-articulo --kind guia --preset /ruta/al/writeonmars
```

**Usa las variables de entorno, no el flag `--sector` de `vivarium new`.** El flag
del ejecutor escribe el sector en el manifiesto *después* del bootstrap, así que el
proyecto se queda con sector pero sin adendas y sin registro declarado: la brújula
deja de pedir `constitution` y la capa 2 de la pirámide de prosa nunca se materializa.
La variable de entorno llega a `bootstrap.py`, que sí escribe las adendas. Lo mismo
vale para el sector por defecto que `vivarium new --kind guia` fija solo. Está
anotado en el ROADMAP como deuda del ejecutor.

## Qué pasos desaparecen (y por qué)

El camino feliz de una pieza única cuesta **6 despachos** en pista corta, frente a
los **11** de la ceremonia estándar sobre la misma pieza. La pista omite cinco de
esos despachos, cada uno porque su trabajo es vacuo en una pieza única:

- **`constitution`**: `bootstrap --sector` ya dejó sector, registro y adendas, así
  que la brújula no lo pide. El comando sigue disponible para calibrar el tono a
  mano cuando la pieza lo pida.
- **`plan`**: la firma del brief materializa el temario degenerado —una fila con el
  título y la promesa que firmaste—, de modo que `chapters_expected == 1` y no queda
  temario que planificar.
- **`review-3` (naturalidad) y `review-5` (formato)**: no se despachan por separado
  porque los registra la pasada combinada en el mismo run de la pasada 1 (lo verás en
  «Los dos relevos de revisión»). Las cinco dimensiones se verifican igual.
- **`intro`**: una pieza única no tiene README de presentación, así que el ejecutor
  no lo exige ni lo despacha; `export.py` produce una portada compacta (título,
  autora, fecha) sin índice de capítulos.

## Los dos relevos de revisión

La revisión corre en dos relevos en lugar de cuatro:

- La **pasada combinada** (rol editora de mesa) verifica estructura, utilidad,
  naturalidad y formato —dimensiones 1, 2, 3 y 5— y las registra como los bloques de
  pasada de siempre en `findings.md`. La coherencia entre capítulos, la otra mitad de
  la dimensión 5, es vacua en una pieza única: no hay dos capítulos entre los que
  contradecirse.
- La **pasada de precisión** (dimensión 4, rol documentalista) corre aparte, con
  **otro modelo**, verifica las fuentes en vivo y en `produccion` emite `claims.md`.

La precisión va en un relevo separado por una regla dura del método:
**voz ≠ precisión**. Reescribir prosa y contrastar datos son tareas opuestas que se
degradan al mezclarse, así que las hace siempre otro rol con otro modelo. La
configuración BYOM debe asignar modelos distintos a la editora de mesa y a la
documentalista; colapsarlos en el mismo modelo viola el Principio V.

Si la combinada se queda a medias y registra solo parte de sus bloques, los comandos
sueltos por dimensión (`review-voice`, `review-global`) rellenan los huecos. La
combinada es una comodidad, no un punto único de fallo.

## Escalar a pista estándar

Si a mitad de camino la pieza pide ser guía, escala el proyecto a pista estándar:

```bash
python3 writeonmars/scripts/track.py --escalar --project-dir .
```

El escalado exige **identidad humana**, que el script deriva de tu `git config` y
que rechaza si pertenece a un agente: ningún agente puede escalar por su cuenta. La
operación **no mueve ni un fichero**; solo escribe `track: estandar` y una entrada en
el historial `track_history` del manifiesto. Todo el trabajo se conserva: el brief
sigue siendo el brief, la pieza ya es el capítulo 1, los findings y las claims siguen
valiendo, y las pasadas registradas siguen contando. Después amplías el temario a N
filas y la brújula pide los capítulos 2..N, conservando el 1 como aprobado.

El des-escalado inverso (`--desescalar`) solo es legal mientras el proyecto siga
siendo una pieza única: temario de una fila y sin capítulos de ordinal ≥ 2. Sirve
sobre todo para un proyecto legado sin campo `track` que quiere volverse corto antes
de empezar. Si el temario ya creció o hay capítulos 2 en adelante, el script lo
rechaza con mensaje claro, porque una guía no cabe en pista corta.

## Qué no cambia

La pista corta paga menos rito, no menos verificación. Quedan intactos:

- **Los dos checkpoints humanos**: firmas el brief (checkpoint 1) y anotas el PDF
  (checkpoint 2), igual que en pista estándar. Sin firma, el ciclo no avanza.
- **Las cinco dimensiones del Principio V**: constan todas en `findings.md`, solo que
  verificadas en dos relevos en vez de en cuatro pasadas.
- **Las claims en `produccion`**: `claims.md` se emite igual que en la ceremonia
  completa.
- **Los gates de cierre**: críticos abiertos, firmas pendientes y completitud del
  temario bloquean el cierre con la misma lógica de siempre.
