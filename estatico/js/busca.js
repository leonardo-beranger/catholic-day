/* Barra de pesquisa do cabecalho — busca por tema em todas as paginas.
 *
 * Le uma vez /dados/busca.json (gerado pelo build.py a partir dos titulos
 * h2/h3/h4 de cada pagina) e filtra em memoria, no navegador — sem backend,
 * sem dependencia externa. Casa por substring, ignorando maiusculas e
 * acentos, contra titulo + resumo + nome da pagina.
 */

(function () {
  "use strict";

  const raiz = document.getElementById("busca");
  if (!raiz) return;

  const input = document.getElementById("busca-input");
  const lista = document.getElementById("busca-resultados");
  const MAX_RESULTADOS = 8;
  const MIN_CARACTERES = 2;

  let indice = null; // carregado sob demanda, uma unica vez
  let carregando = null;
  let indiceAtivo = -1;

  function normalizar(texto) {
    return texto
      .normalize("NFD")
      .replace(/[̀-ͯ]/g, "")
      .toLowerCase();
  }

  function carregarIndice() {
    if (indice) return Promise.resolve(indice);
    if (carregando) return carregando;
    const url = (window.BASE_PATH || "") + "/dados/busca.json";
    carregando = fetch(url)
      .then(function (resp) { return resp.ok ? resp.json() : []; })
      .then(function (dados) {
        indice = dados.map(function (item) {
          return Object.assign({}, item, { _busca: normalizar(item.titulo + " " + item.resumo + " " + item.pagina) });
        });
        return indice;
      })
      .catch(function () { return (indice = []); });
    return carregando;
  }

  function marcar(texto, termo) {
    if (!termo) return texto;
    const normTexto = normalizar(texto);
    const pos = normTexto.indexOf(termo);
    if (pos === -1) return texto;
    return (
      texto.slice(0, pos) +
      "<mark>" + texto.slice(pos, pos + termo.length) + "</mark>" +
      texto.slice(pos + termo.length)
    );
  }

  function renderizar(resultados, termo) {
    if (!resultados.length) {
      lista.innerHTML = '<li class="busca__vazio">Nada encontrado.</li>';
      lista.hidden = false;
      return;
    }
    lista.innerHTML = resultados
      .map(function (item, i) {
        return (
          '<li>' +
          '<a href="' + (window.BASE_PATH || "") + item.url + '" data-indice="' + i + '">' +
          '<span class="busca__resultado-titulo">' + marcar(item.titulo, termo) + '</span>' +
          '<span class="busca__resultado-pagina">' + item.pagina + '</span>' +
          (item.resumo ? '<span class="busca__resultado-resumo">' + marcar(item.resumo, termo) + '</span>' : "") +
          '</a>' +
          '</li>'
        );
      })
      .join("");
    lista.hidden = false;
    indiceAtivo = -1;
  }

  function buscar(termoBruto) {
    const termo = normalizar(termoBruto.trim());
    if (termo.length < MIN_CARACTERES) {
      lista.hidden = true;
      lista.innerHTML = "";
      return;
    }
    carregarIndice().then(function (dados) {
      const resultados = [];
      for (let i = 0; i < dados.length && resultados.length < MAX_RESULTADOS; i++) {
        if (dados[i]._busca.indexOf(termo) !== -1) resultados.push(dados[i]);
      }
      renderizar(resultados, termo);
    });
  }

  let temporizador = null;
  input.addEventListener("input", function () {
    clearTimeout(temporizador);
    const valor = input.value;
    temporizador = setTimeout(function () { buscar(valor); }, 150);
  });

  input.addEventListener("focus", function () {
    if (input.value.trim().length >= MIN_CARACTERES && lista.innerHTML) lista.hidden = false;
  });

  input.addEventListener("keydown", function (evento) {
    const itens = lista.querySelectorAll("a");
    if (evento.key === "Escape") {
      lista.hidden = true;
      input.blur();
      return;
    }
    if (!itens.length) return;
    if (evento.key === "ArrowDown") {
      evento.preventDefault();
      indiceAtivo = Math.min(indiceAtivo + 1, itens.length - 1);
      itens[indiceAtivo].focus();
    } else if (evento.key === "ArrowUp") {
      evento.preventDefault();
      indiceAtivo = Math.max(indiceAtivo - 1, 0);
      itens[indiceAtivo].focus();
    }
  });

  lista.addEventListener("keydown", function (evento) {
    if (evento.key === "Escape") {
      lista.hidden = true;
      input.focus();
    }
  });

  document.addEventListener("click", function (evento) {
    if (!raiz.contains(evento.target)) lista.hidden = true;
  });
})();
