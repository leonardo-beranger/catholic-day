#!/usr/bin/env python3
"""Gerador estatico do site (somente biblioteca padrao).

Uso:
    python build.py          # gera o site em dist/
    python build.py --servir # gera e sobe servidor local em http://localhost:8000
"""

from __future__ import annotations

import argparse
import http.server
import json
import os
import re
import shutil
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

RAIZ = Path(__file__).parent
CONTEUDO = RAIZ / "conteudo"
TEMPLATES = RAIZ / "templates"
ESTATICO = RAIZ / "estatico"
DADOS = RAIZ / "dados"
IMG = RAIZ / "img"
DOCUMENTOS = RAIZ / "documentos"
DIST = RAIZ / "dist"

SITE_NOME = "Catholic Day"

# O repositorio chama-se "catholic-day" (nao "leonardo-beranger.github.io"),
# entao o GitHub Pages serve o site em /catholic-day/, nao na raiz do
# dominio. BASE_PATH e' reescrito em todo caminho absoluto ("/estatico/...",
# "/img/...", os links do menu, os fetch() do JS) na hora de gerar o site.
#
# Localmente (`python build.py --servir`) o servidor serve tudo a partir da
# raiz, entao o padrao e' vazio; a Action do GitHub define BASE_PATH via
# variavel de ambiente antes de rodar o build. Se um dia for usado dominio
# proprio, e' so definir BASE_PATH="" no workflow (ou apagar a variavel).
BASE_PATH = os.environ.get("BASE_PATH", "").rstrip("/")

# URL publica completa, usada no sitemap.xml e em tags de SEO. Ajuste aqui se
# trocar de dominio.
SITE_URL = os.environ.get("SITE_URL", "https://leonardo-beranger.github.io/catholic-day").rstrip("/")

# Ordem e rotulo das secoes na navegacao.
SECOES = [
    ("formacao", "Informações de Fé"),
    ("vivencia", "Vivência"),
    ("noticias", "Notícias"),
]


@dataclass
class Pagina:
    slug: str
    titulo: str
    subtitulo: str = ""
    descricao: str = ""
    secao: str = ""
    ordem: int = 99
    menu: str = ""  # rotulo curto usado no menu; cai para `titulo`
    scripts: str = ""  # scripts extras da pagina, separados por virgula
    corpo: str = ""
    meta: dict = field(default_factory=dict)

    @property
    def tags_script(self) -> str:
        """<script> extras desta pagina, a partir do front matter `scripts`."""
        nomes = [s.strip() for s in self.scripts.split(",") if s.strip()]
        return "\n  ".join(
            f'<script src="/estatico/js/{nome}"></script>' for nome in nomes
        )

    @property
    def url(self) -> str:
        return "/" if self.slug == "index" else f"/{self.slug}/"

    @property
    def rotulo_menu(self) -> str:
        return self.menu or self.titulo

    @property
    def destino(self) -> Path:
        return DIST / "index.html" if self.slug == "index" else DIST / self.slug / "index.html"


def ler_front_matter(texto: str) -> tuple[dict, str]:
    """Le um front matter simples `chave: valor` delimitado por ---."""
    if not texto.startswith("---"):
        return {}, texto
    _, bloco, corpo = texto.split("---", 2)
    meta: dict[str, str] = {}
    for linha in bloco.strip().splitlines():
        if not linha.strip() or linha.lstrip().startswith("#"):
            continue
        chave, _, valor = linha.partition(":")
        meta[chave.strip()] = valor.strip()
    return meta, corpo.strip()


def carregar_paginas() -> list[Pagina]:
    paginas: list[Pagina] = []
    for arquivo in sorted(CONTEUDO.glob("*.html")):
        meta, corpo = ler_front_matter(arquivo.read_text(encoding="utf-8"))
        paginas.append(
            Pagina(
                slug=meta.get("slug", arquivo.stem),
                titulo=meta.get("titulo", arquivo.stem),
                subtitulo=meta.get("subtitulo", ""),
                descricao=meta.get("descricao", ""),
                secao=meta.get("secao", ""),
                ordem=int(meta.get("ordem", 99)),
                scripts=meta.get("scripts", ""),
                menu=meta.get("menu", ""),
                corpo=corpo,
                meta=meta,
            )
        )
    paginas.sort(key=lambda p: (p.ordem, p.titulo))
    return paginas


def montar_menu(paginas: list[Pagina], atual: Pagina) -> str:
    """Menu agrupado por secao (usado no header e no rodape).

    Paginas com front matter `pai: <slug>` nao aparecem como item proprio do
    menu — viram um submenu suspenso sob o link da pagina-mae (ex.: as 5
    partes da Suma Teologica aparecem sob "Ensinos de Sao Tomas"). Uma pagina
    sem filhos nao ganha submenu nenhum.
    """
    filhos_por_pai: dict[str, list[Pagina]] = {}
    for p in paginas:
        pai = p.meta.get("pai")
        if pai:
            filhos_por_pai.setdefault(pai, []).append(p)

    def montar_item(p: Pagina) -> str:
        ativo = ' aria-current="page"' if p.slug == atual.slug else ""
        filhos = filhos_por_pai.get(p.slug, [])
        if not filhos:
            return f'            <li><a href="{p.url}"{ativo}>{p.rotulo_menu}</a></li>'
        sublinks = "\n".join(
            '                <li><a href="{url}"{ativo}>{rotulo}</a></li>'.format(
                url=f.url,
                rotulo=f.rotulo_menu,
                ativo=' aria-current="page"' if f.slug == atual.slug else "",
            )
            for f in filhos
        )
        return (
            f'            <li class="menu-item menu-item--tem-submenu">\n'
            f'              <a href="{p.url}"{ativo}>{p.rotulo_menu}</a>\n'
            f'              <ul class="submenu">\n{sublinks}\n              </ul>\n'
            f"            </li>"
        )

    partes: list[str] = []
    for chave, rotulo in SECOES:
        itens = [p for p in paginas if p.secao == chave]
        if not itens:
            continue
        links = "\n".join(montar_item(p) for p in itens)
        partes.append(
            f'        <div class="menu-grupo">\n'
            f'          <p class="menu-grupo__titulo">{rotulo}</p>\n'
            f"          <ul>\n{links}\n          </ul>\n"
            f"        </div>"
        )
    return "\n".join(partes)


def substituir(template: str, valores: dict[str, str]) -> str:
    def troca(m: re.Match[str]) -> str:
        return valores.get(m.group(1).strip(), "")

    return re.sub(r"\{\{\s*([\w_]+)\s*\}\}", troca, template)


def limpar_dist(tentativas: int = 5) -> None:
    """Remove dist/ com tolerancia a locks do OneDrive/antivirus."""

    def ao_falhar(func, caminho, _exc):
        # Arquivo somente-leitura: tira o atributo e tenta de novo.
        try:
            Path(caminho).chmod(0o777)
            func(caminho)
        except OSError:
            pass

    for tentativa in range(tentativas):
        if not DIST.exists():
            return
        shutil.rmtree(DIST, onexc=ao_falhar)
        if not DIST.exists():
            return
        time.sleep(0.4 * (tentativa + 1))

    if DIST.exists():
        print("  aviso: dist/ nao pôde ser removida (arquivo em uso); sobrescrevendo")


_PADRAO_CAMINHO_ABSOLUTO = re.compile(r'(href|src|action|data-pdf)="/(?!/)')


def prefixar_base_path(html: str) -> str:
    """Prefixa BASE_PATH em todo href/src/action que comeca com uma unica
    barra (caminho absoluto do site). Nao toca em "//" (protocol-relative,
    aponta para outro dominio) nem em URLs http(s) completas."""
    if not BASE_PATH:
        return html
    return _PADRAO_CAMINHO_ABSOLUTO.sub(rf'\1="{BASE_PATH}/', html)


def gerar() -> None:
    limpar_dist()
    DIST.mkdir(parents=True, exist_ok=True)

    base = (TEMPLATES / "base.html").read_text(encoding="utf-8")
    paginas = carregar_paginas()

    for pagina in paginas:
        html = substituir(
            base,
            {
                "titulo": pagina.titulo,
                "titulo_documento": (
                    SITE_NOME
                    if pagina.slug == "index"
                    else f"{pagina.titulo} — {SITE_NOME}"
                ),
                "subtitulo": pagina.subtitulo,
                "descricao": pagina.descricao or pagina.subtitulo,
                "slug": pagina.slug,
                "menu": montar_menu(paginas, pagina),
                "conteudo": pagina.corpo,
                "scripts": pagina.tags_script,
                "classe_pagina": f"pagina-{pagina.slug}",
                "base_path": BASE_PATH,
                "url_canonica": f"{SITE_URL}{pagina.url}",
            },
        )
        html = prefixar_base_path(html)
        pagina.destino.parent.mkdir(parents=True, exist_ok=True)
        pagina.destino.write_text(html, encoding="utf-8")
        print(f"  gerado  {pagina.destino.relative_to(RAIZ)}")

    if ESTATICO.exists():
        shutil.copytree(ESTATICO, DIST / "estatico", dirs_exist_ok=True)
        print("  copiado estatico/")
    if DADOS.exists():
        shutil.copytree(DADOS, DIST / "dados", dirs_exist_ok=True)
        print("  copiado dados/")
    if IMG.exists():
        shutil.copytree(IMG, DIST / "img", dirs_exist_ok=True)
        print("  copiado img/")
    if DOCUMENTOS.exists():
        shutil.copytree(
            DOCUMENTOS, DIST / "documentos", dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("_bruto"),
        )
        print("  copiado documentos/ (sem _bruto/, materia-prima de preparacao)")

    # Sinaliza ao GitHub Pages para nao processar com Jekyll.
    (DIST / ".nojekyll").write_text("", encoding="utf-8")

    # Arquivos de verificacao de propriedade (Google Search Console, Bing
    # Webmaster Tools etc.) precisam ficar na RAIZ do site publicado, com o
    # conteudo intacto — nao passam pelo motor de paginas. Qualquer
    # "*-verification*.html" ou "google*.html"/"BingSiteAuth.xml" solto na
    # raiz do projeto e copiado como esta para dist/.
    padroes_verificacao = ["google*.html", "*-verification*.html", "BingSiteAuth.xml", "yandex_*.html"]
    for padrao in padroes_verificacao:
        for arquivo in RAIZ.glob(padrao):
            shutil.copy2(arquivo, DIST / arquivo.name)
            print(f"  copiado {arquivo.name} (verificacao de propriedade)")

    indice = [
        {"slug": p.slug, "titulo": p.titulo, "url": p.url, "secao": p.secao}
        for p in paginas
    ]
    (DIST / "dados" / "paginas.json").write_text(
        json.dumps(indice, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    gerar_seo(paginas)

    print(f"\n{len(paginas)} páginas geradas em dist/")


def gerar_seo(paginas: list[Pagina]) -> None:
    """Gera sitemap.xml e robots.txt para facilitar a indexacao por
    motores de busca (Google, Bing, etc.)."""
    hoje = time.strftime("%Y-%m-%d")
    # SITE_URL ja inclui o BASE_PATH quando aponta para um projeto do GitHub
    # Pages (ex.: ".../catholic-day"); nao acrescentar BASE_PATH de novo aqui.
    urls = "\n".join(
        f"  <url>\n"
        f"    <loc>{SITE_URL}{p.url}</loc>\n"
        f"    <lastmod>{hoje}</lastmod>\n"
        f"  </url>"
        for p in paginas
    )
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n"
        "</urlset>\n"
    )
    (DIST / "sitemap.xml").write_text(sitemap, encoding="utf-8")

    robots = (
        "User-agent: *\n"
        "Allow: /\n"
        f"Sitemap: {SITE_URL}/sitemap.xml\n"
    )
    (DIST / "robots.txt").write_text(robots, encoding="utf-8")
    print("  gerado  dist/sitemap.xml e dist/robots.txt")


def servir(porta: int = 8000) -> None:
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(DIST), **kwargs)

        def end_headers(self):
            # Evita cache durante o desenvolvimento.
            self.send_header("Cache-Control", "no-store")
            super().end_headers()

        def log_message(self, fmt, *args):  # menos ruido no console
            pass

    # ThreadingHTTPServer: sem isso, CSS/JS/fontes ficam em fila num unico thread.
    with http.server.ThreadingHTTPServer(("", porta), Handler) as httpd:
        print(f"Servindo dist/ em http://localhost:{porta} (Ctrl+C para parar)")
        httpd.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gera o site estatico.")
    parser.add_argument("--servir", action="store_true", help="sobe servidor local apos gerar")
    parser.add_argument("--porta", type=int, default=8000)
    parser.add_argument(
        "--noticias",
        action="store_true",
        help="roda o coletor de noticias antes de gerar (rede necessaria)",
    )
    parser.add_argument(
        "--santo",
        action="store_true",
        help="roda o coletor do santo do dia antes de gerar (rede necessaria)",
    )
    parser.add_argument(
        "--atualizar",
        action="store_true",
        help="equivale a --noticias --santo",
    )
    args = parser.parse_args()

    def rodar_coletor(nome_script: str, rotulo: str) -> None:
        import subprocess

        print(f"Coletando {rotulo}...\n")
        resultado = subprocess.run(
            [sys.executable, str(RAIZ / nome_script)], cwd=str(RAIZ)
        )
        if resultado.returncode != 0:
            print(f"\nAviso: o coletor de {rotulo} falhou; mantendo os dados atuais.\n")
        print()

    if args.noticias or args.atualizar:
        rodar_coletor("coletar_noticias.py", "noticias")
    if args.santo or args.atualizar:
        rodar_coletor("coletar_santo.py", "santo do dia")

    gerar()
    if args.servir:
        servir(args.porta)
