"""
Padrão GoF: Strategy — Upload de Imagem
-----------------------------------------
Permite trocar o destino de armazenamento de imagens (local / nuvem)
sem alterar o chamador. Atualmente implementa armazenamento local via
ImageField do Django. Estender adicionando, por exemplo, S3Strategy.

Princípio O (SOLID): novas estratégias de storage não exigem modificar
o código existente — apenas adicionar uma nova classe concreta.
"""
from abc import ABC, abstractmethod


class ImageUploadStrategy(ABC):
    """Interface base para estratégias de upload de imagem."""

    @abstractmethod
    def get_upload_path(self, subfolder: str, filename: str) -> str:
        """Retorna o caminho de destino do arquivo dentro de MEDIA_ROOT."""


class LocalImageUploadStrategy(ImageUploadStrategy):
    """Salva imagens na pasta MEDIA_ROOT/<subfolder>/ (padrão local)."""

    def get_upload_path(self, subfolder: str, filename: str) -> str:
        return f'{subfolder}/{filename}'


class ImageUploadContext:
    """Contexto que delega o cálculo do caminho à estratégia configurada.

    Uso:
        ctx = ImageUploadContext()                     # usa estratégia local
        path = ctx.resolve_path('pets', 'foto.jpg')
    """

    def __init__(self, strategy: ImageUploadStrategy | None = None):
        # Princípio D (SOLID): dependência injetada; padrão é local
        self._strategy: ImageUploadStrategy = strategy or LocalImageUploadStrategy()

    def set_strategy(self, strategy: ImageUploadStrategy) -> None:
        self._strategy = strategy

    def resolve_path(self, subfolder: str, filename: str) -> str:
        return self._strategy.get_upload_path(subfolder, filename)
