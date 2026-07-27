/* Concílios — leitor de PDF embutido, generico para varios documentos
 * (um por documento do Vaticano II), ao contrario do leitor do Catecismo
 * (principal.js), que aponta sempre para o mesmo PDF.
 */

(function () {
  "use strict";

  const leitor = document.getElementById("leitor-concilios");
  if (!leitor) return;

  const iframe = document.getElementById("leitor-concilios-iframe");
  const tituloEl = document.getElementById("leitor-concilios-titulo");
  const paginaEl = document.getElementById("leitor-concilios-pagina");
  const botaoBaixar = document.getElementById("leitor-concilios-baixar");
  const botaoFechar = document.getElementById("leitor-concilios-fechar");

  function abrir(pdfUrl, pagina, titulo) {
    iframe.src = `${pdfUrl}#page=${pagina}&view=FitH`;
    botaoBaixar.href = pdfUrl;
    const nomeArquivo = pdfUrl.split("/").pop();
    botaoBaixar.setAttribute("download", nomeArquivo);
    tituloEl.textContent = (titulo || "Documento") + " — página ";
    tituloEl.appendChild(paginaEl);
    paginaEl.textContent = pagina;
    leitor.hidden = false;
    leitor.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  document.querySelectorAll("[data-pdf][data-pagina-pdf]").forEach(function (botao) {
    botao.addEventListener("click", function () {
      abrir(botao.getAttribute("data-pdf"), botao.getAttribute("data-pagina-pdf"), botao.getAttribute("data-titulo-pdf"));
    });
  });

  botaoFechar.addEventListener("click", function () {
    leitor.hidden = true;
    iframe.src = "";
  });
})();
