from abc import ABC, abstractmethod


class NLPResolverInterface(ABC):
    @abstractmethod
    def resolve_intention(self, user_query: str):
        pass
