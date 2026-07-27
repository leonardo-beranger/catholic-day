# -*- coding: utf-8 -*-
"""Monta o conteudo final da pagina Concilios: intro + tabela + leitor
embutido + arvore do Vaticano II + fichas dos outros 20 concilios."""
import html as html_mod
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _outros_concilios import CONCILIOS

RAIZ = Path(__file__).parent


def esc(txt):
    return html_mod.escape(txt, quote=True)


FRONT_MATTER = """---
slug: concilios
titulo: Concílios
menu: Concílios
secao: formacao
ordem: 35
scripts: concilios.js
subtitulo: As assembleias em que a Igreja definiu e guardou a fé recebida.
descricao: Os vinte e um concílios ecuménicos da Igreja Católica — o Vaticano II com os 16 documentos completos e leitor de PDF embutido; os demais com resumo, citações latinas e referência Denzinger-Hünermann.
---
"""

INTRO = """      <section class="secao">
        <p class="secao__intro">
          Um concílio ecuménico reúne os bispos do mundo inteiro, sob convocação e
          confirmação do Romano Pontífice (ou, na Antiguidade, do imperador com posterior
          recepção papal), para definir a fé ou legislar sobre a disciplina de toda a
          Igreja — distinguindo-se, por isso, de sínodos e concílios particulares, cuja
          autoridade é regional. As definições dogmáticas de um concílio ecuménico
          obrigam em consciência todos os fiéis.
        </p>

        <div class="leitor-cic" id="leitor-concilios" hidden>
          <div class="leitor-cic__barra">
            <span class="leitor-cic__titulo" id="leitor-concilios-titulo">Documento — página <span id="leitor-concilios-pagina">1</span></span>
            <div class="leitor-cic__acoes">
              <a id="leitor-concilios-baixar" class="botao-baixar" href="#" download>Baixar PDF</a>
              <button type="button" class="botao-fechar" id="leitor-concilios-fechar" aria-label="Fechar leitor">✕</button>
            </div>
          </div>
          <iframe id="leitor-concilios-iframe" class="leitor-cic__quadro" title="Leitor de documentos conciliares" loading="lazy"></iframe>
        </div>
      </section>

      <section class="secao">
        <h2>Os vinte e um concílios ecuménicos</h2>
        <p class="secao__intro">
          Visão de conjunto. As duas últimas colunas levam à ficha de cada concílio mais
          abaixo — os 16 documentos completos do Vaticano II, ou o resumo com citação
          latina e referência dos demais.
        </p>

        <div class="tabela-rolagem">
          <table>
            <thead>
              <tr>
                <th>#</th>
                <th>Concílio</th>
                <th>Ano</th>
                <th>Definições principais</th>
              </tr>
            </thead>
            <tbody>
              <tr><td>1</td><td><a href="#concilio-1">Niceia I</a></td><td>325</td><td>Consubstancialidade do Filho (homoousios)</td></tr>
              <tr><td>2</td><td><a href="#concilio-2">Constantinopla I</a></td><td>381</td><td>Divindade do Espírito Santo; Símbolo Niceno-Constantinopolitano</td></tr>
              <tr><td>3</td><td><a href="#concilio-3">Éfeso</a></td><td>431</td><td>Maria Theotokos (Mãe de Deus)</td></tr>
              <tr><td>4</td><td><a href="#concilio-4">Calcedônia</a></td><td>451</td><td>Duas naturezas em uma só Pessoa</td></tr>
              <tr><td>5</td><td><a href="#concilio-5">Constantinopla II</a></td><td>553</td><td>Reafirma Calcedônia; Três Capítulos</td></tr>
              <tr><td>6</td><td><a href="#concilio-6">Constantinopla III</a></td><td>680–681</td><td>Duas vontades em Cristo (antimonotelismo)</td></tr>
              <tr><td>7</td><td><a href="#concilio-7">Niceia II</a></td><td>787</td><td>Legitimidade do culto às imagens</td></tr>
              <tr><td>8</td><td><a href="#concilio-8">Constantinopla IV</a></td><td>869–870</td><td>Questão foviana</td></tr>
              <tr><td>9</td><td><a href="#concilio-9">Latrão I</a></td><td>1123</td><td>Fim da Questão das Investiduras</td></tr>
              <tr><td>10</td><td><a href="#concilio-10">Latrão II</a></td><td>1139</td><td>Fim do cisma de Anacleto II</td></tr>
              <tr><td>11</td><td><a href="#concilio-11">Latrão III</a></td><td>1179</td><td>Regras da eleição papal</td></tr>
              <tr><td>12</td><td><a href="#concilio-12">Latrão IV</a></td><td>1215</td><td>Transubstanciação; confissão e comunhão anuais</td></tr>
              <tr><td>13</td><td><a href="#concilio-13">Lyon I</a></td><td>1245</td><td>Deposição de Frederico II</td></tr>
              <tr><td>14</td><td><a href="#concilio-14">Lyon II</a></td><td>1274</td><td>Tentativa de união com Bizâncio</td></tr>
              <tr><td>15</td><td><a href="#concilio-15">Viena</a></td><td>1311–1312</td><td>Supressão dos Templários</td></tr>
              <tr><td>16</td><td><a href="#concilio-16">Constança</a></td><td>1414–1418</td><td>Fim do Grande Cisma do Ocidente</td></tr>
              <tr><td>17</td><td><a href="#concilio-17">Basileia–Ferrara–Florença</a></td><td>1431–1445</td><td>União com Igrejas orientais; primado romano</td></tr>
              <tr><td>18</td><td><a href="#concilio-18">Latrão V</a></td><td>1512–1517</td><td>Imortalidade da alma; reforma pré-tridentina</td></tr>
              <tr><td>19</td><td><a href="#concilio-19">Trento</a></td><td>1545–1563</td><td>Resposta à Reforma; justificação; sacramentos</td></tr>
              <tr><td>20</td><td><a href="#concilio-20">Vaticano I</a></td><td>1869–1870</td><td>Primado e infalibilidade papal</td></tr>
              <tr><td>21</td><td><a href="#vaticano-ii">Vaticano II</a></td><td>1962–1965</td><td>16 documentos — ver árvore completa abaixo</td></tr>
            </tbody>
          </table>
        </div>
      </section>

      <section class="secao">
        <h2>Eixos de estudo</h2>
        <div class="grade">
          <div class="cartao">
            <span class="cartao__etiqueta">Eixo 1 · Concílios 1-7</span>
            <h3>Concílios cristológicos</h3>
            <p>De Niceia a Niceia II: a Trindade e as duas naturezas de Cristo.</p>
          </div>
          <div class="cartao">
            <span class="cartao__etiqueta">Eixo 2 · Concílios 8-19</span>
            <h3>Reforma e disciplina</h3>
            <p>Os concílios medievais e Trento diante das crises da Igreja.</p>
          </div>
          <div class="cartao">
            <span class="cartao__etiqueta">Eixo 3 · Concílios 20-21</span>
            <h3>Concílios modernos</h3>
            <p>Vaticano I e Vaticano II: fé e razão, Igreja e mundo contemporâneo.</p>
          </div>
          <div class="cartao">
            <span class="cartao__etiqueta">Eixo 4</span>
            <h3>Hermenêutica conciliar</h3>
            <p>Continuidade e ruptura: como ler os textos conciliares corretamente.</p>
          </div>
        </div>
      </section>

      <section class="secao" id="vaticano-ii">
        <h2>Vaticano II — os 16 documentos completos</h2>
        <p class="secao__intro">
          Único concílio com texto integral em português disponível na fonte oficial
          (<a href="https://www.vatican.va" target="_blank" rel="noopener">vatican.va</a>).
          Cada capítulo abaixo abre o leitor de PDF embutido na página exacta.
        </p>
"""

FIM_INTRO_VII = """      </section>

      <section class="secao">
        <h2>Os outros vinte concílios</h2>
        <div class="painel">
          <p>
            Estes vinte concílios não têm tradução portuguesa de texto integral
            disponível nas fontes consultadas. Os resumos abaixo são <strong>redação
            própria</strong>; as citações, quando existem, reproduzem fórmulas latinas
            estáveis (credos e definições, tal como registadas em qualquer edição do
            Denzinger-Hünermann), com tradução portuguesa própria e a referência DH
            correspondente.
          </p>
        </div>
"""


def gerar_ficha_concilio(c):
    partes = [
        f'        <article class="ficha" id="concilio-{c["numero"]}">',
        '          <div class="ficha__cabecalho">',
        f'            <h3>{c["numero"]}. {esc(c["nome"])}</h3>',
        f'            <span class="ficha__ref">{esc(c["ano"])}</span>',
        "          </div>",
        f"          <p>{esc(c['resumo'])}</p>",
    ]
    if c["citacao_latina"]:
        partes.append('          <blockquote class="citacao citacao--latim">')
        partes.append(f"            <em>{esc(c['citacao_latina'])}</em>")
        partes.append(f"            <footer>Latim original — {esc(c['referencia'])}</footer>")
        partes.append("          </blockquote>")
        partes.append('          <blockquote class="citacao">')
        partes.append(f"            {esc(c['traducao'])}")
        partes.append("            <footer>Tradução própria</footer>")
        partes.append("          </blockquote>")
    elif c["referencia"] and c["referencia"] != "—":
        partes.append(f'          <p class="ficha__nota"><strong>Referência:</strong> {esc(c["referencia"])}</p>')
    partes.append("        </article>")
    return "\n".join(partes) + "\n"


def main():
    arvore_vii = (RAIZ / "_arvore_vaticano_ii.html").read_text(encoding="utf-8")

    fichas = "".join(gerar_ficha_concilio(c) for c in CONCILIOS)

    conteudo = (
        FRONT_MATTER
        + INTRO
        + arvore_vii
        + FIM_INTRO_VII
        + fichas
        + "      </section>\n"
    )

    destino = RAIZ / "conteudo" / "35-concilios.html"
    destino.write_text(conteudo, encoding="utf-8")
    print("Escrito em", destino, "-", len(conteudo), "caracteres")


if __name__ == "__main__":
    main()
