#!/usr/bin/env python3
"""
caption.py - revisa un caption de Instagram en español y enseña exactamente lo
que el feed muestra antes del «... más».

Instagram enseña unos 125 caracteres del caption en el feed y esconde el resto
detrás de un toque. Casi todos los captions que fallan, fallan ahí: el gancho
está en la tercera oración, la primera línea es un saludo, o abre con un
hashtag. En español esto pesa más, porque el mismo mensaje sale entre un 20 y
un 25 % más largo que en inglés y en 125 caracteres cabe menos idea.

Además de lo de la plataforma, revisa dos cosas que en México cuestan multas
o quejas y que un caption hecho de prisa casi siempre olvida:
  - PRECIO: si das un precio, que sea el total (con IVA). Es lo que pide PROFECO.
  - PROMOCIÓN: si anuncias descuento, 2x1, «gratis» o meses sin intereses,
    que diga vigencia y condiciones.
Son avisos, no asesoría legal. Ver ig-caption/reglas-mx.md.

El corte de 125 es aproximado: se mueve con el dispositivo, el tamaño de letra
y los saltos de línea. Por eso conviene dejar margen. Cámbialo con --corte.

Uso
  python3 caption.py caption.txt
  python3 caption.py caption.txt --busquedas "pan de muerto,panadería en morelia"
  pbpaste | python3 caption.py -
  python3 caption.py caption.txt --json
"""

import argparse
import json
import re
import sys
import textwrap

LIMIT = 2200             # límite duro de Instagram.
TRUNCATE = 125           # más o menos donde el feed corta a «... más».
HASHTAG_LIMIT = 5        # tope de Instagram por post o reel desde el 18 dic 2025
                         # (antes eran 30), anunciado por la cuenta @Creators.

HASHTAG_RE = re.compile(r"(?:^|\s)(#\w+)")
MENTION_RE = re.compile(r"(?:^|\s)(@[\w.]+)")
LINK_RE = re.compile(r"https?://\S+|\bwww\.\S+|\bwa\.me/\S*|"
                     r"\b[a-z0-9-]+\.(?:com\.mx|com|mx|co|io|net|org|ai|app|shop|store)(?:/\S*)?\b",
                     re.IGNORECASE)
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿←-⇿]")
PHONE_RE = re.compile(r"(?<!\d)(?:\+?52[\s-]?)?(?:\(?\d{2,3}\)?[\s-]?)\d{3,4}[\s-]?\d{4}(?!\d)")
CONCRETE_RE = re.compile(
    r"\$\s?\d|\b\d[\d,.]*\b|(?<![.!?¿¡]\s)(?<![¿¡\n])(?<!^)\b[A-ZÁÉÍÓÚÑ][\wáéíóúñ]{2,}\b",
    re.MULTILINE)
PRICE_RE = re.compile(r"\$\s?\d[\d,]*(?:\.\d+)?|\b\d[\d,]*(?:\.\d+)?\s?(?:pesos|mxn)\b", re.IGNORECASE)
TAX_RE = re.compile(r"(?i)\b(?:iva|precio (?:final|total)|impuestos incluidos|neto)\b")
PROMO_RE = re.compile(r"(?i)\b(?:\d+\s?%\s?(?:de\s)?(?:desc|off)\w*|descuento|2\s?x\s?1|3\s?x\s?2|gratis|"
                      r"promo(?:ción)?|oferta|meses sin intereses|msi|rebaja|liquidación|regalo)\b")
TERMS_RE = re.compile(r"(?i)\b(?:vigencia|válid[oa]|hasta (?:el|agotar)|del \d{1,2}|al \d{1,2} de|"
                      r"aplican (?:restricciones|condiciones)|consulta (?:condiciones|términos|bases)|"
                      r"términos y condiciones|t&c|solo (?:hoy|este|esta)|hasta el)\b")

ASKS = [
    (re.compile(r"(?i)\bcomenta\b(?: la palabra)?\s+[\"«]?[A-ZÁÉÍÓÚÑ0-9]{2,}\b"), "comentar una palabra"),
    (re.compile(r"(?i)\b(?:mándanos|mándame|envíanos|escríbenos|escríbeme)\b(?! (?:por|al|en) (?:whats|wa)\w*)"
                r"(?: (?:un )?(?:dm|mensaje|inbox|md))?"), "mandar DM"),
    (re.compile(r"(?i)\b(?:por|al|en) (?:whatsapp|whats|wa)\b|\bwa\.me/"), "WhatsApp"),
    (re.compile(r"(?i)\bguarda (?:este|esta|esto) (?:post|reel|video|carrusel|receta|lista|tip)\b|"
                r"\b(?:guárdalo|guárdala|guárdatelo|guárdatela)\b|\bguarda(?:lo)? para (?:después|luego|cuando)\b"), "guardar"),
    (re.compile(r"(?i)\b(?:compártelo|compártela|comparte (?:este|esto|con)|mándaselo a|pásaselo a)\b"), "compartir"),
    (re.compile(r"(?i)\b(?:síguenos|sígueme)\b"), "seguir"),
    (re.compile(r"(?i)\betiqueta a\b"), "etiquetar"),
    (re.compile(r"(?i)\b(?:conócelo|conócela|conoce cómo funciona|pruébalo|pruébala|visítanos) en\b"), "ir a un sitio"),
    (re.compile(r"(?i)\b(?:link|liga|enlace) en (?:la |mi |nuestra )?bio\b"), "link en bio"),
    (re.compile(r"(?i)\b(?:desliza|swipe|pásale) (?:a la|para|hacia)\b"), "deslizar"),
    (re.compile(r"(?i)\b(?:cuéntanos|cuéntame|dinos|dime)\b|¿(?:cuál|con cuál) (?:prefieres|eliges|te quedas)"), "contestar una pregunta"),
    (re.compile(r"(?i)\b(?:haz tu pedido|pide (?:el|la|los|las|tu|ya|hoy)|aparta (?:el|la|tu)|reserva (?:tu|ya|tu mesa)|agenda (?:tu|una)|cotiza)\b"), "pedir o reservar"),
]

FILLER_TAGS = {"#viral", "#fyp", "#explore", "#explorepage", "#explorar", "#foryou",
               "#foryoupage", "#parati", "#paratii", "#trending", "#tendencia", "#instagood",
               "#love", "#amor", "#follow", "#sígueme", "#sigueme", "#like4like", "#likeforlike",
               "#megusta", "#reels", "#reelsinstagram", "#viralreels", "#instadaily",
               "#mexico", "#méxico", "#emprendedores", "#emprendimiento", "#negocios"}


def visible_window(text, cut):
    """Lo que el feed enseña. Instagram corta a media palabra, así que esto también."""
    flat = text.strip()
    return flat if len(flat) <= cut else flat[:cut]


def render_box(window, truncated, out=sys.stdout, width=52):
    print("\n  LO QUE ENSEÑA EL FEED", file=out)
    print("  +" + "-" * (width + 2) + "+", file=out)
    lines = []
    for raw in window.split("\n"):
        lines.extend(textwrap.wrap(raw, width) or [""])
    for line in lines[:8]:
        print(f"  | {line:<{width}} |", file=out)
    tail = "... más" if truncated else "(cabe completo)"
    print("  +" + "-" * (width + 2 - len(tail) - 2) + f" {tail} " + "+", file=out)


def analyse(text, cut=TRUNCATE, keywords=None):
    stripped = text.strip()
    chars = len(stripped)
    lines = stripped.split("\n")
    first_line = lines[0].strip() if lines else ""
    tags = HASHTAG_RE.findall(stripped)
    mentions = MENTION_RE.findall(stripped)
    links = LINK_RE.findall(stripped)
    emoji = EMOJI_RE.findall(stripped)
    window = visible_window(stripped, cut)
    truncated = chars > cut
    asks = [name for pattern, name in ASKS if pattern.search(stripped)]
    filler = [t for t in tags if t.lower() in FILLER_TAGS]
    keywords = [k.strip() for k in (keywords or []) if k.strip()]

    checks = []

    def add(name, status, detail):
        checks.append({"check": name, "status": status, "detail": detail})

    add("LARGO", "FALLA" if chars > LIMIT else "OK",
        f"{chars} / {LIMIT} caracteres" + (f", {chars - LIMIT} de más" if chars > LIMIT else ""))

    if not first_line:
        add("PRIMERA LÍNEA", "FALLA", "el caption abre con una línea en blanco")
    elif first_line.startswith(("#", "@")):
        add("PRIMERA LÍNEA", "FALLA",
            "abre con hashtag o mención, en el único lugar que vale una oración")
    elif re.match(r"(?i)^\s*¡?(?:hola|qué onda|buen(?:os|as) (?:días|tardes|noches)|bienvenid)", first_line):
        add("PRIMERA LÍNEA", "FALLA", "abre con saludo y se gasta la ventana en nada")
    elif EMOJI_RE.match(first_line):
        add("PRIMERA LÍNEA", "AVISO", "abre con emoji: lo primero que se lee debería ser una palabra")
    elif len(first_line) > cut:
        add("PRIMERA LÍNEA", "AVISO",
            f"{len(first_line)} caracteres, se corta en {cut} a media idea. "
            "Está bien si el corte deja suspenso, mal si corta una subordinada")
    else:
        add("PRIMERA LÍNEA", "OK", f"{len(first_line)} caracteres, cabe entera")

    add("GANCHO CONCRETO", "OK" if CONCRETE_RE.search(window) else "AVISO",
        f"{len(CONCRETE_RE.findall(window))} número(s) o nombre(s) en la parte visible"
        + ("" if CONCRETE_RE.search(window) else " - nada que se pueda checar antes del toque"))

    if len(tags) > HASHTAG_LIMIT:
        add("HASHTAGS", "FALLA", f"{len(tags)} hashtags, arriba del tope de {HASHTAG_LIMIT} de Instagram. "
                                 "Los que pasan del quinto no cuentan y el bloque se ve viejo")
    elif filler:
        add("HASHTAGS", "AVISO", f"{len(tags)} hashtags, {len(filler)} genéricos "
                                 f"({', '.join(filler[:3])}). No describen nada")
    else:
        add("HASHTAGS", "OK", f"{len(tags)} hashtag(s)" + (f": {' '.join(tags)}" if tags else ""))

    if not tags:
        add("LUGAR DE HASHTAGS", "OK", "no hay hashtags que acomodar")
    elif any(re.search(r"(?:^|\s)" + re.escape(t) + r"\b", window) for t in tags):
        add("LUGAR DE HASHTAGS", "AVISO", "hay un hashtag en la parte visible, "
                                          "gastando espacio del feed en una etiqueta")
    else:
        add("LUGAR DE HASHTAGS", "OK", "los hashtags quedan abajo del corte")

    add("LIGAS", "AVISO" if links else "OK",
        f"{len(links)} liga(s) en el caption, y en el caption no se les puede dar clic. "
        "Pásala a la bio, a una historia con sticker de enlace o al DM" if links
        else "no hay ligas muertas en el texto")

    phones = PHONE_RE.findall(stripped)
    if phones:
        add("TELÉFONO", "OK", f"{len(phones)} teléfono(s) escrito(s). En Latinoamérica la gente sí "
                              "los copia para mandar WhatsApp: que esté completo, con lada")

    if len(asks) == 1:
        add("UN SOLO PEDIDO", "OK", f"un llamado a la acción: {asks[0]}")
    elif not asks:
        add("UN SOLO PEDIDO", "AVISO", "no hay llamado a la acción. Decide para qué es este post")
    else:
        add("UN SOLO PEDIDO", "AVISO", f"{len(asks)} pedidos ({', '.join(asks)}). "
                                       "Dos pedidos es lo mismo que ninguno")

    density = len(emoji) * 100 / max(chars, 1)
    add("EMOJIS", "AVISO" if density > 4 else "OK",
        f"{len(emoji)} emojis, {density:.1f} por cada 100 caracteres"
        + (" - se lee como decoración" if density > 4 else ""))

    # «desde $0» no tiene IVA que aclarar
    prices = [x for x in PRICE_RE.findall(stripped) if re.sub(r"[^\d]", "", x).strip("0")]
    if prices and not TAX_RE.search(stripped):
        add("PRECIO", "AVISO", f"das precio ({', '.join(prices[:2])}) sin decir si es el total. "
                               "PROFECO pide el precio total con impuestos: «IVA incluido» o el final")
    elif prices:
        add("PRECIO", "OK", "precio con IVA o total indicado")

    if PROMO_RE.search(stripped) and not TERMS_RE.search(stripped):
        add("PROMOCIÓN", "AVISO", "anuncias promoción sin vigencia ni condiciones. "
                                  "Di hasta cuándo y qué aplica (PROFECO)")
    elif PROMO_RE.search(stripped):
        add("PROMOCIÓN", "OK", "la promoción trae vigencia o condiciones")

    if keywords:
        low = stripped.lower()
        found = [k for k in keywords if k.lower() in low]
        missing = [k for k in keywords if k.lower() not in low]
        in_window = [k for k in found if k.lower() in window.lower()]
        status = "OK" if not missing else ("AVISO" if found else "FALLA")
        add("BÚSQUEDAS", status,
            f"{len(found)}/{len(keywords)} presentes"
            + (f", {len(in_window)} en la parte visible" if found else "")
            + (f". Faltan: {', '.join(missing)}" if missing else ""))

    fails = sum(1 for c in checks if c["status"] == "FALLA")
    warns = sum(1 for c in checks if c["status"] == "AVISO")
    verdict = "ARREGLAR" if fails else ("REVISAR" if warns else "LISTO")

    return {
        "characters": chars, "limit": LIMIT, "truncate_at": cut,
        "visible": window, "truncated": truncated,
        "first_line_chars": len(first_line),
        "hashtags": tags, "mentions": mentions, "links": links,
        "emoji": len(emoji), "asks": asks,
        "checks": checks, "verdict": verdict,
    }


def render(a, out=sys.stdout):
    head = (f"REVISIÓN DEL CAPTION  ·  {a['characters']} / {a['limit']} caracteres  ·  "
            f"{len(a['hashtags'])} hashtags  ·  {len(a['asks'])} pedido(s)")
    print("\n" + head, file=out)
    print("=" * max(len(head), 62), file=out)
    render_box(a["visible"], a["truncated"], out=out)
    print("", file=out)
    for c in a["checks"]:
        print(f"  {c['status']:<6} {c['check']:<18} {c['detail']}", file=out)
    print("-" * max(len(head), 62), file=out)
    print(f"  VEREDICTO  {a['verdict']}\n", file=out)


def main():
    ap = argparse.ArgumentParser(description="Revisa un caption de Instagram.")
    ap.add_argument("input", nargs="?", default="-", help="archivo del caption, o - para stdin")
    ap.add_argument("--corte", "--truncate", dest="truncate", type=int, default=TRUNCATE,
                    help=f"caracteres visibles antes del «... más» (default {TRUNCATE})")
    ap.add_argument("--busquedas", "--keywords", dest="keywords", default="",
                    help="términos separados por coma con los que quieres que te encuentren")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    a = analyse(raw, cut=args.truncate, keywords=args.keywords.split(","))
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    sys.exit(0 if a["verdict"] == "LISTO" else 1)


if __name__ == "__main__":
    main()
