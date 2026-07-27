#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera um PDF por documento do Vaticano II a partir do HTML baixado, e
grava documentos/concilios/vaticano-ii.json com a estrutura (capitulos,
faixas de paragrafo, pagina do PDF de cada capitulo).

Usa reportlab (nao HTML->PDF): construimos o PDF nos mesmos, paragrafo por
paragrafo, e registamos a pagina exata em que cada capitulo comeca via
callback do proprio gerador — mais preciso que inferir depois com regex
(como foi preciso fazer para o Catecismo, cujo PDF ja vinha pronto).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Flowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

sys.path.insert(0, str(Path(__file__).parent))
from _lib_concilios import estruturar_documento
from baixar_vaticano_ii import DOCUMENTOS

RAIZ = Path(__file__).parent
BRUTO = RAIZ / "documentos" / "concilios" / "_bruto"
SAIDA_PDF = RAIZ / "documentos" / "concilios" / "vaticano-ii"
SAIDA_JSON = RAIZ / "documentos" / "concilios" / "vaticano-ii.json"

# Fonte com bom suporte a acentuacao portuguesa; o Windows tem a Georgia/
# Times New Roman, mas para nao depender do SO usamos as fontes-base do
# reportlab (Helvetica), que ja cobrem latin-1 (acentos portugueses inclusos).
ESTILO_TITULO = ParagraphStyle(
    "TituloDoc", fontName="Helvetica-Bold", fontSize=16, leading=20,
    alignment=TA_CENTER, spaceAfter=6,
)
ESTILO_SUBTITULO_DOC = ParagraphStyle(
    "SubtituloDoc", fontName="Helvetica", fontSize=11, leading=14,
    alignment=TA_CENTER, spaceAfter=24, textColor="#555555",
)
ESTILO_CAPITULO = ParagraphStyle(
    "Capitulo", fontName="Helvetica-Bold", fontSize=13, leading=16,
    alignment=TA_CENTER, spaceBefore=18, spaceAfter=14,
)
ESTILO_SUBTITULO_SECAO = ParagraphStyle(
    "SubtituloSecao", fontName="Helvetica-BoldOblique", fontSize=10.5, leading=14,
    spaceBefore=10, spaceAfter=4,
)
ESTILO_PARAGRAFO = ParagraphStyle(
    "CorpoParagrafo", fontName="Helvetica", fontSize=10.5, leading=15,
    alignment=TA_JUSTIFY, spaceAfter=8,
)


class _MarcadorPagina(Flowable):
    """Flowable invisivel (altura zero) que so serve para o callback
    onFirstPage/onLaterPages do documento registar em que pagina ele caiu."""

    def __init__(self, chave):
        Flowable.__init__(self)
        self.chave = chave
        self.width = 0
        self.height = 0

    def wrap(self, availWidth, availHeight):
        return (0, 0)

    def draw(self):
        pass


class _DocComRegistoDePaginas(SimpleDocTemplate):
    """SimpleDocTemplate que regista, para cada _MarcadorPagina desenhado,
    a pagina exata em que ele caiu — usado para os links "abrir na pagina
    X do PDF"."""

    def __init__(self, *args, **kwargs):
        SimpleDocTemplate.__init__(self, *args, **kwargs)
        self.paginas_registadas: dict[str, int] = {}

    def afterFlowable(self, flowable):
        if isinstance(flowable, _MarcadorPagina):
            self.paginas_registadas[flowable.chave] = self.page


def gerar_pdf_documento(slug: str, titulo: str, tipo: str, data: str, capitulos) -> dict:
    caminho_pdf = SAIDA_PDF / f"{slug}.pdf"
    SAIDA_PDF.mkdir(parents=True, exist_ok=True)

    doc = _DocComRegistoDePaginas(
        str(caminho_pdf), pagesize=A4,
        topMargin=2.2 * cm, bottomMargin=2.2 * cm,
        leftMargin=2.4 * cm, rightMargin=2.4 * cm,
        title=titulo, author="Concílio Vaticano II",
    )

    elementos = [
        Paragraph(f"{tipo.upper()}", ESTILO_SUBTITULO_DOC),
        Paragraph(titulo, ESTILO_TITULO),
        Paragraph(f"Concílio Ecuménico Vaticano II — {data}", ESTILO_SUBTITULO_DOC),
    ]

    for i_cap, capitulo in enumerate(capitulos):
        if i_cap > 0:
            elementos.append(PageBreak())
        if capitulo.titulo:
            elementos.append(_MarcadorPagina(f"capitulo:{i_cap}"))
            elementos.append(Paragraph(capitulo.titulo, ESTILO_CAPITULO))

        subtitulo_anterior = None
        for paragrafo in capitulo.paragrafos:
            elementos.append(_MarcadorPagina(f"paragrafo:{paragrafo.numero}"))
            if paragrafo.subtitulo and paragrafo.subtitulo != subtitulo_anterior:
                elementos.append(Paragraph(paragrafo.subtitulo, ESTILO_SUBTITULO_SECAO))
                subtitulo_anterior = paragrafo.subtitulo
            texto = f"<b>{paragrafo.numero}.</b>&nbsp; {paragrafo.texto}"
            elementos.append(Paragraph(texto, ESTILO_PARAGRAFO))

    doc.build(elementos)
    paginas = doc.paginas_registadas

    return {
        "arquivo_pdf": f"{slug}.pdf",
        "paginas_capitulo": {k.split(":", 1)[1]: v for k, v in paginas.items() if k.startswith("capitulo:")},
        "paginas_paragrafo": {k.split(":", 1)[1]: v for k, v in paginas.items() if k.startswith("paragrafo:")},
        "total_paginas": doc.page,
    }


def main():
    resultado = {"documentos": []}

    for arquivo, slug, tipo, titulo, data in DOCUMENTOS:
        caminho_html = BRUTO / f"{slug}.html"
        if not caminho_html.exists():
            print(f"  ! faltando: {slug}.html — rode baixar_vaticano_ii.py primeiro")
            continue

        html = caminho_html.read_text(encoding="utf-8", errors="replace")
        capitulos = estruturar_documento(html)
        if not capitulos:
            print(f"  ! nao foi possivel estruturar: {slug}")
            continue

        info_pdf = gerar_pdf_documento(slug, titulo, tipo, data, capitulos)

        doc_json = {
            "slug": slug,
            "tipo": tipo,
            "titulo": titulo,
            "data": data,
            "arquivo_pdf": info_pdf["arquivo_pdf"],
            "total_paginas": info_pdf["total_paginas"],
            "paragrafo_final": capitulos[-1].paragrafos[-1].numero,
            "capitulos": [],
        }
        for i_cap, capitulo in enumerate(capitulos):
            pagina_cap = info_pdf["paginas_capitulo"].get(str(i_cap))
            if pagina_cap is None:
                # capitulo sem titulo proprio (proemio): pagina do 1o paragrafo
                pagina_cap = info_pdf["paginas_paragrafo"].get(str(capitulo.paragrafos[0].numero), 1)
            doc_json["capitulos"].append(
                {
                    "titulo": capitulo.titulo or "Proémio",
                    "paragrafo_inicial": capitulo.paragrafos[0].numero,
                    "paragrafo_final": capitulo.paragrafos[-1].numero,
                    "pagina_pdf": pagina_cap,
                }
            )

        resultado["documentos"].append(doc_json)
        print(f"  ok  {slug:28s}  {info_pdf['total_paginas']:3d} paginas  {len(capitulos)} capitulos")

    SAIDA_JSON.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nGravado {SAIDA_JSON.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
