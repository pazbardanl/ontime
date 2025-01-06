from abc import ABC, abstractmethod
from src.model import IntentionDTO
from src.model import SlotsDTO


class SlotsFinderInterface(ABC):
    @abstractmethod
    def find_slots(self, intention_dto: IntentionDTO, slots_dto: SlotsDTO) -> str:
        pass
