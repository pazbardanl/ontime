from src.services.interfaces import QueryResolverInterface
from src.services.interfaces import NLPResolverInterface
from src.services import QueryResolver
from src.services import OpenAINLPResolver


def get_nlp_resolver() -> NLPResolverInterface:
    return OpenAINLPResolver()


def get_query_resolver() -> QueryResolverInterface:
    return QueryResolver(get_nlp_resolver())
