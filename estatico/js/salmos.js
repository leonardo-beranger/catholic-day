/* Salmos (Sto. Agostinho) — leitor de PDF embutido do comentario aos
 * Salmos 101-150, mesmo mecanismo do Catecismo (principal.js), mas com
 * atributo proprio (data-pagina-salmo) para nao colidir com o leitor do
 * Catecismo quando ambos os scripts carregam na mesma pagina.
 */

(function () {
  "use strict";

  const leitor = document.getElementById("leitor-salmos");
  if (!leitor) return;

  const iframe = document.getElementById("leitor-salmos-iframe");
  const paginaLabel = document.getElementById("leitor-salmos-pagina");
  const botaoBaixar = document.getElementById("leitor-salmos-baixar");
  const botaoFechar = document.getElementById("leitor-salmos-fechar");
  const PDF_URL = (window.BASE_PATH || "") + "/documentos/agostinho-comentario-salmos-101-150.pdf";

  iframe.addEventListener("load", function () {
    leitor.classList.remove("leitor-cic--carregando");
  });

  function abrirNaPagina(pagina) {
    leitor.classList.add("leitor-cic--carregando");
    iframe.src = `${PDF_URL}#page=${pagina}&view=FitH`;
    botaoBaixar.href = PDF_URL;
    paginaLabel.textContent = pagina;
    leitor.hidden = false;
    leitor.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  document.querySelectorAll("[data-pagina-salmo]").forEach(function (botao) {
    botao.addEventListener("click", function () {
      abrirNaPagina(botao.getAttribute("data-pagina-salmo"));
    });
  });

  botaoFechar.addEventListener("click", function () {
    leitor.hidden = true;
    iframe.src = "";
  });
})();
