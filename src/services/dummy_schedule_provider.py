from datetime import date, time

from src.services.interfaces import ScheduleProviderInterface
from src.model import SlotsDTO

class DummyScheduleProvider(ScheduleProviderInterface):

    def get_busy_slots_for_date(self, the_date: date) -> SlotsDTO:
        return SlotsDTO(the_date, self.__get_slots(the_date))

    def __get_slots(self, the_date:date) -> list[tuple[time,time]]:
        weekday = the_date.weekday()
        if weekday == 0: # Monday
            return [(time(0, 0), time(9, 0))]
        elif weekday == 1: # Tuesday
            return [(time(0, 0), time(9, 0)), (time(14, 0), time(15, 0)), (time(21, 30), time(23, 59))]
        elif weekday == 2: # Wednesday
            return [(time(0, 0), time(9, 0)), (time(15, 0), time(17, 0)), (time(21, 30), time(23, 59))]
        elif weekday == 3: # Thursday
            return [(time(0, 0), time(9, 0)), (time(16, 0), time(19, 0))]
        elif weekday == 4: # Friday
            return [(time(0, 0), time(9, 0)), (time(17, 0), time(21, 0))]
        else: # 5-6, Saturday-Sunday
            return []