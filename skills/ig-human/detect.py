#!/usr/bin/env python3
"""
detect.py - cinco revisiones que califican qué tan escrito-por-máquina se ve un
borrador en español.

Qué es:  cinco heurísticas locales, modeladas en las señales que miden los
detectores públicos: variación del largo de las oraciones, cosas concretas,
vocabulario de relleno, huella tipográfica y voz. Todo se calcula en tu máquina
a partir del texto. No se sube nada.

Qué NO es:  GPTZero, Originality, Copyleaks, Winston ni Turnitin. No llama a sus
APIs y no puede prometer su veredicto. Atrapa las cosas en las que todos se
fijan, y por eso arreglarlas suele mover sus números, pero la única promesa
honesta es la de esta línea.

En español no hay contracciones como en inglés, así que la VOZ se mide con
marcas de oralidad (pues, la neta, ojo, mira…, editables en slop.json), con la
persona (yo, tú, usted, nosotros) y con las estructuras de modelo.

Cada revisión da una calificación HUMANA de 0 a 100. Más alto es mejor.

Uso
  python3 detect.py borrador.txt
  pbpaste | python3 detect.py -
  python3 detect.py borrador.txt --json
  python3 detect.py antes.txt despues.txt      # comparar dos versiones
"""

import argparse
import json
import os
import re
import statistics
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "slop.json")

SENT_RE = re.compile(r"[^.!?\n]+[.!?]*")
WORD_RE = re.compile(r"[^\W\d_]+")
PRONOUNS = re.compile(
    r"(?<!\w)(yo|me|mi|mis|m[ií]o|m[ií]a|conmigo|nosotr[oa]s|nos|nuestr[oa]s?|"
    r"tú|te|ti|contigo|usted|ustedes|vos)(?!\w)", re.IGNORECASE)
# «tu/tus» quedan fuera a propósito: «tus ventas, tus tiempos, tus clientes» es
# justo como escribe el marketing generado, y contarlo como voz premiaba al modelo.
NUMBERS = re.compile(r"\$\s?\d|\b\d[\d,.]*\s?%?")
NUM_WORDS = re.compile(
    r"(?<!\w)(dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|once|doce|trece|catorce|"
    r"quince|veinte|treinta|cuarenta|cincuenta|cien|cientos|mil|millón|millones|"
    r"docena|pesos|dólares|varos|quincena|aguinaldo)(?!\w)", re.IGNORECASE)
TOKEN_RE = re.compile(r"[^\W\d_][\w'’]*|[.!?¿¡\n]")


def clamp(n):
    return max(0.0, min(100.0, n))


def scale(value, human, machine):
    """Lleva value a 0-100, donde `human` -> 100 y `machine` -> 0."""
    if human == machine:
        return 50.0
    return clamp((value - machine) / (human - machine) * 100)


def sentences(text):
    return [s.strip() for s in SENT_RE.findall(text) if len(s.split()) > 2]


def words(text):
    return WORD_RE.findall(text)


def proper_names(text):
    """Palabras con mayúscula que no abren oración.

    Una racha de palabras con mayúscula («Lo Mejor Para Tu Negocio») cuenta
    como una sola, y solo si no abre oración: así un título calcado del inglés
    no se disfraza de datos concretos, y «Panadería La Espiga» cuenta una vez.
    """
    found, start, prev_cap = set(), True, False
    for tok in TOKEN_RE.findall(text):
        if tok in ".!?¿¡\n":
            start, prev_cap = True, False
            continue
        cap = tok[0].isupper() and len(tok) >= 3
        if cap and not start and not prev_cap:
            found.add(tok)
        prev_cap = cap if not start else tok[0].isupper()
        start = False
    return found


def _pattern(find):
    return re.compile(r"(?<!\w)" + re.escape(find).replace(r"\ ", r"\s+") + r"(?!\w)",
                      re.IGNORECASE)


def check_burstiness(text):
    """Las personas varían mucho el largo de las oraciones. Los modelos, parejo."""
    lens = [len(s.split()) for s in sentences(text)]
    if len(lens) < 4:
        return 50.0, "muy corto para juzgar"
    mean = statistics.mean(lens)
    cv = statistics.pstdev(lens) / mean if mean else 0
    score = scale(cv, human=0.65, machine=0.22)
    return score, f"variación {cv:.2f} en {len(lens)} oraciones (lo bueno: 0.5 o más)"


def check_specificity(text):
    """Números, nombres, cosas concretas. El relleno es abstracto."""
    w = words(text)
    if len(w) < 25:
        return 50.0, "muy corto para juzgar"
    per100 = 100 / len(w)
    hits = (len(NUMBERS.findall(text)) + len(NUM_WORDS.findall(text))
            + len(proper_names(text)))
    density = hits * per100
    score = scale(density, human=6.0, machine=0.5)
    return score, f"{hits} datos concretos, {density:.1f} por cada 100 palabras (lo bueno: 4 o más)"


def check_slop(text, lex):
    """Densidad de muletillas contra el léxico."""
    w = words(text)
    if not w:
        return 50.0, "vacío"
    hits, found = 0, []
    for entry in lex["words"] + lex["phrases"]:
        n = len(_pattern(entry["find"]).findall(text))
        if n:
            hits += n
            found.append(entry["find"])
    density = hits * 100 / len(w)
    score = scale(density, human=0.0, machine=4.0)
    detail = f"{hits} muletillas, {density:.1f} por cada 100 palabras"
    if found:
        detail += " (" + ", ".join(sorted(found)[:4]) + (", ..." if len(found) > 4 else "") + ")"
    return score, detail


def check_fingerprint(text):
    """Caracteres que el teclado de un celular no produce."""
    invisible = sum(1 for c in text if unicodedata.category(c) == "Cf"
                    and c != "‍")          # la unión de emojis es legítima
    em = text.count("—")
    curly = sum(text.count(c) for c in "‘’“”«»")
    ellip = text.count("…")
    nbsp = sum(text.count(c) for c in "   ")
    total = invisible * 4 + em * 2 + curly + ellip + nbsp
    per1k = total * 1000 / max(len(text), 1)
    score = scale(per1k, human=0.0, machine=12.0)
    detail = (f"{invisible} invisibles, {em} rayas, {curly} comillas curvas o angulares, "
              f"{ellip} puntos suspensivos de un carácter, {nbsp} espacios duros")
    return score, detail


def check_voice(text, lex):
    """Oralidad, persona y las formas por defecto del modelo."""
    w = words(text)
    if len(w) < 25:
        return 50.0, "muy corto para juzgar"
    per100 = 100 / len(w)
    oral = sum(len(_pattern(m).findall(text)) for m in lex.get("oralidad", [])) * per100
    person = len(PRONOUNS.findall(text)) * per100
    tells, names = 0, []
    for s in lex["structures"]:
        try:
            n = len(re.compile(s["regex"], re.MULTILINE).findall(text))
        except re.error:
            continue
        if n:
            tells += n
            names.append(s["id"])
    bullets = [len(b.split()) for b in re.findall(r"(?m)^\s*[-*•]\s+(.+)$", text)]
    uniform = (len(bullets) >= 3 and statistics.pstdev(bullets) < 1.6)
    score = (scale(oral, human=1.5, machine=0.0) * 0.30
             + scale(person, human=8.0, machine=1.0) * 0.40
             + clamp(100 - tells * 22) * 0.30)
    if uniform:
        score -= 12
        names.append("viñetas-parejas")
    detail = (f"{oral:.1f} marcas de oralidad y {person:.1f} pronombres personales "
              f"por cada 100 palabras, {tells} estructura(s) de modelo")
    if names:
        detail += " [" + ", ".join(names[:4]) + "]"
    return clamp(score), detail


CHECKS = ["RITMO", "CONCRETO", "MULETILLAS", "HUELLA", "VOZ"]


def run(text, lex):
    results = {
        "RITMO": check_burstiness(text),
        "CONCRETO": check_specificity(text),
        "MULETILLAS": check_slop(text, lex),
        "HUELLA": check_fingerprint(text),
        "VOZ": check_voice(text, lex),
    }
    scores = [results[c][0] for c in CHECKS]
    # La revisión más débil arrastra el veredicto: a un detector le basta una señal.
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4
    verdict = "PASA" if overall >= 70 and min(scores) >= 55 else (
        "REVISAR" if overall >= 50 else "MARCADO")
    return results, overall, verdict


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render(results, overall, verdict, label=None, out=sys.stdout):
    title = "PANEL DE DETECCIÓN" + (f"  -  {label}" if label else "")
    print("\n" + title, file=out)
    print("=" * max(len(title), 62), file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {name:<13} {bar(score)} {score:5.1f}", file=out)
        print(f"  {'':<13} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'HUMANO':<13} {bar(overall)} {overall:5.1f}   {verdict}", file=out)
    if verdict != "PASA":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Señal más débil: {weakest}. Arregla esa primero.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Califica qué tan escrito-por-máquina se ve un texto.")
    ap.add_argument("input", nargs="?", default="-", help="archivo, o - para stdin")
    ap.add_argument("compare", nargs="?", help="segundo archivo, para ver antes y después")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--lexicon", default=LEX)
    args = ap.parse_args()

    lex = json.load(open(args.lexicon, encoding="utf-8"))
    read = lambda p: sys.stdin.read() if p == "-" else open(p, encoding="utf-8").read()

    targets = [(args.input, read(args.input))]
    if args.compare:
        targets.append((args.compare, read(args.compare)))

    payload = []
    for name, text in targets:
        results, overall, verdict = run(text, lex)
        payload.append({
            "source": name,
            "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
            "human_score": round(overall, 1),
            "verdict": verdict,
        })

    if args.json:
        print(json.dumps(payload if args.compare else payload[0], indent=2, ensure_ascii=False))
        return

    for (name, text), p in zip(targets, payload):
        results, overall, verdict = run(text, lex)
        render(results, overall, verdict, label=os.path.basename(name) if args.compare else None)
    if args.compare:
        a, b = payload
        delta = b["human_score"] - a["human_score"]
        print(f"  {a['human_score']:.1f} {a['verdict']}  ->  "
              f"{b['human_score']:.1f} {b['verdict']}   ({delta:+.1f})\n")

    sys.exit(0 if payload[-1]["verdict"] == "PASA" else 1)


if __name__ == "__main__":
    main()
