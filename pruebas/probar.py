#!/usr/bin/env python3
"""
probar.py - revisa que todo el paquete siga funcionando después de un cambio.

  python3 pruebas/probar.py

Sale con 0 si todo pasa. Úsalo después de editar slop.json, hooks.json o
cualquier script: un regex mal escapado rompe en silencio.
"""

import importlib.util
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(RAIZ, "skills")
PRUEBAS = os.path.join(RAIZ, "pruebas")
fallas = []


def cargar(skill, modulo):
    ruta = os.path.join(SKILLS, skill, modulo + ".py")
    sys.path.insert(0, os.path.dirname(ruta))
    spec = importlib.util.spec_from_file_location(f"{skill}_{modulo}", ruta)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def check(nombre, ok, detalle=""):
    print(("  ok    " if ok else "  FALLA ") + nombre + (f"  ({detalle})" if detalle and not ok else ""))
    if not ok:
        fallas.append(nombre)


def leer(nombre):
    return open(os.path.join(PRUEBAS, nombre), encoding="utf-8").read()


print("\nskills")
for carpeta in sorted(os.listdir(SKILLS)):
    md = os.path.join(SKILLS, carpeta, "SKILL.md")
    texto = open(md, encoding="utf-8").read()
    m = re.match(r"^---\nname: (\S+)\ndescription: >-\n(.+?)\n---\n", texto, re.S)
    check(f"{carpeta}: frontmatter con name y description", bool(m) and m.group(1) == carpeta)
    check(f"{carpeta}: sin la frase prohibida", "de barrio" not in texto.lower())

print("\nig-human")
human = cargar("ig-human", "humanize")
detect = cargar("ig-human", "detect")
lex = human.load_lexicon()
for s in lex["structures"]:
    re.compile(s["regex"])
check("los regex de slop.json compilan", True)
limpio, _ = human.humanize("La chef 👩‍🍳 cocina​ rico — y barato.", lex)
check("respeta emojis compuestos", "👩‍🍳" in limpio, limpio)
check("borra el espacio de ancho cero suelto", "​" not in limpio)
check("raya a coma", "rico, y barato" in limpio, limpio)
limpio, _ = human.humanize("Cabe destacar que el envío es gratis.", lex)
check("borra relleno y recupera la mayúscula", limpio.strip() == "El envío es gratis.", limpio)
limpio, _ = human.humanize("Visítanos en https://ejemplo.com/potenciar-ventas hoy en día.", lex)
check("no toca URLs", "https://ejemplo.com/potenciar-ventas" in limpio and "hoy." in limpio, limpio)
_, ia, _ = detect.run(leer("caption-ia.txt"), lex)
_, hum, _ = detect.run(leer("caption-humano.txt"), lex)
check("el caption hecho por IA sale MARCADO (<50)", ia < 50, f"{ia:.1f}")
check("el caption humano sale arriba de 65", hum > 65, f"{hum:.1f}")

print("\nig-reel")
sil = cargar("ig-reel", "silabas")
for palabra, n in [("desafortunadamente", 8), ("día", 2), ("aire", 2), ("aéreo", 4),
                   ("Paraguay", 3), ("construcción", 3), ("leer", 2), ("hoy", 1)]:
    check(f"sílabas de «{palabra}» = {n}", sil.silabas(palabra) == n, str(sil.silabas(palabra)))
hs = cargar("ig-reel", "hookscore")
_, malo, v1, f1 = hs.run("Hola a todos, en este video les voy a enseñar cómo vender más")
_, bueno, v2, _ = hs.run("Perdí $18,000 por una cláusula que no puse en el contrato.")
check("gancho con saludo y preámbulo sale FLOJO", v1 == "FLOJO" and len(f1) == 2, f"{malo:.1f} {v1}")
check("gancho con costo y número sale FUERTE", v2 == "FUERTE", f"{bueno:.1f} {v2}")
hooks = json.load(open(os.path.join(SKILLS, "ig-reel", "hooks.json"), encoding="utf-8"))
por_id = {h["id"]: h for h in hooks["hooks"]}
check("classify_order cubre las 29 fórmulas", sorted(hooks["classify_order"]) == list(range(1, 30)))
patrones = [(i, re.compile(por_id[i]["match"], re.I)) for i in hooks["classify_order"]]
for h in hooks["hooks"]:
    got = next((i for i, p in patrones if p.search(h["example"])), None)
    check(f"fórmula #{h['id']} reconoce su propio ejemplo", got == h["id"], f"salió {got}")
beats = cargar("ig-reel", "beats")
a = beats.analyse(leer("guion.txt"), target=25)
check("beats: arma la hoja y detecta el loop", a and any("Hay loop" in n for n in a["notes"]))

print("\nig-caption")
cap = cargar("ig-caption", "caption")
a = cap.analyse(leer("caption-promo.txt"))
estados = {c["check"]: c["status"] for c in a["checks"]}
check("promo: saludo de entrada es FALLA", estados.get("PRIMERA LÍNEA") == "FALLA")
check("promo: 6 hashtags es FALLA", estados.get("HASHTAGS") == "FALLA")
check("promo: precio sin IVA es AVISO", estados.get("PRECIO") == "AVISO")
check("promo: promoción sin vigencia es AVISO", estados.get("PROMOCIÓN") == "AVISO")
a = cap.analyse(leer("caption-humano.txt"))
check("humano: un solo pedido (WhatsApp)", a["asks"] == ["WhatsApp"], str(a["asks"]))
a = cap.analyse("Pan de muerto a $65 IVA incluido. 2x1 del 25 de octubre al 2 de noviembre.")
estados = {c["check"]: c["status"] for c in a["checks"]}
check("precio con IVA y promo con vigencia pasan", estados.get("PRECIO") == "OK"
      and estados.get("PROMOCIÓN") == "OK", str(estados))

print("\nig-viral")
sw = cargar("ig-viral", "swipe")
check("lee «4.2k», «12 mil» y «1,800»", (sw._num("4.2k"), sw._num("12 mil"), sw._num("1,800"))
      == (4200, 12000, 1800))
rows = sw.read_rows(os.path.join(PRUEBAS, "capturados.tsv"))
r = sw.analyse(rows, sw.load_formulas(sw.HOOKS))
check("ordena por múltiplo y clasifica #28 arriba", r["reels"][0]["formula_id"] == 28)

print("\nig-perfil")
rub = json.load(open(os.path.join(SKILLS, "ig-perfil", "rubric.json"), encoding="utf-8"))
check("la rúbrica suma 100", sum(i["points"] for i in rub["items"]) == 100)

print(f"\n{'TODO PASA' if not fallas else str(len(fallas)) + ' FALLA(S)'}\n")
sys.exit(1 if fallas else 0)
