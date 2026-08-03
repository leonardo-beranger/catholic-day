/* Calendario Liturgico — calcula a Pascoa (algoritmo de Meeus/Jones/Butcher,
 * calendario gregoriano) e, a partir dela, todas as festas moveis do ano
 * pedido; combina com as festas fixas e as dedicacoes mensais vindas de
 * dados/calendario.json. Tudo calculado no navegador: o calendario muda
 * sozinho conforme o ano escolhido, sem precisar reconstruir o site.
 */

(function () {
  "use strict";

  const raiz = document.getElementById("calendario-liturgico");
  if (!raiz) return;

  const seletorAno = document.getElementById("calendario-ano");
  const botaoHoje = document.getElementById("calendario-ano-hoje");
  const elResumo = document.getElementById("calendario-resumo");
  const elMeses = document.getElementById("calendario-meses");

  const NOMES_MES = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
  ];

  const CLASSE_COR = {
    verde: "selo--verde",
    branco: "selo--branco",
    vermelho: "selo--vermelho",
    roxo: "selo--violeta",
    violeta: "selo--violeta",
  };

  function escapar(txt) {
    const d = document.createElement("div");
    d.textContent = txt == null ? "" : String(txt);
    return d.innerHTML;
  }

  /* Data da Pascoa (domingo) para um ano, calendario gregoriano. */
  function calcularPascoa(ano) {
    const a = ano % 19;
    const b = Math.floor(ano / 100);
    const c = ano % 100;
    const d = Math.floor(b / 4);
    const e = b % 4;
    const f = Math.floor((b + 8) / 25);
    const g = Math.floor((b - f + 1) / 3);
    const h = (19 * a + b - d - g + 15) % 30;
    const i = Math.floor(c / 4);
    const k = c % 4;
    const l = (32 + 2 * e + 2 * i - h - k) % 7;
    const m = Math.floor((a + 11 * h + 22 * l) / 451);
    const mes = Math.floor((h + l - 7 * m + 114) / 31); // 3=marco, 4=abril
    const dia = ((h + l - 7 * m + 114) % 31) + 1;
    return new Date(ano, mes - 1, dia);
  }

  function somarDias(data, dias) {
    const nova = new Date(data);
    nova.setDate(nova.getDate() + dias);
    return nova;
  }

  /* Domingo mais proximo de 30 de novembro = 1.º Domingo do Advento. */
  function calcularAdvento1(ano) {
    const nov30 = new Date(ano, 10, 30);
    const diaSemana = nov30.getDay(); // 0 = domingo
    if (diaSemana <= 3) return somarDias(nov30, -diaSemana);
    return somarDias(nov30, 7 - diaSemana);
  }

  function montarSelo(cor, grau) {
    const classe = CLASSE_COR[String(cor || "").toLowerCase()] || "";
    return (
      '<span class="selo ' + classe + '">' + escapar(cor || "—") + "</span>" +
      (grau ? '<span class="calendario__grau">' + escapar(grau) + "</span>" : "")
    );
  }

  function carregarDados() {
    const base = window.BASE_PATH || "";
    return fetch(base + "/dados/calendario.json").then(function (resp) {
      if (!resp.ok) throw new Error("HTTP " + resp.status);
      return resp.json();
    });
  }

  function construirEventosDoAno(dados, ano) {
    const eventos = []; // { data: Date, nome, grau, cor }

    (dados.festas_fixas || []).forEach(function (f) {
      const [mm, dd] = f.dia.split("-").map(Number);
      eventos.push({
        data: new Date(ano, mm - 1, dd),
        nome: f.nome,
        grau: f.grau,
        cor: f.cor,
        preceito: !!f.preceito,
        movel: false,
      });
    });

    const pascoa = calcularPascoa(ano);
    (dados.festas_moveis || []).forEach(function (f) {
      eventos.push({
        data: somarDias(pascoa, f.offset_pascoa_dias),
        nome: f.nome,
        grau: f.grau,
        cor: f.cor,
        preceito: false,
        movel: true,
      });
    });

    const advento1 = calcularAdvento1(ano);
    eventos.push({
      data: advento1,
      nome: "1.º Domingo do Advento (início do Ano Litúrgico)",
      grau: "Início de tempo",
      cor: "roxo",
      preceito: false,
      movel: true,
    });
    eventos.push({
      data: somarDias(advento1, -7),
      nome: "Nosso Senhor Jesus Cristo, Rei do Universo",
      grau: "Solenidade",
      cor: "vermelho",
      preceito: false,
      movel: true,
    });

    // Tambem calcula o Advento/Cristo Rei do ano anterior quando cai em
    // dezembro do ano pedido (ex.: Cristo Rei de novembro do ano corrente
    // ja esta coberto acima; falta o Advento1 de dezembro do ano anterior,
    // que pode cair nos primeiros dias de dezembro do proprio "ano" civil
    // seguinte — mas como calculamos por ano civil, isso já e o esperado).

    eventos.sort(function (a, b) { return a.data - b.data; });
    return eventos;
  }

  function renderizar(dados, ano) {
    const eventos = construirEventosDoAno(dados, ano);
    const porMes = Array.from({ length: 12 }, function () { return []; });
    eventos.forEach(function (ev) { porMes[ev.data.getMonth()].push(ev); });

    const dedicacoes = {};
    (dados.dedicacoes_mensais || []).forEach(function (d) { dedicacoes[d.mes] = d.dedicacao; });

    const pascoa = calcularPascoa(ano);
    elResumo.innerHTML =
      "<p><strong>Ano " + ano + ".</strong> Domingo de Páscoa: " +
      escapar(pascoa.toLocaleDateString("pt-BR", { day: "2-digit", month: "long", year: "numeric" })) +
      ". Quarta-feira de Cinzas: " +
      escapar(somarDias(pascoa, -46).toLocaleDateString("pt-BR", { day: "2-digit", month: "long" })) +
      ". 1.º Domingo do Advento: " +
      escapar(calcularAdvento1(ano).toLocaleDateString("pt-BR", { day: "2-digit", month: "long" })) +
      ".</p>";

    elMeses.innerHTML = porMes
      .map(function (lista, indice) {
        const mes = indice + 1;
        const linhas = lista
          .map(function (ev) {
            return (
              '<tr>' +
              "<td>" + ev.data.getDate() + "</td>" +
              "<td>" + escapar(ev.nome) + (ev.preceito ? ' <span class="calendario__preceito">(preceito)</span>' : "") + "</td>" +
              "<td>" + montarSelo(ev.cor, ev.grau) + "</td>" +
              "</tr>"
            );
          })
          .join("");
        return (
          '<article class="calendario__mes">' +
          "<h3>" + NOMES_MES[indice] + "</h3>" +
          '<p class="calendario__dedicacao">Dedicado a: <strong>' +
          escapar(dedicacoes[mes] || "—") +
          "</strong></p>" +
          (linhas
            ? '<div class="tabela-rolagem"><table><thead><tr><th>Dia</th><th>Celebração</th><th>Cor / grau</th></tr></thead><tbody>' +
              linhas +
              "</tbody></table></div>"
            : '<p class="calendario__vazio">Sem celebrações fixas cadastradas neste mês.</p>') +
          "</article>"
        );
      })
      .join("");
  }

  function iniciar() {
    const hoje = new Date();
    seletorAno.value = hoje.getFullYear();

    carregarDados()
      .then(function (dados) {
        function atualizar() {
          let ano = parseInt(seletorAno.value, 10);
          if (!Number.isFinite(ano) || ano < 1) ano = hoje.getFullYear();
          renderizar(dados, ano);
        }
        seletorAno.addEventListener("change", atualizar);
        seletorAno.addEventListener("input", atualizar);
        botaoHoje.addEventListener("click", function () {
          seletorAno.value = hoje.getFullYear();
          atualizar();
        });
        atualizar();
      })
      .catch(function (erro) {
        elResumo.innerHTML =
          '<p class="liturgia__estado--erro">Não foi possível carregar os dados do calendário (' +
          escapar(erro.message) + ").</p>";
      });
  }

  iniciar();
})();
