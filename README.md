# Catholic Day — site de apologética e formação católica

Site estático gerado por um script Python de ~150 linhas (somente biblioteca padrão).
Sem Node, sem npm, sem dependências para instalar.

## Como rodar

```bash
python build.py --servir
```

Gera `dist/` e abre um servidor local em <http://localhost:8000>.
Para apenas gerar, sem servir: `python build.py`.

Para atualizar as notícias do All Day Vatican e gerar numa só passagem
(precisa de rede):

```bash
python build.py --noticias
```

Para atualizar o Santo do Dia:

```bash
python build.py --santo
```

Para atualizar os dois de uma vez: `python build.py --atualizar`.

## Estrutura

```
site/
├── build.py                # gerador: front matter + template -> dist/
├── coletar_noticias.py     # busca os feeds RSS -> dados/noticias.json
├── coletar_santo.py        # raspa santo.cancaonova.com -> dados/santos.json
├── baixar_vaticano_ii.py   # baixa os 16 docs do Vaticano II (vatican.va) -> _bruto/
├── gerar_pdfs_vaticano_ii.py  # HTML -> PDF proprio (reportlab) + vaticano-ii.json
├── gerar_html_concilios.py    # gera a arvore HTML do Vaticano II
├── gerar_pagina_concilios.py  # monta conteudo/35-concilios.html final
├── _lib_concilios.py          # parser de capitulos/paragrafos (Vaticano II)
├── _resumos_vaticano_ii.py    # resumos originais, por (documento, capitulo)
├── _outros_concilios.py       # os outros 20 concilios: resumo + citacao latina + DH
├── templates/
│   └── base.html           # layout único (cabeçalho, menu, rodapé)
├── conteudo/               # uma página por arquivo, prefixo numérico = ordem
│   ├── 00-index.html
│   ├── 10-vida-de-cristo.html
│   ├── 20-profecias.html
│   ├── 30-patristica.html
│   ├── 35-concilios.html
│   ├── 40-catecismo.html
│   ├── 45-compendio-de-conceitos.html
│   ├── 50-liturgia-diaria.html
│   ├── 60-santo-do-dia.html
│   ├── 70-calendario-liturgico.html
│   └── 80-all-day-vatican.html
├── estatico/
│   ├── css/estilos.css
│   ├── js/principal.js      # menu, leitor do CIC, data de hoje (todas as páginas)
│   ├── js/liturgia.js       # só na Liturgia Diária (via front matter `scripts:`)
│   ├── js/noticias.js       # só no All Day Vatican (carrossel)
│   ├── js/santo.js          # só no Santo do Dia
│   └── js/concilios.js      # só nos Concílios (leitor genérico, multi-PDF)
├── img/
│   ├── logo.png                    # logotipo e favicon
│   ├── Jesus_Cristo.png            # foto de referência (fundo original)
│   └── Jesus_Cristo_recortado.png  # gerado com rembg — fundo removido, é o usado no site
├── documentos/
│   ├── catecismo-cic.pdf    # CIC (edição Loyola) — fonte da página Catecismo
│   └── concilios/
│       ├── _bruto/          # HTML baixado de vatican.va (não vai para dist/)
│       ├── vaticano-ii/     # 16 PDFs gerados (um por documento)
│       └── vaticano-ii.json # estrutura: capítulos, §§, página de cada um
├── dados/                  # JSON com o conteúdo dinâmico (esqueletos)
│   ├── liturgia.json
│   ├── santos.json
│   ├── calendario.json
│   └── noticias.json
└── dist/                   # saída gerada — não editar, não versionar
```

## Como adicionar uma página

Crie um arquivo em `conteudo/` com front matter e o corpo em HTML:

```html
---
slug: nome-na-url
titulo: Título da Página
menu: Rótulo curto
secao: formacao        # formacao (Informações de Fé) | vivencia | noticias
ordem: 45              # posição no menu
subtitulo: Uma linha de apresentação.
descricao: Texto usado na meta description.
scripts: exemplo.js     # opcional: JS extra só desta página (separar por vírgula)
---
<section class="secao">
  ...
</section>
```

O menu do cabeçalho e do rodapé é montado automaticamente a partir desses campos.

## Classes CSS úteis

| Classe | Uso |
| --- | --- |
| `.secao` | bloco de conteúdo com separador |
| `.grade` + `.cartao` | grade responsiva de cartões |
| `.linha-tempo` | lista cronológica com marcadores |
| `.tabela-rolagem` + `table` | tabela com rolagem horizontal no mobile |
| `.painel` | caixa destacada (ex.: "hoje") |
| `.placeholder` | marca conteúdo ainda não escrito |
| `.ficha` (+ `--longa`, `--termo`) | bloco de conteúdo: profecia, conceito, termo |
| `.ficha__objecao` | ponto de debate / objeção dentro de uma ficha |
| `.citacao` | citação bíblica ou magisterial com fonte |
| `.selo-biblia` | pastilha de referência bíblica |
| `.selo selo--verde/violeta/branco/vermelho` | cor litúrgica |

## Situação atual

Páginas **com conteúdo redigido**: Catecismo (CIC), Profecias, Compêndio de
Conceitos. As demais ainda são esqueleto, com blocos `.placeholder` marcando o
que falta escrever.

O conteúdo de Profecias e do Compêndio veio do vault Obsidian em
`../Vida de Cristo/` (pastas `Profecias/`, `Conceitos/`, `Palavras-chave/`).
Ao atualizar as notas lá, o site **não** se atualiza sozinho — a migração foi
manual e pontual.

### Vida de Cristo — imagem recortada com rembg + tilt 3D em CSS/JS

`Jesus_Cristo_recortado.png` foi gerado a partir de `Jesus_Cristo.png` com a
biblioteca `rembg` (remoção de fundo por segmentação, modelo u2net), depois
recortado para a caixa delimitadora do conteúdo opaco. Script usado (não faz
parte do site, é uma ferramenta pontual):

```bash
pip install rembg onnxruntime
python -c "from rembg import remove; open('img/Jesus_Cristo_recortado.png','wb').write(remove(open('img/Jesus_Cristo.png','rb').read()))"
```

O efeito "saindo da tela" é CSS + JS, sem nenhuma biblioteca 3D:
- Um brilho radial (`::before`) menor que a imagem simula um "portal" atrás
  da figura, para que ela pareça atravessá-lo, não apenas flutuar na frente.
- `principal.js` aplica um tilt (`rotateX`/`rotateY` via `perspective`) que
  segue o cursor do mouse e, em celular, a inclinação do giroscópio
  (`deviceorientation`, com o pedido de permissão exigido pelo iOS). Respeita
  `prefers-reduced-motion`.
- Sombra dupla (`drop-shadow`) reforça a profundidade.

### Concílios — Vaticano II com documentos completos + os outros 20 com Latim/DH

**Vaticano II (21º concílio).** Diferente do Catecismo (cujo PDF já vinha
pronto e precisou de heurística para mapear § → página), aqui o PDF **não
existia** — foi gerado do zero:

1. `baixar_vaticano_ii.py` baixa os 16 documentos oficiais em português de
   `vatican.va` (código de idioma `po`, não `pt` — é assim mesmo no site do
   Vaticano) para `documentos/concilios/_bruto/` (HTML bruto, não publicado).
2. `_lib_concilios.py` faz o parsing: separa capítulos/partes de parágrafos
   numerados. A numeração dos capítulos é feita **por nós** (contador
   sequencial), não extraída do HTML — a fonte tem inconsistências reais
   (falta o numeral "IV" em um capítulo de *Dei Verbum*; a segunda parte de
   *Gaudium et Spes* usa "II PARTE" em vez de "PARTE II" ou "SEGUNDA
   PARTE") que tornariam a extração do numeral frágil sem necessidade,
   já que a ordem de leitura garante a numeração certa de qualquer forma.
3. `gerar_pdfs_vaticano_ii.py` **gera o PDF com reportlab**, parágrafo por
   parágrafo — e, ao contrário do Catecismo, sabe com exatidão em que
   página cada capítulo cai, porque é o próprio gerador que a registra
   (via `afterFlowable`), sem precisar de heurística de regex depois.
4. `_resumos_vaticano_ii.py` — 69 resumos originais (um por capítulo/parte/
   proémio/conclusão dos 16 documentos), redigidos a partir de conhecimento
   teológico geral, não copiados do texto conciliar.
5. `gerar_html_concilios.py` + `gerar_pagina_concilios.py` montam o HTML
   final: mesma árvore recolhível do Catecismo, mas com um **leitor
   genérico** (`concilios.js`), já que aqui há 16 PDFs diferentes, não um
   só — cada botão carrega `data-pdf` + `data-pagina-pdf` próprios.

Para reprocessar do zero (ex.: se vatican.va atualizar algum documento):
`python baixar_vaticano_ii.py && python gerar_pdfs_vaticano_ii.py && python gerar_html_concilios.py && python gerar_pagina_concilios.py`.

**Os outros vinte concílios.** Testámos `vatican.va` e
`documentacatholicaomnia.eu`: nenhum tem tradução portuguesa de texto
integral para esses concílios (só o Vaticano II tem), e o segundo não tem
estrutura de URL previsível para automatizar a coleta no tempo disponível
— ao contrário do Vaticano II, não foi feito download automático aqui. Por
decisão explícita do utilizador, `_outros_concilios.py` traz, para cada um:
resumo original em português e, quando o concílio produziu uma fórmula
doutrinal célebre (credos, definições), o **texto latino** (fórmula estável,
igual em qualquer edição do Denzinger-Hünermann) + **tradução portuguesa
própria** + **referência DH**. Sem PDF de texto integral nem leitor —
são fórmulas curtas, citadas directamente na página.

### Liturgia Diária — dado externo ao vivo

A página busca as leituras **no navegador do visitante**, a cada acesso, na API
pública `https://liturgia.up.railway.app/v2/` (responde com
`access-control-allow-origin: *`, por isso funciona sem backend nem proxy).
Nada é armazenado: não há histórico, cache nem banco.

A data é enviada a partir do relógio local do visitante (`?dia=&mes=&ano=`),
para não depender do fuso do servidor da API.

Notas importantes:

- **Dependência de terceiros.** Se essa API sair do ar, a página mostra um erro
  com botão de repetir e link para a Liturgia Diária da Canção Nova. É o único
  ponto do site que depende de um serviço externo em tempo real.
- **Por que não a Canção Nova diretamente:** o site deles não envia
  `Access-Control-Allow-Origin`, então o navegador bloqueia a leitura por JS;
  além disso seria preciso raspar HTML, o que quebra a cada mudança de layout.
  Ficou como link de referência e alternativa em caso de falha.
- A aba "2ª Leitura" só aparece quando o dia tem segunda leitura (domingos e
  solenidades); em dias feriais ela é ocultada automaticamente.

### All Day Vatican — notícias coletadas no build

Ao contrário da Liturgia Diária, aqui a coleta **não pode acontecer no
navegador**: testei os sete feeds e nenhum envia `Access-Control-Allow-Origin`
liberado (Folha e Veja restringem ao próprio domínio), portanto o navegador do
visitante bloquearia a leitura. Além disso, extrair imagem exige ler `media:*` /
`enclosure` do XML, o que é trabalho de servidor.

Por isso: `coletar_noticias.py` roda no build, busca os feeds, filtra, e grava
`dados/noticias.json`. A página lê esse JSON local (mesma origem, sem CORS) e
faz o carrossel.

**Consequência importante:** a página mostra as notícias da última coleta, não
"ao vivo". Para cumprir "sempre as notícias do dia" é preciso rodar
`python build.py --noticias` **uma vez por dia** — cron, GitHub Actions ou o
Agendador de Tarefas do Windows. Se o JSON for de outro dia, a própria página
avisa em vermelho no rodapé, em vez de fingir que está atualizada.

Fontes e filtro:

- **Vatican News** (3 feeds: geral, papa, igreja) e **Canção Nova** entram
  inteiras — são veículos católicos.
- **G1, Folha, Estadão, O Antagonista, Veja** passam por filtro de assunto.
- O filtro olha apenas o **título e os primeiros 200 caracteres** do resumo.
  Isso não é detalhe: o G1 publica o artigo inteiro na `<description>`, e sem
  esse limite uma frase de passagem («o candidato se apresenta como católico»)
  fazia entrar notícia de convenção partidária. Termos ambíguos como `dom ` e
  `nossa senhora` foram removidos — casavam com «Avenida Dom Pedro II» e com o
  município de Nossa Senhora do Socorro.
- O coletor imprime o termo que fez cada notícia de jornal generalista passar,
  para conferência: útil ao ajustar as listas `TERMOS_FORTES` / `TERMOS_TITULO`.

Janela: `--dias 1` (padrão) pega só hoje; `--dias 3` amplia quando o dia rende
pouco. Só título, resumo e imagem são exibidos, e o clique vai sempre à página
original do veículo, **em nova aba** — o cartão tem `target="_blank"` e, além
disso, um clique em JS que chama `window.open(url, "_blank", "noopener,noreferrer")`
explicitamente, para não depender só do atributo em navegadores/extensões que
reaproveitam a aba corrente.

### Santo do Dia — mesmo método do All Day Vatican, não o da Liturgia

Pedido original: "faça o mesmo método da liturgia diária" (busca ao vivo, no
navegador, sem histórico). Testei — `santo.cancaonova.com` **não envia
`Access-Control-Allow-Origin`** na página em si (só o `wp-json` do site tem
CORS aberto, e esse endpoint não expõe o conteúdo do santo, só posts/páginas
padrão, vazios). Portanto o método da Liturgia (fetch direto no navegador) não
é possível aqui; usei o mesmo método do All Day Vatican: coleta no build.

`coletar_santo.py` busca `https://santo.cancaonova.com/` (a home do site
sempre mostra o santo do dia corrente) e grava `dados/santos.json` com nome,
imagem em resolução total, biografia (parágrafos com subtítulos preservados),
oração (quando o dia tiver) e as fontes que o próprio artigo cita ao final
(tipicamente vatican.va, Martirológio Romano, Arquisp.org.br). A página lê
esse JSON local.

Mesma consequência da coleta em build: rodar `python build.py --santo` (ou
`--atualizar`) uma vez por dia para a página não ficar com o santo de ontem.
Diferente do All Day Vatican, esta página **não** avisa se os dados estiverem
desatualizados — como não há problema em mostrar o santo de um dia próximo,
julguei o aviso dispensável aqui; se preferir o mesmo aviso, é o mesmo padrão
usado em `noticias.js`.

O parser depende do HTML específico deste site (títulos em `<strong>`/`<b>`
sozinhos num parágrafo viram subtítulo; o parágrafo "Minha oração" separa
biografia de oração). Se o site mudar o layout, o coletor para de reconhecer
a página e mantém o `santos.json` anterior, avisando no terminal.

### Ligação entre páginas

Referências ao Catecismo em qualquer página podem abrir o leitor de PDF já na
página certa usando `/catecismo/?pagina=N` (N = página do PDF, 1-indexada). O
mapeamento §§ → página do PDF está nos blocos da própria página do Catecismo.

### Pendências conhecidas

- A página do Catecismo cobre apenas as Partes I-III (§§ 1-2557): o PDF fornecido
  (`documentos/catecismo-cic.pdf`) não contém a Parte IV (Oração, §§ 2558-2865).
  Falta decidir a fonte para completá-la.
- Antes de publicar publicamente, verificar o licenciamento do PDF do Catecismo
  guardado em `documentos/` (é um documento de terceiros, com direitos próprios).
  Mesma questão para os documentos conciliares, se vierem a ser adicionados.
- As referências bíblicas na página do Catecismo foram extraídas automaticamente
  por regex a partir do PDF; revisar antes de tratar como lista definitiva.
- A página do Catecismo tem um leitor de PDF embutido (`<iframe>` + navegação por
  `#page=N`) com botão de download separado (atributo `download`, força salvar em
  vez de abrir). Navegadores reais (Chrome/Firefox/Edge) renderizam PDF em
  `<iframe>` nativamente; isso não é visível em todo ambiente de teste sandboxed.
- Gerar versões otimizadas do logo (`logo.png` tem 1254×1254 e é exibido a 40px;
  vale servir uma versão menor, e um `.ico`/`.svg` para o favicon).
- Escolher a fonte da liturgia diária (CNBB / Vatican News) e checar direitos de uso
  do texto bíblico.
- Decidir entre agregar RSS ou publicar resumos próprios no All Day Vatican.
- Implementar o cálculo da data da Páscoa para as festas móveis.
- Revisão teológica de todo o conteúdo antes de publicar.

## Publicação

`dist/` é uma pasta estática comum — serve em GitHub Pages, Netlify, Vercel ou
Cloudflare Pages. O arquivo `.nojekyll` já é gerado para o GitHub Pages.
