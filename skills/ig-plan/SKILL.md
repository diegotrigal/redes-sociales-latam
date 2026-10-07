---
name: ig-plan
description: >-
  Arma la semana en Instagram: qué publicar, en qué formato, cuándo y con
  quién interactuar, con el calendario comercial de México y Latinoamérica a la
  mano (quincenas, Buen Fin, Hot Sale, Día de las Madres, Día de Muertos).
  Úsala cuando digan «planea mi semana», «qué publico», «calendario de
  contenido», «parrilla», «no tengo nada que publicar», o quieran un horario de
  publicación y una lista de cuentas para interactuar.
---

# ig-plan

La sala de control. Todo lo demás en este paquete ejecuta; esto decide qué se
ejecuta. Córrelo una vez a la semana, el mismo día.

## Entrada

Si existen `~/.claude/instagram/voz.md`, `referencias.md` y `bitacora.md`,
léelos. Las referencias son la evidencia del propio usuario, de `/ig-viral`,
sobre qué fórmulas están pegando en su giro, y le ganan a cualquier cosa de
este archivo. La bitácora evita que el plan repita un tema de las últimas dos
semanas.

Lee también `fechas-mx.md` en esta carpeta y revisa qué cae en las próximas
**tres** semanas, no solo en esta: el contenido de temporada se empieza antes.

Si no existen, pide cuatro cosas y apúntalas:

1. Qué vende el usuario, y a quién. Si es local, en qué ciudad.
2. Los tres o cuatro temas por los que quiere que lo conozcan.
3. Qué pasó de verdad esta semana: un cliente, un número, un error, algo que
   hizo, una discusión. De ahí salen los posts.
4. Diez cuentas a las que vale la pena dejarse ver.

## Qué publicar

De cuatro a cinco posts por semana, y por lo menos tres reels. Los reels son
el único formato de Instagram que llega de forma confiable a gente que no
sigue la cuenta. Los carruseles profundizan con los que ya siguen. Las
historias son diarias y se planean aparte.

Mezcla en la semana, nunca dos del mismo tipo seguidos:

| tipo | cuántos | trabajo |
| --- | --- | --- |
| **Prueba** | 1 por semana | algo que pasó, con un número. Reel. |
| **Enseña** | 1 a 2 por semana | una cosa que quien ve puede hacer hoy. Reel o carrusel. |
| **Opinión** | 1 por semana | una postura que podría costarte seguidores. Reel. |
| **Historia** | 1 cada dos semanas | una escena con un costo. Reel. |
| **Oferta** | 1 cada dos semanas | lo que vendes, dicho directo, sin pedir perdón. Carrusel o historias. |
| **Detrás** | 1 cada dos semanas | el proceso del negocio (fórmula #28). Reel. Para negocios locales cuenta como Prueba. |

Para cada lugar da: el tema, el ángulo concreto que sale de lo que pasó esta
semana, el formato y el número de fórmula de `ig-reel/hooks.json`. No un tema,
un ángulo. «Pan de muerto» no es plan. «El año pasado se nos acabó a las 11 y
cien personas se fueron sin pan» es un reel.

## Fechas: úsalas sin volverte calendario

`fechas-mx.md` trae las fechas que mueven ventas en México y algunas de otros
países. Reglas para usarlas:

- **Empieza dos o tres semanas antes.** El reel de pan de muerto se publica a
  mediados de octubre, no el 1 de noviembre.
- **Solo si al negocio le toca.** Un despacho contable no tiene nada que decir
  del Día del Niño. Sí tiene mucho que decir en abril (declaración anual).
- **La quincena es semanal, no anual.** Si el negocio vende al consumidor, las
  ofertas van el 14-15 y el 29-30, cuando hay dinero.
- **Fechas serias se tratan en serio.** El 8 de marzo no es una promoción. El
  2 de octubre tampoco.
- **Revisa las fechas exactas del año.** Buen Fin, Hot Sale y Semana Santa se
  mueven. Si no estás seguro de la fecha de este año, dilo y pídele al usuario
  que la confirme.

## Cuándo publicar

Cuando el público está despierto y no trabajando. Para la mayoría del público
consumidor, eso es la tarde-noche, hora local; para un público de negocios,
temprano en la mañana. En México se cena tarde: de 8 a 10 de la noche suele
funcionar mejor que a las 6 para comida y entretenimiento.

Pero dilo claro: **la hora pesa mucho menos que los primeros dos segundos.**
Instagram sigue enseñando un reel por días si funciona, y entierra uno bien
programado que no. Si el usuario está afinando horarios antes de que sus
ganchos funcionen, está puliendo lo que no es, y hay que decírselo.

Usa la zona horaria del público, no la del usuario, si son distintas. México
tiene cuatro zonas y Quintana Roo no es la del centro.

## La ronda de interacción, que no es opcional

20 minutos al día, antes de publicar, no después. Arma una lista de 10:

- **5 de alcance**: cuentas con el público que el usuario quiere, donde un
  buen comentario se ve. Comenta temprano, antes de que el hilo tenga 200.
- **3 pares**: mismo tamaño, mismo giro, o negocios vecinos que no compiten
  (la cafetería y la panadería de la misma calle). Este grupo corresponde.
- **2 compradores**: gente que de verdad podría comprar. Comenta semanas antes
  de cualquier DM, y nunca vendas en un comentario.

Pásale la lista a `/ig-comentar`.

## Salida

```
SEMANA DEL 13 DE OCTUBRE
(en 3 semanas: Día de Muertos. Ya toca empezar.)

LUN  solo interacción  (20 min, lista abajo)
MAR  8:30pm  REEL      DETRÁS    #28 Así Se Hace      - 300 conchas antes de las 6
MIE  solo historias + interacción
JUE  8:00pm  CARRUSEL  OFERTA    Caption trabajo B    - cómo apartar pan de muerto sin fila
VIE  8:30pm  REEL      OPINIÓN   #22 El Dicho Al Revés - «el pan de muerto no se congela» (sí se puede)
SAB  -
DOM  7:00pm  REEL      HISTORIA  #21 A Media Frase    - el año que se acabó a las 11

HISTORIAS  todos los días, 3 a 5 cuadros, caja de preguntas el jueves.
QUINCENA   miércoles 15: historia con la oferta de la semana.

INTERACCIÓN  (5 alcance / 3 pares / 2 compradores)
  ...

Dime «escribe el martes» y lo hago.
```

Escribe el plan en `~/.claude/instagram/plan.md` para que las demás skills lo
lean. No se programa ni se publica nada en ningún lado. Esto es un plan y lo
corre el usuario.
