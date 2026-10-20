/* Liturgia Diaria — as leituras do dia, com navegacao pela semana.
 *
 * Fonte: API publica https://liturgia.up.railway.app/v2/ (CORS liberado).
 * Abre sempre no dia de hoje. As setas percorrem a semana anterior, a atual
 * e a seguinte — tres semanas, nao mais: e o horizonte que a pagina promete.
 * Cada dia ja buscado fica em memoria durante a visita, para nao repetir
 * pedidos a origem quando o leitor volta a um dia que ja viu.
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

  const elEtiqueta = document.getElementById("liturgia-etiqueta");
  const elData = document.getElementById("liturgia-data");
  const elRotuloSemana = document.getElementById("liturgia-semana-rotulo");
  const elDias = document.getElementById("liturgia-semana-dias");
  const botaoAnterior = document.getElementById("liturgia-semana-anterior");
  const botaoSeguinte = document.getElementById("liturgia-semana-seguinte");
  const botaoHoje = document.getElementById("liturgia-hoje");

  // Cores liturgicas -> classe do selo ja existente na folha de estilos.
  const CLASSE_COR = {
    verde: "selo--verde",
    branco: "selo--branco",
    vermelho: "selo--vermelho",
    roxo: "selo--violeta",
    violeta: "selo--violeta",
    rosa: "selo--violeta",
  };

  /* ----------------------------------------------------------------- datas */

  /* Todas as contas de data usam ano/mes/dia locais e meia-noite local.
     Somar horas a um Date cru erraria o dia nas mudancas de horario de
     verao; construir um Date novo a partir das componentes, nao. */
  function diaLocal(d) {
    return new Date(d.getFullYear(), d.getMonth(), d.getDate());
  }

  function somarDias(d, n) {
    return new Date(d.getFullYear(), d.getMonth(), d.getDate() + n);
  }

  // A semana liturgica comeca no domingo.
  function domingoDaSemana(d) {
    return somarDias(d, -d.getDay());
  }

  function chave(d) {
    return (
      d.getFullYear() +
      "-" +
      String(d.getMonth() + 1).padStart(2, "0") +
      "-" +
      String(d.getDate()).padStart(2, "0")
    );
  }

  function mesmoDia(a, b) {
    return chave(a) === chave(b);
  }

  const HOJE = diaLocal(new Date());

  const fmtCompleto = new Intl.DateTimeFormat("pt-BR", {
    weekday: "long",
    day: "numeric",
    month: "long",
    year: "numeric",
  });
  const fmtDiaMes = new Intl.DateTimeFormat("pt-BR", { day: "numeric", month: "long" });
  const fmtDiaMesAno = new Intl.DateTimeFormat("pt-BR", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });
  const fmtMesLongo = new Intl.DateTimeFormat("pt-BR", { month: "long" });
  const fmtSemanaCurta = new Intl.DateTimeFormat("pt-BR", { weekday: "short" });

  function maiuscula(txt) {
    return txt.charAt(0).toUpperCase() + txt.slice(1);
  }

  function rotuloSemana(inicio, fim) {
    if (inicio.getFullYear() !== fim.getFullYear()) {
      return fmtDiaMesAno.format(inicio) + " a " + fmtDiaMesAno.format(fim);
    }
    if (inicio.getMonth() !== fim.getMonth()) {
      return fmtDiaMes.format(inicio) + " a " + fmtDiaMes.format(fim);
    }
    return inicio.getDate() + " a " + fim.getDate() + " de " + fmtMesLongo.format(inicio);
  }

  /* ---------------------------------------------------------------- estado */

  // Deslocamento em semanas a partir da atual: so -1, 0 e +1.
  const MIN_SEMANA = -1;
  const MAX_SEMANA = 1;
  let semana = 0;
  let selecionado = HOJE;

  // Dias ja buscados nesta visita, por chave ISO.
  const cache = Object.create(null);

  /* Cada pedido recebe um numero. Se o leitor trocar de dia antes da
     resposta chegar, a resposta antiga e descartada em vez de sobrescrever
     a nova — sem isto, dois cliques rapidos podem mostrar o dia errado. */
  let pedido = 0;
  let controladorAtual = null;

  /* ------------------------------------------------------------- utilidades */

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

  /* ------------------------------------------------------------------ abas */

  // Partes com leitura no dia que esta a mostra.
  let disponiveis = [];

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

  /* Os ouvintes das abas sao ligados uma vez so. Liga-los a cada dia
     carregado acumularia um ouvinte por visita ao mesmo botao. */
  PARTES.forEach(function (parte) {
    const aba = document.getElementById("aba-" + parte);
    if (!aba) return;
    aba.addEventListener("click", function () {
      selecionarAba(parte);
    });
    aba.addEventListener("keydown", function (evento) {
      const indice = disponiveis.indexOf(parte);
      if (indice < 0 || disponiveis.length < 2) return;
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

  /* ------------------------------------------------------- navegacao da semana */

  function pintarSemana() {
    const inicio = somarDias(domingoDaSemana(HOJE), semana * 7);
    const fim = somarDias(inicio, 6);

    elRotuloSemana.textContent = maiuscula(rotuloSemana(inicio, fim));
    botaoAnterior.disabled = semana <= MIN_SEMANA;
    botaoSeguinte.disabled = semana >= MAX_SEMANA;

    const botoes = [];
    for (let i = 0; i < 7; i += 1) {
      const dia = somarDias(inicio, i);
      const ehHoje = mesmoDia(dia, HOJE);
      const ehSelecionado = mesmoDia(dia, selecionado);
      botoes.push(
        '<button type="button" class="liturgia__dia' +
          (ehHoje ? " liturgia__dia--hoje" : "") +
          '" data-data="' + chave(dia) + '"' +
          ' aria-pressed="' + String(ehSelecionado) + '"' +
          (ehHoje ? ' aria-current="date"' : "") +
          ' aria-label="' + escapar(maiuscula(fmtCompleto.format(dia))) + '">' +
          '<span class="liturgia__dia-semana">' +
          escapar(maiuscula(fmtSemanaCurta.format(dia).replace(".", ""))) +
          "</span>" +
          '<span class="liturgia__dia-numero">' + dia.getDate() + "</span>" +
          "</button>"
      );
    }
    elDias.innerHTML = botoes.join("");
  }

  function pintarCabecalho() {
    const ehHoje = mesmoDia(selecionado, HOJE);
    elEtiqueta.textContent = ehHoje ? "Liturgia de hoje" : "Liturgia do dia";
    elData.textContent = maiuscula(fmtCompleto.format(selecionado));
    botaoHoje.hidden = ehHoje;
  }

  /* Um dia fora das tres semanas nao tem botao: a selecao volta para hoje.
     Acontece se a pagina ficar aberta ate depois da meia-noite. */
  function dentroDoHorizonte(data) {
    const inicio = somarDias(domingoDaSemana(HOJE), MIN_SEMANA * 7);
    const fim = somarDias(domingoDaSemana(HOJE), MAX_SEMANA * 7 + 6);
    return data >= inicio && data <= fim;
  }

  function semanaDe(data) {
    const base = domingoDaSemana(HOJE).getTime();
    const alvo = domingoDaSemana(data).getTime();
    return Math.round((alvo - base) / 604800000); // 7 dias em ms
  }

  /* ----------------------------------------------------------- apresentacao */

  function mostrar(dados) {
    elCelebracao.textContent = dados.liturgia || "Liturgia do dia";

    // O selo e as oracoes sao de um dia so: recomeçam escondidos a cada
    // carregamento, senao o dia novo herdaria a cor ou as oracoes do anterior.
    elCor.hidden = true;
    elCor.className = "selo";
    elCor.textContent = "";
    elOracoes.hidden = true;
    elOracoesCorpo.innerHTML = "";

    if (dados.cor) {
      const chaveCor = String(dados.cor).toLowerCase().trim();
      elCor.className = "selo " + (CLASSE_COR[chaveCor] || "");
      elCor.textContent = dados.cor;
      elCor.hidden = false;
    }

    const leituras = dados.leituras || {};
    disponiveis = [];

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
        painel.innerHTML = "";
      }
    });

    if (!disponiveis.length) {
      falhar("A liturgia de " + nomeDoDia() + " foi carregada, mas veio sem leituras.");
      return;
    }

    selecionarAba(disponiveis[0]);

    const oracoesHtml = montarOracoes(dados);
    if (oracoesHtml) {
      elOracoesCorpo.innerHTML = oracoesHtml;
      elOracoes.hidden = false;
    }

    raiz.removeAttribute("aria-busy");
    elCarregando.hidden = true;
    elErro.hidden = true;
    elConteudo.hidden = false;
  }

  function nomeDoDia() {
    return mesmoDia(selecionado, HOJE) ? "hoje" : fmtDiaMes.format(selecionado);
  }

  function falhar(mensagem) {
    raiz.removeAttribute("aria-busy");
    elCarregando.hidden = true;
    elConteudo.hidden = true;
    elErroTexto.textContent = mensagem;
    elErro.hidden = false;
    elCelebracao.textContent = "Não foi possível carregar";
    elCor.hidden = true;
    elOracoes.hidden = true;
  }

  /* -------------------------------------------------------------- carregamento */

  function carregar(data, forcar) {
    if (data) {
      if (!dentroDoHorizonte(data)) data = HOJE;
      selecionado = data;
      semana = semanaDe(selecionado);
    }

    pintarCabecalho();
    pintarSemana();

    const k = chave(selecionado);
    if (!forcar && cache[k]) {
      mostrar(cache[k]);
      return;
    }

    elErro.hidden = true;
    elConteudo.hidden = true;
    elCarregando.hidden = false;
    raiz.setAttribute("aria-busy", "true");
    elCelebracao.textContent = "A carregar…";

    const meu = ++pedido;
    if (controladorAtual) controladorAtual.abort();

    const controlador = new AbortController();
    controladorAtual = controlador;
    let expirou = false;
    const relogio = setTimeout(function () {
      expirou = true;
      controlador.abort();
    }, TEMPO_LIMITE);

    const parametros = new URLSearchParams({
      dia: String(selecionado.getDate()).padStart(2, "0"),
      mes: String(selecionado.getMonth() + 1).padStart(2, "0"),
      ano: String(selecionado.getFullYear()),
    });

    fetch(API + "?" + parametros.toString(), { signal: controlador.signal })
      .then(function (resposta) {
        if (!resposta.ok) throw new Error("HTTP " + resposta.status);
        return resposta.json();
      })
      .then(function (dados) {
        clearTimeout(relogio);
        if (meu !== pedido) return; // chegou atrasada: o leitor já trocou de dia
        cache[k] = dados;
        mostrar(dados);
      })
      .catch(function (erro) {
        clearTimeout(relogio);
        if (meu !== pedido) return; // pedido substituído por outro
        falhar(
          expirou
            ? "A busca demorou demais. Verifique a ligação e tente de novo."
            : "Não foi possível carregar a liturgia de " + nomeDoDia() +
              " (" + erro.message + ")."
        );
      });
  }

  /* ------------------------------------------------------------------ ligacoes */

  // Delegacao: os botoes dos dias sao refeitos a cada semana, o ouvinte nao.
  elDias.addEventListener("click", function (evento) {
    const botao = evento.target.closest(".liturgia__dia");
    if (!botao) return;
    const partes = botao.dataset.data.split("-").map(Number);
    carregar(new Date(partes[0], partes[1] - 1, partes[2]));
  });

  botaoAnterior.addEventListener("click", function () {
    if (semana <= MIN_SEMANA) return;
    semana -= 1;
    // Mantem o dia da semana: quem estava na quinta vai para a quinta anterior.
    carregar(somarDias(selecionado, -7));
  });

  botaoSeguinte.addEventListener("click", function () {
    if (semana >= MAX_SEMANA) return;
    semana += 1;
    carregar(somarDias(selecionado, 7));
  });

  botaoHoje.addEventListener("click", function () {
    carregar(HOJE);
  });

  botaoRecarregar.addEventListener("click", function () {
    carregar(selecionado, true);
  });

  carregar(HOJE);

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
