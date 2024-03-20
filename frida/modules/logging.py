from colorama import init, Fore, Style
from datetime import datetime

def setup_logging():
    init()

    logging.basicConfig(level=logging.DEBUG, format=Fore.YELLOW + '%(asctime)s' + Fore.GREEN + ' - %(levelname)s - ' + Fore.CYAN + '%(message)s' + Style.RESET_ALL)
    debug_formatter = logging.Formatter(Fore.YELLOW + '[%(asctime)s]' + Fore.GREEN + '- [%(levelname)s] -' + Fore.CYAN + '[%(message)s]' + Style.RESET_ALL)
    info_formatter = logging.Formatter(Fore.GREEN + '[%(asctime)s]' + Fore.GREEN + '- [%(levelname)s] -' + Fore.CYAN + '[%(message)s]' + Style.RESET_ALL)
    error_formatter = logging.Formatter(Fore.RED + Style.BRIGHT + '[%(asctime)s]' + Fore.GREEN + '- [%(levelname)s] -' + Fore.CYAN + '[%(message)s]' + Style.RESET_ALL)
    warning_formatter = logging.Formatter(Fore.YELLOW + '[%(asctime)s]' + Fore.GREEN + '- [%(levelname)s] -' + Fore.CYAN + '[%(message)s]' + Style.RESET_ALL)

    debug_handler = logging.FileHandler('logs/debug.log')
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(debug_formatter)
    info_handler = logging.FileHandler('logs/info.log')
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(info_formatter)
    error_handler = logging.FileHandler('logs/error.log')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(error_formatter)
    warning_handler = logging.FileHandler('logs/warning.log')
    warning_handler.setLevel(logging.WARNING)
    warning_handler.setFormatter(warning_formatter)
    logger = logging.getLogger()
    logger.addHandler(debug_handler)
    logger.addHandler(info_handler)
    logger.addHandler(error_handler)
    logger.addHandler(warning_handler)
