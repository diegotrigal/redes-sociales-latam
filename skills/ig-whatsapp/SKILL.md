---
name: ig-whatsapp
description: >-
  El tramo que en Latinoamérica cierra la venta: de Instagram a WhatsApp
  Business. Escribe la liga wa.me con mensaje ya escrito, el mensaje de
  bienvenida y de ausencia, las respuestas rápidas, el catálogo, las etiquetas
  y el seguimiento, sin spam y con permiso. Úsala cuando digan «WhatsApp»,
  «pásalos al Whats», «mensaje de bienvenida», «respuestas rápidas», «catálogo
  de WhatsApp», «lista de difusión», «cómo cierro la venta», o cuando un
  embudo de Instagram tenga que terminar en una venta.
---

# ig-whatsapp

Esta skill no existe en el original en inglés porque allá la venta termina en
una página. Aquí termina en WhatsApp: el cliente quiere preguntar, ver fotos,
mandar ubicación y pagar con transferencia, y quiere hacerlo donde ya platica
con todo mundo.

Instagram atrae; WhatsApp cierra. Esta skill escribe todo lo que pasa del
primer «Hola, vi su Instagram» al «ya le transferí».

## Lo que sí y lo que no

**Sí:** contestar a quien te escribió, mandar catálogo cuando lo piden, dar
seguimiento a una cotización que alguien pidió, avisar a quien aceptó que le
avises.

**No:** agregar a una lista de difusión o a un grupo a quien te dio su número
para otra cosa, mandar promociones a contactos que nunca pidieron, comprar
bases de datos, usar herramientas no oficiales que mandan en masa desde un
WhatsApp normal. WhatsApp banea números por eso, y en México mandar
publicidad a quien no la autorizó choca con la ley de protección de datos
personales y con PROFECO (ver `ig-caption/reglas-mx.md`). La API oficial de
WhatsApp Business pide permiso explícito y plantillas aprobadas para escribir
primero; que la herramienta lo permita no quiere decir que se pueda.

Esta skill escribe los mensajes. **No manda nada**, no se conecta a WhatsApp y
no automatiza envíos.

## 1. La liga con mensaje ya escrito

La puerta desde Instagram. Va en la bio, en el sticker de enlace de las
historias y en las respuestas a «¿precio?».

```
https://wa.me/52{10 dígitos}?text={mensaje codificado}
```

- `52` es México; sin el `1` viejo de celulares. Otros países: 57 Colombia, 54
  Argentina (con 9 para celular), 56 Chile, 51 Perú.
- El mensaje dice de dónde viene y qué quiere, para que el negocio sepa
  contestar sin preguntar: «Hola, vi su Instagram y quiero apartar pan de
  muerto».
- Una liga por intención si vale la pena: una para pedidos, otra para
  cotizaciones. Así se sabe cuál post trajo a quién.
- **Codifica el texto** (espacios a `%20`, acentos con su código) y **prueba la
  liga** antes de entregarla. Para codificarlo:
  `python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "Hola, vi su Instagram"`

## 2. Los mensajes automáticos de WhatsApp Business

WhatsApp Business (la app gratis) trae tres. Escríbelos los tres:

**Bienvenida** (a quien escribe por primera vez o después de 14 días):
corto, con el horario y el siguiente paso. No un folleto.

```
¡Hola! Somos La Espiga 🥐 Te contestamos en un ratito.
Mientras: el catálogo con precios está aquí arriba (ícono de tienda).
Horario: lunes a sábado de 7 a 9.
```

**Ausencia** (fuera de horario): cuándo vas a contestar, de verdad.

```
Ya cerramos por hoy. Mañana a las 7 te contestamos.
Si es para apartar, déjanos nombre, cuántas piezas y a qué hora pasas.
```

**Respuestas rápidas** (se llaman con `/`): las cinco preguntas que llegan
diario, contestadas una vez bien. Precio, horario, ubicación, formas de pago,
cómo apartar. Pídele al usuario sus cinco preguntas más repetidas; si no las
sabe, pídele que revise sus últimos 30 chats.

## 3. El catálogo

WhatsApp Business permite catálogo con foto, precio y descripción. Para cada
producto:

- **Nombre** como lo pide el cliente, no como lo llama la cocina.
- **Precio total con IVA.** Si varía, «desde $X».
- **Descripción** en una línea: para cuántos, qué trae, cuánto tarda.
- **Foto** del producto real, no de banco de imágenes.

Pasa nombres y descripciones por `/ig-human`.

## 4. Etiquetas

WhatsApp Business permite etiquetas de colores. Propón cinco que sigan la
venta: `Nuevo`, `Cotizado`, `Apartado / anticipo`, `Pagado`, `Entregado`. Con
eso el usuario ve de un vistazo a quién darle seguimiento.

## 5. El seguimiento de una cotización

Mismas reglas que en `/ig-dm`: dos seguimientos y se para.

- **+2 días**: algo nuevo o útil (una foto de un pedido parecido, la fecha
  límite real para apartar). Nunca «¿lo pensaste?».
- **+7 días**: el cierre: «Te dejo de molestar; si lo necesitas más adelante,
  aquí estamos». Y ya.

En temporada (Día de las Madres, Día de Muertos, diciembre) la fecha límite es
real y se dice: «Cerramos pedidos de pan el jueves 30».

## 6. Listas de difusión, solo con permiso

Las listas de difusión solo le llegan a quien guardó tu número, y solo deben
llevar a quien **pidió** estar: «¿Quieres que te avise cuando salga la rosca?
Contéstame SÍ». Guarda quién dijo que sí. Una lista de 40 que pidió vale más
que una de 900 que no.

Mensaje de difusión: uno a la semana como mucho, con algo que sirva (qué hay
hoy, la fecha límite de temporada), y siempre con la salida: «Si ya no quieres
estos avisos, contesta BAJA».

## Salida

Lo que aplique, en bloques listos para copiar:

```
WHATSAPP  ·  La Espiga

LIGA (bio)        https://wa.me/524431234567?text=Hola%2C%20vi%20su%20Instagram%20y%20quiero%20pedir
LIGA (pan muerto) https://wa.me/524431234567?text=Hola%2C%20quiero%20apartar%20pan%20de%20muerto

BIENVENIDA        ...
AUSENCIA          ...
RESPUESTAS RÁPIDAS
  /precio     ...
  /horario    ...
  /ubicacion  ...
  /pago       ...
  /apartar    ...
ETIQUETAS         Nuevo · Cotizado · Apartado · Pagado · Entregado
```

Todo pasado por `/ig-human`. El usuario lo configura en su WhatsApp Business.
Nada se manda solo.
