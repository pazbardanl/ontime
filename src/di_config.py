from src.services.interfaces import QueryResolverInterface
from src.services.interfaces import NLPResolverInterface
from src.services.interfaces import OpenAIClientWrapperInterface
from src.services import QueryResolver
from src.services import OpenAINLPResolver
from src.services import OpenAIClientWrapper


def get_openai_client_wrapper() -> OpenAIClientWrapperInterface:
    return OpenAIClientWrapper()

def get_nlp_resolver() -> NLPResolverInterface:
    return OpenAINLPResolver(get_openai_client_wrapper())


def get_query_resolver() -> QueryResolverInterface:
    return QueryResolver(get_nlp_resolver())
