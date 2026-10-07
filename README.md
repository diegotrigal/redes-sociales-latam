# redes-sociales-latam

Catorce skills de Claude para llevar las redes de un negocio en español,
pensadas para México y Latinoamérica. Hoy cubren **Instagram y el paso a
WhatsApp Business**; TikTok y Facebook todavía no. Gratis, MIT, sin API ni nada
que conectar.

Es una adaptación de
[instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill)
de Jake Schincariol. No es una traducción: los diccionarios, las reglas y los
ejemplos se reescribieron para cómo se habla y se vende aquí.

**No se publica nada hasta que tú digas que sí.** Las skills escriben. Tú
publicas.

## Qué cambió respecto al original

| | original (inglés) | redes-sociales-latam |
| --- | --- | --- |
| Humanizador | 154 muletillas de IA en inglés | 170 muletillas de IA **en español** («potenciar», «sumérgete», «en el vertiginoso mundo de», «cabe destacar»), con masculino y femenino para no romper la concordancia |
| Estructuras de modelo | 16 | 27, con las del español: «No es solo X, es Y», «¿Sabías que…?», «al siguiente nivel», «no dudes en», títulos Con Mayúscula En Cada Palabra, preguntas sin «¿» |
| Voz | cuenta contracciones (*don't*, *it's*) | cuenta oralidad («pues», «la neta», «ojo», «ni modo»), y no cuenta «tu/tus» porque es justo como escribe el marketing generado |
| Emojis | borra el carácter de unión y parte 👩‍🍳 en dos | respeta los emojis compuestos |
| Tiempos de guion | palabras a 165 por minuto | **sílabas** a 6 por segundo (en español una palabra puede tener ocho sílabas) |
| Ganchos | 26 fórmulas | 26 adaptadas + 3 nuevas de negocio local: el comentario leído, así se hace, cuánto cuesta |
| Captions | revisión de la plataforma | lo mismo + **PROFECO**: precio total con IVA y vigencia de promociones; el teléfono sí puede ir |
| Perfil | la liga pesa 8 | **WhatsApp y contacto pesan 12**: aquí la venta se cierra ahí |
| Plan | genérico | con calendario comercial de México y otros países (quincena, Buen Fin, Hot Sale, 10 de mayo, Día de Muertos) |
| WhatsApp | no existe | **skill nueva** `/ig-whatsapp`: liga wa.me, bienvenida, ausencia, respuestas rápidas, catálogo, etiquetas, seguimiento con permiso |
| Reglas | — | `ig-caption/reglas-mx.md`: PROFECO, COFEPRIS, publicidad de creadores, datos personales |

## Instalar

En Claude Code, como plugin:

```
/plugin marketplace add diegotrigal/redes-sociales-latam
/plugin install redes-sociales-latam@redes-sociales-latam
```

O a mano:

```bash
git clone https://github.com/diegotrigal/redes-sociales-latam.git
cp -r redes-sociales-latam/skills/ig-* ~/.claude/skills/
mkdir -p ~/.claude/instagram
cp redes-sociales-latam/skills/ig-reel/voz-plantilla.md ~/.claude/instagram/voz.md
```

Sin Claude Code: pega cualquier `SKILL.md` al inicio de un chat y funciona como
modo. Pierdes los scripts de Python, que son lo mejor de `/ig-reel`, `/ig-human`
y `/ig-caption`, pero lo demás funciona.

Luego dedícale diez minutos a `~/.claude/instagram/voz.md`, o mándale a Claude
tres de tus reels y dile «escríbeme mi voz.md con esto». Todas las skills lo
leen.

## Las catorce

| comando | qué hace |
| --- | --- |
| `/ig-reel` | Una idea a reel. Tres ganchos de [29 fórmulas](skills/ig-reel/hooks.json) con calificación, el guion, el texto en pantalla y la hoja de tiempos. |
| `/ig-viral` | Busca lo que funciona en tu giro, lo ordena por cuánto le ganó a su propia cuenta y escribe tus referencias. |
| `/ig-caption` | El caption, revisado. Te enseña los 125 caracteres que se ven antes del toque, y avisa precio sin IVA o promociones sin vigencia. |
| `/ig-carrusel` | La portada, el texto de cada lámina y los archivos de 1080x1350. |
| `/ig-historias` | La secuencia del día, qué sticker para qué, y el embudo al DM y al WhatsApp. |
| `/ig-perfil` | Califica tu perfil sobre 100 con una [rúbrica de 12 puntos](skills/ig-perfil/rubric.json) y lo reescribe en orden. |
| `/ig-plan` | La semana: qué, en qué formato, cuándo, con las [fechas comerciales](skills/ig-plan/fechas-mx.md). |
| `/ig-human` | El humanizador. Dos scripts que corren de verdad. |
| `/ig-comentar` | Comentarios en posts de otros. Nueve tipos. Nunca «🔥🔥🔥». |
| `/ig-responder` | Los comentarios de tus posts: palabra, cliente, queja, fondo, pregunta, apoyo, ruido. Y «¿precio?» se contesta en público. |
| `/ig-dm` | La entrega de la palabra clave, el primer mensaje, la colaboración, los dos seguimientos y cuándo pasar a WhatsApp. |
| `/ig-whatsapp` | De Instagram a WhatsApp Business: liga, mensajes automáticos, catálogo, etiquetas, seguimiento. |
| `/ig-reciclar` | Un video, podcast o en vivo convertido en una semana de reels y carruseles. |
| `/ig-auditoria` | Lo que ya publicaste: múltiplo, compartidos por alcance y chats de WhatsApp, no vistas. |

## Las herramientas que corren

Sin dependencias, sin red, nada se sube. Python 3.9 o más nuevo.

```bash
python3 skills/ig-human/humanize.py borrador.txt --reporte
python3 skills/ig-human/detect.py antes.txt despues.txt
python3 skills/ig-reel/hookscore.py ganchos.txt
python3 skills/ig-reel/beats.py guion.txt --meta 30
python3 skills/ig-caption/caption.py caption.txt --busquedas "pan de muerto,panadería en morelia"
python3 skills/ig-viral/swipe.py capturados.tsv
```

Ejemplo real (los archivos están en `pruebas/`): un caption hecho por IA para
una comandera de restaurante inventada pasa de **21.5 MARCADO** a **38.8** con la
limpieza automática; el resto (la tercia, el «No es solo X, es Y», las
viñetas de ✅) lo señala para que lo reescriba una persona. Un caption escrito
a mano del mismo tema saca **70.6**.

```
RANKING DE GANCHOS
->  80.2 FUERTE  Nadie te dice que tus primeros 30 reels van a fracasar.
    75.2 FUERTE  Perdí $18,000 por una cláusula que no puse en el contrato.
    62.6 VA      El 70% de las taquerías en Morelia no cobran con tarjeta.
    ...
     0.0 FLOJO   Hola a todos, en este video les voy a enseñar cómo vender m...
        descalifica: Preámbulo. Bórralo y empieza en el resultado.
        descalifica: Saludo. Nadie llegó al feed para que lo saludaran.
```

## Pruebas

```bash
python3 pruebas/probar.py
```

86 revisiones: que cada fórmula reconozca su propio ejemplo, que el
humanizador respete emojis y URLs, que el conteo de sílabas sea correcto, que
la revisión de captions detecte precio sin IVA, etc. Córrelo después de editar
`slop.json` o `hooks.json`: un regex mal escapado rompe en silencio.

## Honestidad

- **Las calificaciones son heurísticas locales**, no GPTZero ni Originality, y
  no predicen vistas. El original se validó contra 74 ganchos reales en
  inglés; esta versión todavía no tiene validación propia con reels en
  español. Los umbrales vienen del original con ajustes. Si algo que sabes que
  es humano sale mal, créele a tu oído.
- **Nada se inventa.** Si un borrador necesita un número que no diste,
  regresa con `{{tu número}}`.
- **Las reglas de la plataforma y las fechas cambian.** El tope de 5 hashtags
  es de diciembre de 2025. Buen Fin, Hot Sale y Semana Santa se mueven cada
  año. Si algo de aquí contradice lo que hace Instagram cuando lo leas,
  Instagram tiene la razón.
- **`reglas-mx.md` no es asesoría legal.**
- **`/ig-viral` lee, no raspa.** Nunca pide tu contraseña ni inicia sesión por
  ti, y no deja nada corriendo en segundo plano.

## Licencia

MIT. Original © 2026 Jake Schincariol; adaptación © 2026 Diego Trigal
([Soluciones para PyMEs](https://soluciones-para-pymes.com)).
