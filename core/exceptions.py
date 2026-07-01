"""Handler global de exceções para respostas de erro em português."""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """Padroniza todas as respostas de erro com mensagem em português."""
    response = exception_handler(exc, context)

    if response is None:
        return Response(
            {'message': 'Erro interno do servidor. Tente novamente mais tarde.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if response.status_code == status.HTTP_401_UNAUTHORIZED:
        response.data = {'message': 'Acesso não autorizado. Por favor, faça login.'}
    elif response.status_code == status.HTTP_403_FORBIDDEN:
        response.data = {'message': 'Você não tem permissão para realizar esta ação.'}
    elif response.status_code == status.HTTP_404_NOT_FOUND:
        response.data = {'message': 'Recurso não encontrado.'}
    elif response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
        response.data = {'message': 'Método não permitido.'}

    return response
