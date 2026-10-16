# Importa o módulo socket para comunicação de rede em Python
from socket import socket, AF_INET, SOCK_DGRAM
# Importa o módulo sys para controle de saída do programa
import sys
# Importa as utilidades compartilhadas de rede e estética
from utils import (
    SERVER_NAME, SERVER_PORT, BUFFER_SIZE,
    C_CYAN, C_GREEN, C_YELLOW, C_RED, C_RESET, C_DIM, B_BOLD,
    print_box
)


def main() -> None:
    print(f"{C_CYAN}{B_BOLD}=== CLIENTE DE HORA CERTA (UDP) ==={C_RESET}")
    print(f"Pressione {B_BOLD}[ENTER]{C_RESET} para solicitar o horário do servidor, ou digite 'sair'.\n")

    # Utiliza o gerenciador de contexto 'with' para gerenciar o ciclo de vida do socket UDP
    try:
        with socket(AF_INET, SOCK_DGRAM) as client_socket:  # AF_INET: IPv4 | SOCK_DGRAM: UDP
            while True:
                cmd = input(f"{C_YELLOW}Solicitar hora certa? (Enter/sair) > {C_RESET}").strip().lower()
                if cmd == "sair":
                    print(f"{C_RED}Encerrando cliente. Até logo!{C_RESET}")
                    break
                    
                # Se o usuário digitar qualquer outra coisa (que não seja Enter vazio), avisa e pede de novo
                if cmd != "":
                    print(f"{C_RED}[!] Comando inválido. Pressione apenas [ENTER] para buscar a hora ou 'sair'.{C_RESET}\n")
                    continue

                # Mensagem de requisição enviada ao servidor
                request_msg = "GET_TIME"

                # Envia o pacote UDP diretamente via sendto() sem necessidade de conexão prévia
                client_socket.sendto(request_msg.encode("utf-8"), (SERVER_NAME, SERVER_PORT))
                print(f"{C_DIM}[UDP] Requisição enviada. Aguardando resposta...{C_RESET}")

                # Recebe a resposta do servidor e o endereço de origem via recvfrom()
                response_bytes, _ = client_socket.recvfrom(BUFFER_SIZE)
                server_time = response_bytes.decode("utf-8")

                # Exibe o resultado utilizando a função de caixa estilizada compartilhada
                print_box("Serviço de Hora (UDP)", server_time, C_GREEN)

    except KeyboardInterrupt:
        print(f"\n{C_RED}[!] Cliente interrompido pelo usuário.{C_RESET}")
        sys.exit(0)


if __name__ == "__main__":
    main()
