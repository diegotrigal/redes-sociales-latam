---
name: ig-human
description: >-
  Quita la huella de máquina de cualquier texto en español (rayas, comillas
  angulares, muletillas de IA como «potenciar», «sumérgete», «en el vertiginoso
  mundo de», caracteres invisibles) y lo califica con cinco revisiones antes de
  que salga. Úsala cuando haya que humanizar, cuando digan «¿esto suena a IA?»,
  «quítale lo de ChatGPT», «que no se note que lo hizo una IA», «límpialo», y
  siempre antes de enseñar un caption, guion, comentario, respuesta o DM.
---

# ig-human

En esta carpeta viven dos herramientas y las dos corren de verdad. Úsalas. No
lo hagas a ojo.

```bash
python3 humanize.py borrador.txt --reporte        # lo limpia y dice qué cambió
python3 detect.py borrador.txt                     # lo califica, cinco revisiones
python3 detect.py antes.txt despues.txt            # demuestra la diferencia
```

Las dos leen `slop.json`: 170 muletillas con su reemplazo llano, 18 tipos de
caracteres invisibles, 13 cambios tipográficos, 27 estructuras de modelo y una
lista de marcas de oralidad. No es una traducción del original en inglés: son
las muletillas que suelta un modelo cuando escribe en español, con entradas en
masculino y femenino para no romper la concordancia. Está hecho para editarse:
si la marca usa a propósito una palabra que el léxico quita, bórrala del
archivo.

## Por qué esto pesa más en Instagram de lo que parece

Los captions son cortos y los guiones se dicen en voz alta. Una línea que
suena a folleto pesa más en un caption de 600 caracteres que en un ensayo, y un
guion que nadie diría así se nota en la primera toma. La señal aquí no es que
un detector marque el post. Es que alguien se lo salta porque «suena a
agencia», o que el dueño del negocio se traba leyendo su propio guion.

En español, además, hay una huella que no existe en inglés: el texto que se
pensó en inglés y se tradujo. Títulos Con Mayúscula En Cada Palabra, «hace
sentido», «juega un rol clave», «al final del día», preguntas sin «¿». Eso
también se marca.

## Lo que se arregla solo

**1. Caracteres invisibles.** Espacios de ancho cero, unidores, guiones
suaves, BOM, caracteres de etiqueta, espacios duros y finos. Un teclado no los
produce, sobreviven al copiar y pegar y son lo más mecánico del texto
generado. `humanize.py` los borra todos, **menos** los que forman emojis
compuestos (👩‍🍳, 👨‍👩‍👧, 🏳️‍🌈): esos usan el mismo carácter de unión y
borrarlo parte el emoji en dos. En captions latinos, con emojis por todos
lados, eso importa.

**2. Tipografía.** Raya a coma (y la raya de diálogo al inicio de línea se va
sin dejar coma), guion medio a guion, comillas curvas y angulares («») a
rectas, puntos suspensivos de un carácter a tres puntos, viñeta a guion. En un
libro las comillas angulares están bien; en un caption de una pyme mexicana
son huella de modelo.

**3. Las muletillas.** «potenciar», «eleva tu», «sumérgete en», «desbloquea»,
«en el vertiginoso mundo de», «cabe destacar que», «a la hora de», «una amplia
gama de», «experiencia única», «solución integral», «aliado estratégico»,
«contenido de valor», «brindamos». Cada una se cambia por algo llano o se
borra, respetando mayúsculas y sin tocar URLs ni ligas de `wa.me`.

## Lo que NO se arregla solo

Las estructuras se **señalan, no se reescriben**, porque cambiarle la forma a
una oración necesita criterio:

- «No es solo X, es Y» y «No solo X, sino también Y»
- Tercias: «rápido, fácil y seguro.»
- «¿El resultado?» en una línea sola
- «¿Alguna vez te has preguntado…?», «¿Sabías que…?», «Imagina un mundo…»
- «Al siguiente nivel», «tu mejor versión», «no dudes en», «¡No esperes más!»
- Preámbulo de video: «en este video te voy a enseñar»
- Saludos de entrada: «¡Hola a todos!», «Qué onda, banda»
- Listas con emojis de viñeta (✅ ✅ ✅)
- Tres o más palabras en mayúsculas seguidas
- Muros de hashtags
- Pedidos en automático: «síguenos para más», «etiqueta a alguien», «dale like»
- Preguntas o exclamaciones sin «¿» o «¡» de apertura
- Títulos Con Mayúscula En Cada Palabra

Esa lista te toca. Reescribe cada línea señalada a mano, sin cambiar el
sentido, y vuelve a correr `detect.py`. Esto es lo que mueve la calificación
de REVISAR a PASA, y es lo que un script no puede hacer.

**Sobre los signos de apertura:** mucha gente en redes escribe «que onda?» sin
«¿», y eso es humano. Lo raro es mezclar: tres preguntas con «¿» y una sin.
Si la marca escribe estilo chat, que sea en todo el texto. Decídelo con
`voz.md`, no con la regla.

## Las cinco revisiones

`detect.py` califica cinco señales de 0 a 100, más alto es más humano:

| revisión | qué mide | cómo se ve la máquina |
| --- | --- | --- |
| RITMO | variación del largo de las oraciones | todas las oraciones del mismo largo |
| CONCRETO | números, nombres, cifras dichas («catorce mesas», «pesos») por cada 100 palabras | sustantivos abstractos, ni una cifra |
| MULETILLAS | muletillas del léxico por cada 100 palabras | vocabulario de folleto |
| HUELLA | invisibles, rayas, comillas curvas o angulares por cada 1,000 caracteres | tipografía perfecta |
| VOZ | marcas de oralidad, primera y segunda persona, estructuras de modelo | cero oralidad, revelaciones montadas |

Dos cosas de la versión en español que conviene saber:

- **VOZ no cuenta contracciones** (en español no hay) sino marcas de oralidad:
  «pues», «la neta», «ojo», «mira», «ni modo», «ahorita». La lista está en
  `slop.json` y está cargada a México: si el cliente es de Colombia, Argentina
  o Perú, agrégale sus muletillas reales («parce», «che», «pucha»).
- **«tu» y «tus» no cuentan como voz.** «Potencia tus ventas, optimiza tus
  tiempos, sorprende a tus clientes» es justo como escribe el marketing
  generado. Contar «tus» premiaba al modelo.
- **Un título en Mayúsculas no cuenta como dato concreto.** Una racha de
  palabras con mayúscula se cuenta como un solo nombre, y solo si no abre
  oración.

El veredicto pesa el promedio al 60 % y la **revisión más débil** al 40 %,
porque basta una señal. PASA pide 70 o más en total y ninguna revisión debajo
de 55.

## Dilo con honestidad

Son cinco heurísticas locales basadas en las señales que miran los detectores
públicos. Corren completas en la máquina del usuario y no se sube nada. **No**
son GPTZero, Originality, Copyleaks, Winston ni Turnitin, no llaman a sus APIs
y no pueden prometer su veredicto. Arreglar lo que miden suele mover esos
números, porque miden lo mismo de fondo. Esa es la promesa. No hagas una más
grande en nombre del usuario, y no le digas que su texto es «indetectable».

Tampoco hay todavía una validación con textos reales en español: los umbrales
vienen del original en inglés con ajustes. Si un texto que sabes que es humano
sale REVISAR, créele a tu oído y ajusta el umbral, no al revés.

## Orden de trabajo

1. `humanize.py borrador.txt -o limpio.txt --reporte`
2. Lee las estructuras señaladas. Reescribe esas líneas tú.
3. `detect.py borrador.txt limpio.txt` para enseñar el antes y después.
4. Si no PASA, arregla la revisión más débil y vuelve a correrlo. Dos vueltas
   es normal. Cinco quiere decir que el borrador se escribió con fórmula, y la
   solución es otro borrador, no más vueltas.
5. Enséñale al usuario el texto limpio y la calificación. Nunca la
   calificación sola.
