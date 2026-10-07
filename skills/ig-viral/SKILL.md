---
name: ig-viral
description: >-
  Investiga qué reels están funcionando ahorita en el giro del usuario, los
  ordena por cuánto le ganaron a su propia cuenta, nombra la fórmula de gancho
  de cada uno y lo vuelve un archivo de referencias para grabar. Úsala cuando
  digan «busca videos virales», «qué está funcionando», «qué publica la
  competencia», «destripa esta cuenta», «hazme referencias», «por qué este reel
  pegó», o cuando pregunten qué hacer después y no haya evidencia.
---

# ig-viral

La skill de investigación. Las demás escriben; esta va y mira. Córrela cada
mes, no cada día. Las fórmulas duran una temporada.

En esta carpeta vive una herramienta y corre:

```bash
python3 swipe.py capturados.tsv --out ~/.claude/instagram/referencias.md
```

## La idea que hace que valga la pena

**Las vistas solas no son evidencia.** Una cuenta con dos millones de
seguidores y 400,000 vistas tuvo un martes tranquilo. Una de cuatro mil con
400,000 vistas encontró algo, y ese algo se puede copiar.

Así que aquí todo se ordena por **múltiplo**: vistas entre la mediana reciente
de esa misma cuenta. Arriba de 3x es señal. Abajo de 1.5x es un día normal de
esa cuenta y no enseña nada, por grande que se vea el número.

Junta cuentas **de hasta unas 10 veces el tamaño del usuario**. Una fórmula
que funciona con 2 millones de seguidores muchas veces funciona porque tiene 2
millones de seguidores.

## Paso 1: escoge las cuentas

Pide de 6 a 12 cuentas al usuario, o propónlas y que las apruebe:

- **4 directas**: mismo giro, misma oferta, un poco más adelante. Si el negocio
  es local, que incluya competidores de otras ciudades: el de tu ciudad no te
  va a enseñar nada que no veas en la calle.
- **4 de al lado**: otro giro, mismo público. De aquí se toman formatos antes
  de que alguien del giro los tenga.
- **2 a 4 grandes**: cuentas mucho más grandes, solo para formato, nunca para
  frecuencia ni tono. En español hay mucho de dónde sacar: México, España,
  Colombia y Argentina publican distinto; vale la pena ver los cuatro.

Pídele también que abra su colección de **Guardados**. Es el corpus más rápido
y más relevante que existe, y ya viene filtrado por su gusto.

## Paso 2: ve a ver

Usa la herramienta de navegación que la sesión tenga de verdad: un navegador
integrado, la extensión conectada al Chrome del usuario, o uso de computadora.
No hay API para esto y no hace falta, porque el volumen es tan chico que se
puede leer.

**Reglas que no se negocian:**

- **Nunca inicies sesión en Instagram por el usuario y nunca pidas su
  contraseña.** Si una página pide sesión, el que ya tiene sesión es él. Maneja
  su navegador con él presente, o pídele que pegue los datos. Si no está
  presente, **pídele que pegue**: es la opción segura y casi igual de rápida.
- **Esto es leer, no raspar.** Diez cuentas, una docena de reels cada una, a
  velocidad humana. La recolección automática en volumen viola los Términos de
  Uso de Instagram y le bloquea acciones a la cuenta. No armes un crawler, no
  uses un servicio de scraping y no lo dejes corriendo en segundo plano.
- **Copia la fórmula, nunca el video.** La forma del gancho, la estructura, la
  duración, el patrón de cortes. No su guion, no su voz, no su edición. Pon de
  qué cuenta salió cada renglón.

**Qué apuntar de cada reel**, en las palabras del creador:

| campo | notas |
| --- | --- |
| cuenta | el usuario |
| seguidores | del perfil (sirven «48k» o «48 mil») |
| mediana | ve los últimos 12 reels y toma la cifra de en medio |
| vistas | de este reel |
| gancho | la primera línea, dicha o en pantalla, tal cual, con todo y faltas |
| pantalla | la primera tarjeta de texto, si es distinta |
| duración | segundos |
| pedido | qué pidió al final |

La mediana es la importante. Sin ella regresas a ordenar por seguidores, que es
justo lo que esta skill existe para evitar.

**Cuando Instagram no enseña suficiente:** la misma gramática de gancho corre
en YouTube Shorts y en TikTok. En YouTube las vistas y los subtítulos son
públicos y no hace falta sesión. Si `yt-dlp` está instalado, sirve para sacar
la primera línea dicha; si no, pídele al usuario que pegue los datos. **No lo
instales sin preguntar.**

```bash
# vistas de los shorts de un canal
python3 -m yt_dlp --flat-playlist --playlist-end 40 -J \
  "https://www.youtube.com/@CANAL/shorts" > canal.json

# la primera línea dicha de un short, de sus subtítulos automáticos
python3 -m yt_dlp --skip-download --write-auto-subs --sub-langs "es.*" \
  --sub-format json3 -o gancho "https://www.youtube.com/watch?v=ID_DEL_VIDEO"
```

Toma cada palabra de los subtítulos con marca de tiempo antes de 3.0 segundos.
Ese es el gancho, como se dijo, no como se escribió.

## Paso 3: ordénalo

Llena un archivo separado por tabuladores con encabezado y corre el script:

```
cuenta	seguidores	mediana	vistas	gancho
@pan_espiga	4.2k	1800	96k	Así hacemos 300 conchas antes de las 6 de la mañana.
```

```bash
python3 swipe.py capturados.tsv --out ~/.claude/instagram/referencias.md
```

Calcula el múltiplo, nombra la fórmula del gancho con las mismas 29 fórmulas
de las que escribe `/ig-reel`, califica cada gancho con `hookscore.py` e
imprime qué separa al tercio de arriba del de abajo.

## Paso 4: di qué significa, con cuidado

Reporta tres cosas y nada más:

1. **Qué fórmulas se repiten** en el tercio de arriba, con conteo. Dos fórmulas
   que salen cuatro veces cada una en seis cuentas es hallazgo. Una que sale
   dos veces, no.
2. **Qué tienen en común en la estructura** los de arriba que los de abajo no:
   largo del gancho, si la entrega es visual, si el primer cuadro se mueve,
   dónde va el pedido.
3. **Los que quedaron sin clasificar.** Cada gancho que el clasificador no pudo
   nombrar es ruido o una fórmula que todavía no está en `hooks.json`. Léelos a
   mano. Es la columna más valiosa de la salida y es la razón por la que el
   script imprime el conteo. Si encuentras una fórmula nueva que se repite,
   propón agregarla a `hooks.json` con su regex.

Luego di el tamaño de la muestra y la confianza en palabras. Cuarenta reels en
seis cuentas sostienen una afirmación. Doce no, y decirlo es la diferencia
entre investigar y leer el horóscopo.

## Paso 5: vuélvelo algo que se grabe

Para las tres fórmulas de arriba, escribe **la versión del usuario**: su
historia, su número, con la forma que está funcionando. Pásale cada una a
`/ig-reel` con el número de fórmula ya escogido.

Nunca entregues «haz un reel como este». Entrega una línea que pueda decir
mañana.

## Salida

```
REFERENCIAS  ·  38 reels  ·  7 cuentas  ·  base: mediana de la cuenta

ARRIBA DE 3x
  53.3x  gancho 60  #28 Así Se Hace     @pan_espiga    96,000  (mediana 1,800)
  11.2x  gancho 79  #9  Róbate Esto     @cafe_c       180,000  (mediana 16,100)
  ...

QUÉ SE REPITE
  #28 Así Se Hace     x5 en el tercio de arriba, 0 abajo
  #29 Cuánto Cuesta   x4
  largo del gancho    8 palabras arriba, 19 abajo

SIN CLASIFICAR (6)
  Dos tienen la misma forma y no está en hooks.json: abren con la
  reacción de un cliente probando algo. Vale la pena agregarla.

TU VERSIÓN
  #28  «Así sacamos 120 pedidos de pan de muerto en una mañana.»
  ...
```

Escribe el archivo en `~/.claude/instagram/referencias.md`. `/ig-reel` y
`/ig-plan` lo leen, y ese es el punto: después de correr esto una vez, el resto
del paquete trabaja con la evidencia del usuario y no con supuestos.

Esta skill no publica, no sigue, no da like ni manda mensajes. Lee.
