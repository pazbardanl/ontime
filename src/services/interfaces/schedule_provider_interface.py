from abc import ABC, abstractmethod
from datetime import date
from src.model.slots_dto import SlotsDTO


class ScheduleProviderInterface(ABC):
    @abstractmethod
    def get_busy_slots_for_date(self, the_date: date) -> SlotsDTO:
        pass
