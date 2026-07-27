# -*- coding: utf-8 -*-
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib_concilios import estruturar_documento

BRUTO = Path(__file__).parent / "documentos" / "concilios" / "_bruto"

for arquivo in sorted(BRUTO.glob("*.html")):
    html = arquivo.read_text(encoding="utf-8", errors="replace")
    capitulos = estruturar_documento(html)
    total_par = sum(len(c.paragrafos) for c in capitulos)
    ultimo_num = capitulos[-1].paragrafos[-1].numero if capitulos and capitulos[-1].paragrafos else 0
    print(f"{arquivo.stem:28s}  capitulos={len(capitulos):2d}  paragrafos={total_par:3d}  ultimo_num={ultimo_num}")
    for c in capitulos:
        titulo = c.titulo or "(sem titulo / proemio)"
        faixa = f"§{c.paragrafos[0].numero}-{c.paragrafos[-1].numero}" if c.paragrafos else "vazio"
        print(f"     - {titulo[:70]:70s} {faixa}")
