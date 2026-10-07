---
name: ig-reel
description: >-
  Escribe un reel de Instagram en español a partir de una idea suelta: tres
  ganchos de 29 fórmulas con calificación, el guion hablado, el texto en
  pantalla y una hoja de tiempos por sílabas, en la voz del usuario y revisado
  antes de grabar. Úsala cuando pidan un reel, un guion de video corto, un
  gancho, un voiceover, «hazme un reel de X», «qué digo en este video», o
  cuando estén por grabar y no tengan la primera línea.
---

# ig-reel

Convierte una idea suelta en un reel que la gente termina de ver.

En esta carpeta viven tres herramientas y corren de verdad. Úsalas. No
califiques el gancho a ojo y no adivines la duración.

```bash
python3 hookscore.py ganchos.txt              # ordena tus opciones de gancho
python3 hookscore.py --gancho "una línea"     # califica una sola
python3 beats.py guion.txt --meta 30          # hoja de tiempos antes de grabar
python3 silabas.py guion.txt                  # sílabas y segundos por línea
```

**Por qué sílabas y no palabras:** en español una palabra puede tener ocho
sílabas («desafortunadamente») y el mismo guion sale más largo que en inglés.
Los tiempos se calculan a 6 sílabas por segundo, que es un ritmo normal de
reel hablado a cámara. Si el usuario habla más rápido o más lento, que lea un
guion con cronómetro y pásale `--sps`.

## Antes de escribir

1. Lee `~/.claude/instagram/voz.md` si existe. Es el perfil de voz: cómo habla
   a cámara, si es de tú o de usted, de dónde es, qué nunca diría. Si no
   existe, pide **tres de sus reels**, transcríbelos o léelos, deduce la voz y
   escribe el archivo con la plantilla de `ig-reel/voz-plantilla.md`. Un guion en la
   voz equivocada no sirve, porque lo tiene que decir en voz alta.
2. Lee `hooks.json` en esta carpeta: 29 fórmulas, cada una con plantilla,
   ejemplo lleno, versión en pantalla, para qué sirve y cómo se echa a
   perder. Las 26 primeras vienen del original adaptadas; la 27 (comentario
   leído), la 28 (así se hace) y la 29 (cuánto cuesta) son nuevas y son las que
   más le funcionan a negocios locales.
3. Si la idea está flaca, no la rellenes. Haz una sola pregunta con todo junto:
   qué pasó, a quién, y cuánto costó o cuánto dejó. Un reel necesita una cosa
   concreta y cierta. Consíguela antes de escribir.
4. Si existe `~/.claude/instagram/referencias.md`, léelo. Lo escribe `/ig-viral`
   y es la evidencia del propio usuario sobre qué fórmulas funcionan hoy en su
   giro. Le gana a lo que dice este archivo.

## La forma

Un reel se decide en los primeros tres segundos y se sostiene en los
siguientes cinco.

```
0:00 - 0:03   GANCHO      la afirmación. Línea hablada y línea en pantalla,
                          escritas por separado. Movimiento en el primer cuadro.
0:03 - 0:08   LO QUE ESTÁ EN JUEGO   por qué le importa a quien ve. Una línea.
0:08 - ...    EL CUERPO   una idea por tramo, y la imagen cambia en cada tramo.
ÚLTIMOS 3s    LA ENTREGA  cumple lo que el gancho prometió, luego un solo pedido.
ÚLTIMA LÍNEA  EL LOOP     repite una palabra del gancho para que la segunda vista caiga limpia.
```

Duración: de 15 a 45 segundos es el rango útil. Los reels llegan a 3 minutos
y casi nadie debería usarlos.

## El ciclo

**1. Tres ganchos, no uno.** Pasa la idea por `hooks.json`, escoge tres
fórmulas que de verdad le queden y escribe la línea hablada y la de pantalla
de cada una. Fórmulas distintas, no tres versiones de la misma.

**2. Califícalos.** Las tres líneas habladas en un archivo, una por renglón, y
corre `hookscore.py`. Enséñale el ranking al usuario. Si el primero queda
debajo de 50, todavía no tienes el gancho y ninguna corrección lo arregla.

**3. Escribe el guion** con el gancho ganador. Español hablado, como habla el
usuario de verdad: «nos cayó», «ni se enteró», «ahorita». Líneas cortas. Nada
que tenga que ensayar. Respeta el tú o el usted de `voz.md` de principio a fin.

**4. Tómale el tiempo.** Corre `beats.py guion.txt --meta {duración}`. Arregla
cada marca: gancho de más de 3 segundos, tramo de más de 4, racha de tramos sin
nada concreto, falta de loop. Vuelve a correrlo hasta que salga limpio.

**5. Humanízalo.** Pasa el guion por `/ig-human` antes de enseñarlo. Una línea
que suena a escrita se nota en cuanto alguien la dice.

**6. Imprime el bloque.** El guion en un bloque de código, el texto en
pantalla aparte con sus tiempos, y luego:

```
REEL LISTO
gancho:      #3 Nadie Te Dice, 80 FUERTE
duración:    25.5s en 7 tramos, 153 sílabas a 6 síl/s
pantalla:    5 tarjetas
humanizador: 3 huellas quitadas, 78 PASA
caption:     corre /ig-caption después

Contesta «va» para guardarlo en la bitácora, o dime qué cambio.
```

**7. Nunca publiques.** Esta skill hace un guion. El usuario lo graba y lo
sube. Con el «va», agrega a `~/.claude/instagram/bitacora.md` la fecha, la
fórmula del gancho y la primera línea, para que `/ig-auditoria` tenga historia.

## El texto en pantalla es otro guion

Escríbelo aparte, siempre. Se lee antes de que se oiga.

- **Seis palabras o menos por tarjeta.** Lo está leyendo alguien con el
  celular en la mano que todavía no está escuchando.
- **La tarjeta del gancho aparece en el cuadro 1**, no después de un silencio.
- **Dentro de la zona segura.** En un cuadro de 1080x1920, nada arriba de y=230
  ni abajo de y=1440, y deja libres los 230 píxeles de la derecha. Ahí encima
  va la interfaz: el caption, los botones, el audio.
- **Subtítulos quemados en el cuerpo.** Casi todos ven el primer pase sin sonido.
- **Mayúscula solo al inicio y en nombres propios.** «Error de $18,000», no
  «Error De $18,000».

## Reglas que hacen la diferencia

- **Una idea por reel.** Si el guion trae dos, son dos reels. Dilo.
- **Números en vez de adjetivos.** «$4,200 pesos» le gana a «un buen de
  lana». Si el usuario no dio el número, pídelo en vez de escribir alrededor
  del hueco.
- **Corta la intro.** Sin saludo, sin «en este video», sin nombre, sin logo.
  El video empieza en la frase a la que normalmente llegarías en el segundo
  seis.
- **Cambia la imagen en cada tramo.** Una toma fija de 8 segundos es donde la
  gente se va, y `beats.py` lo marca.
- **Un solo pedido al final.** Comentar una palabra, guardar, o escribir por
  WhatsApp. Uno.
- **Nunca inventes.** Ni cifras, ni clientes, ni ventas, ni resultados a
  nombre del usuario, ni siquiera de relleno. Si falta un número, deja
  `{{tu número}}` en el guion y márcalo.
- **No escribas para un audio en tendencia que el usuario no puede usar.** Las
  cuentas de negocio tienen la biblioteca de música limitada. Si la idea
  necesita su propia voz, dilo.
- **Si el negocio vende algo regulado** (alcohol, suplementos, tratamientos
  estéticos, servicios médicos), revisa `ig-caption/reglas-mx.md` antes de
  prometer resultados.

## Ejemplo

```
/ig-reel se nos cayó el internet en viernes y la comandera siguió funcionando
```

```
GANCHOS  (calificados)
  80  FUERTE  #1  Lo Que Me Costó   «Un viernes sin internet nos costó $9,000 en comandas.»
                                    pantalla: $9,000 EN UNA NOCHE
  51  VA      #3  Nadie Te Dice     «Nadie te dice qué pasa cuando se cae el internet en viernes.»
                                    pantalla: SE CAYÓ EL INTERNET
  41  FLOJO   #28 Así Se Hace       «Así funciona la cocina cuando no hay señal.»
                                    pantalla: SIN SEÑAL

Grabaría el #1: el número es suyo, se lee de un vistazo y el loop
cierra con «viernes».
```
