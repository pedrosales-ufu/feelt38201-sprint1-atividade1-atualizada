# Importa o módulo socket para gerenciar conexões TCP
from socket import socket, AF_INET, SOCK_STREAM
# Importa as utilidades compartilhadas
from utils import (
    SERVER_PORT, BUFFER_SIZE,
    C_CYAN, C_GREEN, C_RED, C_RESET, B_BOLD
)


def main() -> None:
    # Cria o socket do servidor utilizando o gerenciador de contexto 'with'
    with socket(AF_INET, SOCK_STREAM) as server_socket:  # AF_INET: Família IPv4 | SOCK_STREAM: TCP
        # Vincula a porta do servidor por meio do método bind()
        server_socket.bind(('', SERVER_PORT))

        # Coloca o servidor em modo de escuta com listen()
        server_socket.listen(5)

        print(f"{C_CYAN}{B_BOLD}=== SERVIDOR CONTADOR DE PALAVRAS ATIVO (TCP) ==={C_RESET}")
        print("[INFO] Aguardando conexões de texto...\n")

        try:
            # Laço principal para aceitar conexões TCP consecutivas
            while True:
                # Aceita a conexão do cliente com accept(), gerando um socket dedicado (connection_socket)
                connection_socket, client_address = server_socket.accept()
                print(f"[CONEXÃO] Handshake estabelecido com {client_address[0]}")

                try:
                    # Loop interno: mantém a sessão ativa para múltiplos envios do mesmo cliente na mesma conexão
                    while True:
                        # Recebe os dados do texto enviado pelo cliente via stream TCP com recv()
                        text_bytes = connection_socket.recv(BUFFER_SIZE)
                        
                        # Se não há bytes, significa que o cliente fechou a conexão (FIN), então sai do loop
                        if not text_bytes:
                            break

                        text = text_bytes.decode("utf-8")

                        # Regra de negócio: Divide o texto por espaços em branco para contar as palavras
                        words = text.split()
                        word_count = len(words)
                        char_count = len(text)

                        # Monta a mensagem de resposta estatística
                        response_msg = f"Palavras: {word_count} | Caracteres: {char_count}"

                        print(f"{C_GREEN}[PROCESSADO] Texto de {char_count} chars analisado ({word_count} palavras) de {client_address[0]}.{C_RESET}")

                        # Envia de volta o resultado garantido pela conexão TCP utilizando send()
                        connection_socket.send(response_msg.encode("utf-8"))

                except (ValueError, UnicodeDecodeError) as e:
                    print(f"{C_RED}[ALERTA] Erro ao processar texto de {client_address[0]}: {e}{C_RESET}")
                    error_msg = "Status: ERRO | Falha no processamento do texto."
                    connection_socket.send(error_msg.encode("utf-8"))

                finally:
                    # Fecha obrigatoriamente o socket de conexão específico deste cliente ao término da sessão
                    connection_socket.close()
                    print(f"[DESCONEXÃO] Sessão com {client_address[0]} encerrada de forma limpa.\n")

        except KeyboardInterrupt:
            print(f"\n{C_RED}[!] Servidor contador encerrado com segurança.{C_RESET}")


if __name__ == "__main__":
    main()
