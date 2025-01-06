from abc import ABC, abstractmethod
from src.model import IntentionDTO
from src.model import SlotsDTO


class AvailabilityResolverInterface(ABC):
    @abstractmethod
    def check_availability(self, intention_dto: IntentionDTO, slots_dto: SlotsDTO) -> str:
        pass
