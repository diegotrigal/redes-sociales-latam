---
name: ig-caption
description: >-
  Escribe el caption de Instagram en español (la línea que sobrevive al corte
  de «... más», el cuerpo, el único pedido, las palabras de búsqueda y los
  hashtags) y lo revisa antes de que salga, incluido lo que pide PROFECO cuando
  hay precio o promoción. Úsala cuando digan «escribe el caption», «el copy»,
  «la descripción», «qué le pongo», cuando tengan un reel o un carrusel listo y
  falte el texto, o cuando pregunten por hashtags.
---

# ig-caption

En esta carpeta vive una herramienta y corre:

```bash
python3 caption.py caption.txt
python3 caption.py caption.txt --busquedas "pan de muerto,panadería en morelia"
```

Imprime el caption como lo enseña el feed: los primeros 125 caracteres en una
caja, todo lo demás detrás del toque. Lee esa caja antes que cualquier otra
cosa que hayas escrito. En español esto aprieta más: el mismo mensaje sale
entre 20 y 25 % más largo que en inglés.

## Primero, decide qué trabajo tiene este caption

Esta decisión es la que arruina captions cuando se salta.

**Trabajo A: el video ya enganchó.** Un reel trae su propio gancho en los
primeros segundos, hablado y en pantalla. El caption no es un segundo gancho,
y competir con el video es la forma de perder los dos. Su trabajo es el
pedido, el contexto que hace que el pedido tenga sentido, y las palabras con
las que la gente busca.

**Trabajo B: el caption es el contenido.** Una foto, una imagen sola, la
portada de un carrusel que abre una pregunta. Aquí la primera línea es el
gancho y funciona igual que el de un reel: concreta, corta y cortada en
suspenso, no a media subordinada.

Pregunta cuál estás escribiendo. Si el usuario tiene un reel con un gancho
fuerte, escribe A y di por qué.

## La forma

```
Línea 1     125 caracteres visibles. Trabajo A: el pedido, directo.
            Trabajo B: el gancho.
            Nunca un saludo, nunca un hashtag, nunca un emoji de primer carácter.
Cuerpo      párrafos cortos, una línea en blanco entre cada uno. De dos a seis.
            Aquí van las palabras de búsqueda.
El pedido   uno. Comentar una palabra, guardar, o escribir por WhatsApp. Uno.
Hashtags    hasta cinco, en su propia línea al final, o ninguno.
```

El límite es de 2,200 caracteres y casi nada necesita 2,200. Un caption que
se gana el toque y entrega 600 caracteres le gana a uno que entrega 1,800.

## Hashtags, sin cuento

Los hashtags ya no dan alcance, y la plataforma lo dijo con un cambio de
producto: **Instagram topó los hashtags en cinco por publicación el 18 de
diciembre de 2025**, antes eran treinta, diciendo que «usar menos (hasta 5) y
más específicos» funciona mejor que muchos genéricos. Adam Mosseri ya había
dicho en febrero de 2025 que los hashtags son una etiqueta, no una palanca de
distribución.

Así que: hasta cinco, específicos, como etiquetas de tema. `#viral`,
`#parati`, `#fyp`, `#explorar`, `#mexico`, `#emprendedores` no describen nada.
Fuera. Si el negocio es local, el hashtag útil lleva la ciudad o la colonia:
`#panaderiamorelia`, no `#panaderia`.

## Las búsquedas pesan más que los hashtags

La búsqueda de Instagram lee el texto del caption. Así que la frase con la que
el usuario quiere que lo encuentren va en el caption como frase que alguien
escribiría, en una oración normal. «Pan de muerto en Morelia» como palabras en
la tercera línea, no «#pandemuertomorelia» en un bloque al final. Para negocios
locales, nombra la ciudad o la colonia: es lo que la gente teclea.

Pide dos o tres de esos términos y pásalos a la revisión:

```bash
python3 caption.py borrador.txt --busquedas "pan de muerto,panadería en morelia"
```

## Lo que en México se revisa además

Esto no está en el original en inglés y en México cuesta quejas o multas.
`caption.py` lo avisa; tú decides con el usuario. No es asesoría legal: ver
`reglas-mx.md` (en esta carpeta).

- **PRECIO.** Si das precio, que sea el total con impuestos: «$65 IVA
  incluido» o el precio final. Un «$65 + IVA» en un post para consumidor final
  es justo lo que PROFECO observa.
- **PROMOCIÓN.** «2x1», «gratis», «20 % de descuento», «meses sin intereses»
  necesitan vigencia y condiciones: «del 25 de octubre al 2 de noviembre o
  hasta agotar existencias».
- **Productos regulados** (alcohol, suplementos, tratamientos estéticos,
  servicios de salud): nada de promesas de resultado. Si es alcohol, la leyenda
  de consumo responsable.
- **Publicidad pagada de un creador:** que se marque como tal (la etiqueta de
  «colaboración pagada» de Instagram o un «publicidad» claro).

## Reglas

- **Sin ligas en el caption.** No se les puede dar clic. Una URL en el texto es
  texto muerto. Va en la bio, en una historia con sticker de enlace, o en el DM.
- **El teléfono sí puede ir.** En Latinoamérica la gente copia el número para
  escribir por WhatsApp. Si va, completo y con lada: «443 123 4567».
- **Un pedido.** Dos pedidos es lo mismo que ninguno. `caption.py` los cuenta.
  «Pide por WhatsApp» y «síguenos» son dos.
- **La palabra para comentar tiene que poder escribirse.** Una palabra, sin
  espacios, sin emoji, sin acento si se puede, y dila en voz alta en el video.
  `Comenta PAN` sirve. `Comenta «quiero la receta del pan»` no.
- **El emoji es puntuación, no decoración.** La revisión marca más de 4 por
  cada 100 caracteres.
- **El texto alternativo vale 20 segundos.** En carruseles y fotos, escríbelo.
  Lo leen los lectores de pantalla y lo lee Instagram.

## El ciclo

1. Decide trabajo A o B y dilo.
2. Escribe el borrador, en la voz de `~/.claude/instagram/voz.md`.
3. Pásalo por `/ig-human`. Los captions son cortos, así que el relleno se nota
   más aquí que en cualquier otra parte.
4. Corre `caption.py` con las búsquedas del usuario. Arregla cada FALLA.
   Decide cada AVISO en voz alta, no en silencio.
5. Imprime el bloque listo para copiar y luego el resumen:

```
CAPTION LISTO
trabajo:    A - el reel trae el gancho
visible:    118 de 125 caracteres antes del corte
pedido:     uno, comentar PAN
hashtags:   3
búsquedas:  «pan de muerto» en la línea 1, «panadería en Morelia» en la 3
precio:     $65 IVA incluido
promoción:  vigencia del 25 oct al 2 nov
revisión:   LISTO
```

No se publica nada. El usuario lo pega.
