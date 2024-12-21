from src.services.interfaces import QueryResolverInterface
from src.services import QueryResolver


def get_query_resolver() -> QueryResolverInterface:
    return QueryResolver()
