# Registros (capa 2 de la pirámide de prosa)

Un **registro** es el contrato estilístico de un género: cuánta formalidad,
cuánta densidad, qué figuras se permiten, cómo se afirma y cómo conviven prosa
y artefactos (código, tablas, datos). Es la capa 2 de la pirámide:

1. **Capa 1, prosa-base** (`references/prosa/SKILL.md`): cohesión y fluidez.
   Universal, siempre activa, innegociable.
2. **Capa 2, registro** (esta carpeta): el color del género. Se declara una vez
   por guía.
3. **Capa 3, voz** (`references/voz/SKILL.md`): la firma del autor.

En conflicto: la voz gana en sabor (léxico, humor, aperturas, cierres), el
registro gana en formalidad y densidad globales, y la prosa-base no la deroga
nadie (frases completas y progresión conocido → nuevo).

El registro materializa el campo **"Tono calibrado"** de las adendas del
proyecto (constitución § Adendas): la adenda declara el registro elegido y la
pasada de naturalidad verifica contra él, no contra un tono genérico.

## Cómo se selecciona

- Cada registro es **una carpeta** con su `SKILL.md`
  (`references/registros/<slug>/SKILL.md`).
- `/speckit-constitution` lista los registros disponibles (ignora este índice)
  y pregunta cuál aplica; la **base de sector** propone el default (p. ej.
  tecnología propone `tecnico-divulgativo`).
- La elección se escribe en `.writeonmars-manifest.json` (clave `registro`) y
  en las adendas ("Tono calibrado").
- `speckit.implement` y `speckit.review-voice` cargan el registro declarado;
  si el manifiesto no declara ninguno, usan el default del sector.

## Cómo añadir un registro

1. Copia una carpeta existente (p. ej. `tecnico-divulgativo/`) a `<slug>/`,
   minúsculas-con-guiones (`academico`, `narrativo`, `poetico`).
2. Rellena las secciones del esquema (abajo). No borres ninguna: los comandos
   leen estos encabezados.
3. Listo. `/speckit-constitution` lo mostrará en la lista.

## Esquema de un registro

```
# Registro: <nombre>
## Contrato del género            (quién lee, qué espera, qué promete la prosa)
## Frontera de capas              (qué decide este registro y qué no)
## Diales                          (formalidad, persona, densidad, figuras,
                                    humor, aserción, terminología, artefactos)
## La escala                       (mismo contenido en 3 registros: el propio
                                    y los dos hacia los que deriva)
## Deriva: síntomas y corrección   (hacia dónde se desliza el texto)
## Registro por modalidad          (cómo modula tutorial/how-to/reference/
                                    explanation, si aplica al género)
## Checklist de registro           (máx. 10 puntos)
## Origen                          (fuentes o decisión propia)
```

Ningún registro puede debilitar los principios NO NEGOCIABLES ni los dos
innegociables de la prosa-base. Un registro calibra; no exime.

## Registros disponibles

- `tecnico-divulgativo/`: guías técnicas para profesionales (default del
  sector tecnología).

(Pendientes: `academico`, `narrativo`, `poetico`.)

## Qué pasa si tu género no tiene registro propio (fallback)

Mientras el registro de tu género no exista, la guía usa `tecnico-divulgativo`
como **fallback declarado**: se escribe igualmente en el manifiesto (clave
`registro`) y en la adenda "Tono calibrado", nunca queda implícito. Las capas 1
(prosa-base) y 3 (voz) aplican exactamente igual; la deriva de género que el
fallback no cubre se compensa calibrando la adenda de tono en
`/speckit-constitution`. Cuando el registro propio exista (o lo crees con el
esquema de arriba), migrar es editar la clave `registro` del manifiesto y la
adenda: ningún capítulo escrito se invalida, la siguiente pasada de naturalidad
ya verifica contra el registro nuevo.

---

v1.0.0 (2026-07-04). Nace con la capa 2 de la pirámide de prosa.
