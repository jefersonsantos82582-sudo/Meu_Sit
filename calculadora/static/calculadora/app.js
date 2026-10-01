// Frontend em JavaScript da calculadora.
// Conversa com o backend Django (Python) pelo endpoint /api/calcular/.

const form = document.getElementById('calc-form');
const campoX = document.getElementById('x');
const campoY = document.getElementById('y');
const campoOp = document.getElementById('op');
const saida = document.getElementById('resultado');
const painelHistorico = document.getElementById('historico');
const listaHistorico = document.getElementById('historico-lista');

function mostrarResultado(valor, erro) {
  if (!saida) return;
  saida.textContent = 'Resultado: ' + valor;
  saida.classList.toggle('erro', Boolean(erro));
}

// O backend devolve o resultado pronto; aqui so formatamos para a tela.
async function calcular(x, y, op) {
  const resposta = await fetch('/api/calcular/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ x: x, y: y, op: op }),
  });
  const dados = await resposta.json();
  if (!resposta.ok) {
    throw new Error(dados.erro || 'Falha ao calcular');
  }
  return dados;
}

async function carregarHistorico() {
  if (!listaHistorico) return;
  try {
    const resposta = await fetch('/api/historico/');
    const dados = await resposta.json();
    listaHistorico.innerHTML = '';
    (dados.calculos || []).forEach(function (item) {
      const li = document.createElement('li');
      li.textContent = item.expressao + ' = ' + item.resultado;
      listaHistorico.appendChild(li);
    });
    painelHistorico.hidden = !(dados.calculos || []).length;
  } catch (e) {
    painelHistorico.hidden = true;
  }
}

if (form) {
  form.addEventListener('submit', async function (evento) {
    evento.preventDefault();
    const x = campoX.value.trim();
    const y = campoY.value.trim();
    if (x === '' || y === '') {
      mostrarResultado('Erro', true);
      return;
    }
    try {
      const dados = await calcular(Number(x), Number(y), campoOp.value);
      mostrarResultado(dados.resultado, dados.erro);
      carregarHistorico();
    } catch (e) {
      mostrarResultado(e.message || 'Erro', true);
    }
  });
}

carregarHistorico();
