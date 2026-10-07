#!/usr/bin/env python3
"""
swipe.py - ordena los reels que juntaste por cuánto le ganaron a su propia
cuenta, nombra la fórmula de gancho de cada uno y escribe el archivo de
referencias.

La idea es una sola corrección: las vistas solas no son evidencia. Una cuenta
de 2,000,000 de seguidores con 400,000 vistas tuvo un día tranquilo. Una de
4,000 seguidores con 400,000 vistas encontró algo. Esto ordena por el múltiplo
sobre la mediana de la propia cuenta, que es la única versión de «se hizo
viral» que te dice algo que puedes copiar.

La entrada es un archivo separado por tabuladores que llenas mientras ves,
un reel por renglón, con encabezado (en español o en inglés):

    cuenta    seguidores   mediana   vistas    gancho
    @alguien  48000        11000     412000    nadie te dice que tus primeros 30 van a fracasar

`mediana` son las vistas típicas recientes de esa cuenta y es la mejor base.
Si solo tienes `seguidores`, deja fuera la mediana y el script lo avisa.
`gancho` es la primera línea del reel, dicha o en pantalla, tal cual.

Uso
  python3 swipe.py capturados.tsv
  python3 swipe.py capturados.tsv --out ~/.claude/instagram/swipe.md
  python3 swipe.py capturados.tsv --json
"""

import argparse
import json
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HOOKS = os.path.join(HERE, "..", "ig-reel", "hooks.json")
WORD_RE = re.compile(r"[\w$%'’-]+")
COLUMNAS = {"cuenta": "account", "seguidores": "followers", "mediana": "median",
            "vistas": "views", "reproducciones": "views", "gancho": "hook"}

try:                                              # opcional: calificar los ganchos
    sys.path.insert(0, os.path.join(HERE, "..", "ig-reel"))
    from hookscore import run as score_hook       # noqa: E402
except Exception:                                 # ig-viral copiado solo
    score_hook = None


def load_formulas(path):
    try:
        d = json.load(open(path, encoding="utf-8"))
    except Exception:
        return None
    by_id = {h["id"]: h for h in d["hooks"]}
    order = d.get("classify_order") or sorted(by_id)
    return [(by_id[i]["id"], by_id[i]["name"],
             re.compile(by_id[i]["match"], re.IGNORECASE)) for i in order if i in by_id]


def classify(hook, formulas):
    if not formulas:
        return None, "sin clasificar"
    for fid, name, pattern in formulas:
        if pattern.search(hook):
            return fid, name
    return None, "sin clasificar"


def _num(s):
    """'48k', '1.2M', '48,000' y '48 mil' -> entero."""
    s = (s or "").strip().lower().replace(" ", "")
    m = re.match(r"^([\d.,]+)(k|mil|m|mill|millones)?$", s)
    if not m:
        digits = re.sub(r"[^\d]", "", s)
        return int(digits) if digits else None
    n, suf = m.group(1), m.group(2)
    if suf:
        n = float(n.replace(",", "."))
        return int(n * (1_000 if suf in ("k", "mil") else 1_000_000))
    return int(re.sub(r"[^\d]", "", n) or 0)


def read_rows(path):
    raw = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
    lines = [l for l in raw.splitlines() if l.strip() and not l.lstrip().startswith("#")]
    if not lines:
        return []
    head = [COLUMNAS.get(c.strip().lower(), c.strip().lower()) for c in lines[0].split("\t")]
    if "views" in head and "hook" in head:
        cols, body = head, lines[1:]
    else:
        cols, body = ["account", "followers", "views", "hook"], lines
    rows = []
    for line in body:
        cells = line.split("\t")
        if len(cells) < len(cols):
            cells += [""] * (len(cols) - len(cells))
        r = dict(zip(cols, [c.strip() for c in cells]))
        r["views"] = _num(r.get("views")) or 0
        for k in ("followers", "median"):
            r[k] = _num(r.get(k))
        if r["views"] and r.get("hook"):
            rows.append(r)
    return rows


def analyse(rows, formulas):
    used_median = any(r.get("median") for r in rows)
    for r in rows:
        base = r.get("median") or r.get("followers") or 0
        r["baseline"] = base
        r["outlier"] = round(r["views"] / base, 2) if base else None
        r["formula_id"], r["formula"] = classify(r["hook"], formulas)
        r["words"] = len(WORD_RE.findall(r["hook"]))
        if score_hook:
            _, overall, verdict, _ = score_hook(r["hook"])
            r["hook_score"], r["hook_verdict"] = round(overall, 1), verdict
        else:
            r["hook_score"], r["hook_verdict"] = None, None
    ranked = sorted(rows, key=lambda r: -(r["outlier"] or 0))
    third = max(1, len(ranked) // 3)
    top, bottom = ranked[:third], ranked[-third:]

    def med(items, key):
        vals = [i[key] for i in items if i.get(key) is not None]
        return round(statistics.median(vals), 1) if vals else None

    counts = {}
    for r in top:
        counts[r["formula"]] = counts.get(r["formula"], 0) + 1
    return {
        "baseline": "mediana de la cuenta" if used_median else "seguidores",
        "n": len(ranked),
        "accounts": len({r.get("account", "") for r in ranked}),
        "reels": ranked,
        "top_formulas": sorted(counts.items(), key=lambda kv: -kv[1]),
        "top_hook_score": med(top, "hook_score"),
        "bottom_hook_score": med(bottom, "hook_score"),
        "top_words": med(top, "words"),
        "bottom_words": med(bottom, "words"),
        "unclassified": sum(1 for r in ranked if r["formula"] == "sin clasificar"),
    }


def render(a, out=sys.stdout):
    head = (f"REFERENCIAS  ·  {a['n']} reels  ·  {a['accounts']} cuentas  ·  "
            f"base: {a['baseline']}")
    print("\n" + head, file=out)
    print("=" * max(len(head), 78), file=out)
    for r in a["reels"]:
        mult = f"{r['outlier']:.1f}x" if r["outlier"] else "   ?"
        score = f"{r['hook_score']:.0f}" if r["hook_score"] is not None else " -"
        fid = f"#{r['formula_id']:<2}" if r["formula_id"] else "-  "
        print(f"  {mult:>7}  gancho {score:>3}  {fid} {r['formula'][:22]:<22} "
              f"{r.get('account', '')[:16]:<16} {r['views']:>9,}", file=out)
        print(f"           \"{r['hook'][:96]}\"", file=out)
    print("-" * max(len(head), 78), file=out)
    print("QUÉ ESTÁ FUNCIONANDO EN ESTE LOTE", file=out)
    if a["top_formulas"]:
        print("  tercio de arriba:        "
              + ", ".join(f"{n} x{c}" for n, c in a["top_formulas"][:4]), file=out)
    if a["top_hook_score"] is not None:
        print(f"  mediana del gancho:      arriba {a['top_hook_score']:.0f}  "
              f"vs abajo {a['bottom_hook_score']:.0f}", file=out)
    print(f"  largo del gancho:        arriba {a['top_words']} palabras  "
          f"vs abajo {a['bottom_words']} palabras", file=out)
    print(f"  sin clasificar:          {a['unclassified']} de {a['n']}. Léelos a mano: ahí "
          "se esconde una fórmula que todavía no tienes.", file=out)
    print("\n  Un lote juntado a mano es evidencia, no prueba. Doce reels no enseñan nada;\n"
          "  cuarenta en seis cuentas ya dicen algo. Junta más antes de creértelo.\n", file=out)


def to_markdown(a):
    lines = ["# Referencias", "",
             f"{a['n']} reels de {a['accounts']} cuentas. "
             f"Ordenados por múltiplo sobre {a['baseline']}.", ""]
    for r in a["reels"]:
        mult = f"{r['outlier']:.1f}x" if r["outlier"] else "?"
        lines += [f"## {mult}  {r['formula']}  ({r.get('account', '')})",
                  f"- vistas: {r['views']:,}  base: {r['baseline']:,}",
                  f"- calificación del gancho: {r['hook_score']}  palabras: {r['words']}",
                  f"- gancho: \"{r['hook']}\"", ""]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Ordena reels por múltiplo sobre su propia cuenta.")
    ap.add_argument("input", nargs="?", default="-", help="archivo TSV, o - para stdin")
    ap.add_argument("--hooks", default=HOOKS, help="ruta a ig-reel/hooks.json")
    ap.add_argument("--out", help="escribe también el archivo de referencias en markdown aquí")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rows = read_rows(args.input)
    if not rows:
        print("no hay renglones útiles. Hace falta un archivo separado por tabuladores con "
              "al menos vistas y gancho.", file=sys.stderr)
        sys.exit(2)
    formulas = load_formulas(args.hooks)
    a = analyse(rows, formulas)
    if not formulas:
        print("nota: no encontré hooks.json, las fórmulas quedan sin nombre. Usa --hooks.", file=sys.stderr)
    if score_hook is None:
        print("nota: no pude importar hookscore.py, sin calificación de ganchos.", file=sys.stderr)

    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    if args.out:
        path = os.path.expanduser(args.out)
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        open(path, "w", encoding="utf-8").write(to_markdown(a))
        print(f"escrito: {path}", file=sys.stderr)


if __name__ == "__main__":
    main()
