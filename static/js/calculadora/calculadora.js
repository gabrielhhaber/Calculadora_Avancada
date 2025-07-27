const URLServidor = "http://localhost:8000";
const visor = document.getElementById("visor");
const botoes = document.querySelectorAll(".botao[data-valor]");
const botaoIgual = document.querySelector(".botao-igual");
const idUsuario = document.body.dataset.idUsuario;

let expressao = "";

botoes.forEach(botao => {
    botao.addEventListener("click", () => {
        const valor = botao.dataset.valor;

        if (valor === "C") {
            expressao = "";
            visor.textContent = "0";
        } else {
            expressao += valor;
            visor.textContent = expressao;
        }
    });
});

botaoIgual.addEventListener("click", (evento) => {
    const expressaoCalculada = expressao
        .replace(/÷/g, "/")
        .replace(/×/g, "*")
        .replace(/−/g, "-");

    try {
        const resultado = eval(expressaoCalculada);
        registrarOperacao(expressaoCalculada, resultado);
    } catch (erro) {
        visor.textContent = "Erro";
    }
});

atualizarHistorico();

async function atualizarHistorico() {
    const listaHistorico = document.getElementById("lista-historico");
    const response = await fetch(`${URLServidor}/calculadora/listar_operacoes_usuario/${idUsuario}/`, {
        method: "get",
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    });
    const data = await response.json();
    listaHistorico.innerHTML = "";
    for (operacao of listaHistorico.operacoes) {
        listaHistorico.innerHTML += `
        <li class="operacao">
        ${operacao.parametros}=${operacao.resultado}
        </li>
        `;
    }
}

async function registrarOperacao(parametros, resultado) {
    const response = await fetch(`${URLServidor}/calculadora/registrar_operacao/`, 
        {
        method: "post",
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        body: JSON.stringify({id_usuario: idUsuario, parametros: parametros, resultado: resultado})
    });
    await atualizarHistorico();
}