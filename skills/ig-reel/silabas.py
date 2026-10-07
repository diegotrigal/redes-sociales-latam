#!/usr/bin/env python3
"""
silabas.py - cuánto tarda en decirse una línea en español.

El original en inglés contaba palabras a 165 por minuto. En español eso falla:
«desafortunadamente» es una palabra y ocho sílabas, y un guion en español sale
más largo que el mismo guion en inglés. Aquí se cuentan sílabas, que es lo que
de verdad marca el tiempo al hablar.

Reglas de conteo (las del español, simplificadas):
  - cada núcleo vocálico es una sílaba;
  - dos vocales abiertas juntas (a, e, o) se separan: «pe-or», «a-é-re-o»;
  - una abierta con una cerrada (i, u) sin acento forman diptongo: «ai-re»;
  - una cerrada con acento rompe el diptongo: «dí-a», «ba-úl»;
  - la «y» final suena a vocal pero va en diptongo: «hoy», «muy»;
  - las cifras se cuentan como se dicen, aproximado: «$18,000» ≈ «dieciocho mil
    pesos».

Ritmo por defecto: 6 sílabas por segundo, que es un ritmo de reel hablado a
cámara (la conversación normal en español anda entre 5 y 7). Mídete con un
guion en voz alta y ajústalo con --sps.
"""

import re

SPS = 6.0

FUERTES = set("aeoáéóíú")        # í y ú con acento se portan como abiertas
VOCALES = set("aeiouáéíóúü")
TOKEN_RE = re.compile(r"\$?\s?\d[\d,.]*\s?%?|[^\W\d_]+")


def _silabas_palabra(w):
    w = w.lower()
    if w == "y":
        return 1
    n, prev = 0, None
    for i, c in enumerate(w):
        es_vocal = c in VOCALES or (c == "y" and i == len(w) - 1 and i > 0
                                    and w[i - 1] in VOCALES)
        if not es_vocal:
            prev = None
            continue
        if prev is None:
            n += 1
        elif c in FUERTES and prev in FUERTES:
            n += 1
        prev = c
    return max(n, 1)


def _silabas_cifra(tok):
    digitos = re.sub(r"\D", "", tok.split(".")[0] if "," in tok else tok)
    largo = len(digitos.lstrip("0")) or 1
    n = {1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7}.get(largo, 8)
    if "$" in tok:
        n += 2                     # «pesos»
    if "%" in tok:
        n += 3                     # «por ciento»
    return n


def silabas(texto):
    total = 0
    for tok in TOKEN_RE.findall(texto):
        total += _silabas_cifra(tok) if any(ch.isdigit() for ch in tok) else _silabas_palabra(tok)
    return total


def segundos(texto, sps=SPS):
    return silabas(texto) / sps


if __name__ == "__main__":
    import sys
    for linea in (sys.stdin.read() if len(sys.argv) < 2 else " ".join(sys.argv[1:])).splitlines():
        if linea.strip():
            print(f"{silabas(linea):>3} sílabas  ~{segundos(linea):4.1f}s  {linea}")
