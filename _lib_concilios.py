# -*- coding: utf-8 -*-
"""Utilidades compartilhadas para processar os documentos do Vaticano II
baixados de vatican.va (HTML antigo, com fonte e alinhamentos inline).

Nao faz parte do site publicado — e uma ferramenta de preparacao de dados,
usada por gerar_pdfs_vaticano_ii.py.
"""
from __future__ import annotations

import html as html_mod
import re
from dataclasses import dataclass, field

PADRAO_TAG = re.compile(r"<[^>]+>")

# As paginas usam tags inline variadas (<span lang="pt">, <font>) e espacos
# soltos entre a abertura do <p> e o conteudo de fato; este miolo absorve
# zero ou mais delas para o parser nao depender do wrapping exato de cada
# documento (varia de documento para documento, e as vezes dentro do mesmo).
_ENTRE = r'(?:\s|<(?:span|font)[^>]*>)*'

# Marcador de secao: Capitulo, Parte (numeral romano OU ordinal por extenso,
# como no Catecismo), Introducao, Conclusao, Preambulo, Epilogo. O numeral
# em si NAO e capturado com confianca (a fonte do vatican.va tem barbaridades
# como "CAPÍTULO </b>" sem numeral em Dei Verbum) — por isso so identificamos
# o TIPO do marcador aqui, e numeramos nos mesmos ao montar a estrutura.
PADRAO_CABECALHO = re.compile(
    r'<p[^>]*align="center"[^>]*>' + _ENTRE + r"<b>" + _ENTRE +
    r"(CAP[IÍ]TULO|(?:PRIMEIRA|SEGUNDA|TERCEIRA|QUARTA)\s+PARTE|PARTE\s+[IVX]+|[IVX]+\s+PARTE"
    r"|PRE[AÂ]MBULO|INTRODU[CÇ][AÃ]O|CONCLUS[AÃ]O|EP[IÍ]LOGO)"
    r"[^<]*</b>",
    re.I,
)

# Titulo do capitulo: proximo <p align="center"><b>...</b></p> logo depois do rotulo.
PADRAO_TITULO_CAB = re.compile(
    r'^' + _ENTRE + r'<p[^>]*align="center"[^>]*>' + _ENTRE + r"<b>" + _ENTRE + r"(.*?)</b>",
    re.I | re.S,
)

# Paragrafo numerado: inicio de <p ...> (com possiveis tags/espacos no meio)
# seguido do numero e ponto.
PADRAO_PARAGRAFO = re.compile(
    r"<p[^>]*>" + _ENTRE + r"(?:&nbsp;)*" + _ENTRE + r"(\d{1,3})\." + _ENTRE, re.I
)

# Subtitulo de secao dentro de um capitulo (negrito + italico, sem numero).
PADRAO_SUBTITULO = re.compile(
    r'<p[^>]*align="left"[^>]*>' + _ENTRE + r"<b>" + _ENTRE + r"<i>\s*(.*?)\s*</i>" + _ENTRE + r"</b>",
    re.I | re.S,
)

ROMANOS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]


def limpar(fragmento: str) -> str:
    """Remove tags, decodifica entidades, normaliza espacos."""
    texto = PADRAO_TAG.sub(" ", fragmento or "")
    texto = html_mod.unescape(texto)
    texto = texto.replace("\xa0", " ")
    return re.sub(r"\s+", " ", texto).strip()


@dataclass
class Paragrafo:
    numero: int
    texto: str
    subtitulo: str = ""  # subtitulo de secao imediatamente anterior, se houver


@dataclass
class Capitulo:
    titulo: str  # ex.: "Capítulo I — A Revelação em Si Mesma", ou "" se for proemio
    paragrafos: list[Paragrafo] = field(default_factory=list)


def extrair_paragrafos_sequenciais(html: str) -> list[tuple[int, int, int]]:
    """Retorna [(numero, pos_inicio, pos_fim_do_marcador)] apenas para a
    sequencia MONOTONICA 1..N a partir do primeiro paragrafo (o corpo do
    documento). Notas de rodape, que renumeram do 1, ficam de fora porque
    quebram a sequencia (quando o corpo ja passou do numero 1)."""
    candidatos = [(int(m.group(1)), m.start(), m.end()) for m in PADRAO_PARAGRAFO.finditer(html)]
    sequencia = []
    esperado = 1
    for numero, ini, fim in candidatos:
        if numero == esperado:
            sequencia.append((numero, ini, fim))
            esperado += 1
    return sequencia


def _classificar_rotulo(rotulo: str) -> str:
    rotulo = rotulo.upper()
    if "PARTE" in rotulo:
        return "parte"
    if "CAP" in rotulo:
        return "capitulo"
    if "INTROD" in rotulo:
        return "introducao"
    if "CONCLUS" in rotulo:
        return "conclusao"
    if "PRE" in rotulo:
        return "preambulo"
    if "EP" in rotulo:
        return "epilogo"
    return "secao"


NOME_TIPO = {
    "introducao": "Introdução",
    "conclusao": "Conclusão",
    "preambulo": "Preâmbulo",
    "epilogo": "Epílogo",
}


def estruturar_documento(html: str) -> list[Capitulo]:
    """Divide o documento em capitulos (ou um unico capitulo sem titulo, se
    o documento nao tiver subdivisoes) e, dentro de cada um, em paragrafos
    numerados com o subtitulo de secao mais proximo (se houver).

    A numeracao dos capitulos/partes e feita por NOS (contador sequencial),
    nao extraida do texto: a fonte (vatican.va) tem inconsistencias de
    formatacao (numeral romano ausente em pelo menos um capitulo de Dei
    Verbum) que tornariam a extracao do numeral fragil sem trazer beneficio
    real — a ordem de leitura ja garante a numeracao correta.
    """
    html = html_mod.unescape(html)
    paragrafos_seq = extrair_paragrafos_sequenciais(html)
    if not paragrafos_seq:
        return []

    cabecalhos_brutos = [(m.start(), m.end(), _classificar_rotulo(m.group(1))) for m in PADRAO_CABECALHO.finditer(html)]

    def titulo_para(pos_fim_rotulo: int, tipo: str, contador_parte: int, contador_cap: int) -> str:
        resto = html[pos_fim_rotulo : pos_fim_rotulo + 500]
        m = PADRAO_TITULO_CAB.match(resto)
        texto_extra = limpar(m.group(1)) if m else ""
        if tipo == "parte":
            base = f"Parte {ROMANOS[contador_parte - 1]}"
        elif tipo == "capitulo":
            base = f"Capítulo {ROMANOS[contador_cap - 1]}"
        else:
            base = NOME_TIPO.get(tipo, "Seção")
        return f"{base} — {texto_extra}" if texto_extra else base

    capitulos: list[Capitulo] = []
    cap_atual = Capitulo(titulo="")
    idx_cab = 0
    contador_parte = 0
    contador_cap = 0

    for i, (numero, ini, fim) in enumerate(paragrafos_seq):
        while idx_cab < len(cabecalhos_brutos) and cabecalhos_brutos[idx_cab][0] < ini:
            pos_ini, pos_fim, tipo = cabecalhos_brutos[idx_cab]
            if tipo == "parte":
                contador_parte += 1
                contador_cap = 0  # capitulos recomecam a contar dentro de cada parte
            elif tipo == "capitulo":
                contador_cap += 1
            if cap_atual.paragrafos or cap_atual.titulo:
                capitulos.append(cap_atual)
            cap_atual = Capitulo(titulo=titulo_para(pos_fim, tipo, contador_parte, contador_cap))
            idx_cab += 1

        inicio_busca = paragrafos_seq[i - 1][2] if i > 0 else 0
        trecho_entre = html[max(inicio_busca, ini - 600) : ini]
        subs = PADRAO_SUBTITULO.findall(trecho_entre)
        subtitulo = limpar(subs[-1]) if subs else ""

        fim_p = html.find("</p>", fim)
        texto = limpar(html[fim:fim_p]) if fim_p != -1 else limpar(html[fim : fim + 2000])

        cap_atual.paragrafos.append(Paragrafo(numero=numero, texto=texto, subtitulo=subtitulo))

    if cap_atual.paragrafos or cap_atual.titulo:
        capitulos.append(cap_atual)

    return capitulos
