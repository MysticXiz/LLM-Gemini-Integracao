# 🧠 Processador de Texto com IA

Interface web + API FastAPI integrada ao Gemini para **resumir,
simplificar, explicar e traduzir textos**.

Este projeto combina um frontend simples e moderno com uma API backend
em FastAPI que utiliza o modelo **Gemini 2.5 Flash** para processar
textos. O usuário cola um texto, escolhe uma ação e recebe o resultado
processado pela IA.

------------------------------------------------------------------------

## 🚀 Funcionalidades

### 🔹 Processamento de Texto via IA

O sistema permite quatro operações: - **Resumir** --- Gera um resumo
objetivo do texto. - **Simplificar** --- Reescreve o texto de forma mais
simples. - **Explicar** --- Gera uma explicação clara sobre o
conteúdo. - **Traduzir** --- Tradução automática para inglês.

### 🔹 Interface Web

-   Campo de texto com contador de caracteres\
-   Botões de ação\
-   Animação de loading\
-   Modo claro/escuro automático\
-   Layout responsivo

### 🔹 API Backend

-   Criada com **FastAPI**\
-   Endpoint único: `POST /perguntar`\
-   Integração com `google.generativeai`\
-   Suporte a CORS\
-   Pronto para deploy no Render\
-   Aceita deploy com ou sem frontend estático

------------------------------------------------------------------------

## 🧩 Estrutura do Projeto

    /
    ├── index.html        # Interface do usuário
    ├── styles.css        # Estilos (light/dark mode incluídos)
    ├── script.js         # Lógica frontend e chamada à API
    └── main.py           # Backend FastAPI + integração com Gemini

------------------------------------------------------------------------

## 🛠️ Como Rodar Localmente

### 1. Instale as dependências

``` bash
pip install -r requirements.txt 
```

### 2. Defina sua chave da API do Gemini

``` bash
set GENAI_API_KEY="SUA_CHAVE_AQUI"   # Windows
export GENAI_API_KEY="SUA_CHAVE_AQUI" # Linux/macOS
```

### 3. Inicie o servidor

``` bash
uvicorn main:app --reload
```

A API ficará disponível em:\
👉 **http://localhost:8000/perguntar**

Se quiser testar no navegador, basta abrir o `index.html`.

------------------------------------------------------------------------

## 📡 Endpoint da API

### `POST /perguntar`

#### Corpo da requisição:

``` json
{
  "texto": "seu texto aqui",
  "metodo": "Resumir"
}
```

#### Resposta:

``` json
{
  "resultado": "Texto processado pela IA"
}
```

------------------------------------------------------------------------

## 🌐 Deploy no Render

### Variáveis de Ambiente:

  Nome              Descrição
  ----------------- ----------------------------
  `GENAI_API_KEY`   Sua chave do Google Gemini

### Observações:

-   O backend serve apenas o endpoint `/perguntar`.\
-   Caso deseje deploy único (frontend + backend):
    -   Coloque os arquivos HTML/CSS/JS na pasta `frontend/`\
    -   A app FastAPI serve automaticamente essa pasta.

------------------------------------------------------------------------

## 🧩 Tecnologias Utilizadas

-   FastAPI\
-   Gemini 2.5 Flash (Google Generative AI)\
-   JavaScript / Fetch API\
-   HTML5 / CSS3\
-   CORS Middleware\
-   Render.com (opcional)

------------------------------------------------------------------------

## 📝 Licença

Livre para uso e modificação.
