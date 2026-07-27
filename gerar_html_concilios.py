# -*- coding: utf-8 -*-
"""Gera o fragmento HTML da secao 'Vaticano II' da pagina Concilios, no
mesmo padrao usado na pagina do Catecismo: arvore recolhivel, ficha por
capitulo com resumo + faixa de paragrafos, botao que abre o leitor de PDF
embutido na pagina exata."""
import html as html_mod
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _resumos_vaticano_ii import RESUMOS

RAIZ = Path(__file__).parent
DADOS = json.loads((RAIZ / "documentos" / "concilios" / "vaticano-ii.json").read_text(encoding="utf-8"))

PDF_BASE = "/documentos/concilios/vaticano-ii/"


def esc(txt):
    return html_mod.escape(txt, quote=True)


def gerar_capitulo(doc, idx_cap, cap):
    resumo = RESUMOS.get((doc["slug"], idx_cap), "")
    faixa = f"§§ {cap['paragrafo_inicial']}-{cap['paragrafo_final']}" if cap["paragrafo_inicial"] != cap["paragrafo_final"] else f"§ {cap['paragrafo_inicial']}"
    return f'''        <article class="cic-folha">
          <div class="cic-folha__cabecalho">
            <h4>{esc(cap["titulo"])}</h4>
            <span class="cic-faixa">{faixa}</span>
          </div>
          <p>{esc(resumo)}</p>
          <button type="button" class="cic-link-pdf" data-pdf="{esc(PDF_BASE + doc['arquivo_pdf'])}" data-pagina-pdf="{cap['pagina_pdf']}" data-titulo-pdf="{esc(doc['titulo'])}">Abrir no leitor (página {cap['pagina_pdf']})</button>
        </article>
'''


def gerar_documento(doc):
    filhos = "".join(gerar_capitulo(doc, i, c) for i, c in enumerate(doc["capitulos"]))
    return f'''      <details class="cic-capitulo">
        <summary>{esc(doc["tipo"])} — {esc(doc["titulo"])} <span class="cic-pagina-tag">{doc["data"]} · {doc["total_paginas"]} pág.</span></summary>
        <div class="cic-capitulo__corpo">
{filhos}        </div>
      </details>
'''


html_final = "".join(gerar_documento(doc) for doc in DADOS["documentos"])

destino = RAIZ / "_arvore_vaticano_ii.html"
destino.write_text(html_final, encoding="utf-8")
print("Gerado", destino, "-", len(html_final), "caracteres,", len(DADOS["documentos"]), "documentos")
