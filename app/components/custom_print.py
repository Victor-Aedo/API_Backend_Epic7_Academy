class Style:
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# Códigos de formato ANSI para cambiar el color del texto
class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'


def custom_print(*args, **kwargs):
    if not args:
        print(Color.RED + Style.BOLD + Style.UNDERLINE + "Print:  La variable está vacía (None).")
    elif all(isinstance(arg, str) and not arg for arg in args):
        print(Color.RED + Style.BOLD + Style.UNDERLINE + "Print:  El argumento es una cadena vacía.")
    else:
        # Imprime los argumentos normales de la función print
        print(Color.CYAN + Style.BOLD + Style.UNDERLINE + "Print:  ", *args, **kwargs)