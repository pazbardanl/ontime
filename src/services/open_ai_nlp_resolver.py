from .interfaces import NLPResolverInterface
from .interfaces import OpenAIClientWrapperInterface


class OpenAINLPResolver(NLPResolverInterface):

    def __init__(self, openai_client_wrapper:OpenAIClientWrapperInterface):
        self.__openai_client_wrapper = openai_client_wrapper

    def resolve_intention(self, user_query: str):
        print(f'resolving intention for user_query = {user_query}')
        return self.__openai_client_wrapper.resolve_intention(user_query)