---
name: ig-comentar
description: >-
  Escribe comentarios en posts y reels de otras cuentas que se lean como una
  persona con opinión, no como bot, en español. Úsala cuando el usuario pegue
  un post o un reel y quiera comentar, diga «comenta esto», «qué le pongo
  aquí», «interactúa con esto», o quiera un lote para su ronda diaria de
  interacción.
---

# ig-comentar

Comentar son los veinte minutos que más rinden en Instagram y los más fáciles
de hacer mal. Un comentario arriba en un reel de 40,000 vistas lo ve más gente
que la mayoría de los posts de una cuenta, y es el único lugar donde un
desconocido puede brincar directo a un perfil.

Un comentario genérico es peor que ninguno. Gasta un toque que no lleva a
ningún lado y marca a la cuenta como «grupo de interacción» ante la única
persona cuya opinión importaba: el creador.

## Entrada

El usuario pega el texto del post o reel, o una captura, con el nombre de la
cuenta. Si da una URL que no puedes abrir, pídele que la pegue. No uses un
navegador para raspar el feed y no publiques nada.

## Los nueve tipos de comentario

Escoge según lo que es el post. Nunca te vayas al tipo 1 por default.

| # | tipo | cuándo | forma |
| --- | --- | --- | --- |
| 1 | **Aporta un dato** | el post afirma algo que puedes respaldar con un número | «Igual con nosotros: el 40 % de…» |
| 2 | **El caso que falta** | el post tiene razón pero está incompleto | «Esto aplica hasta que {condición}.» |
| 3 | **Desacuerdo con respeto** | de verdad crees que está mal | primero en qué coincides, luego dónde te separas |
| 4 | **Extiende una línea** | hay una línea buena en el post | cítala y construye sobre ella |
| 5 | **La pregunta de verdad** | el post se saltó la parte difícil | una pregunta, concreta |
| 6 | **El recibo** | tú ya hiciste lo que describe | qué pasó, en dos oraciones |
| 7 | **La corrección** | hay un error de hecho | ten razón, sé breve, sé amable, ten la certeza |
| 8 | **Otra lectura** | los datos están bien, el marco no | «Otra forma de verlo:» |
| 9 | **La de una línea** | el post no necesita nada, quieres presencia | menos de 10 palabras, chistosa o cierta |

## Reglas

- **De una a tres oraciones.** Los comentarios se leen en una columna angosta
  abajo de un video. Un párrafo se esconde detrás de «más» y nadie le pica.
- **Nunca abras con** «Excelente post», «Me encanta», «Qué cierto», «Esto 👏»,
  «Lo necesitaba hoy», «Brutal», «Tal cual 🙌» ni con el nombre del creador
  con signos de admiración. Todos son invisibles.
- **Nada de comentarios de puro emoji** y nada de emoji como primer carácter.
- **Nunca repitas el reel.** Todos los que ven ya lo vieron.
- **Una idea.** Un comentario con dos puntos se lee como secuestro del hilo.
- **Di lo específico.** Si el comentario cabe abajo de cualquier post del tema,
  no es comentario, es ruido.
- **Nunca vendas.** Ni la oferta, ni la liga, ni «pásate a mi perfil», ni
  «info por DM». Es la forma más rápida de que te bloquee justo la persona a la
  que querías llegar.
- **El registro del otro.** Si la cuenta habla de usted, contesta de usted. Si
  es de «qué onda, banda», no contestes como notario.
- **Temprano pesa más aquí que en cualquier lado.** Un comentario en la
  primera hora de un reel que luego viaja, viaja con él.

## Salida

Da **dos opciones de tipos distintos**, con etiqueta, más una línea de cuál
publicarías y por qué. Pasa las dos por `/ig-human` primero: los comentarios
son cortos, así que una raya o una frase de folleto pesa más que en un caption.

```
OPCIONES DE COMENTARIO  (en el reel de @cuenta sobre subir precios)

[6 · Recibo]
Subimos 15 % en marzo y se fue un solo cliente, el que pedía factura con
tres semanas de retraso. Tardamos ocho meses en dejar de tenerle miedo.

[3 · Desacuerdo con respeto]
De acuerdo con avisar antes. Lo que yo no haría es subirlo a media temporada:
nos pasó en diciembre y perdimos una posada que ya estaba amarrada.

Publica la primera. Concede algo y trae un número.
```

## Modo lote

Para una ronda de interacción, pide los 5 a 10 posts como texto pegado en un
solo mensaje, regresa un comentario por post en un solo bloque, y lleva nota
en `~/.claude/instagram/bitacora.md` de a quién se le comentó esta semana.
Comentarle a las mismas tres cuentas todos los días se nota, y se ve como lo
que es.

## Nunca

No publiques solo, no automatices comentarios y no uses un navegador para
publicar en nombre del usuario. La interacción automatizada viola los
Términos de Uso de Instagram y bloquea acciones de la cuenta. Esta skill
escribe el comentario. El usuario lo publica.
