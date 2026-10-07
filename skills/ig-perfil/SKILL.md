---
name: ig-perfil
description: >-
  Califica un perfil de Instagram sobre 100 con una rúbrica de 12 puntos
  pensada para negocios en México y Latinoamérica, y reescribe lo que pierde
  puntos: campo de nombre, bio, WhatsApp y contacto, liga, destacadas,
  fijados, cuadrícula. Úsala cuando digan «optimiza mi perfil», «arregla mi
  bio», «califica mi Instagram», «por qué no me siguen», «por qué no me
  escriben», o peguen su perfil y pregunten cómo se lee.
---

# ig-perfil

Casi todos optimizan lo que no es. El perfil no es un aparador que la gente
recorre. Es una **pantalla de decisión** a la que se llega desde un reel, y
tiene como tres segundos para contestar: ¿hay más de eso aquí, es para mí, y
cómo le compro?

Esa última pregunta es la que el original en inglés no pesaba lo suficiente.
En Latinoamérica la venta se cierra casi siempre por WhatsApp o en el local,
así que el camino al WhatsApp vale tanto como la bio.

## Entrada

Pídele al usuario que pegue o mande captura de: el campo de nombre, el
usuario, la bio, a dónde apunta la liga, si tiene botón de WhatsApp o de
«Cómo llegar», los nombres de las destacadas, qué tiene fijado y las primeras
nueve portadas. Con una captura de la parte de arriba del perfil y las dos
primeras filas de la cuadrícula alcanza para una primera pasada.

No inicies sesión en Instagram por el usuario.

## Califícalo

Lee `rubric.json` en esta carpeta. Doce puntos, 100 en total, cada uno con
cómo se ve la calificación completa y cómo suele fallar. Califica cada punto,
enseña la tabla y da el total. Con honestidad. La mayoría de los perfiles
quedan entre 30 y 49 la primera vez, y una calificación generosa no sirve.

```
CALIFICACIÓN DEL PERFIL  41/100

  campo de nombre     2/12   solo el nombre, sin lo que la gente busca
  primera línea bio   3/12   «Calidad, servicio y sabor ✨»
  WhatsApp/contacto   4/12   «pedidos por DM», sin botón de WhatsApp
  fijados             0/10   nada fijado
  destacadas          2/8    «Random», «Yo», «2023»
  cuadrícula          4/8    seis de nueve portadas son flyers iguales
  ...
```

## Luego reescribe, en este orden

Arregla de mayor a menor según los puntos perdidos. No lo reescribas todo de
golpe: el usuario tiene que ir a cambiar cada cosa.

**1. El campo de nombre (30 caracteres).** La línea en negritas abajo de la
foto, no el usuario. Es el campo que lee la búsqueda de Instagram, y casi
todas las cuentas ponen el nombre y nada más. Formato que funciona:
`{Nombre} | {qué hace, en palabras que se buscan} {ciudad}`. Da tres opciones.
Si atiende en local, la ciudad o la colonia no es opcional.

**2. El camino a comprar.** Botón de WhatsApp vinculado a WhatsApp Business,
o una liga `wa.me/52XXXXXXXXXX?text=...` con el primer mensaje ya escrito
(«Hola, vi su Instagram y quiero pedir…»). Si hay local: dirección con «Cómo
llegar» y la ficha de Google Maps con el mismo horario. Prueba la liga antes
de entregarla.

**3. Primera línea de la bio.** Para quién es y qué le cambia. No un puesto,
no adjetivos, no una lista de identidades con barras. El resto de los 150
caracteres trae una prueba, una oferta concreta, o el horario.

**4. Los tres fijados.** Tres lugares, tres trabajos: la mejor prueba (reseña,
antes y después), qué vendes y cómo se pide o cuánto cuesta, y quién está
detrás. Es el arreglo que más mueve de todo el perfil y son cuatro toques.

**5. Destacadas.** De cuatro a seis, con el nombre de lo que pregunta el
cliente: Menú, Precios, Cómo pedir, Reseñas, Ubicación. Nada de «Random».
Borra el resto.

**6. La liga.** Un destino que cumple lo que la bio prometió. Se permiten
cinco; dos ya es un menú, y un menú convierte peor que una puerta.

**7. Portadas de la cuadrícula.** Las primeras nueve en miniatura. Las
portadas de los reels se escogen, no se quedan en el cuadro uno. Cuatro
palabras de texto en una portada hacen que la cuadrícula se lea de un vistazo.

## Salida

La tabla de calificación, luego las reescrituras como bloques listos para
copiar en orden de arreglo, cada una pasada por `/ig-human`. Vuelve a
calificar al final y enseña la diferencia con honestidad. Si la reescritura
llega a 84 y no a 98, di 84, y di qué falta, que casi siempre es una
cuadrícula, la costumbre de subir historias y un fijado que todavía no existe.
Nada de eso es reescribir.

Esta skill no guarda nada en Instagram. El usuario cambia cada campo.
