---
name: Catholic Day
description: Apologética católica e vivência da fé — Vida de Cristo, profecias, patrística, Catecismo e liturgia.
colors:
  bordo-profundo: "#6d1f2b"
  bordo-claro: "#8f3140"
  ouro-envelhecido: "#a9852f"
  ouro-texto: "#83641b"
  verde-musgo: "#3f6350"
  violeta-acinzentado: "#5c4571"
  fundo-pergaminho: "#fdfaf4"
  fundo-alt: "#f6f0e4"
  superficie: "#ffffff"
  borda: "#e4dac4"
  texto: "#241f1c"
  texto-suave: "#5f574e"
typography:
  display:
    fontFamily: "EB Garamond, Georgia, Times New Roman, serif"
    fontSize: "clamp(2rem, 4.5vw, 3rem)"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "-.01em"
  headline:
    fontFamily: "EB Garamond, Georgia, Times New Roman, serif"
    fontSize: "clamp(1.5rem, 3vw, 2rem)"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "-.01em"
  photo-headline:
    fontFamily: "EB Garamond, Georgia, Times New Roman, serif"
    fontSize: "clamp(1.25rem, 2.2vw, 2.1rem)"
    fontWeight: 600
    lineHeight: 1.2
  subhead:
    fontFamily: "EB Garamond, Georgia, Times New Roman, serif"
    fontSize: "1.2rem"
    fontWeight: 400
    lineHeight: 1.25
  title:
    fontFamily: "EB Garamond, Georgia, Times New Roman, serif"
    fontSize: "1.25rem"
    fontWeight: 600
    lineHeight: 1.2
  body:
    fontFamily: "Libre Franklin, -apple-system, Segoe UI, Roboto, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.65
  body-small:
    fontFamily: "Libre Franklin, -apple-system, Segoe UI, Roboto, sans-serif"
    fontSize: ".9rem"
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: "Libre Franklin, -apple-system, Segoe UI, Roboto, sans-serif"
    fontSize: ".72rem"
    fontWeight: 600
    letterSpacing: ".08em"
rounded:
  sm: "3px"
  md: "10px"
  pill: "999px"
  circle: "50%"
spacing:
  xs: ".4rem"
  sm: ".75rem"
  md: "1.25rem"
  lg: "1.75rem"
  xl: "3rem"
components:
  button-primary:
    backgroundColor: "{colors.bordo-profundo}"
    textColor: "#ffffff"
    rounded: "{rounded.pill}"
    padding: ".35rem .9rem"
  button-primary-hover:
    backgroundColor: "{colors.bordo-claro}"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.bordo-profundo}"
    rounded: "{rounded.pill}"
    padding: ".45rem 1.1rem"
  button-ghost-hover:
    backgroundColor: "{colors.bordo-profundo}"
    textColor: "#ffffff"
  card:
    backgroundColor: "{colors.superficie}"
    rounded: "{rounded.md}"
    padding: "1.5rem"
  badge-scripture:
    backgroundColor: "{colors.superficie}"
    textColor: "{colors.texto-suave}"
    rounded: "{rounded.pill}"
    padding: ".1rem .5rem"
---

# Design System: Catholic Day

## Overview

**Creative North Star: "Lumen Fidei"**

O próprio código já batiza o sistema — "Lumen Fidei — folha de estilos base", paleta inspirada nas cores litúrgicas: bordô, ouro velho e pergaminho. É a luz da fé mediada por um objeto quase físico: fundo cor de pergaminho, tipografia serifada nos títulos, cores litúrgicas usadas com parcimônia para marcar tempo e sentido, não para decorar.

O clima é sóbrio e litúrgico, mas com um tom deliberadamente descontraído — não é um site que imita um missal solene do início ao fim; é mais perto de um caderno de estudo bem cuidado, sério no conteúdo sem ser hermético na forma. Longas leituras (Catecismo, Suma, Concílios) recebem tratamento editorial: hierarquia de texto discreta, cor como acento raro, nunca como ruído.

Nenhuma referência visual de rejeição foi confirmada além do que decorre do próprio clima escolhido: nada de estética "app de tech" genérica, gradientes ou efeitos chamativos que compitam com o texto.

**Key Characteristics:**
- Fundo cor de pergaminho (`#fdfaf4`), nunca branco puro, exceto nas superfícies elevadas (cards, fichas).
- Bordô como cor de ação e identidade; ouro como acento de destaque textual (etiquetas, ícones); verde e violeta reservados a marcações litúrgicas específicas.
- Serifa (EB Garamond) em títulos, sans-serif (Libre Franklin) no corpo — divisão clássica de leitura longa.
- Componentes discretos e sólidos: bordas finas, cantos moderadamente arredondados, sem gradiente nem glow.
- Modo escuro definido via `prefers-color-scheme`, com a mesma estrutura de papéis (bordô vira um vermelho mais claro para legibilidade sobre fundo escuro).

## Colors

Paleta de baixa saturação, papel de fundo quente, com quatro acentos que carregam significado litúrgico e são usados com parcimônia.

### Primary
- **Bordô Profundo** (`#6d1f2b`, claro: `#8f3140`): cor de ação e identidade — links, botões primários, títulos de ficha, cabeçalhos de destaque. É a cor mais usada de propósito, ligada no código à Paixão/mártires.

### Secondary
- **Ouro Envelhecido** (`#a9852f`): acento não-textual — bordas de destaque, pontos de selo, ícones/setas decorativas (▸, ▾, ✎). Exige só 3:1 (contraste de componente não-textual), que já cumpre.
- **Ouro Texto** (`#83641b`): mesma família, escurecida para uso em texto real — etiquetas (`cartao__etiqueta`, `menu-grupo__titulo`), referências (`ficha__ref`, `leitura__ref`, `cic-faixa`), rótulos de oração/tempo litúrgico. Criado para corrigir uma falha de contraste (3.3:1) encontrada em audit — ver Named Rule abaixo.

### Tertiary
- **Verde Musgo** (`#3f6350`) e **Violeta Acinzentado** (`#5c4571`): reservados a marcações litúrgicas específicas (selos de tempo comum / advento-quaresma) e a blocos de objeção/debate dentro de fichas. Não são cores de uso geral — aparecem só onde o sentido litúrgico ou argumentativo pede.

### Neutral
- **Pergaminho** (`#fdfaf4`): fundo de página.
- **Pergaminho Alt** (`#f6f0e4`): fundo de painel/realce (`.painel`, `.ficha__objecao`, cabeçalho do leitor de PDF).
- **Branco Puro** (`#ffffff`): superfície elevada — cards, fichas, cabeçalho do menu suspenso.
- **Bege-Borda** (`#e4dac4`): toda borda de 1px do sistema.
- **Tinta** (`#241f1c`): texto principal.
- **Tinta Suave** (`#5f574e`): texto secundário, legendas, metadados.

### Named Rules
**A Regra da Parcimônia Litúrgica.** Verde e violeta nunca são cor de fundo nem de texto corrido — só aparecem em selos, bordas de destaque e ícones, marcando um tempo ou um tipo de conteúdo específico.

**A Regra do Ouro Duplo.** `--cor-ouro` (`#a9852f`) é só para borda/ponto/ícone decorativo (exige apenas 3:1). Qualquer `color` aplicado a texto real usa `--cor-ouro-texto` (`#83641b`) — nunca o tom claro, que reprova WCAG AA em texto pequeno.

## Typography

**Display/Headline/Title Font:** EB Garamond (com Georgia, Times New Roman, serif)
**Body/Label Font:** Libre Franklin (com -apple-system, Segoe UI, Roboto, sans-serif)

**Character:** serifa clássica para títulos dá peso editorial e um tom quase de livro impresso; sans-serif neutra no corpo mantém páginas longas (Catecismo, Suma) legíveis sem cansar — a dupla separa claramente "isto é um título/marco" de "isto é para ler com atenção".

### Hierarchy
- **Display** (600, `clamp(2rem, 4.5vw, 3rem)`, 1.2): `h1`, título de página.
- **Headline** (600, `clamp(1.5rem, 3vw, 2rem)`, 1.2): `h2`, título de seção.
- **Photo Headline** (600, `clamp(1.25rem, 2.2vw, 2.1rem)`, 1.2): título sobre imagem (nome do santo em `.santo__nome`, título de card do carrossel de notícias) — mesma família de escala fluida do Headline, com endpoints próprios por caber num cartão menor.
- **Subhead** (400–600, 1.15–1.35rem, 1.2–1.3): subtítulo de página (`.pagina-cabecalho__subtitulo`), nome da marca no cabeçalho, título de seção recolhível do leitor do CIC (`.cic-seccao > summary`) — usa a família serifada quando é subtítulo/marca, sans quando é controle de interface.
- **Title** (600, 1.25rem, 1.2): `h3`, título de card/ficha.
- **Body** (400, 1rem, 1.65): parágrafo corrido; linha alta (1.65) sustenta leitura longa.
- **Body Small** (400, .82–.95rem, 1.4–1.7): variante compacta do corpo — legenda de ficha, nota de rodapé de citação, texto de card, resumo de tabela. É a faixa mais usada depois do Body: qualquer texto secundário que precise de menos peso visual sem virar rótulo.
- **Label** (500–600, .68–.86rem, letter-spacing 0–.09em, versalete quando é categoria): etiquetas de categoria, cabeçalhos de tabela, selo bíblico, referência de ficha/leitura, período de linha do tempo. A faixa mais ampla do sistema — cobre desde a pastilha bíblica (.78rem) até o rótulo de categoria em versalete (.68rem).
- **Glifo grande** (400, 3.5–4rem, sem hierarquia tipográfica): a cruz "✝" que preenche a moldura de foto antes da imagem carregar (`.santo__moldura::before`, `.carrossel__moldura::after`) — tamanho de ilustração de fundo, não de texto; não faz parte da escala de leitura.

### Named Rules
**A Regra do Livro-Caderno.** Serifa é reservada a título e citação (`.citacao` também usa `--fonte-titulo`); todo o resto — corpo, rótulo, interface — fica em sans-serif. Misturar as duas fora desse padrão quebra a leitura editorial.

## Layout

Container único (`--largura: 1120px`), centralizado com padding lateral de `1.25rem`. Seções (`.secao`) empilham verticalmente com `padding: 3rem 0` e um filete de 1px (`--cor-borda`) separando-as — sem cartões de seção, o espaço em branco e a borda superior fazem a divisão.

Grades usam `repeat(auto-fit, minmax(260px, 1fr))` (cards) ou `auto-fill, minmax(300px, 1fr)` (calendário), com `gap: 1.25rem` — sempre responsivo por conteúdo, nunca breakpoint fixo por dispositivo. Abaixo de `1060px` o menu de cabeçalho colapsa num painel vertical com botão hambúrguer.

Ritmo de espaçamento gira em torno de `.4rem` (entre elementos inline, ex. selos), `.75rem`–`1.25rem` (padding interno de componente) e `1.25rem`–`1.75rem` (gap entre cards/fichas).

## Elevation & Depth

O sistema usa uma sombra dupla sutil (`--sombra: 0 1px 2px rgba(36,31,28,.06), 0 8px 24px rgba(36,31,28,.06)`) em quase toda superfície elevada — cards, fichas, painéis do calendário, leitor de PDF. Não é uma decisão de profundidade deliberada até agora (o próprio autor confirma que "não foi pensado, pode revisar"): documentado aqui como o estado atual, não como regra a preservar sem questionamento.

### Shadow Vocabulary
- **Sombra padrão** (`0 1px 2px rgba(36,31,28,.06), 0 8px 24px rgba(36,31,28,.06)`; no escuro, `0 1px 2px rgba(0,0,0,.4), 0 8px 24px rgba(0,0,0,.3)`): aplicada uniformemente a card, ficha, painel de calendário, leitor de PDF, submenu — não há hoje uma escala de elevação por importância, é um único valor reaproveitado.

## Shapes

Raio padrão `10px` (`--raio`) em quase todo container (card, ficha, painel, input, submenu). Elementos de ação/etiqueta (botões, selos, badges bíblicos) usam `999px` (pílula total). Avatares e ícones circulares (marca, botão fechar, spinner) usam `50%`. Bordas são sempre 1px sólida em `--cor-borda`, exceto realces de sentido (citação, objeção, resumo do calendário) que usam borda esquerda de 3px numa cor de acento.

## Components

Discretos e sólidos: bordas finas, cantos moderadamente arredondados, sem gradiente nem glow — o conteúdo é sempre protagonista.

### Buttons
- **Shape:** pílula (`border-radius: 999px`) em toda ação (`.botao-acao`, `.botao-baixar`, link de PDF por parte).
- **Primary (`.botao-baixar`):** fundo bordô (`#6d1f2b`), texto branco, padding `.35rem .9rem`.
- **Ghost (`.botao-acao`):** transparente, borda 1px bordô, texto bordô, padding `.45rem 1.1rem`.
- **Hover:** ambos invertem para preenchimento sólido — ghost vira fundo bordô + texto branco; primary escurece para o bordô claro (`#8f3140`). Transição `160ms ease` em toda a interface (`--transicao`).
- **Ícone circular (`.botao-fechar`):** 28px, borda 1px, hover troca borda/texto para bordô.

### Chips / Selos
- **Selo litúrgico (`.selo`):** pílula, borda 1px `--cor-borda`, ponto colorido (`::before`) com `currentColor` — verde/violeta/ouro/bordô conforme o tempo.
- **Selo bíblico (`.selo-biblia`):** pílula pequena, fundo superfície, borda 1px, texto suave — usado em referência de cumprimento de profecia.

### Cards / Containers
- **Corner Style:** `10px` (`--raio`).
- **Background:** branco puro (`--cor-superficie`) sobre fundo pergaminho — é o contraste que sinaliza "conteúdo elevado".
- **Shadow Strategy:** ver Elevation & Depth — sombra dupla sutil uniforme.
- **Border:** 1px sólida `--cor-borda`; ficha e painel de citação adicionam borda esquerda de 3px numa cor de acento (ouro por padrão, bordô em ficha longa, violeta em objeção).
- **Internal Padding:** `1.5rem`–`1.75rem` (card, ficha); `1.75rem` (painel).

### Inputs / Fields
- **Style:** borda 1px `--cor-borda`, fundo `--cor-superficie`, raio `10px`, fonte Libre Franklin.
- **Focus:** anel dourado (`outline: 2px solid var(--cor-ouro)`, offset 2px) — aplicado globalmente via `:focus-visible`, não por componente.

### Navigation
- **Estilo:** links sem fundo, sublinhado de 2px que aparece no hover (dourado) ou na página atual (bordô).
- **Submenu suspenso:** aparece sob itens de menu com subpáginas (seta dourada `▾`), painel branco com sombra padrão, sem gap entre o link-pai e o painel — a área de hover é contínua entre o item de menu e o submenu.
- **Mobile (`<1060px`):** menu colapsa em painel vertical; submenu perde posicionamento absoluto e vira lista aninhada com borda esquerda, sempre visível (sem hover em toque).

### Quadro Expansível ("Tema") — signature component
`<details>`/`<summary>` estilizado como quadrado clicável: cabeçalho com etiqueta + título + seta que gira 180° ao abrir; conteúdo (fichas) revelado nativamente pelo `<details>`, sem JavaScript. Usado para agrupar profecias por categoria — expande a "avó" de conteúdo em vez de navegar para outra página.

## Do's and Don'ts

### Do:
- **Do** usar bordô como cor de ação/identidade e ouro como acento textual raro — são os dois únicos acentos de uso amplo.
- **Do** manter serifa (EB Garamond) restrita a título e citação; tudo o mais em Libre Franklin.
- **Do** usar `--raio: 10px` em containers e `999px` (pílula) em toda ação/etiqueta — não introduzir uma terceira escala de raio.
- **Do** manter transições em `160ms ease` (`--transicao`) para hover/estado — consistente em todo o sistema.
- **Do** garantir hover contínuo em qualquer menu suspenso futuro (sem gap entre gatilho e painel), como corrigido no submenu do cabeçalho.

### Don't:
- **Don't** usar verde ou violeta como cor de fundo ou de texto corrido — são reservados a selo litúrgico e bloco de objeção.
- **Don't** introduzir gradientes, glow ou sombra dramática — a sombra do sistema é deliberadamente quase imperceptível.
- **Don't** adicionar dependência de build (framework JS, bundler) para atingir um efeito visual — o orçamento técnico do projeto é HTML/CSS/JS simples servido por um gerador Python sem dependências.
