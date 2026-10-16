# FEELT38201 - Sprint 1 - 1ª Atividade Avaliativa - Sockets

Aluno: Pedro dos Santos Sales

Este repositório apresenta a solução desenvolvida para a primeira atividade avaliativa da disciplina FEELT38201 - Segurança WEB, estruturada de forma modular conforme a organização abaixo:

```
feelt38201-sprint1-atividade1-atualizada/
├── src/
│   ├── tcp/
│   │   ├── tcp_client.py
│   │   └── tcp_server.py
│   ├── udp/
│   │   ├── udp_client.py
│   │   └── udp_server.py
│   └── utils.py
└── README.md
```

---

## 1. Arquitetura Modular e Componentes Compartilhados (`utils.py`)

Com o objetivo de seguir o princípio de separação de responsabilidades (*Separation of Concerns*) e padronizar o layout visual dos terminais, as configurações globais de rede e as funções auxiliares de formatação foram centralizadas em um módulo comum (`utils.py`).

### 1.1. Organização e Implementação
- **Constantes Globais de Rede:**
  - `SERVER_NAME`: Define o endereço de loopback (`127.0.0.1`), mantendo o tráfego isolado na máquina local.
  - `SERVER_PORT`: Estabelece a porta padrão (`1205`) compartilhada entre os serviços para escuta e comunicação.
  - `BUFFER_SIZE`: Determina o limite de leitura de blocos de bytes (`4096` bytes), garantindo espaço suficiente para os payloads e datagramas.
- **Estética ANSI:** Uso de códigos de escape ANSI (`C_GREEN`, `C_CYAN`, `C_YELLOW`, `C_RED`, `C_DIM`, `B_BOLD`) para colorir a interface de terminal, fornecendo um feedback visual claro sobre o status das operações.
- **Função `sanitize_input(text)`:** Trata as entradas fornecidas pelo usuário, removendo quebras de linha acidentais (`\n`) e caracteres delimitadores (`|`) para preservar a integridade da mensagem.
- **Função `print_box(title, content, color)`:** Desenha painéis formatados no terminal, calculando dinamicamente a largura ideal com base no texto para garantir um alinhamento simétrico.

---

## 2. Aplicação Cliente-Servidor Baseada em UDP (Serviço de Consulta de Hora)

Esta implementação baseia-se nos conceitos de programação de sockets UDP apresentados na Seção 2.7.1 do livro de Kurose & Ross. O projeto foca em leveza, baixo *overhead* e transações diretas, dispensando o estabelecimento prévio de conexões.

### 2.1. Arquitetura e Dinâmica do Cliente (`udp_client.py`)
- **Dependências:** Importa o módulo `socket` com suporte a datagramas (`SOCK_DGRAM`) em IPv4 (`AF_INET`), além do módulo `sys` para controle de execução.
- **Gerenciamento de Contexto (`with`):** O socket é aberto com um gerenciador de contexto, garantindo que os recursos do sistema sejam liberados automaticamente ao encerrar.
- **Modelo Sem Estado (*Stateless*):** O cliente envia mensagens de forma avulsa, sem manter uma sessão contínua. O usuário dispara as requisições pressionando `[ENTER]`.
- **Envio (`sendto`):** A string `"GET_TIME"` é codificada em UTF-8 e enviada diretamente informando a tupla de destino (endereço IP e porta do servidor).
- **Recepção (`recvfrom`):** O cliente aguarda o retorno do datagrama, decodifica os bytes recebidos e os exibe de forma estilizada na tela.

### 2.2. Arquitetura e Dinâmica do Servidor (`udp_server.py`)
- **Dependências:** Utiliza as bibliotecas `socket`, `datetime` (para capturar o horário atual do sistema) e os utilitários visuais.
- **Associação de Porta (`bind`):** O socket do servidor vincula-se à porta padrão (`1205`) em todas as interfaces locais disponíveis (`''`), ficando pronto para escutar requisições.
- **Escuta Contínua:** Permanece ativo em um laço infinito (`while True`), aguardando pacotes de qualquer cliente.
- **Tratamento de Origem e Resposta (`recvfrom` / `sendto`):** O servidor captura os dados e o endereço de origem (`client_address`). Após validar a requisição e consultar o relógio, ele envia a resposta de volta ao cliente correto. Exceções inesperadas, como bytes corrompidos que gerem `UnicodeDecodeError`, são tratadas de forma defensiva para evitar a queda do serviço.

### 2.3. Análise do Modelo UDP
- **Esforço Máximo (*Best-Effort*):** O protocolo não assegura entrega garantida ou ordenação de pacotes na camada de transporte.
- **Transações Independentes:** Cada consulta de horário funciona como um evento isolado, ideal para aplicações simples e de alta velocidade.

---

## 3. Aplicação Cliente-Servidor Baseada em TCP (Serviço de Contagem de Palavras)

A aplicação TCP segue os fundamentos da Seção 2.7.2 de Kurose & Ross, garantindo a entrega confiável e ordenada de um fluxo contínuo de bytes (*stream*) por meio de uma sessão persistente.

### 3.1. Arquitetura e Dinâmica do Cliente (`tcp_client.py`)
- **Dependências:** Importa o módulo `socket` configurado para fluxos orientados à conexão (`SOCK_STREAM`).
- **Estabelecimento de Conexão (*3-Way Handshake*):** O cliente invoca o método `connect()`, disparando a apresentação de três vias com o servidor para firmar um canal lógico confiável.
- **Sessão Persistente:** Um laço interno permite o envio de múltiplos blocos de texto sequenciais pela mesma conexão estabelecida, evitando o custo de reabrir canais a cada interação.
- **Transmissão e Recepção (`send` / `recv`):** Os dados tratados são enviados como um fluxo de bytes e o cliente aguarda o retorno estatístico do servidor.
- **Encerramento Controlado:** Ao receber o comando `'sair'`, a conexão é fechada de maneira limpa, enviando o sinalizador `FIN` na camada de transporte.

### 3.2. Arquitetura e Dinâmica do Servidor (`tcp_server.py`)
- **Escuta Passiva (`bind` e `listen`):** O socket principal se vincula à porta `1205` e entra em modo de escuta com `listen(5)`, organizando uma fila para novas conexões.
- **Aceitação e Isolamento (`accept`):** Ao receber uma solicitação, o servidor executa `accept()`, gerando um socket dedicado (`connection_socket`) exclusivo para aquele cliente, mantendo o socket principal livre para atender outros.
- **Sessão e Término:** Um loop secundário gerencia as interações do cliente conectado até que o fluxo retorne vazio (`not text_bytes`), indicando o encerramento da sessão (`FIN`).
- **Processamento e Fechamento (`finally`):** O texto recebido é dividido por espaços (`text.split()`) para computar as estatísticas de palavras e caracteres, retornando o resultado ao cliente. O bloco `finally` garante o fechamento adequado do socket de conexão (`connection_socket.close()`).

### 3.3. Análise do Modelo TCP
- **Confiabilidade Orientada a Fluxo:** O TCP gerencia a ordenação e a recuperação de pacotes perdidos de forma transparente na camada de transporte.
- **Sessões Dedicadas:** O uso de sockets específicos para cada cliente reflete a arquitetura ideal para serviços que exigem precisão absoluta e comunicação contínua. 
