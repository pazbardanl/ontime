from abc import ABC, abstractmethod
from src.model import IntentionDTO


class NLPResolverInterface(ABC):
    @abstractmethod
    def resolve_intention(self, user_query: str) -> IntentionDTO:
        pass
