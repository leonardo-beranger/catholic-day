# -*- coding: utf-8 -*-
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _resumos_vaticano_ii import RESUMOS

d = json.load(open(Path(__file__).parent / "documentos" / "concilios" / "vaticano-ii.json", encoding="utf-8"))

faltando = []
total = 0
for doc in d["documentos"]:
    for i, cap in enumerate(doc["capitulos"]):
        total += 1
        if (doc["slug"], i) not in RESUMOS:
            faltando.append((doc["slug"], i, cap["titulo"]))

print("Total de nos:", total)
print("Faltando:", len(faltando))
for f in faltando:
    print("  -", f)

sobrando = [k for k in RESUMOS if k not in {(doc["slug"], i) for doc in d["documentos"] for i in range(len(doc["capitulos"]))}]
print("Sobrando (chaves invalidas):", len(sobrando))
for s in sobrando:
    print("  -", s)
