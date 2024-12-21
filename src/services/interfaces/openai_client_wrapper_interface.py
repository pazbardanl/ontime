from abc import ABC, abstractmethod


class OpenAIClientWrapperInterface(ABC):

    @abstractmethod
    def resolve_intention(self, user_query:str):
        pass
