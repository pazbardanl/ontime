from .interfaces import QueryResolverInterface


class QueryResolver(QueryResolverInterface):
    def resolve_user_query(self, user_query: str):
        print(f'user_query = {user_query}')
        pass