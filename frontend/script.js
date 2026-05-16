const textInput = document.getElementById('textInput');
const charCount = document.getElementById('charCount');
const buttons = document.querySelectorAll('.btn-action');
const outputSection = document.getElementById('outputSection');
const outputMethod = document.getElementById('outputMethod');
const outputContent = document.getElementById('outputContent');
const apiUrl = '/perguntar';
const modelSelect = document.getElementById('modelSelect');

// Atualizar contagem de caracteres
textInput.addEventListener('input', () => {
    charCount.textContent = textInput.value.length;
});

// Buscar modelos disponíveis ao carregar a página
async function fetchModels() {
    console.log('Iniciando busca de modelos...');
    try {
        const response = await fetch('/modelos');
        console.log('Resposta recebida:', response);
        const data = await response.json(); // Ler o corpo da resposta
        console.log('Dados recebidos (corpo):', data);
        if (data.modelos) {
            const defaultOption = document.getElementById('modelSelect').querySelector('option');
            if (defaultOption) {
                defaultOption.remove(); // Remover a opção de carregamento
            }
            data.modelos.forEach(modelo => {
                const option = document.createElement('option');
                option.value = modelo;
                option.textContent = modelo;
                modelSelect.appendChild(option);
            });
        } else {
            console.error('Nenhum modelo disponível:', data);
        }
    } catch (error) {
        console.error('Erro ao buscar modelos:', error);
    }
}
fetchModels();

// Adicionar listeners aos botões
buttons.forEach(button => {
    button.addEventListener('click', async () => {
        const texto = textInput.value.trim();
        const metodo = button.getAttribute('data-method');
        if (!texto) {
            showError('Por favor, insira um texto antes de processar.');
            return;
        }
        await processText(texto, metodo);
    });
});

async function processText(texto, metodo) {
    const modeloSelecionado = modelSelect.value;
    buttons.forEach(btn => btn.disabled = true);
    outputMethod.textContent = `${metodo}...`;
    outputContent.innerHTML = '<div class="loading"><div class="spinner"></div> Processando...</div>';
    outputSection.classList.add('visible');
    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                texto: texto,
                metodo: metodo,
                modelo: modeloSelecionado
            })
        });
        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status}`);
        }
        const data = await response.json();
        outputMethod.textContent = `✓ ${metodo}`;
        outputContent.innerHTML = data.resultado || 'Nenhum resultado retornado.';
        console.log('Dados recebidos (corpo):', data);
    } catch (error) {
        console.error('Erro:', error);
        outputContent.innerHTML = `<div class="error">Erro ao processar: ${error.message}</div>`;
    } finally {
        buttons.forEach(btn => btn.disabled = false);
    }
}

function showError(message) {
    outputMethod.textContent = 'Atenção';
    outputContent.innerHTML = `<div class="error">${message}</div>`;
    outputSection.classList.add('visible');
}