import pytest
from datetime import date, time

from unittest.mock import Mock
from src.services import QueryResolver
from src.services.interfaces import NLPResolverInterface, ScheduleProviderInterface, AvailabilityResolverInterface, SlotsFinderInterface
from src.model import IntentionDTO, SlotsDTO


class TestQueryResolver:
    __USER_QUERY_CHECK_AVAILABILITY = 'am i free tomorrow morning?'
    __INTENTION_DTO_CHECK_AVAILABILITY = IntentionDTO(
        query=__USER_QUERY_CHECK_AVAILABILITY,
        today_date='2025-01-01',
        today_weekday='Wednesday',
        intention='check_availability',
        target_date='2025-01-02',
        target_time_frame='8:00-12:00')
    __USER_QUERY_PROPOSE_SLOTS = 'propose slots for a 1hr meeting tomorrow morning'
    __INTENTION_DTO_PROPOSE_SLOTS = IntentionDTO(
                                query=__USER_QUERY_PROPOSE_SLOTS,
                                today_date='2025-01-01',
                                today_weekday='Wednesday',
                                intention='propose_slots',
                                target_date='2025-01-02',
                                target_time_frame='8:00-12:00',
                                target_slot_duration_hrs='1')
    __SLOTS_DTO = SlotsDTO(date(2025, 1, 2), [(time(8, 0), time(10, 0)), ((time(11, 30), time(13, 0)), (time(15, 0), time(17, 15)))])
    __EXPECTED_RESPONSE_CHECK_AVAILABILITY = 'No, you are busy tomorrow 8am till 10am, and also you have a meeting starting at 11am until 1pm'
    __EXPECTED_RESPONSE_PROPOSE_SLOTS = 'Sure, you can have a free 1.5 hour slot from 10am till 11:30am'

    def setup_method(self):
        mock_nlp_resolver = Mock(spec=NLPResolverInterface)
        mock_schedule_provider = Mock(spec=ScheduleProviderInterface)
        mock_availability_resolver = Mock(spec=AvailabilityResolverInterface)
        mock_slots_finder = Mock(spec=SlotsFinderInterface)
        mock_nlp_resolver.resolve_intention.side_effect = self.__mock_resolve_intention
        mock_schedule_provider.get_busy_slots_for_date.side_effect = self.__mock_get_busy_slots_for_date
        mock_availability_resolver.check_availability.side_effect = self.__mock_check_availability
        mock_slots_finder.find_slots.side_effect = self.__mock_find_slots
        self.__query_resolver = QueryResolver(mock_nlp_resolver, mock_schedule_provider, mock_availability_resolver,
                                       mock_slots_finder)

    def test_check_availability(self):
        actual_response = self.__query_resolver.resolve_user_query(self.__USER_QUERY_CHECK_AVAILABILITY)
        assert self.__EXPECTED_RESPONSE_CHECK_AVAILABILITY == actual_response

    def test_propose_slots(self):
        actual_response = self.__query_resolver.resolve_user_query(self.__USER_QUERY_PROPOSE_SLOTS)
        assert self.__EXPECTED_RESPONSE_PROPOSE_SLOTS == actual_response


    def __mock_resolve_intention(self, user_query: str):
        if user_query == self.__USER_QUERY_CHECK_AVAILABILITY:
            return self.__INTENTION_DTO_CHECK_AVAILABILITY
        elif user_query == self.__USER_QUERY_PROPOSE_SLOTS:
            return self.__INTENTION_DTO_PROPOSE_SLOTS
        else:
            raise ValueError(f"'__mock_resolve_intention failed, unexpected user_query:{user_query}")

    def __mock_get_busy_slots_for_date(self, target_date:str):
        if target_date == '2025-01-02':
            return self.__SLOTS_DTO
        else:
            raise ValueError(f"'__mock_get_busy_slots_for_date failed, unexpected target_date:{target_date}")

    def __mock_check_availability(self, intention_dto:IntentionDTO, slots_dto:SlotsDTO):
        if intention_dto == self.__INTENTION_DTO_CHECK_AVAILABILITY and slots_dto == self.__SLOTS_DTO:
            return self.__EXPECTED_RESPONSE_CHECK_AVAILABILITY
        else:
            raise ValueError(f"'__mock_check_availability failed, unexpected intention_dto X slots_dto combination:{intention_dto}, {slots_dto}")

    def __mock_find_slots(self, intention_dto:IntentionDTO, slots_dto:SlotsDTO):
        if intention_dto == self.__INTENTION_DTO_PROPOSE_SLOTS and slots_dto == self.__SLOTS_DTO:
            return self.__EXPECTED_RESPONSE_PROPOSE_SLOTS
        else:
            raise ValueError(f"'__mock_find_slots failed, unexpected intention_dto X slots_dto combination:{intention_dto}, {slots_dto}")