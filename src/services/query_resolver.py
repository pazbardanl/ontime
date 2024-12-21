from .interfaces import QueryResolverInterface
from .interfaces import NLPResolverInterface


class QueryResolver(QueryResolverInterface):
    def __init__(self, nlp_resolver: NLPResolverInterface):
        self.__nlp_resolver = nlp_resolver

    def resolve_user_query(self, user_query: str):
        print(f'user_query = {user_query}')
        intention = self.__nlp_resolver.resolve_intention(user_query)
        print(f'intention = {intention}')
        pass