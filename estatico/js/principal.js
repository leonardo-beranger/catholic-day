/* Lumen Fidei — comportamentos basicos do site. */

(function () {
  "use strict";

  // Menu mobile.
  const botao = document.querySelector(".menu-botao");
  const menu = document.getElementById("menu-principal");

  if (botao && menu) {
    botao.addEventListener("click", function () {
      const aberto = menu.classList.toggle("aberto");
      botao.setAttribute("aria-expanded", String(aberto));
      botao.querySelector(".sr").textContent = aberto ? "Fechar menu" : "Abrir menu";
    });

    document.addEventListener("keydown", function (evento) {
      if (evento.key === "Escape" && menu.classList.contains("aberto")) {
        menu.classList.remove("aberto");
        botao.setAttribute("aria-expanded", "false");
        botao.focus();
      }
    });
  }

  // Leitor de PDF embutido do Catecismo (CIC).
  const leitor = document.getElementById("leitor-cic");
  if (leitor) {
    const iframe = document.getElementById("leitor-cic-iframe");
    const paginaLabel = document.getElementById("leitor-cic-pagina");
    const botaoBaixar = document.getElementById("leitor-cic-baixar");
    const botaoFechar = document.getElementById("leitor-cic-fechar");
    const PDF_URL = "/documentos/catecismo-cic.pdf";

    function abrirNaPagina(pagina) {
      iframe.src = `${PDF_URL}#page=${pagina}&view=FitH`;
      botaoBaixar.href = PDF_URL;
      paginaLabel.textContent = pagina;
      leitor.hidden = false;
      leitor.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    document.querySelectorAll("[data-pagina-pdf]").forEach(function (botao) {
      botao.addEventListener("click", function () {
        abrirNaPagina(botao.getAttribute("data-pagina-pdf"));
      });
    });

    botaoFechar.addEventListener("click", function () {
      leitor.hidden = true;
      iframe.src = "";
    });

    // Permite chegar de outra pagina ja com o leitor aberto: /catecismo/?pagina=128
    const paginaPedida = new URLSearchParams(location.search).get("pagina");
    if (paginaPedida && /^\d+$/.test(paginaPedida)) {
      abrirNaPagina(paginaPedida);
    }
  }

  // Efeito 3D (tilt/paralaxe) na imagem de destaque da Vida de Cristo:
  // a figura inclina-se para o lado oposto ao cursor, como se saltasse da
  // tela em direcao a ele. Em toque (mobile) usa a inclinacao do aparelho;
  // sem suporte a nenhum dos dois, a imagem so fica parada — nunca quebra.
  const imagemTilt = document.querySelector(".vida-hero__imagem img");
  if (imagemTilt && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    const INCLINACAO_MAX = 14; // graus
    const container = imagemTilt.parentElement;

    function aplicarTilt(px, py) {
      // px, py vao de -1 a 1 (posicao relativa ao centro do container)
      const rotY = px * INCLINACAO_MAX;
      const rotX = -py * INCLINACAO_MAX;
      imagemTilt.style.transform =
        `perspective(1000px) rotateX(${rotX}deg) rotateY(${rotY}deg) scale(1.04)`;
    }

    function repousar() {
      imagemTilt.style.transform = "perspective(1000px) rotateX(0) rotateY(0) scale(1)";
    }

    container.addEventListener("mousemove", function (evento) {
      const r = container.getBoundingClientRect();
      const px = ((evento.clientX - r.left) / r.width) * 2 - 1;
      const py = ((evento.clientY - r.top) / r.height) * 2 - 1;
      aplicarTilt(px, py);
    });
    container.addEventListener("mouseleave", repousar);

    // Giroscopio do aparelho, quando disponivel (a maioria dos navegadores
    // moveis exige permissao explicita por gesto do usuario em iOS).
    function usarGiroscopio(evento) {
      if (evento.beta == null || evento.gamma == null) return;
      const px = Math.max(-1, Math.min(1, evento.gamma / 30));
      const py = Math.max(-1, Math.min(1, (evento.beta - 40) / 30));
      aplicarTilt(px, py);
    }

    function pedirPermissaoGiroscopio() {
      if (typeof DeviceOrientationEvent !== "undefined" &&
          typeof DeviceOrientationEvent.requestPermission === "function") {
        DeviceOrientationEvent.requestPermission()
          .then(function (estado) {
            if (estado === "granted") window.addEventListener("deviceorientation", usarGiroscopio);
          })
          .catch(function () {});
      } else {
        window.addEventListener("deviceorientation", usarGiroscopio);
      }
    }

    container.addEventListener("touchstart", pedirPermissaoGiroscopio, { once: true, passive: true });
  }

  // Data de hoje em pt-BR, usada nas paginas de liturgia/santo do dia.
  const formato = new Intl.DateTimeFormat("pt-BR", {
    weekday: "long",
    day: "numeric",
    month: "long",
    year: "numeric",
  });

  document.querySelectorAll("[data-data-hoje]").forEach(function (elemento) {
    const texto = formato.format(new Date());
    elemento.textContent = texto.charAt(0).toUpperCase() + texto.slice(1);
  });
})();
