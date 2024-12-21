from .interfaces import NLPResolverInterface


class OpenAINLPResolver(NLPResolverInterface):
    def resolve_intention(self, user_query: str):
        print(f'resolving intention for user_query = {user_query}')
        return "pass"