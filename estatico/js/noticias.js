/* All Day Vatican — carrossel das notícias do dia.
 *
 * Lê `dados/noticias.json`, gravado pelo coletor `coletar_noticias.py` que roda
 * no build. Os feeds de origem não enviam Access-Control-Allow-Origin, por isso
 * a coleta não pode acontecer aqui no navegador. Ver README.
 */

(function () {
  "use strict";

  const raiz = document.getElementById("noticias");
  if (!raiz) return;

  const FONTE_DADOS = "/dados/noticias.json";
  const INTERVALO = 7000;

  const elCarregando = document.getElementById("noticias-carregando");
  const elErro = document.getElementById("noticias-erro");
  const elErroTexto = document.getElementById("noticias-erro-texto");
  const elCarrossel = document.getElementById("noticias-carrossel");

  const elLink = document.getElementById("noticia-link");
  const elImagem = document.getElementById("noticia-imagem");
  const elFonte = document.getElementById("noticia-fonte");
  const elData = document.getElementById("noticia-data");
  const elTitulo = document.getElementById("noticia-titulo");
  const elResumo = document.getElementById("noticia-resumo");
  const elPontos = document.getElementById("noticia-pontos");
  const elPosicao = document.getElementById("noticia-posicao");
  const elTotal = document.getElementById("noticia-total");
  const elPausa = document.getElementById("noticia-pausa");
  const elPausaIcone = document.getElementById("noticia-pausa-icone");
  const elLista = document.getElementById("noticias-lista");
  const elListaTotal = document.getElementById("noticias-lista-total");
  const elAtualizacao = document.getElementById("noticias-atualizacao");

  let itens = [];
  let indice = 0;
  let temporizador = null;
  let pausado = false;

  const menosMovimento = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function formatarData(iso) {
    if (!iso) return "";
    const d = new Date(iso);
    if (isNaN(d)) return "";
    return d.toLocaleString("pt-BR", {
      day: "2-digit",
      month: "short",
      hour: "2-digit",
      minute: "2-digit",
    });
  }

  function mostrarItem(novo) {
    const item = itens[novo];
    if (!item) return;
    indice = novo;

    elLink.href = item.url;
    elTitulo.textContent = item.titulo;
    elResumo.textContent = item.resumo || "";
    elFonte.textContent = item.fonte;
    elData.textContent = formatarData(item.data);

    // Imagem: alt vazio de propósito — o título ao lado já descreve a notícia.
    if (item.imagem) {
      elImagem.src = item.imagem;
      elImagem.hidden = false;
    } else {
      elImagem.removeAttribute("src");
      elImagem.hidden = true;
    }

    elPosicao.textContent = String(novo + 1);

    Array.prototype.forEach.call(elPontos.children, function (ponto, i) {
      const ativo = i === novo;
      ponto.setAttribute("aria-selected", String(ativo));
      ponto.tabIndex = ativo ? 0 : -1;
    });

    if (!menosMovimento) {
      elLink.classList.remove("carrossel__cartao--entrando");
      void elLink.offsetWidth; // reinicia a animação
      elLink.classList.add("carrossel__cartao--entrando");
    }
  }

  function avancar(passo) {
    mostrarItem((indice + passo + itens.length) % itens.length);
  }

  function iniciarRotacao() {
    pararRotacao();
    if (pausado || itens.length < 2) return;
    temporizador = setInterval(function () { avancar(1); }, INTERVALO);
  }

  function pararRotacao() {
    if (temporizador) clearInterval(temporizador);
    temporizador = null;
  }

  function alternarPausa() {
    pausado = !pausado;
    elPausaIcone.textContent = pausado ? "▶" : "⏸";
    elPausa.setAttribute(
      "aria-label",
      pausado ? "Retomar rotação automática" : "Pausar rotação automática"
    );
    if (pausado) pararRotacao();
    else iniciarRotacao();
  }

  function montarPontos() {
    elPontos.innerHTML = "";
    itens.forEach(function (item, i) {
      const ponto = document.createElement("button");
      ponto.type = "button";
      ponto.className = "carrossel__ponto";
      ponto.setAttribute("role", "tab");
      ponto.setAttribute("aria-label", "Notícia " + (i + 1) + ": " + item.titulo);
      ponto.setAttribute("aria-selected", String(i === 0));
      ponto.tabIndex = i === 0 ? 0 : -1;
      ponto.addEventListener("click", function () {
        mostrarItem(i);
        iniciarRotacao();
      });
      elPontos.appendChild(ponto);
    });
  }

  function montarLista() {
    elLista.innerHTML = "";
    itens.forEach(function (item) {
      const li = document.createElement("li");
      const a = document.createElement("a");
      a.href = item.url;
      a.target = "_blank";
      a.rel = "noopener";
      a.textContent = item.titulo;
      const meta = document.createElement("span");
      meta.className = "noticias-lista__meta";
      meta.textContent = item.fonte + (item.data ? " · " + formatarData(item.data) : "");
      li.appendChild(a);
      li.appendChild(meta);
      elLista.appendChild(li);
    });
    elListaTotal.textContent = String(itens.length);
  }

  function avisarSeAntigo(atualizadoEm) {
    if (!atualizadoEm) return;
    const quando = new Date(atualizadoEm);
    if (isNaN(quando)) return;

    const hoje = new Date();
    const mesmoDia =
      quando.getFullYear() === hoje.getFullYear() &&
      quando.getMonth() === hoje.getMonth() &&
      quando.getDate() === hoje.getDate();

    elAtualizacao.textContent = mesmoDia
      ? " Atualizado hoje às " +
        quando.toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" }) +
        "."
      : " Atenção: esta lista foi recolhida em " +
        quando.toLocaleDateString("pt-BR") +
        " e pode não refletir as notícias de hoje.";
    if (!mesmoDia) elAtualizacao.className = "aviso-desatualizado";
  }

  function falhar(mensagem) {
    elCarregando.hidden = true;
    elCarrossel.hidden = true;
    elErroTexto.textContent = mensagem;
    elErro.hidden = false;
  }

  fetch(FONTE_DADOS, { cache: "no-store" })
    .then(function (r) {
      if (!r.ok) throw new Error("HTTP " + r.status);
      return r.json();
    })
    .then(function (dados) {
      itens = (dados.itens || []).filter(function (n) { return n && n.titulo && n.url; });

      if (!itens.length) {
        falhar("Ainda não há notícias recolhidas para hoje.");
        return;
      }

      elTotal.textContent = String(itens.length);
      montarPontos();
      montarLista();
      mostrarItem(0);
      avisarSeAntigo(dados.atualizado_em);

      elCarregando.hidden = true;
      elErro.hidden = true;
      elCarrossel.hidden = false;

      // Forca abertura em nova aba, sem depender so do atributo target="_blank"
      // do <a> (alguns navegadores/extensoes reaproveitam a aba corrente).
      elLink.addEventListener("click", function (evento) {
        evento.preventDefault();
        window.open(elLink.href, "_blank", "noopener,noreferrer");
      });

      document.getElementById("noticia-proxima").addEventListener("click", function () {
        avancar(1);
        iniciarRotacao();
      });
      document.getElementById("noticia-anterior").addEventListener("click", function () {
        avancar(-1);
        iniciarRotacao();
      });
      elPausa.addEventListener("click", alternarPausa);

      // Não trocar a notícia enquanto o visitante está a lê-la / a apontar.
      const cartao = document.querySelector(".carrossel");
      cartao.addEventListener("mouseenter", pararRotacao);
      cartao.addEventListener("mouseleave", function () { if (!pausado) iniciarRotacao(); });
      cartao.addEventListener("focusin", pararRotacao);
      cartao.addEventListener("focusout", function () { if (!pausado) iniciarRotacao(); });

      cartao.addEventListener("keydown", function (evento) {
        if (evento.key === "ArrowRight") { evento.preventDefault(); avancar(1); }
        if (evento.key === "ArrowLeft") { evento.preventDefault(); avancar(-1); }
      });

      // Imagem que não carrega não deve deixar um buraco no cartão.
      elImagem.addEventListener("error", function () { elImagem.hidden = true; });
      elImagem.addEventListener("load", function () { elImagem.hidden = false; });

      if (menosMovimento) {
        pausado = true;
        elPausaIcone.textContent = "▶";
      } else {
        iniciarRotacao();
      }
    })
    .catch(function (erro) {
      falhar("Não foi possível carregar as notícias (" + erro.message + ").");
    });
})();
