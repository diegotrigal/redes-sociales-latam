#!/usr/bin/env python3
"""
hookscore.py - califica la primera línea de un reel en las cinco cosas que
tienen en común los ganchos que sí detienen el dedo, y ordena un lote.

Qué es:  cinco heurísticas locales sobre el texto, en español: que se diga en
menos de tres segundos (medido en sílabas, no en palabras), que traiga algo
concreto, que algo esté en juego, que lo interesante vaya al frente y que le
hable a alguien.

Qué NO es:  un predictor de vistas. El original en inglés se probó contra 74
ganchos reales: separa bien un gancho real de uno hecho para ser malo, y casi
no separa los aciertos de un creador de sus fallas. Esta versión hereda esa
lógica y todavía no tiene una validación propia con reels en español. Úsalo
para lo que sí mide: saludos, preámbulos, ganchos sin nada concreto y ganchos
que tardan cinco segundos en decirse. Cuál de dos ganchos decentes va a viajar
lo deciden tu cara, tu edición, tu audio y a quién se lo enseña Instagram.
Confía más en la gráfica de retención que en este script.

Cada revisión da de 0 a 100. Más alto es mejor.

Uso
  python3 hookscore.py ganchos.txt                 # uno por línea, ordenados
  python3 hookscore.py --gancho "Perdí $18,000 por una cláusula."
  pbpaste | python3 hookscore.py -
  python3 hookscore.py ganchos.txt --json
  python3 hookscore.py ganchos.txt --sps 6.5        # tu ritmo, en sílabas por segundo
"""

import argparse
import json
import os
import re
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from silabas import SPS, silabas  # noqa: E402

WORD_RE = re.compile(r"[\w$%'’-]+")
NUMBER_RE = re.compile(
    r"\$\s?\d[\d,]*(?:\.\d+)?"                              # dinero
    r"|\b\d[\d,]*(?:\.\d+)?\s?"                             # una cifra, con o
    r"(?:%|k\b|mil\b|x\b|hrs?\b|horas?\b|min\b|minutos?\b"   # sin unidad
    r"|segundos?\b|d[ií]as?\b|semanas?\b|mes(?:es)?\b|años?\b|pesos\b|mdp\b)?",
    re.IGNORECASE)
HASHTAG_RE = re.compile(r"(?:^|\s)#\w+")
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿]")

# Los ganchos hablados dicen los números en voz alta. «Cero pesos» y «veinte
# mil» son tan concretos como «$0» y «$20,000». «Uno», «un» y «primer» se
# quedan fuera a propósito: casi siempre son relleno, no cantidad.
SPOKEN_NUMBERS = {
    "cero", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve",
    "diez", "once", "doce", "trece", "catorce", "quince", "veinte", "treinta",
    "cuarenta", "cincuenta", "sesenta", "setenta", "ochenta", "noventa", "cien",
    "ciento", "cientos", "doscientos", "trescientos", "quinientos", "mil",
    "millón", "millones", "docena", "mitad", "doble", "triple",
}
MONEY_WORDS = {
    "pesos", "peso", "varos", "lana", "dólares", "dólar", "centavos", "ciento",
    "ganancia", "ganancias", "sueldo", "renta", "ventas", "facturación",
    "utilidad", "quincena", "aguinaldo", "mdp", "millonario", "deuda", "multa",
}

# Palabras que ponen algo en juego. Un gancho sin ninguna es una afirmación;
# con una, es una razón para quedarse.
STAKES = {
    "deja", "dejé", "dejes", "nunca", "jamás", "error", "errores", "mal", "perdí",
    "perder", "pierdes", "perdiendo", "perdimos", "cuesta", "costó", "cuestan",
    "quiebra", "quebré", "quebramos", "fallé", "falla", "fracaso", "fracasé",
    "fracasar", "fracasa", "fracasan", "fallan", "pierden", "perdieron",
    "nadie", "no", "ni", "sin", "renuncié", "renuncia", "despedido", "despidieron",
    "corrí", "borré", "borra", "cerré", "cerramos", "cambió", "reemplazó",
    "reemplaza", "gratis", "pagué", "pagas", "pagando", "cobré", "cobras",
    "cobran", "cobrando", "ahorré", "ahorras", "ahorra", "prohibido", "ilegal",
    "multa", "peor", "odio", "odiaba", "tiré", "tiras", "tirando", "estafa",
    "fraude", "mentira", "mentí", "verdad", "secreto", "oculto", "escondido",
    "robó", "robaron", "antes", "hasta", "excepto", "problema", "riesgo",
    "peligro", "cuidado", "ojo", "aguas", "arrepiento", "deberías", "debes",
    "todavía", "aún", "solo", "sólo", "contra", "vs", "neta", "realmente",
    "demanda", "demandaron", "devolución", "reembolso", "regañó", "clausuraron",
}

# Aperturas que gastan el primer segundo sin decir nada.
WEAK_OPENERS = [
    "bueno", "pues", "entonces", "ok", "okey", "hola", "qué onda", "que onda",
    "oigan", "chicos", "chicas", "amigos", "amigas", "bienvenidos", "bienvenidas",
    "hoy", "básicamente", "honestamente", "miren", "este", "eh", "em", "quiero",
    "quería", "les quiero", "te quiero", "uno de", "una de", "alguna vez",
    "sabías", "en este", "en el video", "la cosa", "hay", "esto es", "es que",
    "como saben", "ya saben", "ustedes saben", "así que", "buenas", "buenos días",
    "buenas tardes", "buenas noches", "les voy", "te voy", "vamos a",
]

# Imperativos que se ganan el primer lugar.
IMPERATIVES = {
    "deja", "roba", "copia", "borra", "prueba", "mira", "lee", "guarda", "usa",
    "haz", "escribe", "manda", "toma", "empieza", "renuncia", "nunca", "siempre",
    "no", "pon", "revisa", "cobra", "sube", "baja", "cambia", "compra", "vende",
    "olvida", "aprende", "evita", "checa", "pide", "aparta", "corre", "ojo", "aguas",
}

DEALBREAKERS = [
    (re.compile(r"(?i)^\s*¡?(?:deja de (?:scrollear|deslizar|hacer scroll)|no (?:deslices|scrollees))"),
     "Abre con «deja de deslizar». Pedir atención delata que no te la ganaste."),
    (re.compile(r"(?i)\b(?:en (?:este|el) (?:video|reel)(?: de hoy)? (?:te |les )?(?:voy|vamos) a"
                r"|(?:te|les) voy a (?:enseñar|mostrar|explicar|contar)|hoy (?:te |les )?(?:voy|vamos) a)\b"),
     "Preámbulo. Bórralo y empieza en el resultado."),
    (re.compile(r"(?i)^\s*¡?(?:hola|qué onda|que onda|buenas|bienvenid[oa]s|buenos días)\b"),
     "Saludo. Nadie llegó al feed para que lo saludaran."),
    (HASHTAG_RE,
     "Hashtag en el gancho. Los hashtags van al final del caption, si acaso."),
    (EMOJI_RE,
     "Emoji en el gancho. El texto en pantalla a tamaño de gancho tiene espacio para palabras o para un emoji, no para ambos."),
]

PROPER_START = re.compile(r"^[A-ZÁÉÍÓÚÑ]")


def clamp(n):
    return max(0.0, min(100.0, n))


def words(text):
    # «$18,000» es una palabra cuando se dice, así que aquí también.
    return WORD_RE.findall(re.sub(r"(?<=\d),(?=\d)", "", text))


def _low(w):
    return w.lower().strip("'’¿¡")


def _propers(text):
    """Palabras con mayúscula que no abren oración (nombres, marcas, lugares)."""
    out, start = [], True
    for tok in re.findall(r"[\w'’]+|[.!?¿¡]", text):
        if tok in ".!?¿¡":
            start = True
            continue
        if not start and PROPER_START.match(tok) and len(tok) >= 3:
            out.append(tok)
        start = False
    return out


def check_length(text, sps=SPS):
    """El gancho tiene que caer antes de que el dedo se mueva: unos tres segundos."""
    n = len(words(text))
    syl = silabas(text)
    secs = syl / sps
    chars = len(text.strip())
    if 1.2 <= secs <= 3.0:
        score = 100.0
    elif secs < 1.2:
        score = clamp(100 - (1.2 - secs) * 60)
    else:
        score = clamp(100 - (secs - 3.0) * 30)
    if chars > 60:                       # dos renglones de texto grande en pantalla
        score -= 12
    return clamp(score), (f"{n} palabras, {syl} sílabas, ~{secs:.1f}s dicho, {chars} caracteres "
                          f"(lo bueno: 3 segundos o menos)")


def check_specificity(text):
    """Una cosa concreta le gana a tres abstractas."""
    nums = [n.strip() for n in NUMBER_RE.findall(text) if n.strip()]
    propers = set(_propers(text))
    low = [_low(w) for w in words(text)]
    spoken = [w for w in low if w in SPOKEN_NUMBERS or w in MONEY_WORDS]
    hits = len(nums) + len(propers) + len(spoken)
    score = 15.0 if hits == 0 else clamp(45 + hits * 30)
    found = ", ".join(nums[:2] + sorted(propers)[:2] + spoken[:2])
    return score, (f"{hits} dato(s) concreto(s)" + (f": {found}" if found else
                   " - ni número, ni nombre, nada que se pueda checar"))


def check_stakes(text):
    """Tensión, costo, negación. Algo que quien ve podría perder."""
    hits = [x for x in (_low(w) for w in words(text)) if x in STAKES]
    markers = sorted(set(hits))
    if re.search(r"\$\s?\d", text):
        markers.append("un precio")
    n = len(markers)
    score = {0: 20.0, 1: 70.0}.get(n, 100.0)
    detail = f"{n} marca(s) de tensión" + (f": {', '.join(markers[:4])}" if markers else
                                           " - en esta línea no hay nada en juego")
    return clamp(score), detail


def check_frontload(text):
    """La palabra interesante no puede estar en el lugar nueve."""
    w = words(text)
    if not w:
        return 0.0, "vacío"
    low = [_low(x) for x in w]
    opener = " ".join(low[:2])
    penalty, hit_opener = 0, None
    for weak in WEAK_OPENERS:
        if opener.startswith(weak + " ") or opener == weak or low[0] == weak:
            penalty, hit_opener = 30, weak
            break
    propers = set(_propers(text))
    payload = None
    for i, token in enumerate(low):
        if (token in STAKES or token in SPOKEN_NUMBERS or token in MONEY_WORDS
                or NUMBER_RE.match(w[i]) or (i and w[i] in propers)):
            payload = i
            break
    if payload is None:
        base, where = 30.0, "no hay palabra fuerte en toda la línea"
    elif payload <= 3:
        base, where = 100.0, f"lo fuerte en la palabra {payload + 1}"
    elif payload <= 6:
        base, where = 70.0, f"lo fuerte en la palabra {payload + 1}, puede ir antes"
    else:
        base, where = 40.0, f"lo fuerte en la palabra {payload + 1}, muy tarde"
    detail = where + (f"; apertura floja «{hit_opener}»" if hit_opener else "")
    return clamp(base - penalty), detail


def check_address(text):
    """Le habla a alguien, o flota en el aire."""
    low = text.lower()
    w = [_low(x) for x in words(text)]
    if re.search(r"(?<!\w)(tú|tu|tus|te|ti|contigo|usted|ustedes|su negocio)(?!\w)", low):
        return 100.0, "le habla a quien ve"
    if w and w[0] in IMPERATIVES:
        return 90.0, f"abre en imperativo («{w[0]}»)"
    if re.search(r"(?<!\w)(yo|mi|mis|me|nosotros|nosotras|nuestro|nuestra|nos)(?!\w)", low) \
            or re.search(r"(?<!\w)(?!(?:aquí|así|sí|allí|ahí|café|bebé|qué|ojalá|mamá|papá|"
                         r"sofá|menú|josé|perú|maní|rubí)(?!\w))\w+(?:é|í)(?!\w)", low):
        # El español se come el «yo»: «Perdí», «cerré», «aprendí» ya son primera persona.
        return 70.0, "primera persona, sin nombrar a quien ve"
    return 35.0, "tercera persona, no hay nadie en el cuarto"


CHECKS = ["DURACIÓN", "CONCRETO", "TENSIÓN", "AL FRENTE", "A QUIÉN"]


def run(text, sps=SPS):
    results = {
        "DURACIÓN": check_length(text, sps),
        "CONCRETO": check_specificity(text),
        "TENSIÓN": check_stakes(text),
        "AL FRENTE": check_frontload(text),
        "A QUIÉN": check_address(text),
    }
    flags = [msg for pattern, msg in DEALBREAKERS if pattern.search(text)]
    scores = [results[c][0] for c in CHECKS]
    # La propiedad más débil le pone techo al gancho, igual que en detect.py.
    overall = clamp(statistics.mean(scores) * 0.6 + min(scores) * 0.4 - len(flags) * 15)
    verdict = "FUERTE" if overall >= 70 and min(scores) >= 55 and not flags else (
        "VA" if overall >= 50 else "FLOJO")
    return results, overall, verdict, flags


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render_one(text, results, overall, verdict, flags, out=sys.stdout):
    print("\nCALIFICACIÓN DEL GANCHO", file=out)
    print("=" * 62, file=out)
    print(f"  \"{text.strip()}\"\n", file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {name:<13} {bar(score)} {score:5.1f}", file=out)
        print(f"  {'':<13} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'GANCHO':<13} {bar(overall)} {overall:5.1f}   {verdict}", file=out)
    for f in flags:
        print(f"\n  DESCALIFICA  {f}", file=out)
    if verdict != "FUERTE":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Propiedad más débil: {weakest}. Arregla esa y vuelve a correrlo.", file=out)
    print("", file=out)


def render_table(rows, out=sys.stdout):
    print("\nRANKING DE GANCHOS\n" + "=" * 78, file=out)
    for i, r in enumerate(rows, 1):
        mark = "->" if i == 1 else "  "
        hook = r["hook"] if len(r["hook"]) <= 62 else r["hook"][:59] + "..."
        print(f"{mark} {r['score']:5.1f} {r['verdict']:<7} {hook}", file=out)
        print(f"        más débil: {r['weakest']} ({r['checks'][r['weakest']]['score']:.0f})", file=out)
        for f in r["flags"]:
            print(f"        descalifica: {f}", file=out)
    print("\nGraba el primero. Si el primero está debajo de 50, ninguno de estos es el gancho.\n",
          file=out)


def score_lines(lines, sps=SPS):
    payload = []
    for line in lines:
        results, overall, verdict, flags = run(line, sps)
        payload.append({
            "hook": line,
            "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
            "weakest": min(CHECKS, key=lambda c: results[c][0]),
            "flags": flags,
            "score": round(overall, 1),
            "verdict": verdict,
        })
    return payload


def main():
    ap = argparse.ArgumentParser(description="Califica el gancho de un reel en cinco propiedades.")
    ap.add_argument("input", nargs="?", default="-", help="archivo con un gancho por línea, o -")
    ap.add_argument("--gancho", "--hook", dest="hook", help="califica un solo gancho")
    ap.add_argument("--sps", type=float, default=SPS, help=f"sílabas por segundo (default {SPS})")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.hook:
        lines = [args.hook]
    else:
        raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
        lines = [l.strip() for l in raw.splitlines() if l.strip()]
    if not lines:
        print("no hay nada que calificar", file=sys.stderr)
        sys.exit(2)

    payload = score_lines(lines, args.sps)

    if args.json:
        print(json.dumps(payload if len(payload) > 1 else payload[0], indent=2, ensure_ascii=False))
        return

    if len(payload) == 1:
        results, overall, verdict, flags = run(lines[0], args.sps)
        render_one(lines[0], results, overall, verdict, flags)
    else:
        render_table(sorted(payload, key=lambda r: -r["score"]))

    sys.exit(0 if max(p["score"] for p in payload) >= 70 else 1)


if __name__ == "__main__":
    main()
