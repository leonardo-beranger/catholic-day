/* Liturgia Diaria — carrega as leituras do dia corrente.
 *
 * Fonte: API publica https://liturgia.up.railway.app/v2/ (CORS liberado).
 * Nada e armazenado: a cada visita os textos sao buscados na origem.
 */

(function () {
  "use strict";

  const raiz = document.getElementById("liturgia");
  if (!raiz) return;

  const API = "https://liturgia.up.railway.app/v2/";
  const TEMPO_LIMITE = 15000;

  const PARTES = ["primeiraLeitura", "salmo", "segundaLeitura", "evangelho"];

  const elCarregando = document.getElementById("liturgia-carregando");
  const elErro = document.getElementById("liturgia-erro");
  const elErroTexto = document.getElementById("liturgia-erro-texto");
  const elConteudo = document.getElementById("liturgia-conteudo");
  const elCelebracao = document.getElementById("liturgia-celebracao");
  const elCor = document.getElementById("liturgia-cor");
  const elOracoes = document.getElementById("liturgia-oracoes");
  const elOracoesCorpo = document.getElementById("liturgia-oracoes-corpo");
  const botaoRecarregar = document.getElementById("liturgia-recarregar");

  // Cores liturgicas -> classe do selo ja existente na folha de estilos.
  const CLASSE_COR = {
    verde: "selo--verde",
    branco: "selo--branco",
    vermelho: "selo--vermelho",
    roxo: "selo--violeta",
    violeta: "selo--violeta",
    rosa: "selo--violeta",
  };

  function escapar(txt) {
    const d = document.createElement("div");
    d.textContent = txt == null ? "" : String(txt);
    return d.innerHTML;
  }

  /* Os textos vem com o numero do versiculo colado na palavra ("7trazemos").
     Separa e marca o numero, deixando a leitura fluida. */
  function marcarVersiculos(txt) {
    return escapar(txt).replace(
      /(\d{1,3})(?=[A-Za-zÀ-ÿ«"])/g,
      '<sup class="versiculo">$1</sup>'
    );
  }

  function emParagrafos(txt, marcar) {
    return String(txt || "")
      .split(/\n+|(?=—\s)/)
      .map(function (p) { return p.trim(); })
      .filter(Boolean)
      .map(function (p) {
        return "<p>" + (marcar ? marcarVersiculos(p) : escapar(p)) + "</p>";
      })
      .join("");
  }

  function montarLeitura(item) {
    if (!item) return "";
    const partes = [];
    partes.push('<div class="leitura__topo">');
    if (item.titulo) partes.push("<h3>" + escapar(item.titulo) + "</h3>");
    if (item.referencia) {
      partes.push('<span class="leitura__ref">' + escapar(item.referencia) + "</span>");
    }
    partes.push("</div>");
    if (item.refrao) {
      partes.push(
        '<p class="leitura__refrao"><strong>R.</strong> ' + escapar(item.refrao) + "</p>"
      );
    }
    partes.push('<div class="leitura__texto">' + emParagrafos(item.texto, true) + "</div>");
    return partes.join("");
  }

  function primeiroItem(valor) {
    if (Array.isArray(valor)) return valor.length ? valor[0] : null;
    return valor && valor.texto ? valor : null;
  }

  function selecionarAba(parte) {
    PARTES.forEach(function (p) {
      const aba = document.getElementById("aba-" + p);
      const painel = document.getElementById("painel-" + p);
      if (!aba || !painel) return;
      const ativa = p === parte;
      aba.setAttribute("aria-selected", String(ativa));
      aba.tabIndex = ativa ? 0 : -1;
      painel.hidden = !ativa;
    });
  }

  function ligarAbas(disponiveis) {
    disponiveis.forEach(function (parte, indice) {
      const aba = document.getElementById("aba-" + parte);
      aba.addEventListener("click", function () {
        selecionarAba(parte);
      });
      aba.addEventListener("keydown", function (evento) {
        let destino = null;
        if (evento.key === "ArrowRight") destino = disponiveis[(indice + 1) % disponiveis.length];
        if (evento.key === "ArrowLeft") {
          destino = disponiveis[(indice - 1 + disponiveis.length) % disponiveis.length];
        }
        if (destino) {
          evento.preventDefault();
          selecionarAba(destino);
          document.getElementById("aba-" + destino).focus();
        }
      });
    });
  }

  function montarOracoes(dados) {
    const blocos = [];
    const o = dados.oracoes || {};
    const a = dados.antifonas || {};
    const linhas = [
      ["Antífona de entrada", a.entrada],
      ["Oração do dia (Coleta)", o.coleta || o.dia],
      ["Sobre as oferendas", o.oferendas],
      ["Antífona da comunhão", a.comunhao],
      ["Depois da comunhão", o.comunhao],
    ];
    linhas.forEach(function (par) {
      if (par[1]) {
        blocos.push(
          '<div class="oracao"><h4>' + escapar(par[0]) + "</h4><p>" + escapar(par[1]) + "</p></div>"
        );
      }
    });
    return blocos.join("");
  }

  function mostrar(dados) {
    elCelebracao.textContent = dados.liturgia || "Liturgia do dia";

    if (dados.cor) {
      const chave = String(dados.cor).toLowerCase().trim();
      elCor.className = "selo " + (CLASSE_COR[chave] || "");
      elCor.textContent = dados.cor;
      elCor.hidden = false;
    }

    const leituras = dados.leituras || {};
    const disponiveis = [];

    PARTES.forEach(function (parte) {
      const item = primeiroItem(leituras[parte]);
      const aba = document.getElementById("aba-" + parte);
      const painel = document.getElementById("painel-" + parte);
      if (item) {
        painel.innerHTML = montarLeitura(item);
        aba.hidden = false;
        disponiveis.push(parte);
      } else {
        // Dia sem 2ª leitura (ferial): a aba simplesmente não aparece.
        aba.hidden = true;
        painel.hidden = true;
      }
    });

    if (!disponiveis.length) {
      falhar("A liturgia de hoje foi carregada, mas veio sem leituras.");
      return;
    }

    ligarAbas(disponiveis);
    selecionarAba(disponiveis[0]);

    const oracoesHtml = montarOracoes(dados);
    if (oracoesHtml) {
      elOracoesCorpo.innerHTML = oracoesHtml;
      elOracoes.hidden = false;
    }

    elCarregando.hidden = true;
    elErro.hidden = true;
    elConteudo.hidden = false;
  }

  function falhar(mensagem) {
    elCarregando.hidden = true;
    elConteudo.hidden = true;
    elErroTexto.textContent = mensagem;
    elErro.hidden = false;
    elCelebracao.textContent = "Não foi possível carregar";
  }

  function carregar() {
    elErro.hidden = true;
    elConteudo.hidden = true;
    elCarregando.hidden = false;
    elCelebracao.textContent = "A carregar…";

    // Usa a data local do visitante, para não depender do fuso do servidor.
    const hoje = new Date();
    const parametros = new URLSearchParams({
      dia: String(hoje.getDate()).padStart(2, "0"),
      mes: String(hoje.getMonth() + 1).padStart(2, "0"),
      ano: String(hoje.getFullYear()),
    });

    const controlador = new AbortController();
    const relogio = setTimeout(function () { controlador.abort(); }, TEMPO_LIMITE);

    fetch(API + "?" + parametros.toString(), { signal: controlador.signal })
      .then(function (resposta) {
        if (!resposta.ok) throw new Error("HTTP " + resposta.status);
        return resposta.json();
      })
      .then(function (dados) {
        clearTimeout(relogio);
        mostrar(dados);
      })
      .catch(function (erro) {
        clearTimeout(relogio);
        const semRede = erro.name === "AbortError";
        falhar(
          semRede
            ? "A busca demorou demais. Verifique a ligação e tente de novo."
            : "Não foi possível carregar a liturgia de hoje (" + erro.message + ")."
        );
      });
  }

  botaoRecarregar.addEventListener("click", carregar);
  carregar();

  /* Tamanho da letra: escala aplicada via variavel CSS --liturgia-escala,
     persistida em localStorage para manter a preferencia entre visitas. */
  (function () {
    const CHAVE = "catholicday-liturgia-escala";
    const MIN = 0.8;
    const MAX = 1.6;
    const PASSO = 0.1;

    const botaoMenos = document.getElementById("liturgia-fonte-menos");
    const botaoMais = document.getElementById("liturgia-fonte-mais");
    if (!botaoMenos || !botaoMais) return;

    let escala = parseFloat(localStorage.getItem(CHAVE)) || 1;

    function aplicar() {
      escala = Math.min(MAX, Math.max(MIN, escala));
      raiz.style.setProperty("--liturgia-escala", escala.toFixed(2));
      botaoMenos.disabled = escala <= MIN;
      botaoMais.disabled = escala >= MAX;
      localStorage.setItem(CHAVE, escala.toFixed(2));
    }

    botaoMenos.addEventListener("click", function () {
      escala -= PASSO;
      aplicar();
    });
    botaoMais.addEventListener("click", function () {
      escala += PASSO;
      aplicar();
    });

    aplicar();
  })();
})();
