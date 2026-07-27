#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Coletor do Santo do Dia.

Busca a página do dia em santo.cancaonova.com e grava `dados/santos.json`
com nome, imagem, biografia resumida, oração (quando houver) e a fonte.

Roda no build (servidor), não no navegador: a página não envia
`Access-Control-Allow-Origin`, portanto o navegador do visitante não
consegue lê-la directamente (só o wp-json do site tem CORS aberto, e não
expõe o conteúdo do santo). Ver README.

Uso:
    python coletar_santo.py
"""

from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from html import unescape
from pathlib import Path

RAIZ = Path(__file__).parent
SAIDA = RAIZ / "dados" / "santos.json"
URL_ORIGEM = "https://santo.cancaonova.com/"

CABECALHOS = {
    "User-Agent": "Mozilla/5.0 (compatible; CatholicDay/1.0; leitor do santo do dia)",
}


def buscar(url: str) -> str | None:
    try:
        req = urllib.request.Request(url, headers=CABECALHOS)
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(f"! falha ao buscar {url} — {type(e).__name__}: {e}")
        return None


def limpar_html(texto: str) -> str:
    texto = re.sub(r"<[^>]+>", "", texto or "")
    texto = unescape(texto)
    return re.sub(r"\s+", " ", texto).strip()


def extrair(html: str) -> dict | None:
    m_titulo = re.search(
        r'<h1 class="entry-title">\s*<span>(.*?)</span>', html, re.S
    )
    if not m_titulo:
        return None
    nome = limpar_html(m_titulo.group(1))

    m_conteudo = re.search(
        r'<div class="entry-content content-santo">(.*?)</div>\s*</article>',
        html,
        re.S,
    )
    if not m_conteudo:
        return None
    conteudo = m_conteudo.group(1)

    # Remove o bloco de botoes de partilha, que nao faz parte do texto.
    conteudo = re.sub(
        r"<ul id='share-buttons'.*?</ul>", "", conteudo, flags=re.S
    )

    # Imagem principal: o link em volta do <img> aponta para a versao em
    # resolucao total (a variante "-300x225" etc. e so a miniatura).
    imagem = ""
    m_imagem = re.search(
        r'<a href="([^"]+\.(?:jpg|jpeg|png|webp))"[^>]*>\s*<img[^>]*class="[^"]*wp-image',
        conteudo,
        re.I,
    )
    if m_imagem:
        imagem = m_imagem.group(1)
    else:
        m_img_solto = re.search(r'<img[^>]+src="([^"]+)"[^>]*class="[^"]*wp-image', conteudo)
        if m_img_solto:
            imagem = m_img_solto.group(1)

    # Retira o paragrafo da imagem para nao duplicar no corpo do texto.
    conteudo_sem_imagem = re.sub(r"<p>\s*<a[^>]*>\s*<img.*?</a>\s*</p>", "", conteudo, count=1, flags=re.S)
    conteudo_sem_imagem = re.sub(r"<p>\s*<img.*?</p>", "", conteudo_sem_imagem, count=1, flags=re.S)

    # Divide em biografia / oracao / "outros santos" pela procura do
    # paragrafo-titulo "Minha oracao" e, depois dele, "Outros santos".
    partes = re.split(
        r"<p>\s*<(?:strong|b)>\s*Minha\s+ora[çc][ãa]o\s*</(?:strong|b)>\s*</p>",
        conteudo_sem_imagem,
        maxsplit=1,
        flags=re.I,
    )
    biografia_html = partes[0]
    resto_html = partes[1] if len(partes) > 1 else ""

    oracao_html = resto_html
    outros_html = ""
    if resto_html:
        partes2 = re.split(
            r"<p>\s*<(?:b|strong)>\s*Outros santos",
            resto_html,
            maxsplit=1,
            flags=re.I,
        )
        oracao_html = partes2[0]
        outros_html = partes2[1] if len(partes2) > 1 else ""

    def paragrafos(bloco_html: str) -> list[dict]:
        resultado = []
        for m in re.finditer(r"<p>(.*?)</p>", bloco_html, re.S):
            bruto = m.group(1).strip()
            if not bruto:
                continue
            so_negrito = re.fullmatch(
                r"<(?:strong|b)>(.*?)</(?:strong|b)>", bruto, re.S
            )
            texto = limpar_html(bruto)
            if not texto:
                continue
            if so_negrito and len(texto) < 60:
                resultado.append({"tipo": "subtitulo", "texto": texto})
            else:
                resultado.append({"tipo": "texto", "texto": texto})
        return resultado

    biografia = paragrafos(biografia_html)
    oracao = paragrafos(oracao_html)

    # Lista de fontes citadas no proprio artigo (quando presente), procurada
    # em todo o conteudo original — no HTML de origem ela aparece dentro da
    # secao "Outros santos", anexada ao ultimo item da lista.
    fontes_citadas: list[str] = []
    m_fontes = re.search(r"<b>\s*Fontes:\s*</b>\s*</li>(.*?)</ul>", outros_html, re.S | re.I)
    if m_fontes:
        for m_li in re.finditer(r"<li>(.*?)</li>", m_fontes.group(1), re.S):
            texto = limpar_html(m_li.group(1))
            if texto:
                fontes_citadas.append(texto)

    if not nome or not biografia:
        return None

    return {
        "nome": nome,
        "imagem": imagem,
        "biografia": biografia,
        "oracao": oracao,
        "fontes_citadas": fontes_citadas,
    }


def main() -> int:
    print(f"Buscando {URL_ORIGEM} ...")
    html = buscar(URL_ORIGEM)
    if not html:
        print("Falha ao buscar a pagina. Mantendo santos.json anterior.")
        return 1

    dados = extrair(html)
    if not dados:
        print("Nao foi possivel reconhecer a estrutura da pagina. Mantendo santos.json anterior.")
        return 1

    agora = datetime.now(timezone.utc)
    conteudo = {
        "atualizado_em": agora.isoformat(),
        "fonte_url": URL_ORIGEM,
        "fonte_nome": "Canção Nova — Santo do Dia",
        **dados,
    }

    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    SAIDA.write_text(json.dumps(conteudo, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\nSanto do dia: {dados['nome']}")
    print(f"Imagem: {'sim' if dados['imagem'] else 'nao encontrada'}")
    print(f"Paragrafos de biografia: {len(dados['biografia'])}")
    print(f"Oracao: {'sim' if dados['oracao'] else 'nao ha nesta pagina'}")
    print(f"Fontes citadas no artigo: {len(dados['fontes_citadas'])}")
    print(f"\nGravado em {SAIDA.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
