from enum import Enum


class Intention(Enum):
    CHECK_AVAILABILITY = "check_availability"
    PROPOSE_SLOTS = "propose_slots"

    @classmethod
    def from_string(cls, value:str):
        for item in cls:
            if item.name == value or item.value == value:
                return item
        raise ValueError(f"unrecognized intention string:'{value}'")