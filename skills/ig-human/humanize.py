#!/usr/bin/env python3
"""
humanize.py - quita la huella de máquina de un borrador en español.

Tres pasadas, en este orden:

  1. INVISIBLES   borra o normaliza los caracteres que un teclado humano no
                  produce: espacios de ancho cero, unidores, guiones suaves,
                  BOM, caracteres de etiqueta, espacios duros y finos. Sobreviven
                  al copiar y pegar y son la huella más mecánica del texto
                  generado. Respeta los emojis compuestos (👩‍🍳, 🏳️‍🌈) y las
                  banderas de subdivisión, que usan esos mismos caracteres.
  2. TIPOGRAFÍA   raya -> coma, guion medio -> guion, comillas curvas y
                  angulares («») -> rectas, puntos suspensivos de un carácter
                  -> tres puntos, viñeta -> guion.
  3. LÉXICO       cambia las muletillas de slop.json por palabras llanas,
                  respetando mayúsculas y sin tocar URLs.

Las estructuras («No es solo X, es Y», tercias, muros de hashtags, preguntas
sin «¿») se SEÑALAN, nunca se reescriben solas: cambiarle la forma a una
oración necesita criterio, y eso le toca al modelo o a una persona.

Uso
  python3 humanize.py borrador.txt
  python3 humanize.py borrador.txt --reporte
  pbpaste | python3 humanize.py - --reporte
  python3 humanize.py borrador.txt --json
  python3 humanize.py borrador.txt -o limpio.txt
"""

import argparse
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "slop.json")

URL_RE = re.compile(r"https?://\S+|www\.\S+|\S+@\S+\.\S+|\bwa\.me/\S+")
SENT_RE = re.compile(r"[^.!?\n]+[.!?]*")
LETRA = r"[^\W\d_]"

# Emojis compuestos: dos pictogramas unidos por U+200D, y las banderas de
# subdivisión (🏴 + caracteres de etiqueta). Borrar esos invisibles parte el
# emoji en dos, y en un caption latino eso se nota más que la huella.
_PICTO = r"[\U0001F000-\U0001FAFF☀-➿⬀-⯿]"
_MOD = r"[️\U0001F3FB-\U0001F3FF]*"
ZWJ_EMOJI_RE = re.compile(_PICTO + _MOD + r"(?:‍" + _PICTO + _MOD + r")+")
FLAG_TAG_RE = re.compile(r"\U0001F3F4[\U000E0020-\U000E007F]+")


def load_lexicon(path=LEX):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _cp(spec):
    """'U+200B' -> 0x200B;  'U+E0000-U+E007F' -> (inicio, fin)."""
    if "-" in spec:
        a, b = spec.split("-")
        return (int(a[2:], 16), int(b[2:], 16))
    return int(spec[2:], 16)


def _stash(pattern, text, tag, found):
    def put(m):
        found.append(m.group(0))
        return f"\x00{tag}{len(found) - 1}\x00"
    return pattern.sub(put, text)


def _unstash(text, tag, found):
    for i, s in enumerate(found):
        text = text.replace(f"\x00{tag}{i}\x00", s)
    return text


def protect_urls(text):
    """Cambia las URLs por marcadores para que ninguna pasada toque un enlace."""
    found = []
    return _stash(URL_RE, text, "URL", found), found


def restore_urls(text, found):
    return _unstash(text, "URL", found)


def pass_invisible(text, lex):
    """Borra o vuelve espacio los invisibles. Regresa (texto, hallazgos)."""
    emojis = []
    text = _stash(ZWJ_EMOJI_RE, text, "EMO", emojis)
    text = _stash(FLAG_TAG_RE, text, "EMO", emojis)
    hits = []
    for entry in lex["invisible"]:
        cp = _cp(entry["cp"])
        if isinstance(cp, tuple):
            pattern = "[" + re.escape(chr(cp[0])) + "-" + re.escape(chr(cp[1])) + "]"
        else:
            pattern = re.escape(chr(cp))
        n = len(re.findall(pattern, text))
        if n:
            hits.append({"name": entry["cp"] + " " + entry["name"], "count": n,
                         "action": "borrar" if entry["action"] == "delete" else "espacio"})
            text = re.sub(pattern, "" if entry["action"] == "delete" else " ", text)
    # Cualquier otro carácter de formato (Cf) es invisible por definición.
    stray = [c for c in text if unicodedata.category(c) == "Cf"]
    if stray:
        hits.append({"name": "otros caracteres de formato invisibles", "count": len(stray),
                     "action": "borrar"})
        text = "".join(c for c in text if unicodedata.category(c) != "Cf")
    return _unstash(text, "EMO", emojis), hits


def pass_typographic(text, lex):
    hits = []
    for entry in lex["typographic"]:
        ch = entry["from"]
        n = text.count(ch)
        if not n:
            continue
        hits.append({"name": f"{ch} {entry['name']}", "count": n,
                     "to": entry["to"].strip() or "(espacio)"})
        if ch == "—":
            # Raya de diálogo al inicio de línea: se va sin dejar coma.
            text = re.sub(r"(?m)^([ \t]*)—\s*", r"\1", text)
            # «palabra — palabra» y «palabra—palabra» quedan en coma y espacio.
            text = re.sub(r"\s*—\s*", ", ", text)
        elif ch == "–":
            text = re.sub(r"\s*–\s*(?=\d)", "-", text)       # 5–10  -> 5-10
            text = re.sub(r"\s+–\s+", ", ", text)             # usado como raya
            text = text.replace("–", "-")
        else:
            text = text.replace(ch, entry["to"])
    # Una coma metida antes de otra puntuación se lee mal.
    text = re.sub(r",\s*([,.;:!?])", r"\1", text)
    text = re.sub(r",\s*\n", "\n", text)
    return text, hits


def _match_case(src, repl):
    if not repl:
        return repl
    if src.isupper() and len(src) > 1:
        return repl.upper()
    if src[0].isupper():
        return repl[0].upper() + repl[1:]
    return repl


def _pattern(find):
    return re.compile(r"(?<!\w)" + re.escape(find).replace(r"\ ", r"\s+") + r"(?!\w)",
                      re.IGNORECASE)


def pass_lexical(text, lex):
    """Cambia muletillas por palabras llanas. Primero las más largas."""
    hits = []
    entries = sorted(lex["phrases"] + lex["words"],
                     key=lambda e: len(e["find"]), reverse=True)
    for entry in entries:
        pattern = _pattern(entry["find"])
        found = pattern.findall(text)
        if not found:
            continue
        hits.append({"find": entry["find"], "replace": entry["replace"] or "(borrado)",
                     "count": len(found), "family": entry["family"]})
        text = pattern.sub(lambda m: _match_case(m.group(0), entry["replace"]), text)
    # Limpiar lo que dejan los borrados: puntuación huérfana, espacios dobles,
    # una línea que ahora empieza con coma, o «¿ ,» y «¡ ,».
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"(?m)^[ \t]*(?:[,.;:]+[ \t]*)+", "", text)
    text = re.sub(r"([¿¡])\s*[,;:]\s*", r"\1", text)
    text = re.sub(r"(?m)^[ \t](?=\S)", "", text)
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = re.sub(r",\s*([,.;:!?])", r"\1", text)
    text = re.sub(r"([¿¡])\s+", r"\1", text)
    text = text.replace("...", "\x00ELL\x00")
    text = re.sub(r"\.\s*\.+", ".", text)
    text = re.sub(r"([!?])\s*\.", r"\1", text)
    text = text.replace("\x00ELL\x00", "...")
    text = re.sub(r"¡\s*!", "", text)
    text = re.sub(r"¿\s*\?", "", text)
    text = re.sub(r"(?m)^[ \t]+$", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Una raya que se volvió coma y luego un conector deja una oración pegada
    # («es importante, además, es la prueba»). Se vuelve punto.
    text = re.sub(r",\s*(además|así que|aun así|básicamente|al final)\s*,\s*",
                  lambda m: ". " + m.group(1)[0].upper() + m.group(1)[1:] + ", ", text)
    return text, hits


def scan_structures(text, lex):
    flags = []
    for s in lex["structures"]:
        try:
            pattern = re.compile(s["regex"], re.MULTILINE)
        except re.error:
            continue
        found = pattern.findall(text)
        if found:
            flags.append({"id": s["id"], "name": s["name"], "count": len(found), "fix": s["fix"]})
    # Que todas las oraciones midan lo mismo también es estructura.
    lens = [len(s.split()) for s in SENT_RE.findall(text) if len(s.split()) > 2]
    if len(lens) >= 4:
        mean = sum(lens) / len(lens)
        var = sum((n - mean) ** 2 for n in lens) / len(lens)
        cv = (var ** 0.5) / mean if mean else 0
        if cv < 0.35:
            flags.append({
                "id": "largo-parejo",
                "name": f"Oraciones del mismo largo (variación {cv:.2f})",
                "count": len(lens),
                "fix": "Parte una oración en dos. Deja que otra se alargue. La máquina escribe parejo.",
            })
    return flags


def restore_capitals(original, text):
    """Borrar una apertura deja la siguiente palabra en minúscula.

    Solo se corrige si quien escribe pone mayúscula al iniciar oración: una voz
    en minúsculas a propósito es estilo, no un error, y gritarle encima sería
    justo lo que este script existe para evitar.
    """
    starts = re.findall(r"(?:^|[.!?]\s+|\n)\s*[¿¡\"']?(" + LETRA + r")", original)
    if not starts or sum(1 for c in starts if c.isupper()) * 2 < len(starts):
        return text
    return re.sub(r"(?:^|(?<=[.!?] )|(?<=[.!?]\n)|(?<=\n))(\s*[¿¡\"']?)(" + LETRA + r")",
                  lambda m: m.group(1) + m.group(2).upper(), text)


def humanize(text, lex):
    raw_for_case = text
    text, urls = protect_urls(text)
    text, inv = pass_invisible(text, lex)
    text, typo = pass_typographic(text, lex)
    text, lexi = pass_lexical(text, lex)
    text = restore_capitals(raw_for_case, text)
    text = restore_urls(text, urls)
    return text.strip() + "\n", {
        "invisible": inv,
        "typographic": typo,
        "lexical": lexi,
        "structures": scan_structures(text, lex),
    }


def render_report(report, out=sys.stderr):
    def head(title):
        print(f"\n{title}\n" + "-" * len(title), file=out)

    total = sum(h["count"] for h in report["invisible"]) \
        + sum(h["count"] for h in report["typographic"]) \
        + sum(h["count"] for h in report["lexical"])

    head("REPORTE DEL HUMANIZADOR")
    print(f"{total} huellas de máquina quitadas, "
          f"{len(report['structures'])} estructuras señaladas para reescribir", file=out)

    if report["invisible"]:
        head("1. CARACTERES INVISIBLES")
        for h in report["invisible"]:
            print(f"  {h['count']:>3}x  {h['name']}  -> {h['action']}", file=out)
    if report["typographic"]:
        head("2. TIPOGRAFÍA")
        for h in report["typographic"]:
            print(f"  {h['count']:>3}x  {h['name']}  -> {h['to']}", file=out)
    if report["lexical"]:
        head("3. MULETILLAS")
        for h in report["lexical"]:
            print(f"  {h['count']:>3}x  {h['find']}  -> {h['replace']}   [{h['family']}]", file=out)
    if report["structures"]:
        head("4. ESTRUCTURAS  (no se arreglan solas: reescríbelas tú)")
        for h in report["structures"]:
            print(f"  {h['count']:>3}x  {h['name']}\n        {h['fix']}", file=out)
    if not any(report.values()):
        head("LIMPIO")
        print("  No había nada que quitar.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Quita la huella de máquina de un borrador.")
    ap.add_argument("input", nargs="?", default="-", help="archivo, o - para stdin")
    ap.add_argument("-o", "--out", help="escribe el texto limpio aquí en vez de stdout")
    ap.add_argument("--reporte", "--report", dest="report", action="store_true",
                    help="imprime qué cambió (a stderr)")
    ap.add_argument("--json", action="store_true", help="emite {text, report} en JSON")
    ap.add_argument("--lexicon", default=LEX, help="ruta a slop.json")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    lex = load_lexicon(args.lexicon)
    clean, report = humanize(raw, lex)

    if args.json:
        print(json.dumps({"text": clean, "report": report}, indent=2, ensure_ascii=False))
        return
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(clean)
        print(f"escrito: {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(clean)
    if args.report:
        render_report(report)


if __name__ == "__main__":
    main()
