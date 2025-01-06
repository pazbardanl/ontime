from .interfaces import QueryResolverInterface
from .interfaces import NLPResolverInterface
from .interfaces import ScheduleProviderInterface
from .interfaces import AvailabilityResolverInterface
from .interfaces import SlotsFinderInterface
from ..model.intention_enum import Intention
from ..model.intention_dto import IntentionDTO
from ..model.slots_dto import SlotsDTO

class QueryResolver(QueryResolverInterface):

    def __init__(self, nlp_resolver: NLPResolverInterface,
                 schedule_provider: ScheduleProviderInterface,
                 availability_resolver: AvailabilityResolverInterface,
                 slots_finder: SlotsFinderInterface):
        self.__nlp_resolver = nlp_resolver
        self.__schedule_provider = schedule_provider
        self.__availability_resolver = availability_resolver
        self.__slots_finder = slots_finder

    def resolve_user_query(self, user_query: str) -> str:
        print(f'user_query = {user_query}')
        intention_dto = self.__nlp_resolver.resolve_intention(user_query)
        print(f'intention_dto = {intention_dto}')
        target_date = intention_dto.target_date
        slots_dto = self.__schedule_provider.get_busy_slots_for_date(target_date)
        print(f'slots_dto = {slots_dto}')
        response = self.__handle_intention(intention_dto, slots_dto)
        print(f'response = {response}')
        return response

    def __handle_intention(self, intention_dto: IntentionDTO, slots_dto: SlotsDTO):
        intention_string = intention_dto.intention
        intention_enum_item = Intention.from_string(intention_string)
        if intention_enum_item == Intention.CHECK_AVAILABILITY:
            return self.__handle_check_availability(intention_dto, slots_dto)
        elif intention_enum_item == Intention.PROPOSE_SLOTS:
            return self.__handle_propose_slots(intention_dto, slots_dto)
        else:
            raise ValueError(f"intention string '{intention_string}' cannot be handled")

    def __handle_check_availability(self, intention_dto:IntentionDTO, slots_dto:SlotsDTO) -> str:
        return self.__availability_resolver.check_availability(intention_dto, slots_dto)

    def __handle_propose_slots(self, intention_dto:IntentionDTO, slots_dto:SlotsDTO) -> str:
        return self.__slots_finder.find_slots(intention_dto, slots_dto)