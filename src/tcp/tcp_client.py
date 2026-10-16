# Importa o módulo socket para conexões TCP orientadas a fluxo
from socket import socket, AF_INET, SOCK_STREAM
# Importa o módulo sys para controle de saída
import sys
# Importa as utilidades compartilhadas
from utils import (
    SERVER_NAME, SERVER_PORT, BUFFER_SIZE,
    C_CYAN, C_GREEN, C_YELLOW, C_RED, C_RESET, C_DIM, B_BOLD,
    sanitize_input, print_box
)


def main() -> None:
    print(f"{C_CYAN}{B_BOLD}=== CONTADOR DE PALAVRAS REMOTO (TCP) ==={C_RESET}")

    try:
        # Cria o socket TCP com SOCK_STREAM utilizando o gerenciador 'with'
        with socket(AF_INET, SOCK_STREAM) as client_socket:  # AF_INET: IPv4 | SOCK_STREAM: TCP
            # Conecta ao servidor por meio do método connect() (realiza o 3-way handshake uma única vez)
            client_socket.connect((SERVER_NAME, SERVER_PORT))
            print(f"{C_DIM}[Conexão TCP estabelecida com sucesso com o servidor]{C_RESET}\n")

            # Laço de repetição da sessão persistente
            while True:
                # Solicita a entrada de texto do usuário
                raw_text = input(f"{C_YELLOW}Digite o texto (ou 'sair') > {C_RESET}")
                
                # Verifica se o usuário deseja encerrar a sessão
                if raw_text.strip().lower() == "sair":
                    print(f"{C_RED}Encerrando sessão TCP. Até logo!{C_RESET}")
                    break

                # Valida e higieniza o texto inserido
                text = sanitize_input(raw_text)
                if not text:
                    print(f"{C_RED}[!] O texto não pode estar vazio.{C_RESET}\n")
                    continue

                # Envia o texto digitado convertido em bytes através do método send() na stream existente
                client_socket.send(text.encode("utf-8"))

                # Aguarda a resposta estatística do servidor pelo método recv()
                response_bytes = client_socket.recv(BUFFER_SIZE)
                if not response_bytes:
                    print(f"{C_RED}[ERRO] O servidor encerrou a conexão inesperadamente.{C_RESET}")
                    break

                result = response_bytes.decode("utf-8")

                # Exibe o resultado formatado no terminal usando a caixa utilitária
                print_box("Resultado da Contagem (TCP)", result, C_GREEN)

    except ConnectionRefusedError:
        print(f"\n{C_RED}[ERRO] Servidor de contagem offline ou recusou a conexão.{C_RESET}")
    except KeyboardInterrupt:
        print(f"\n{C_RED}[!] Operação cancelada pelo usuário.{C_RESET}")
        sys.exit(0)


if __name__ == "__main__":
    main()
