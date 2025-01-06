from datetime import date, time

class SlotsDTO:

    def __init__(self, the_date:date, slots: list[tuple[time,time]]):
        self.__the_date = the_date
        self.__slots = slots

    @property
    def the_date(self):
        return self.__the_date

    @property
    def slots(self):
        return self.__slots

    def __eq__(self, other):
        if not isinstance(other, SlotsDTO):
            return False
        return self.__the_date == other.the_date and self.__slots == other.slots

    def __hash__(self):
        # Convert slots list into a tuple (immutable) to make it hashable
        return hash((self.__the_date, tuple(self.__slots)))

    def __str__(self):
        return (f"SlotsDTO("
                f"the_date='{self.__the_date}', "
                f"today_date='{self.__slots}')")

    def __repr__(self):
        return self.__str__()