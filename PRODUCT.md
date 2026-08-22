# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Gerador estático próprio em Python (~150 linhas, biblioteca padrão), sem Node/npm/dependências de build. Front matter + `templates/base.html` -> `dist/`. Ver README.md para o fluxo completo.

## Users

Dois públicos, servidos igualmente:

- Católicos em formação, buscando aprofundar a fé, a Escritura e a Tradição para estudo pessoal/devocional.
- Pessoas com dúvidas ou objeções à fé católica (protestantes, ateus, céticos) que buscam respostas rigorosas — uso apologético.

## Product Purpose

Disseminar a doutrina católica apostólica romana com rigor doutrinal e linguagem acessível, sempre em comunhão com o Magistério. Compila os estudos pessoais do autor e o conteúdo de obras católicas de referência (Catecismo, Suma Teológica, documentos conciliares, Escritura, Padres da Igreja) em páginas navegáveis e citáveis.

## Positioning

Não é resumo popular nem portal institucional: é uma compilação pessoal e rigorosa, onde cada afirmação remete a uma fonte primária (CIC, Escritura, Concílios, Suma Teológica) em vez de ficar em paráfrase solta. Difere de Wikipédia/Aleteia/Canção Nova por partir do estudo do próprio autor, não de redação jornalística ou verbete genérico.

## Operating Context

- Site estático publicado via GitHub Pages + GitHub Actions (deploy diário às 06:00 BRT, e a cada push em `main`).
- Conteúdo por página em `conteudo/*.html` (front matter + corpo), montado por `build.py` a partir de `templates/base.html`.
- Duas páginas têm dados dinâmicos coletados no build (All Day Vatican, Santo do Dia) e uma busca dado ao vivo no navegador do visitante (Liturgia Diária).
- Páginas longas (Catecismo, Suma Teológica, Concílios) embutem leitor de PDF navegável por parágrafo/questão.
- Migração de conteúdo de um vault Obsidian pessoal (`../Vida de Cristo/`) é manual e pontual — o site não se atualiza sozinho quando as notas mudam lá.

## Capabilities and Constraints

- Sem framework JS, sem build step além do script Python — qualquer trabalho de design deve permanecer HTML/CSS/JS simples, sem introduzir dependências novas de build.
- Páginas variam de completas (Catecismo, Profecias, Compêndio de Conceitos) a esqueleto com blocos `.placeholder` marcando conteúdo pendente — não inventar conteúdo doutrinal nesses placeholders.
- Licenciamento de PDFs de terceiros (Catecismo, futuros documentos conciliares) ainda não verificado antes de publicação ampla — pendência conhecida, não decisão de design.
- Revisão teológica do conteúdo ainda pendente antes de publicar amplamente.

## Brand Commitments

Nome fixado: "Catholic Day". Paleta, tipografia e tom atuais do site (ver `estatico/css/estilos.css` e `templates/base.html`) são a referência vigente — nenhuma restrição adicional além do que já está documentado no README.md.

## Evidence on Hand

- Conteúdo redigido pelo autor para Catecismo (CIC), Profecias e Compêndio de Conceitos, migrado do vault Obsidian pessoal.
- Documentos do Concílio Vaticano II baixados de vatican.va (16 documentos oficiais em português) e processados em PDFs próprios; resumos dos demais 20 concílios são redação original do autor.
- Sem depoimentos, estudos de caso ou métricas de terceiros — não fabricar esse tipo de prova social.

## Product Principles

- Toda afirmação doutrinal remete a uma fonte primária citável (CIC, Escritura, Concílio, Suma) — nunca paráfrase sem referência.
- Rigor doutrinal e comunhão com o Magistério antes de acessibilidade de linguagem — a linguagem simplifica a exposição, nunca a doutrina.
- Serve igualmente o estudo devocional e a pergunta cética — nenhuma página deve presumir só um dos dois públicos.
- Conteúdo incompleto é marcado como tal (`.placeholder`, "a preencher") em vez de fingir estar pronto.
- Zero dependências de build além de Python padrão — qualquer novo recurso de design deve caber nesse orçamento técnico.

## Accessibility & Inclusion

Nenhum requisito específico de acessibilidade foi estabelecido pelo usuário até o momento.
