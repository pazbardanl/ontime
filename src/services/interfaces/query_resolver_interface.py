from abc import ABC, abstractmethod


class QueryResolverInterface(ABC):
    @abstractmethod
    def resolve_user_query(self, user_query: str) -> str:
        pass