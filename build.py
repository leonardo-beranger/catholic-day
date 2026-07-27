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
    """Menu agrupado por secao (usado no header e no rodape)."""
    partes: list[str] = []
    for chave, rotulo in SECOES:
        itens = [p for p in paginas if p.secao == chave]
        if not itens:
            continue
        links = "\n".join(
            '            <li><a href="{url}"{ativo}>{rotulo}</a></li>'.format(
                url=p.url,
                rotulo=p.rotulo_menu,
                ativo=' aria-current="page"' if p.slug == atual.slug else "",
            )
            for p in itens
        )
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
            },
        )
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

    indice = [
        {"slug": p.slug, "titulo": p.titulo, "url": p.url, "secao": p.secao}
        for p in paginas
    ]
    (DIST / "dados" / "paginas.json").write_text(
        json.dumps(indice, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\n{len(paginas)} páginas geradas em dist/")


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
