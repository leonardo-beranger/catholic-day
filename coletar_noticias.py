#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Coletor de notícias do All Day Vatican.

Busca os feeds RSS das fontes escolhidas, filtra o que diz respeito à Igreja
Católica, extrai imagem e resumo, e grava `dados/noticias.json`.

Roda no build (servidor), não no navegador: nenhum destes feeds envia
`Access-Control-Allow-Origin`, portanto o navegador do visitante não consegue
lê-los directamente. Ver README.

Uso:
    python coletar_noticias.py            # só o dia de hoje
    python coletar_noticias.py --dias 3   # janela de 3 dias (útil se houver pouca notícia)
"""

from __future__ import annotations

import argparse
import json
import re
import socket
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from pathlib import Path

RAIZ = Path(__file__).parent
SAIDA = RAIZ / "dados" / "noticias.json"

TEMPO_LIMITE = 30
CABECALHOS = {
    "User-Agent": "Mozilla/5.0 (compatible; CatholicDay/1.0; agregador de noticias catolicas)",
    "Accept": "application/rss+xml, application/xml, text/xml, */*",
}

# ---------------------------------------------------------------- Fontes
# `catolica`: fonte inteiramente católica — dispensa filtro por palavra-chave.
FONTES = [
    {"nome": "Vatican News", "url": "https://www.vaticannews.va/pt.rss.xml", "catolica": True},
    {"nome": "Vatican News", "url": "https://www.vaticannews.va/pt/papa.rss.xml", "catolica": True},
    {"nome": "Vatican News", "url": "https://www.vaticannews.va/pt/igreja.rss.xml", "catolica": True},
    {"nome": "Canção Nova", "url": "https://noticias.cancaonova.com/feed/", "catolica": True},
    {"nome": "G1", "url": "https://g1.globo.com/rss/g1/", "catolica": False},
    {"nome": "Folha de S.Paulo", "url": "https://feeds.folha.uol.com.br/emcimadahora/rss091.xml", "catolica": False},
    {"nome": "Folha de S.Paulo", "url": "https://feeds.folha.uol.com.br/mundo/rss091.xml", "catolica": False},
    {"nome": "Estadão", "url": "https://www.estadao.com.br/arc/outboundfeeds/feeds/rss/sections/brasil/?outputType=xml", "catolica": False},
    {"nome": "Estadão", "url": "https://www.estadao.com.br/arc/outboundfeeds/feeds/rss/sections/internacional/?outputType=xml", "catolica": False},
    {"nome": "O Antagonista", "url": "https://oantagonista.com.br/feed/", "catolica": False},
    {"nome": "Veja", "url": "https://veja.abril.com.br/feed/", "catolica": False},
]

# ------------------------------------------------- Filtro de assunto católico
# Termos precisos: valem em qualquer lugar do texto (título ou resumo).
# Evitam-se aqui termos ambíguos como "dom " (Avenida Dom Pedro II) ou
# "nossa senhora" (Nossa Senhora do Socorro é um município) — geram
# falso positivo em jornais generalistas.
TERMOS_FORTES = [
    "papa leão", "papa leao", "papa francisco", "leão xiv", "leao xiv",
    "vaticano", "santa sé", "santa se", "igreja católica", "igreja catolica",
    "católic", "catolic", "cardeal", "cardeais", "arcebispo", "arquidiocese",
    "cnbb", "conclave", "encíclica", "enciclica", "canoniza", "beatifica",
    "cúria romana", "curia romana", "pontífice", "pontifice", "pontifícia",
    "pontificia", "basílica de são pedro", "basilica de sao pedro",
    "sínodo dos bispos", "sinodo dos bispos", "santuário de aparecida",
    "santuario de aparecida", "jubileu da igreja",
]

# Termos mais frágeis: só contam se aparecerem no TÍTULO, onde a chance de
# serem o assunto da notícia (e não menção de passagem) é bem maior.
TERMOS_TITULO = [
    "papa", "bispo", "diocese", "missa", "vigário", "vigario", "padre",
    "sacerdote", "freira", "religiosa", "jesuíta", "jesuita", "capela",
]

# Descartam o item mesmo que algum termo tenha casado.
RUIDO = [
    "igreja universal", "igreja evangélica", "igreja evangelica", "iurd",
    "assembleia de deus", "edir macedo", "universal do reino",
    "bispo de são josé", "bispo de sao jose",  # nomes de lugares/times
]


def buscar(url: str) -> bytes | None:
    try:
        req = urllib.request.Request(url, headers=CABECALHOS)
        with urllib.request.urlopen(req, timeout=TEMPO_LIMITE) as r:
            return r.read()
    except (urllib.error.URLError, urllib.error.HTTPError, socket.timeout, OSError) as e:
        print(f"  ! falhou {url} — {type(e).__name__}")
        return None


def limpar_html(texto: str) -> str:
    """Remove tags e normaliza espaços de um trecho de HTML."""
    if not texto:
        return ""
    texto = re.sub(r"<script.*?</script>", " ", texto, flags=re.S | re.I)
    texto = re.sub(r"<[^>]+>", " ", texto)
    texto = unescape(texto)
    return re.sub(r"\s+", " ", texto).strip()


def primeira_imagem_no_html(html: str) -> str:
    m = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', html or "", re.I)
    return m.group(1) if m else ""


def texto_de(elemento, *nomes: str) -> str:
    """Primeiro filho não vazio entre os nomes dados (com ou sem namespace)."""
    for nome in nomes:
        for filho in elemento:
            etiqueta = filho.tag.split("}")[-1].lower()
            if etiqueta == nome.lower() and (filho.text or "").strip():
                return filho.text.strip()
    return ""


def extrair_imagem(item) -> str:
    """Procura imagem nas várias convenções de RSS."""
    for filho in item:
        etiqueta = filho.tag.split("}")[-1].lower()
        if etiqueta in ("thumbnail", "content") and filho.get("url"):
            tipo = (filho.get("type") or "").lower()
            if etiqueta == "content" and tipo and not tipo.startswith("image"):
                continue
            return filho.get("url")
        if etiqueta == "enclosure":
            tipo = (filho.get("type") or "").lower()
            if filho.get("url") and (not tipo or tipo.startswith("image")):
                return filho.get("url")
        if etiqueta == "group":
            for neto in filho:
                if neto.get("url"):
                    return neto.get("url")
        if etiqueta == "image":
            url = texto_de(filho, "url")
            if url:
                return url
    # Último recurso: <img> dentro da descrição / conteúdo.
    for campo in ("description", "encoded", "summary"):
        bruto = texto_de(item, campo)
        img = primeira_imagem_no_html(bruto)
        if img:
            return img
    return ""


def extrair_data(item) -> datetime | None:
    bruto = texto_de(item, "pubDate", "published", "updated", "date")
    if not bruto:
        return None
    try:
        d = parsedate_to_datetime(bruto)
    except (TypeError, ValueError):
        try:
            d = datetime.fromisoformat(bruto.replace("Z", "+00:00"))
        except ValueError:
            return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    return d


# Só a abertura do texto entra no filtro. Alguns feeds (G1, por exemplo)
# publicam o artigo inteiro na <description>, e aí qualquer menção de
# passagem — «o candidato se apresenta como católico» — faria a notícia
# passar como se fosse sobre a Igreja. O assunto de uma notícia está no
# título e nas primeiras linhas.
TAMANHO_ABERTURA = 200


def e_assunto_catolico(titulo: str, resumo: str) -> str | None:
    """Devolve o termo que casou, ou None. Serve também para depuração."""
    titulo_min = titulo.lower()
    abertura = f"{titulo} {resumo[:TAMANHO_ABERTURA]}".lower()

    if any(r in abertura for r in RUIDO):
        return None
    for t in TERMOS_FORTES:
        if t in abertura:
            return t
    for t in TERMOS_TITULO:
        if t in titulo_min:
            return t + " (no título)"
    return None


def ler_feed(fonte: dict, limite_data: datetime) -> list[dict]:
    bruto = buscar(fonte["url"])
    if not bruto:
        return []
    try:
        raiz = ET.fromstring(bruto)
    except ET.ParseError as e:
        print(f"  ! XML inválido em {fonte['url']} — {e}")
        return []

    itens = raiz.iter()
    encontrados = []
    for elemento in itens:
        etiqueta = elemento.tag.split("}")[-1].lower()
        if etiqueta not in ("item", "entry"):
            continue

        titulo = limpar_html(texto_de(elemento, "title"))
        if not titulo:
            continue

        link = texto_de(elemento, "link")
        if not link:  # Atom guarda o link no atributo href
            for filho in elemento:
                if filho.tag.split("}")[-1].lower() == "link" and filho.get("href"):
                    link = filho.get("href")
                    break
        if not link:
            continue

        resumo = limpar_html(texto_de(elemento, "description", "summary", "encoded"))
        data = extrair_data(elemento)

        if data and data < limite_data:
            continue

        motivo = ""
        if not fonte["catolica"]:
            motivo = e_assunto_catolico(titulo, resumo) or ""
            if not motivo:
                continue

        encontrados.append(
            {
                "titulo": titulo,
                "resumo": (resumo[:280] + "…") if len(resumo) > 280 else resumo,
                "url": link.strip(),
                "imagem": extrair_imagem(elemento).strip(),
                "fonte": fonte["nome"],
                "data": data.isoformat() if data else "",
                "_ordem": data.timestamp() if data else 0,
                "_motivo": motivo,
            }
        )
    return encontrados


def main() -> int:
    parser = argparse.ArgumentParser(description="Coleta notícias católicas dos feeds.")
    parser.add_argument(
        "--dias", type=int, default=1,
        help="janela em dias (1 = só hoje). Padrão: 1",
    )
    parser.add_argument(
        "--max", type=int, default=24, help="máximo de notícias gravadas. Padrão: 24"
    )
    args = parser.parse_args()

    agora = datetime.now(timezone.utc)
    limite = agora - timedelta(days=args.dias)

    print(f"Coletando notícias desde {limite.date()} ({args.dias} dia(s))\n")

    todas: list[dict] = []
    for fonte in FONTES:
        achados = ler_feed(fonte, limite)
        print(f"  {fonte['nome']:<20} {len(achados):>3} item(ns)")
        todas.extend(achados)

    # Remove duplicadas por URL e por título.
    vistos_url, vistos_titulo, unicas = set(), set(), []
    for n in sorted(todas, key=lambda x: x["_ordem"], reverse=True):
        chave_titulo = re.sub(r"\W+", "", n["titulo"].lower())[:60]
        if n["url"] in vistos_url or chave_titulo in vistos_titulo:
            continue
        vistos_url.add(n["url"])
        vistos_titulo.add(chave_titulo)
        n.pop("_ordem", None)
        motivo = n.pop("_motivo", "")
        if motivo:
            print(f"    · {n['fonte']}: «{n['titulo'][:60]}» ← casou «{motivo}»")
        unicas.append(n)

    unicas = unicas[: args.max]

    conteudo = {
        "atualizado_em": agora.isoformat(),
        "janela_dias": args.dias,
        "total": len(unicas),
        "fontes": sorted({f["nome"] for f in FONTES}),
        "itens": unicas,
    }

    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    SAIDA.write_text(
        json.dumps(conteudo, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    com_imagem = sum(1 for n in unicas if n["imagem"])
    print(f"\n{len(unicas)} notícias gravadas em {SAIDA.relative_to(RAIZ)}")
    print(f"{com_imagem} com imagem, {len(unicas) - com_imagem} sem")
    if not unicas:
        print("\nAviso: nenhuma notícia encontrada. Tente uma janela maior: --dias 3")
    return 0


if __name__ == "__main__":
    sys.exit(main())
