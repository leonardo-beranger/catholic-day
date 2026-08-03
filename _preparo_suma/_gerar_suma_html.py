"""Gera conteudo/*.html para as 5 subpaginas da Suma Teologica, a partir de
_suma_estrutura.json (dados mecanicos: paginas/titulos, extraidos do indice
do PDF) + _suma_conteudo_<slug>.json (prosa escrita pelos agentes: resumos
de grupo e glosas por questao).

Uso: python _gerar_suma_html.py
Roda a partir de documentos/, escreve em ../conteudo/46x-suma-<slug>.html
"""
import json
import html
import re
from pathlib import Path

RAIZ = Path(__file__).parent
CONTEUDO = RAIZ.parent / "conteudo"

PARTES = [
    {
        "chave": "Prima Pars",
        "slug": "prima-pars",
        "arquivo": "46b-suma-prima-pars.html",
        "titulo_pagina": "Suma Teológica — Prima Pars",
        "titulo_menu": "Suma — Prima Pars",
        "subtitulo": "Deus, a Trindade, a criação e o governo divino.",
        "ordem": 461,
    },
    {
        "chave": "Pars Prima Secundae",
        "slug": "prima-secundae",
        "arquivo": "46c-suma-prima-secundae.html",
        "titulo_pagina": "Suma Teológica — Prima Secundae",
        "titulo_menu": "Suma — Prima Secundae",
        "subtitulo": "O homem a caminho de Deus: atos humanos, virtudes, lei e graça.",
        "ordem": 462,
    },
    {
        "chave": "Secunda Secundae",
        "slug": "secunda-secundae",
        "arquivo": "46d-suma-secunda-secundae.html",
        "titulo_pagina": "Suma Teológica — Secunda Secundae",
        "titulo_menu": "Suma — Secunda Secundae",
        "subtitulo": "As virtudes teologais e cardeais em espécie, e os estados de vida.",
        "ordem": 463,
    },
    {
        "chave": "Tertia Pars",
        "slug": "tertia-pars",
        "arquivo": "46e-suma-tertia-pars.html",
        "titulo_pagina": "Suma Teológica — Tertia Pars",
        "titulo_menu": "Suma — Tertia Pars",
        "subtitulo": "Cristo, o Verbo encarnado, e os sacramentos.",
        "ordem": 464,
    },
    {
        "chave": "Suplemento",
        "slug": "suplemento",
        "arquivo": "46f-suma-suplemento.html",
        "titulo_pagina": "Suma Teológica — Suplemento",
        "titulo_menu": "Suma — Suplemento",
        "subtitulo": "Penitência, unção, ordem, matrimônio e os Novíssimos.",
        "ordem": 465,
    },
]


def esc(s):
    return html.escape(str(s), quote=True)


def carregar_estrutura():
    return json.loads((RAIZ / "_suma_estrutura.json").read_text(encoding="utf-8"))


def indexar_questoes(estrutura, chave_parte):
    """Retorna dict num -> {titulo, pagina, artigos:[...]} para a parte."""
    idx = {}
    for tratado in estrutura["partes"][chave_parte]:
        for q in tratado["questoes"]:
            idx[q["num"]] = q
    return idx


def montar_artigos_html(artigos):
    if not artigos:
        return ""
    botoes = []
    for a in artigos:
        pagina = a["pagina"] + 1  # TOC costuma ficar 1 pagina atras do conteudo real
        rotulo = f'Art. {a["num"]} — {a["titulo"]}'
        botoes.append(
            f'<button type="button" class="cic-link-pdf suma-link-artigo" '
            f'data-pdf="/documentos/suma-teologica.pdf" data-pagina-pdf="{pagina}">{esc(rotulo)}</button>'
        )
    return '<div class="suma-artigos">' + "\n          ".join(botoes) + "</div>"


def montar_questao_html(slug_parte, q, glosa):
    num = q["num"]
    pagina = q["pagina"] + 1
    titulo = q["titulo"]
    texto = glosa or f'Ver o texto integral da Questão {num} no leitor.'
    artigos_html = montar_artigos_html(q.get("artigos", []))
    return f"""            <details class="cic-capitulo">
              <summary>Questão {num}: {esc(titulo)} <span class="cic-pagina-tag">pág. {pagina}</span></summary>
              <div class="cic-capitulo__corpo">
                <article class="cic-folha" id="suma-{slug_parte}-q{num}">
                  <div class="cic-folha__cabecalho">
                    <h4>Questão {num}</h4>
                  </div>
                  <p>{esc(texto)}</p>
                  <button type="button" class="cic-link-pdf" data-pdf="/documentos/suma-teologica.pdf" data-pagina-pdf="{pagina}">Abrir no leitor (página {pagina})</button>
                  {artigos_html}
                </article>
              </div>
            </details>"""


def montar_grupo_html(slug_parte, grupo, idx_questoes):
    titulo = grupo["titulo"]
    resumo = grupo.get("resumo", "")
    nums = grupo.get("questoes", [])
    primeira = idx_questoes.get(nums[0]) if nums else None
    pagina = (primeira["pagina"] + 1) if primeira else grupo.get("pagina", 0)
    blocos_q = []
    for n in nums:
        q = idx_questoes.get(n)
        if not q:
            continue
        blocos_q.append(montar_questao_html(slug_parte, q, grupo.get("glosas", {}).get(str(n))))
    return f"""      <details class="cic-seccao" open>
        <summary>{esc(titulo)} <span class="cic-pagina-tag">pág. {pagina}</span></summary>
        <div class="cic-seccao__corpo">
          <div class="painel"><p>{esc(resumo)}</p></div>
{chr(10).join(blocos_q)}
        </div>
      </details>"""


def gerar_pagina(parte_cfg, estrutura):
    chave = parte_cfg["chave"]
    slug_parte = parte_cfg["slug"]
    idx_questoes = indexar_questoes(estrutura, chave)

    caminho_conteudo = RAIZ / f"_suma_conteudo_{slug_parte}.json"
    if not caminho_conteudo.exists():
        print(f"  aviso: {caminho_conteudo.name} nao existe, pulando {parte_cfg['arquivo']}")
        return
    conteudo = json.loads(caminho_conteudo.read_text(encoding="utf-8"))
    grupos = conteudo.get("grupos", [])
    glosas_globais = conteudo.get("questoes", {})

    # injeta glosas globais nos grupos que nao trouxeram 'glosas' proprias
    for g in grupos:
        g.setdefault("glosas", {})
        for n in g.get("questoes", []):
            chave_n = str(n)
            if chave_n not in g["glosas"] and chave_n in glosas_globais:
                g["glosas"][chave_n] = glosas_globais[chave_n]

    primeira_pagina = estrutura["partes"][chave][0]["pagina"] + 1

    blocos = "\n".join(montar_grupo_html(slug_parte, g, idx_questoes) for g in grupos)

    total_q = sum(len(g.get("questoes", [])) for g in grupos)
    total_a = sum(len(idx_questoes[n].get("artigos", [])) for g in grupos for n in g.get("questoes", []) if n in idx_questoes)

    front = f"""---
slug: suma-{slug_parte}
titulo: {parte_cfg['titulo_pagina']}
menu: {parte_cfg['titulo_menu']}
ordem: {parte_cfg['ordem']}
scripts: concilios.js
subtitulo: {parte_cfg['subtitulo']}
descricao: {parte_cfg['titulo_pagina']} — {total_q} questões e {total_a} artigos, com leitor de PDF embutido apontando para a página exata (tradução de Alexandre Correia).
---"""

    corpo = f"""      <section class="secao">
        <p class="secao__intro">
          Esta página faz parte da série <a href="/ensinos-de-sao-tomas/">Ensinos de São Tomás</a>,
          reunindo, em redação própria, a estrutura e o conteúdo doutrinal da
          <strong>{esc(chave)}</strong> da <em>Suma Teológica</em>. Cada Questão abre, no leitor
          embutido, exatamente na página correspondente do PDF completo (tradução clássica de
          Alexandre Correia); os artigos individuais, quando disponíveis, também têm o seu
          próprio atalho.
        </p>

        <div class="leitor-cic" id="leitor-concilios" hidden>
          <div class="leitor-cic__barra">
            <span class="leitor-cic__titulo" id="leitor-concilios-titulo">Suma Teológica — página <span id="leitor-concilios-pagina">1</span></span>
            <div class="leitor-cic__acoes">
              <a id="leitor-concilios-baixar" class="botao-baixar" href="#" download>Baixar PDF</a>
              <button type="button" class="botao-fechar" id="leitor-concilios-fechar" aria-label="Fechar leitor">✕</button>
            </div>
          </div>
          <iframe id="leitor-concilios-iframe" class="leitor-cic__quadro" title="Leitor da Suma Teológica" loading="lazy"></iframe>
        </div>
      </section>

      <section class="cic-parte">
        <h2>{esc(chave.upper())} <button type="button" class="cic-link-pdf cic-link-pdf--parte" data-pdf="/documentos/suma-teologica.pdf" data-pagina-pdf="{primeira_pagina}">Abrir no leitor</button></h2>
{blocos}
      </section>

      <p class="fonte-nota">
        <strong>Sobre este resumo.</strong> Os títulos, a divisão em questões/artigos e os números
        de página vêm do índice do documento <code>documentos/suma-teologica.pdf</code>
        (tradução de Alexandre Correia). Os resumos de cada questão são redação própria deste
        site. Para o texto latino original, consulte
        <a href="https://www.corpusthomisticum.org/" target="_blank" rel="noopener">corpusthomisticum.org</a>.
      </p>
"""

    (CONTEUDO / parte_cfg["arquivo"]).write_text(front + "\n" + corpo, encoding="utf-8")
    print(f"  gerado {parte_cfg['arquivo']}  ({total_q} questoes, {total_a} artigos)")


def main():
    estrutura = carregar_estrutura()
    for cfg in PARTES:
        gerar_pagina(cfg, estrutura)


if __name__ == "__main__":
    main()
