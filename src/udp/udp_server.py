# Importa o módulo socket para comunicação UDP
from socket import socket, AF_INET, SOCK_DGRAM
# Importa o módulo datetime para recuperar a data e hora atual do sistema
from datetime import datetime
# Importa as utilidades compartilhadas
from utils import (
    SERVER_PORT, BUFFER_SIZE,
    C_CYAN, C_GREEN, C_RED, C_YELLOW, C_RESET, B_BOLD
)


def main() -> None:
    # Cria o socket do servidor com o gerenciador de contexto 'with'
    with socket(AF_INET, SOCK_DGRAM) as server_socket:  # AF_INET: Família IPv4. SOCK_DGRAM: Socket UDP
        # Vincula a porta a todas as interfaces de rede locais por meio do método bind()
        server_socket.bind(('', SERVER_PORT))

        print(f"{C_CYAN}{B_BOLD}=== SERVIDOR DE HORA CERTA ATIVO (UDP) ==={C_RESET}")
        print(f"[PRONTO] Aguardando requisições de tempo na porta {SERVER_PORT}...\n")

        try:
            # Laço infinito para escutar e responder pacotes UDP de forma contínua
            while True:
                # Recebe os dados brutos e o endereço do cliente através de recvfrom()
                message_bytes, client_address = server_socket.recvfrom(BUFFER_SIZE)

                try:
                    query = message_bytes.decode("utf-8").strip()

                    # Valida se a requisição é válida
                    if query != "GET_TIME":
                        raise ValueError("Comando desconhecido.")

                    # Captura o horário exato do sistema operacional
                    current_time_str = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
                    payload = f"Data/Hora: {current_time_str}"

                    # Envia a resposta de volta ao cliente específico usando sendto()
                    server_socket.sendto(payload.encode("utf-8"), client_address)

                    print(f"{C_YELLOW}[RESPONDIDO] Horário enviado para {client_address[0]}:{client_address[1]} -> {current_time_str}{C_RESET}")

                except (ValueError, UnicodeDecodeError) as e:
                    print(f"{C_RED}[ALERTA] Requisição UDP inválida recebida de {client_address[0]}: {e}{C_RESET}")

        except KeyboardInterrupt:
            print(f"\n{C_RED}[!] Servidor de hora encerrado.{C_RESET}")


if __name__ == "__main__":
    main()
