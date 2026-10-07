---
name: ig-reciclar
description: >-
  Convierte una pieza larga (un video de YouTube, un podcast, un en vivo, un
  newsletter, una nota de blog, una plática con un cliente, un audio de
  WhatsApp largo) en una semana de reels y carruseles en español. Úsala cuando
  digan «recicla esto», «sácale reels a esto», «tengo un video/podcast/
  transcripción», «pártelo», o peguen algo largo y lo quieran en Instagram.
---

# ig-reciclar

Una buena pieza larga trae de cuatro a seis posts. La mayoría saca uno y tira
el resto.

## Entrada

Una transcripción, un artículo, un newsletter, un guion, el resumen de una
llamada, un en vivo. Si el usuario da una URL y esta sesión tiene una
herramienta para transcribir, úsala; si no, pide que la pegue. Lee todo antes
de sacar nada.

Si la fuente es un video del usuario, pide también el archivo. Un reel con su
propio material le gana a uno donde vuelve a leer lo que ya dijo.

Si la fuente está en inglés, no la traduzcas: **reescríbela.** Los ejemplos
gringos (dólares, «401k», Black Friday) se cambian por los de aquí (pesos,
Afore, Buen Fin), o se quitan. Y nunca presentes como propio algo que dijo
otra persona.

## Extrae, no resumas

Un resumen de un video no es un reel. Nadie quiere el resumen. Recorre la
pieza y saca lo que se sostiene solo:

| sacar | qué es |
| --- | --- |
| **Afirmaciones** | cada oración que empezaría una discusión |
| **Números** | cada cifra, costo, duración, porcentaje |
| **Historias** | cada momento con una persona, una escena y un costo |
| **Mecanismos** | cada «la forma en que esto de verdad funciona es…» |
| **Errores** | cada vez que admite algo que salió mal |
| **Frases** | cada oración que ya se puede citar tal cual |

Haz la lista de lo que encontraste, con conteos, antes de escribir nada. Si la
pieza da menos de cuatro, está flaca, y cuatro posts exprimidos de ahí van a
salir flacos. Dilo.

## Luego escoge el formato de cada cosa

No todo es reel.

- **Afirmación, error, historia**: reel. Necesitan voz y cara.
- **Mecanismo, lista numerada**: carrusel. Se tienen que releer.
- **Una frase citable**: un cuadro de historia, no un post.

## Luego arma la semana

Cada pieza se vuelve un post y cada post se sostiene completamente solo. Quien
lo ve no vio la fuente y nunca la va a ver. Nunca escribas «como dije en mi
último video». El post es la cosa.

Asígnale a cada uno una fórmula de `ig-reel/hooks.json` y varíalas. Cinco
posts de una misma fuente con la misma forma de gancho se leen como fábrica de
contenido, porque lo son.

Si la fuente es un video del usuario, **usa el material real**. El clip donde
lo dijo, con la reacción real, le gana a volver a grabar. Corta en la frase,
no en la respiración.

Ordena la semana para que la afirmación más fuerte vaya primero, la historia a
media semana y el mecanismo al final, cuando los que vieron los primeros ya lo
están esperando.

## Salida

```
FUENTE: «Por qué dejamos de dar cotizaciones por teléfono» (en vivo de 42 min, 8,900 palabras)

ENCONTRÉ  5 afirmaciones, 9 números, 3 historias, 4 mecanismos, 2 errores, 7 frases

SEMANA
MAR  REEL      #2  Deja De Hacerlo     Deja de cotizar por teléfono
                                       usa el clip del 14:20, se ríe al final
MIE  CARRUSEL  caption trabajo B       El formulario de 4 preguntas que reemplazó la llamada
VIE  REEL      #21 A Media Frase       «…y nos pidió el reembolso nueve días después»
DOM  REEL      #5  Antes Tardaba       Seis horas a la semana de vuelta, con una liga de WhatsApp

Dime «escribe el martes» y lo hago.
```

Luego escribe a pedido, de uno en uno, cada uno por `/ig-reel` y `/ig-human`.
No sueltes cuatro guiones terminados de golpe. Van a sonar igual y el usuario
no va a grabar ninguno.
