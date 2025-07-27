const URLServidor = "http://localhost:8000";
const visor = document.getElementById("visor");
const botoes = document.querySelectorAll(".botao[data-valor]");
const botaoIgual = document.querySelector(".botao-igual");
const botaoLixeira = document.querySelector(".botao-lixeira");
const idUsuario = document.body.dataset.id_usuario;

let expressao = "";

botoes.forEach(botao => {
    botao.addEventListener("click", () => {
        const valor = botao.dataset.valor;

        if (valor === "C") {
            expressao = "";
            visor.textContent = "0";
        } else if (valor === "±") {
            const partes = expressao.match(/(-?\d+\.?\d*)$/);
            if (partes) {
                const numeroAtual = partes[0];
                const inicio = expressao.slice(0, expressao.length - numeroAtual.length);
                const numeroInvertido = numeroAtual.startsWith("-")
                    ? numeroAtual.slice(1)
                    : "-" + numeroAtual;
                expressao = inicio + numeroInvertido;
                visor.textContent = expressao;
            }
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
    expressao     = resultado;
        visor.textContent = resultado;
        registrarOperacao(expressaoCalculada, resultado);
    } catch (erro) {
        visor.textContent = "Erro";
    }
});

botaoLixeira.addEventListener("click", apagarHistorico);

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
    for (operacao of data.operacoes) {
        listaHistorico.innerHTML += `
        <li class="operacao">
        ${operacao.parametros
            .replace(/\//g, "÷")
            .replace(/\*/g, "×")
            .replace(/-/g, "−")}
            =${operacao.resultado}    ${formatarDataBrasil(operacao.dt_inclusao)}
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

function formatarDataBrasil(dataISO) {
    const [ano, mes, dia] = dataISO.split("-");
    return `${dia}/${mes}/${ano}`;
}

async function apagarHistorico() {
    await fetch(`${URLServidor}/calculadora/deletar_operacoes_usuario/${idUsuario}/`, {
        method: "delete",
        headers: {
            "Accept": "application/json"
        }
    });
    await atualizarHistorico();
}