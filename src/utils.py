# Configurações de Rede Padrão
SERVER_NAME = "127.0.0.1"
SERVER_PORT = 1205
BUFFER_SIZE = 4096

# Cores ANSI e Estilos Visuais para o Terminal
C_RESET = "\033[0m"
C_CYAN = "\033[96m"
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_RED = "\033[91m"
C_DIM = "\033[2m"
B_BOLD = "\033[1m"


def sanitize_input(text: str) -> str:
    # Remove caracteres perigosos para protocolos baseados em delimitadores (|)
    return text.replace("|", "").replace("\n", " ").strip()

def print_box(title: str, content: str, color: str = C_GREEN) -> None:
    width = max(len(title), len(content), 40)

    separator = "=" * width
    
    print(f"{color}{separator}")
    print(f"│ [{title.upper()}] │")
    print(f"{separator}")
    print(f"│ {content} │")
    print(f"{separator}{C_RESET}\n")
