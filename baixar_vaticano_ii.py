#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Baixa os 16 documentos do Concilio Vaticano II em portugues (vatican.va).

Salva o HTML bruto em documentos/concilios/_bruto/ (materia-prima, nao
versionado no site) para processamento posterior por gerar_pdfs_vaticano_ii.py.
"""
import time
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).parent
DESTINO = RAIZ / "documentos" / "concilios" / "_bruto"
DESTINO.mkdir(parents=True, exist_ok=True)

BASE = "https://www.vatican.va/archive/hist_councils/ii_vatican_council/documents/"

# (arquivo, slug, tipo, titulo, data)
DOCUMENTOS = [
    ("vat-ii_const_19631204_sacrosanctum-concilium_po.html", "sacrosanctum-concilium", "Constituição", "Sacrosanctum Concilium — Sobre a Sagrada Liturgia", "1963-12-04"),
    ("vat-ii_decree_19631204_inter-mirifica_po.html", "inter-mirifica", "Decreto", "Inter Mirifica — Sobre os Meios de Comunicação Social", "1963-12-04"),
    ("vat-ii_const_19641121_lumen-gentium_po.html", "lumen-gentium", "Constituição", "Lumen Gentium — Sobre a Igreja", "1964-11-21"),
    ("vat-ii_decree_19641121_orientalium-ecclesiarum_po.html", "orientalium-ecclesiarum", "Decreto", "Orientalium Ecclesiarum — Sobre as Igrejas Orientais Católicas", "1964-11-21"),
    ("vat-ii_decree_19641121_unitatis-redintegratio_po.html", "unitatis-redintegratio", "Decreto", "Unitatis Redintegratio — Sobre o Ecumenismo", "1964-11-21"),
    ("vat-ii_decree_19651028_christus-dominus_po.html", "christus-dominus", "Decreto", "Christus Dominus — Sobre o Múnus Pastoral dos Bispos", "1965-10-28"),
    ("vat-ii_decree_19651028_perfectae-caritatis_po.html", "perfectae-caritatis", "Decreto", "Perfectae Caritatis — Sobre a Renovação da Vida Religiosa", "1965-10-28"),
    ("vat-ii_decree_19651028_optatam-totius_po.html", "optatam-totius", "Decreto", "Optatam Totius — Sobre a Formação Sacerdotal", "1965-10-28"),
    ("vat-ii_decl_19651028_gravissimum-educationis_po.html", "gravissimum-educationis", "Declaração", "Gravissimum Educationis — Sobre a Educação Cristã", "1965-10-28"),
    ("vat-ii_decl_19651028_nostra-aetate_po.html", "nostra-aetate", "Declaração", "Nostra Aetate — Sobre as Religiões Não-Cristãs", "1965-10-28"),
    ("vat-ii_const_19651118_dei-verbum_po.html", "dei-verbum", "Constituição", "Dei Verbum — Sobre a Divina Revelação", "1965-11-18"),
    ("vat-ii_decree_19651118_apostolicam-actuositatem_po.html", "apostolicam-actuositatem", "Decreto", "Apostolicam Actuositatem — Sobre o Apostolado dos Leigos", "1965-11-18"),
    ("vat-ii_decl_19651207_dignitatis-humanae_po.html", "dignitatis-humanae", "Declaração", "Dignitatis Humanae — Sobre a Liberdade Religiosa", "1965-12-07"),
    ("vat-ii_decree_19651207_ad-gentes_po.html", "ad-gentes", "Decreto", "Ad Gentes — Sobre a Atividade Missionária da Igreja", "1965-12-07"),
    ("vat-ii_decree_19651207_presbyterorum-ordinis_po.html", "presbyterorum-ordinis", "Decreto", "Presbyterorum Ordinis — Sobre o Ministério e Vida dos Presbíteros", "1965-12-07"),
    ("vat-ii_const_19651207_gaudium-et-spes_po.html", "gaudium-et-spes", "Constituição", "Gaudium et Spes — Sobre a Igreja no Mundo Atual", "1965-12-07"),
]

CABECALHOS = {"User-Agent": "Mozilla/5.0 (compatible; CatholicDay/1.0; estudo teologico)"}


def main():
    for arquivo, slug, tipo, titulo, data in DOCUMENTOS:
        destino = DESTINO / f"{slug}.html"
        if destino.exists():
            print(f"  ja existe: {slug}")
            continue
        url = BASE + arquivo
        try:
            req = urllib.request.Request(url, headers=CABECALHOS)
            with urllib.request.urlopen(req, timeout=30) as r:
                conteudo = r.read()
            destino.write_bytes(conteudo)
            print(f"  ok  {slug}  ({len(conteudo)} bytes)")
        except Exception as e:
            print(f"  FALHA {slug}: {type(e).__name__}: {e}")
        time.sleep(0.5)  # gentil com o servidor do Vaticano


if __name__ == "__main__":
    main()
