/* Santo do Dia — carrega a ficha do dia a partir de dados/santos.json.
 *
 * O JSON e gravado pelo coletor `coletar_santo.py`, que roda no build. A
 * pagina de origem (santo.cancaonova.com) nao envia Access-Control-Allow-
 * -Origin, entao o navegador do visitante nao consegue le-la diretamente.
 * Ver README.
 */

(function () {
  "use strict";

  const raiz = document.getElementById("santo");
  if (!raiz) return;

  const FONTE_DADOS = "/dados/santos.json";

  const elCarregando = document.getElementById("santo-carregando");
  const elErro = document.getElementById("santo-erro");
  const elErroTexto = document.getElementById("santo-erro-texto");
  const elConteudo = document.getElementById("santo-conteudo");

  const elImagem = document.getElementById("santo-imagem");
  const elNome = document.getElementById("santo-nome");
  const elBiografia = document.getElementById("santo-biografia");
  const elFonteLink = document.getElementById("santo-fonte-link");
  const elFontesCitadas = document.getElementById("santo-fontes-citadas");
  const elOracaoBloco = document.getElementById("santo-oracao-bloco");
  const elOracaoCorpo = document.getElementById("santo-oracao-corpo");

  function escapar(txt) {
    const d = document.createElement("div");
    d.textContent = txt == null ? "" : String(txt);
    return d.innerHTML;
  }

  function montarParagrafos(lista, comoOracao) {
    return (lista || [])
      .map(function (p) {
        if (p.tipo === "subtitulo") {
          return comoOracao
            ? "<p><strong>" + escapar(p.texto) + "</strong></p>"
            : "<h3>" + escapar(p.texto) + "</h3>";
        }
        return "<p>" + escapar(p.texto) + "</p>";
      })
      .join("");
  }

  function falhar(mensagem) {
    elCarregando.hidden = true;
    elConteudo.hidden = true;
    elErroTexto.textContent = mensagem;
    elErro.hidden = false;
  }

  fetch(FONTE_DADOS, { cache: "no-store" })
    .then(function (r) {
      if (!r.ok) throw new Error("HTTP " + r.status);
      return r.json();
    })
    .then(function (dados) {
      if (!dados || !dados.nome || !dados.biografia || !dados.biografia.length) {
        falhar("O santo de hoje ainda não foi carregado.");
        return;
      }

      elNome.textContent = dados.nome;

      if (dados.imagem) {
        elImagem.src = dados.imagem;
        elImagem.alt = dados.nome;
      } else {
        elImagem.hidden = true;
      }
      elImagem.addEventListener("error", function () { elImagem.hidden = true; });

      elBiografia.innerHTML = montarParagrafos(dados.biografia, false);

      if (dados.fonte_url) elFonteLink.href = dados.fonte_url;
      if (dados.fonte_nome) elFonteLink.textContent = dados.fonte_nome;

      if (dados.fontes_citadas && dados.fontes_citadas.length) {
        elFontesCitadas.textContent =
          " O próprio artigo cita como fontes: " + dados.fontes_citadas.join("; ") + ".";
      }

      if (dados.oracao && dados.oracao.length) {
        elOracaoCorpo.innerHTML = montarParagrafos(dados.oracao, true);
        elOracaoBloco.hidden = false;
      }

      elCarregando.hidden = true;
      elErro.hidden = true;
      elConteudo.hidden = false;
    })
    .catch(function (erro) {
      falhar("Não foi possível carregar o santo de hoje (" + erro.message + ").");
    });
})();
