Extrator de Dados de Folhas de Pagamento
Uma API para extração automática de dados de folhas de pagamento em formato PDF, com um frontend de exemplo em React para interação e download dos resultados em formato Excel.

✨ Funcionalidades
Upload de Arquivos: Interface web para upload de arquivos PDF.

Backend Robusto: API construída com Flask (Python) para o processamento dos arquivos.

Extração de Dados: Lógica de extração de dados estruturados (Matrícula, Nome, Cargo, Salário, Impostos, etc.) usando expressões regulares.

Geração de Planilhas: Criação e download de planilhas Excel (.xlsx) com os dados extraídos.

Frontend Interativo: Interface de usuário construída com React para uma experiência moderna.

Arquitetura Expansível: Projetado para ser facilmente estendido para suportar múltiplos modelos e layouts de PDF no futuro.

🏗️ Arquitetura
O projeto é dividido em duas partes independentes que se comunicam através de uma API REST:

Backend (API Flask):

Responsável por receber o arquivo PDF.

Executa a lógica de extração de texto e parsing dos dados.

Gera o arquivo Excel em memória.

Devolve o arquivo gerado para o frontend, pronto para download.

Frontend (Aplicação React):

Fornece a interface gráfica para o usuário.

Permite que o usuário selecione e envie o arquivo PDF para a API.

Gerencia a comunicação com o backend e aciona o download do arquivo Excel quando o processamento termina.

🛠️ Pré-requisitos
Antes de começar, garanta que você tenha os seguintes softwares instalados:

Python (versão 3.8 ou superior)

Node.js e npm (v16 ou superior)

Git

⚙️ Instalação e Configuração
Siga os passos abaixo para configurar o ambiente de desenvolvimento local.

Clone o repositório:

Bash

git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
Configuração do Backend (Flask):

Bash

# Navegue até a pasta da API (ex: api_extrator)
cd api_extrator

# Crie e ative um ambiente virtual
python -m venv venv
# No Windows:
venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
Configuração do Frontend (React):

Bash

# Navegue até a pasta do frontend (ex: meu-frontend)
cd ../meu-frontend

# Instale as dependências
npm install
🚀 Como Executar
Para rodar a aplicação, você precisará de dois terminais abertos simultaneamente.

Terminal 1 - Executando o Backend:

Bash

# Na pasta da API (api_extrator)
# Certifique-se de que o ambiente virtual está ativado
python app.py
O servidor Flask estará rodando em http://127.0.0.1:5000.

Terminal 2 - Executando o Frontend:

Bash

# Na pasta do frontend (meu-frontend)
npm start
Uma nova aba no seu navegador abrirá automaticamente com a aplicação React em http://localhost:3000.

📖 Documentação da API
Endpoint: /api/extract-and-download
Método: POST

Descrição: Recebe um arquivo PDF, extrai os dados dos funcionários e retorna um arquivo Excel para download.

Corpo da Requisição: multipart/form-data

file: O arquivo PDF a ser processado.

Resposta de Sucesso (200 OK):

Um arquivo dados_extraidos.xlsx é enviado como anexo para download.

Respostas de Erro:

400 Bad Request: Se nenhum arquivo for enviado ou se o arquivo não for um PDF.

JSON

{"erro": "Nenhum arquivo enviado"}
404 Not Found: Se o PDF for processado, mas nenhum dado for encontrado (provavelmente o modelo do PDF é incorreto).

JSON

{"erro": "Nenhum dado foi extraído..."}
📂 Estrutura do Projeto
.
├── api_extrator/             # Pasta do Backend
│   ├── venv/
│   ├── app.py                # Servidor Flask e rotas da API
│   ├── extrator.py           # Lógica de extração do PDF
│   └── requirements.txt      # Dependências do Python
│
├── meu_frontend/             # Pasta do Frontend
│   ├── node_modules/
│   ├── public/
│   ├── src/
│   │   ├── App.css
│   │   └── App.js            # Componente principal do React
│   └── package.json          # Dependências do Node.js
│
└── README.md                 # Este arquivo
📜 Licença
Distribuído sob a licença MIT. Veja LICENSE para mais informações.
