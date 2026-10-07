---
name: ig-carrusel
description: >-
  Arma un carrusel de Instagram en español: la portada que se gana el
  deslizamiento, el texto de cada lámina y los archivos de 1080x1350 para
  subir. Úsala cuando digan «carrusel», «láminas», «slides», «post de varias
  imágenes», «vuélvelo carrusel», o cuando la idea sea una lista o unos pasos
  que se morirían en una sola imagen.
---

# ig-carrusel

El carrusel es el formato que más tiempo retiene en el perfil, porque
deslizar es una interacción y bajar no. Además tiene segunda oportunidad:
Instagram puede volver a enseñarlo empezando en otra lámina a quien no
interactuó la primera vez, así que la lámina dos también tiene que valer sola.

El formato premia una idea partida en pasos. Castiga un caption cortado en
pedazos.

## Cuándo usarlo en vez de un reel

Usa carrusel cuando la idea tiene **secuencia y hay que releerla**: pasos, un
método con partes, un antes y después, una lista que vale la pena guardar
(menú, precios, horarios, cómo pedir). Usa reel cuando la idea tiene
movimiento, una cara, o una entrega que hay que ver pasar.

Si la idea es una sola afirmación, no es ninguno de los dos. Pásala a
`/ig-reel` y dilo.

## Estructura

De 6 a 10 láminas. El tope es 20 y 20 casi siempre es un libro que nadie
termina. Con menos de 5 el deslizamiento ni empieza.

```
1         PORTADA    el gancho. 6 palabras o menos, a un tamaño que se lea en
                     la miniatura del perfil. Una línea de promesa abajo.
2         LO QUE ESTÁ EN JUEGO   por qué importa, en una oración. Esta lámina
                     también es portada, así que no puede ser preparación.
3 a N     UNA IDEA POR LÁMINA. Título de 3 a 7 palabras, máximo 25 palabras
                     abajo. Si una lámina necesita un párrafo, son dos láminas.
N+1       RESUMEN    todo en una lista. Esta es la que se captura y se manda.
ÚLTIMA    PEDIDO     una acción. Guardar, comentar una palabra o escribir por
                     WhatsApp. Una.
```

## Reglas del texto

- **La portada es el 80 % del resultado.** Seis palabras. Grandes. Nada en el
  resto salva una portada que nadie desliza.
- **Mayúscula solo al inicio.** «Cómo pedir sin hacer fila», no «Cómo Pedir
  Sin Hacer Fila». El título con mayúscula en cada palabra es calco del inglés
  y `/ig-human` lo marca.
- **Diseña para el recorte del perfil.** La cuadrícula recorta a un rectángulo
  vertical y la proporción exacta ha cambiado más de una vez. Hazlo a
  1080x1350 y deja el texto de la portada lejos de los 120 píxeles de cada
  orilla, y el recorte deja de importar.
- **Numera las láminas** (3/8). Más gente llega al final cuando ve dónde
  termina.
- **Ninguna lámina es un párrafo.** Si no cabe en 25 palabras, pártela.
- **La lámina de resumen es la que se captura y se manda.** Mandar es la
  señal más fuerte que puedes ganarte, y en Latinoamérica se manda por
  WhatsApp. Que se entienda sola, sin contexto.
- **El usuario en cada lámina**, chiquito, en una esquina. Las capturas viajan
  sin ti, y por WhatsApp más.
- **Si hay precio, que sea el total** con IVA, y si hay promoción, con
  vigencia. Ver `ig-caption/reglas-mx.md`.
- **Texto alternativo en la portada, por lo menos.** Lo leen los lectores de
  pantalla y lo lee Instagram.

## Hacer los archivos

Instagram pide 1080x1350 (4:5), JPEG o PNG, hasta 20. Hazlo en HTML e imprime
cada lámina:

```bash
# una <section> por lámina, 1080x1350, page-break-after: always
# luego Chrome headless --print-to-pdf, o el convertidor de HTML a imagen que ya uses
```

Escribe el HTML con `width:1080px; height:1350px`, un solo color de acento y
letra de 32px como mínimo, porque se lee en un celular a un tercio de su
tamaño real. Si el proyecto tiene manual de marca, skill de marca o sistema de
diseño, úsalo y no inventes paleta. Revisa que las fuentes tengan acentos y
eñe antes de entregar: una tipografía de exhibición sin «ñ» rompe la palabra
«diseño» en la portada.

## Salida

Primero el texto lámina por lámina, como lista numerada que el usuario lea en
diez segundos y corrija antes de que se haga nada. Luego el **caption**, que en
un carrusel es el trabajo B de `/ig-caption`: aquí el caption sí trabaja,
porque la portada ya se gastó sus seis palabras.

Pasa los dos por `/ig-human`. Haz los archivos solo cuando el usuario apruebe
el texto.

```
CARRUSEL  ·  8 láminas

1  PORTADA   EL PAN DE MUERTO SIN FILA
             Apártalo hoy y pásalo a recoger.
2  EN JUEGO  El año pasado se nos acabó a las 11. Cien personas se fueron sin pan.
3            CÓMO APARTAR
             Mándanos tu nombre y cuántas piezas por WhatsApp.
...
7  RESUMEN   Los cuatro pasos, en orden.
8  PEDIDO    Escríbenos «PAN» al 443 123 4567.

Caption: trabajo B, gancho en la línea 1, un pedido, 3 hashtags.
```

No se sube nada. El usuario lo publica.
