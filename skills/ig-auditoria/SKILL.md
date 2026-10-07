---
name: ig-auditoria
description: >-
  Revisión a fondo de lo que el usuario ya publicó: qué reels funcionaron de
  verdad, por qué, y qué dejar de hacer. Úsala cuando el usuario pegue sus
  estadísticas de Instagram o sus posts anteriores y pregunte «qué está
  funcionando», «por qué este no pegó», «lee mis estadísticas», «audita mi
  contenido», «qué hago más», o quiera saber si Instagram le está trayendo
  clientes.
---

# ig-auditoria

La única fuente honesta de lo que funciona para una cuenta es esa cuenta.
Cada regla de cada guía de Instagram, incluidas las de este paquete, es un
supuesto. Los últimos 30 posts del usuario son la evidencia.

## Entrada

Pide lo que el usuario tenga:

- Estadísticas por post: vistas, alcance, interacciones, tiempo de
  reproducción, guardados, compartidos, seguidores ganados y el porcentaje del
  alcance que no lo sigue. Las capturas sirven.
- O la gráfica de retención de sus mejores y peores reels recientes. Esa
  captura vale más que todo lo demás junto.
- O solo los posts y sus vistas, que alcanza para una primera pasada.
- **Si vende por WhatsApp:** cuántos chats nuevos llegaron la semana de cada
  post, aunque sea a ojo. Es el número que más le importa al dueño y el que
  Instagram no enseña.

Lee también `~/.claude/instagram/bitacora.md` si existe: tiene qué fórmula de
gancho usó cada post.

## Qué medir de verdad

Las vistas solas son el número menos útil de la pantalla, porque dependen
sobre todo de cuánta gente ya sigue la cuenta. Calcula estos y enseña la
cuenta:

| métrica | cómo | qué te dice |
| --- | --- | --- |
| **Múltiplo** | vistas / la mediana de vistas de la propia cuenta | si fue un éxito real o un día normal |
| **Alcance de no seguidores** | % del alcance que viene de gente que no sigue | si viajó o no |
| **Retención a 3s** | quienes siguen a los 3s / quienes empezaron | si el gancho funcionó. Esta es la calificación del gancho. |
| **Tiempo promedio** | directo de estadísticas | si funcionó el medio |
| **Compartidos por alcance** | compartidos / alcance | la señal más fuerte que te puedes ganar. Compartir es poner tu nombre. |
| **Seguidores por alcance** | seguidores nuevos / alcance | si el perfil convirtió la atención |
| **Chats por post** | chats de WhatsApp o DMs nuevos esa semana | si trajo clientes, que es para lo que es |

Ordena por múltiplo y compartidos por alcance, no por vistas. Un reel con
4,000 vistas y 90 compartidos le ganó al de 60,000 vistas y 11. Y uno que
trajo 12 chats de WhatsApp le ganó a los dos.

## Luego busca el patrón

Con los cinco de arriba y los cinco de abajo lado a lado, busca qué los
separa, y prepárate para concluir algo que al usuario no le va a gustar:

- **Retención a 3 segundos.** Si arriba y abajo difieren aquí, es el gancho y
  nada más, y todo lo demás es distracción.
- **Fórmula de gancho.** ¿Qué números de `ig-reel/hooks.json` están en los
  cinco de arriba?
- **Formato.** Reel, carrusel, imagen sola.
- **Duración.** Agrupa en menos de 15s, 15 a 30s, 30 a 60s, más de 60s.
- **Tema.**
- **Si el usuario contestó comentarios en la primera hora.**
- **Temporada y quincena.** Un post de oferta el 15 no es comparable con uno el
  día 8.
- **Día y hora.** Revísalo **al último** y solo si lo demás no enseña nada.
  Casi nunca es la causa y es donde la gente quiere que esté.

Di el hallazgo como afirmación con la evidencia pegada, y di qué tan seguro
es. Con 30 posts se ve un patrón. Con 6 no, y decirlo es mejor que inventarlo.

## La distinción que ahorra meses

**Un reel con vistas y sin seguidores no es un reel fallido, es un problema de
perfil.** Un reel sin vistas es un problema de gancho. Y un reel con vistas,
seguidores y cero chats es un problema de **camino a comprar**: la bio no dice
cómo pedir o el WhatsApp no está a un toque. Separa los tres antes de
recomendar nada. Si el alcance de no seguidores es alto y los seguidores o los
chats por alcance son bajos, deja de reescribir ganchos y ve a `/ig-perfil` o
a `/ig-whatsapp`.

## Salida

```
AUDITORÍA  ·  31 posts  ·  12 jun - 5 sep  ·  mediana 4,100 vistas

LOS 5 DE ARRIBA POR MÚLTIPLO
  18.2x  #28 Así Se Hace      74,600 vistas  62% no seguidores  ret@3s 71%  128 compartidos  ~14 chats
   6.4x  #1  Lo Que Me Costó  26,300 vistas  48% no seguidores  ret@3s 64%   71 compartidos   ~6 chats
  ...

LOS 5 DE ABAJO
   0.3x  #11 Lista            1,200 vistas   9% no seguidores  ret@3s 31%    2 compartidos    0 chats
  ...

QUÉ DICEN LOS DATOS
1. La retención a 3 segundos es toda la historia. Arriba promedian 66 %, abajo 33 %.
   Todo lo demás que te preocupa viene después de los primeros dos segundos.
2. Los videos del proceso (la cocina a las 5 am): 8.1x en promedio contra 0.9x
   del resto. n=5. La señal más fuerte aquí, y no está cerca.
3. Los flyers de promoción tienen vistas y nada más. Ni compartidos, ni chats.
   Tres de los cinco de abajo.
4. El día de la semana no enseña nada. Martes y viernes están dentro del ruido.
   Deja de moverle.

DEJA DE: subir flyers.
HAZ MÁS: el proceso, con un número y una hora.
```

Luego pásale las conclusiones a `/ig-plan` para que la semana que viene se arme
con la evidencia del usuario y no con supuestos, y a `/ig-viral` para que las
referencias se filtren a las fórmulas que le funcionan a esta cuenta.
