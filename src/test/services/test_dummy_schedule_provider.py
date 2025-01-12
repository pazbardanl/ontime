from datetime import date, time
from src.services.dummy_schedule_provider import DummyScheduleProvider
from src.model import SlotsDTO


class TestDummyScheduleProvider:

    def setup_method(self):
        self.__dummy_schedule_provider = DummyScheduleProvider()

    def test_get_busy_slots_for_date_sunday(self):
        self.__test_date(date(2025, 1, 12), [])

    def test_get_busy_slots_for_date_monday(self):
        self.__test_date(date(2025, 1, 13), [(time(0, 0), time(9, 0))])

    def test_get_busy_slots_for_date_tuesday(self):
        self.__test_date(date(2025, 1, 14), [(time(0, 0), time(9, 0)), (time(14, 0), time(15, 0)), (time(21, 30), time(23, 59))])

    def test_get_busy_slots_for_date_wednesday(self):
        self.__test_date(date(2025, 1, 15), [(time(0, 0), time(9, 0)), (time(15, 0), time(17, 0)), (time(21, 30), time(23, 59))])

    def test_get_busy_slots_for_date_thursday(self):
        self.__test_date(date(2025, 1, 16), [(time(0, 0), time(9, 0)), (time(16, 0), time(19, 0))])

    def test_get_busy_slots_for_date_friday(self):
        self.__test_date(date(2025, 1, 17), [(time(0, 0), time(9, 0)), (time(17, 0), time(21, 0))])

    def test_get_busy_slots_for_date_saturday(self):
        self.__test_date(date(2025, 1, 18), [])

    def __test_date(self, the_date:date, expected_slots: list[tuple[time,time]]):
        actual_slots_dto = self.__dummy_schedule_provider.get_busy_slots_for_date(the_date)
        expected_slots_dto = SlotsDTO(the_date, expected_slots)
        assert expected_slots_dto == actual_slots_dto
