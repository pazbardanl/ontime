from abc import ABC, abstractmethod


class QueryResolverInterface(ABC):
    @abstractmethod
    def resolve_user_query(self, userQuery: str):
        pass