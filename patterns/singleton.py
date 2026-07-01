"""
Padrão GoF: Singleton
---------------------
Garante que AppConfigService tenha apenas uma instância em toda a aplicação.
Usado como serviço central de logging e acesso a configurações do Django.

Princípio D (SOLID): módulos de alto nível dependem desta abstração de serviço,
não de chamadas diretas a logging.getLogger() ou settings espalhadas pelo código.
"""
import logging


class AppConfigService:
    """Serviço único de configuração e logging (Singleton GoF).

    Uso:
        from patterns.singleton import app_config
        app_config.log_info("Pet criado com sucesso")
    """

    # --- Singleton: armazena a instância única ---
    _instance = None

    def __new__(cls):
        # Cria a instância apenas uma vez; reutiliza nas chamadas seguintes
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.logger = logging.getLogger('get_a_pet')

    # --- Interface pública ---

    def log_info(self, message: str) -> None:
        self.logger.info(message)

    def log_warning(self, message: str) -> None:
        self.logger.warning(message)

    def log_error(self, message: str) -> None:
        self.logger.error(message)

    @property
    def media_url(self) -> str:
        from django.conf import settings
        return settings.MEDIA_URL

    @property
    def debug(self) -> bool:
        from django.conf import settings
        return settings.DEBUG


# Instância global — importar esta variável em vez de instanciar diretamente
app_config = AppConfigService()
