#!/usr/bin/env python3
"""
beats.py - convierte el guion de un reel en una hoja de tiempos antes de grabar.

Calcula cuánto tarda en decirse cada línea (por sílabas, ver silabas.py), las
apila en códigos de tiempo y marca las cuatro cosas que matan un reel en la
edición: un gancho que pasa de los tres segundos, un tramo tan largo que da
tiempo de irse, una racha de líneas sin nada concreto, y un final que no
regresa al principio.

Los tiempos son un estimado, suficiente para planear la edición y no un
sustituto de grabarlo. Pon tu ritmo con --sps después de leer un guion en voz
alta con cronómetro: sílabas totales entre segundos.

Uso
  python3 beats.py guion.txt
  python3 beats.py guion.txt --meta 30
  python3 beats.py guion.txt --sps 6.5 --meta 45
  pbpaste | python3 beats.py -
  python3 beats.py guion.txt --json
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from silabas import SPS, silabas  # noqa: E402

WORD_RE = re.compile(r"[\w$%'’-]+")
SENT_RE = re.compile(r"[^.!?]+[.!?]*")
CONCRETE_RE = re.compile(
    r"\$\s?\d|\b\d[\d,.]*\b|(?<![.!?¿¡]\s)(?<![¿¡\n])(?<!^)\b[A-ZÁÉÍÓÚÑ][\wáéíóúñ]{2,}\b"
    r"|(?i:\b(?:dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|quince|veinte|treinta|"
    r"cincuenta|cien|mil|millones?|pesos)\b)",
    re.MULTILINE)
STOPWORDS = {
    "el", "la", "los", "las", "un", "una", "unos", "unas", "y", "o", "pero", "si",
    "de", "del", "a", "al", "en", "por", "para", "con", "sin", "que", "qué", "es",
    "son", "fue", "era", "ser", "esto", "eso", "este", "esta", "lo", "le", "les",
    "se", "me", "te", "nos", "tu", "tus", "mi", "mis", "su", "sus", "yo", "tú",
    "no", "sí", "ya", "más", "muy", "como", "cómo", "cuando", "todo", "hay", "va",
    "voy", "vas", "uno", "porque", "pues", "así", "también", "solo", "sólo",
}

HOOK_WINDOW = 3.0        # segundos. Después de esto, el dedo ya decidió.
MAX_BEAT = 4.0           # segundos en una sola idea sin que cambie la pantalla.
ABSTRACT_RUN = 3         # tramos seguidos sin nada que se pueda checar.


def words(text):
    return WORD_RE.findall(re.sub(r"(?<=\d),(?=\d)", "", text))


def pretty(token):
    return re.sub(r"(\d)(?=(\d{3})+$)", r"\1,", token)


def tc(seconds):
    m, s = divmod(seconds, 60)
    return f"{int(m)}:{s:04.1f}"


def split_beats(raw, sps):
    """Una línea es un tramo, salvo que sea muy larga para serlo."""
    beats = []
    for line in [l.strip() for l in raw.splitlines()]:
        if not line:
            continue
        if silabas(line) / sps <= MAX_BEAT * 1.5:
            beats.append(line)
            continue
        # Párrafo largo: se parte en fin de oración para que los tiempos
        # signifiquen algo.
        parts = [p.strip() for p in SENT_RE.findall(line) if p.strip()]
        buf = ""
        for part in parts:
            candidate = (buf + " " + part).strip()
            if buf and silabas(candidate) / sps > MAX_BEAT:
                beats.append(buf)
                buf = part
            else:
                buf = candidate
        if buf:
            beats.append(buf)
    return beats


def analyse(raw, sps=SPS, target=None):
    beats = split_beats(raw, sps)
    if not beats:
        return None

    rows, clock = [], 0.0
    for i, text in enumerate(beats):
        syl = silabas(text)
        dur = syl / sps
        rows.append({
            "n": i + 1,
            "start": round(clock, 2),
            "dur": round(dur, 2),
            "words": len(words(text)),
            "syllables": syl,
            "text": text,
            "concrete": len(CONCRETE_RE.findall(text)),
            "label": "",
            "flags": [],
        })
        clock += dur
    total = clock

    for r in rows:
        if r["n"] == 1 or r["start"] + r["dur"] <= HOOK_WINDOW:
            r["label"] = "GANCHO"
    rows[-1]["label"] = "CIERRE" if rows[-1]["label"] != "GANCHO" else "GANCHO/CIERRE"
    half = total / 2
    for r in rows:
        if not r["label"] and r["start"] <= half < r["start"] + r["dur"]:
            r["label"] = "MITAD"

    notes = []
    if rows[0]["dur"] > HOOK_WINDOW:
        rows[0]["flags"].append(f"el gancho dura {rows[0]['dur']:.1f}s, pasa de {HOOK_WINDOW:.0f}s")
        notes.append(f"El tramo 1 tarda {rows[0]['dur']:.1f}s en decirse. Bájalo a unas "
                     f"{int(HOOK_WINDOW * sps)} sílabas o menos, o el gancho llega cuando "
                     "ya se decidió todo.")
    if rows[0]["concrete"] == 0:
        notes.append("El tramo 1 no trae número ni nombre. Los ganchos sin algo que se pueda "
                     "checar son los que se deslizan.")

    for r in rows:
        if r["dur"] > MAX_BEAT:
            r["flags"].append(f"{r['dur']:.1f}s en un solo tramo")
    long_beats = [r["n"] for r in rows if r["dur"] > MAX_BEAT]
    if long_beats:
        notes.append(f"Tramo(s) {', '.join(map(str, long_beats))} pasan de {MAX_BEAT:.0f}s. "
                     "Parte la línea o cambia lo que se ve dentro de ella. "
                     "Una toma fija es donde la gente se va.")

    run, start = 0, None
    for r in rows:
        if r["concrete"] == 0:
            run += 1
            start = start if start is not None else r["n"]
            if run == ABSTRACT_RUN:
                notes.append(f"Los tramos {start}-{r['n']} no traen nada concreto. "
                             "Mete un número, un nombre o un precio en alguno.")
        else:
            run, start = 0, None

    first = {w.lower() for w in words(rows[0]["text"]) if w.lower() not in STOPWORDS}
    last = {w.lower() for w in words(rows[-1]["text"]) if w.lower() not in STOPWORDS}
    loop = sorted(pretty(w) for w in first & last)
    if loop:
        notes.append(f"Hay loop: el último tramo repite «{', '.join(loop[:3])}» del gancho. "
                     "La segunda vista es alcance gratis.")
    else:
        notes.append("Sin loop. El último tramo no comparte ninguna palabra con el gancho y el "
                     "video cierra plano. Repetir una palabra del tramo 1 es la segunda vista "
                     "más barata que hay.")

    if target:
        delta = total - target
        if abs(delta) <= target * 0.1:
            notes.append(f"El largo va bien ({total:.1f}s contra {target:g}s).")
        elif delta > 0:
            notes.append(f"{delta:.1f}s de más. Corta unas {int(delta * sps)} sílabas.")
        else:
            notes.append(f"{-delta:.1f}s de menos. Agrega unas {int(-delta * sps)} sílabas "
                         "o grábalo corto. Corto casi siempre es lo correcto.")

    return {
        "sps": sps, "target": target,
        "total_seconds": round(total, 2),
        "total_words": sum(r["words"] for r in rows),
        "total_syllables": sum(r["syllables"] for r in rows),
        "beats": rows,
        "notes": notes,
    }


def render(a, out=sys.stdout):
    head = (f"HOJA DE TIEMPOS  ·  {a['total_words']} palabras  ·  {a['total_syllables']} sílabas  ·  "
            f"~{a['total_seconds']:.1f}s a {a['sps']:g} síl/s"
            + (f"  ·  meta {a['target']:g}s" if a["target"] else ""))
    print("\n" + head, file=out)
    print("=" * max(len(head), 72), file=out)
    for r in a["beats"]:
        label = f"{r['label']:<9}" if r["label"] else " " * 9
        print(f"  {tc(r['start'])}  {r['dur']:4.1f}s  {label}{r['text']}", file=out)
        for f in r["flags"]:
            print(f"  {'':>6}  {'':>5}  {'':<9}^ {f}", file=out)
    print("-" * max(len(head), 72), file=out)
    for n in a["notes"]:
        print(f"  - {n}", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Cronometra el guion de un reel.")
    ap.add_argument("input", nargs="?", default="-", help="archivo del guion, o - para stdin")
    ap.add_argument("--sps", type=float, default=SPS, help=f"sílabas por segundo (default {SPS})")
    ap.add_argument("--meta", "--target", dest="target", type=float, help="duración meta en segundos")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    a = analyse(raw, sps=args.sps, target=args.target)
    if not a:
        print("guion vacío", file=sys.stderr)
        sys.exit(2)
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    sys.exit(0)


if __name__ == "__main__":
    main()
