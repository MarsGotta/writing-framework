# Bases de sector

Una **base de sector** define los valores por defecto que `/speckit-constitution`
propone al rellenar las *adendas del proyecto* (la capa por guía que se monta
sobre el núcleo de la constitución). El núcleo no cambia entre guías; lo que
cambia es el sector: una guía de desarrollo web no escribe igual que una de
veterinaria, aunque ambas compartan tu voz y tus pasadas de revisión.

Cada sector es **un archivo**. El comando lista todos los `*.md` de esta carpeta
(menos este índice) y los ofrece como opción. Para añadir un sector nuevo basta
crear el archivo: aparece solo, sin tocar código.

## Cómo añadir un sector

1. Copia un archivo existente (p. ej. `tecnologia.md`) a `<slug>.md`, donde
   `<slug>` es minúsculas-con-guiones (`veterinaria`, `medicina`, `ciencia`,
   `humanidades`, `literatura`).
2. Rellena las secciones del esquema (abajo). No borres ninguna: el comando lee
   estos encabezados para derivar los valores por defecto.
3. Listo. `/speckit-constitution` lo mostrará en la lista de sectores.

## Esquema de un archivo de sector

Todos los archivos siguen los mismos encabezados, en este orden:

```
# Sector: <Nombre>
## Alcance                                  (qué temas cubre, ejemplos)
## Registro por defecto                      (capa 2 propuesta: slug de
                                              references/registros/)
## Tono por defecto                          (calibración de voz propuesta)
## Persona gramatical y registro             (plural inclusivo, tú/usted, humor)
## Anglicismos y extranjerismos admitidos    (lista por defecto, ampliable)
## Matices léxicos del sector                (overrides al Principio IV del núcleo)
## Fuentes de autoridad esperadas            (qué cuenta como cita fiable)
## Datos volátiles típicos                   (qué hay que fechar y reverificar)
## Forma típica del ejemplo recurrente       (qué clase de caso recurrente encaja)
## Relajaciones estructurales por defecto    (normalmente: ninguna)
## Convenciones de citación                  (estilo y mínimos del sector)
```

El núcleo de la constitución manda siempre. Una base de sector solo **propone
valores por defecto** y declara **matices** donde el dominio lo justifica (por
ejemplo, en tecnología "comando" es término legítimo y no se fuerza a "orden").
Ninguna base puede debilitar los principios NO NEGOCIABLES (voz, brief,
revisión, neutralidad): solo calibra lo que el núcleo deja explícitamente al
proyecto.

## Sectores disponibles

- `tecnologia.md`: IA, desarrollo web y de software, datos, infraestructura.

(Pendientes de crear: veterinaria, medicina, ciencia, humanidades, literatura.)

## Qué pasa si tu sector no existe todavía (fallback)

`/speckit-constitution` solo lista los sectores con archivo en esta carpeta. Si
el tuyo no está, hay dos caminos y ninguno bloquea la guía:

1. **Crear la base** (recomendado, son minutos): copia `tecnologia.md` al slug
   nuevo y rellena el esquema de arriba. Aparece solo en la lista.
2. **Seguir sin base de sector**: el comando rellena las adendas contigo en el
   diálogo, sin defaults propuestos, y el registro hay que elegirlo
   explícitamente (hoy, `tecnico-divulgativo`, el único implementado; ver el
   fallback en `references/registros/_index.md`).

En ambos casos el núcleo de la constitución aplica entero: la base de sector
solo aporta defaults y matices, nunca condiciona las pasadas ni los gates.
