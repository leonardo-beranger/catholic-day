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
          <div class="leitor-cic__corpo">
            <iframe id="leitor-concilios-iframe" class="leitor-cic__quadro" title="Leitor de documentos conciliares" loading="lazy"></iframe>
            <div class="leitor-cic__carregando" id="leitor-concilios-carregando">
              <span class="girador" aria-hidden="true"></span>
              <p>A carregar o documento…</p>
            </div>
          </div>
        </div>
      </section>

      <section class="secao">
        <h2>Eixos de estudo</h2>
        <ol class="lista-eixos">
          <li>
            <span class="lista-eixos__faixa">Concílios 1–7</span>
            <div>
              <h3>Concílios cristológicos</h3>
              <p>De Niceia a Niceia II: a Trindade e as duas naturezas de Cristo.</p>
            </div>
          </li>
          <li>
            <span class="lista-eixos__faixa">Concílios 8–19</span>
            <div>
              <h3>Reforma e disciplina</h3>
              <p>Os concílios medievais e Trento diante das crises da Igreja.</p>
            </div>
          </li>
          <li>
            <span class="lista-eixos__faixa">Concílios 20–21</span>
            <div>
              <h3>Concílios modernos</h3>
              <p>Vaticano I e Vaticano II: fé e razão, Igreja e mundo contemporâneo.</p>
            </div>
          </li>
          <li>
            <span class="lista-eixos__faixa">Transversal</span>
            <div>
              <h3>Hermenêutica conciliar</h3>
              <p>Continuidade e ruptura: como ler os textos conciliares corretamente.</p>
            </div>
          </li>
        </ol>
      </section>

      <section class="secao">
        <h2>Os vinte e um concílios ecuménicos</h2>
        <p class="secao__intro">
          Visão de conjunto em ordem cronológica. Cada item leva à ficha do concílio mais
          abaixo — os 16 documentos completos do Vaticano II, ou o resumo com citação
          latina e referência dos demais.
        </p>

        <ol class="linha-tempo">
          <li><span class="linha-tempo__periodo">325</span><h3><a href="#concilio-1">1. Niceia I</a></h3><p>Consubstancialidade do Filho (homoousios).</p></li>
          <li><span class="linha-tempo__periodo">381</span><h3><a href="#concilio-2">2. Constantinopla I</a></h3><p>Divindade do Espírito Santo; Símbolo Niceno-Constantinopolitano.</p></li>
          <li><span class="linha-tempo__periodo">431</span><h3><a href="#concilio-3">3. Éfeso</a></h3><p>Maria Theotokos (Mãe de Deus).</p></li>
          <li><span class="linha-tempo__periodo">451</span><h3><a href="#concilio-4">4. Calcedônia</a></h3><p>Duas naturezas em uma só Pessoa.</p></li>
          <li><span class="linha-tempo__periodo">553</span><h3><a href="#concilio-5">5. Constantinopla II</a></h3><p>Reafirma Calcedônia; Três Capítulos.</p></li>
          <li><span class="linha-tempo__periodo">680–681</span><h3><a href="#concilio-6">6. Constantinopla III</a></h3><p>Duas vontades em Cristo (antimonotelismo).</p></li>
          <li><span class="linha-tempo__periodo">787</span><h3><a href="#concilio-7">7. Niceia II</a></h3><p>Legitimidade do culto às imagens.</p></li>
          <li><span class="linha-tempo__periodo">869–870</span><h3><a href="#concilio-8">8. Constantinopla IV</a></h3><p>Questão foviana.</p></li>
          <li><span class="linha-tempo__periodo">1123</span><h3><a href="#concilio-9">9. Latrão I</a></h3><p>Fim da Questão das Investiduras.</p></li>
          <li><span class="linha-tempo__periodo">1139</span><h3><a href="#concilio-10">10. Latrão II</a></h3><p>Fim do cisma de Anacleto II.</p></li>
          <li><span class="linha-tempo__periodo">1179</span><h3><a href="#concilio-11">11. Latrão III</a></h3><p>Regras da eleição papal.</p></li>
          <li><span class="linha-tempo__periodo">1215</span><h3><a href="#concilio-12">12. Latrão IV</a></h3><p>Transubstanciação; confissão e comunhão anuais.</p></li>
          <li><span class="linha-tempo__periodo">1245</span><h3><a href="#concilio-13">13. Lyon I</a></h3><p>Deposição de Frederico II.</p></li>
          <li><span class="linha-tempo__periodo">1274</span><h3><a href="#concilio-14">14. Lyon II</a></h3><p>Tentativa de união com Bizâncio.</p></li>
          <li><span class="linha-tempo__periodo">1311–1312</span><h3><a href="#concilio-15">15. Viena</a></h3><p>Supressão dos Templários.</p></li>
          <li><span class="linha-tempo__periodo">1414–1418</span><h3><a href="#concilio-16">16. Constança</a></h3><p>Fim do Grande Cisma do Ocidente.</p></li>
          <li><span class="linha-tempo__periodo">1431–1445</span><h3><a href="#concilio-17">17. Basileia–Ferrara–Florença</a></h3><p>União com Igrejas orientais; primado romano.</p></li>
          <li><span class="linha-tempo__periodo">1512–1517</span><h3><a href="#concilio-18">18. Latrão V</a></h3><p>Imortalidade da alma; reforma pré-tridentina.</p></li>
          <li><span class="linha-tempo__periodo">1545–1563</span><h3><a href="#concilio-19">19. Trento</a></h3><p>Resposta à Reforma; justificação; sacramentos.</p></li>
          <li><span class="linha-tempo__periodo">1869–1870</span><h3><a href="#concilio-20">20. Vaticano I</a></h3><p>Primado e infalibilidade papal.</p></li>
          <li><span class="linha-tempo__periodo">1962–1965</span><h3><a href="#vaticano-ii">21. Vaticano II</a></h3><p>16 documentos — ver árvore completa mais abaixo.</p></li>
        </ol>
      </section>
"""

VATICANO_II = """      <section class="secao" id="vaticano-ii">
        <h2>Vaticano II — os 16 documentos completos</h2>
        <p class="secao__intro">
          Único concílio com texto integral em português disponível na fonte oficial
          (<a href="https://www.vatican.va" target="_blank" rel="noopener">vatican.va</a>).
          Cada capítulo abaixo abre o leitor de PDF embutido na página exacta.
        </p>
"""

FIM_INTRO_VII = """      <section class="secao">
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
        + FIM_INTRO_VII
        + fichas
        + "      </section>\n"
        + VATICANO_II
        + arvore_vii
        + "      </section>\n"
    )

    destino = RAIZ / "conteudo" / "35-concilios.html"
    destino.write_text(conteudo, encoding="utf-8")
    print("Escrito em", destino, "-", len(conteudo), "caracteres")


if __name__ == "__main__":
    main()
