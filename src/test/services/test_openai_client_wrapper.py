import pytest
import json

from src.services.openai_client_wrapper import OpenAIClientWrapper

class TestOpenAIClientWrapper:

    CHECK_AVAILABILITY = 'check_availability'
    PROPOSE_SLOTS = 'propose_slots'

    def setup_method(self):
        self.__openai_client_wrapper = OpenAIClientWrapper()

    # [I] intention:    [C] check_availability, [P] propose_slots
    # [S] start time:   [u] unspecified, [12h] specified 12h, [24h] specified 24h, [V] verbal
    # [E] end time:     [u] unspecified, [12h] specified 12h, [24h] specified 24h, [V] verbal
    # [D] duration:     [u] unspecified, [hrs] specified hrs, [mins] specified mins

    # I   S   E   D
    # -------------

    # # C   u   u   u
    # def test__check_availability__no_start__no_end__no_duration(self):
    #     self.__test_user_query('am i free on Sunday?', self.CHECK_AVAILABILITY, '8:00-20:00', 'NA', True)
    #
    # # C   12h u   u
    # def test__check_availability__start_12h__no_end__no_duration(self):
    #     self.__test_user_query('am i free on Sunday at 3pm?', self.CHECK_AVAILABILITY, '15:00', 'NA', True)
    #
    # # C   24h u   u
    # def test__check_availability__start_24h__no_end__no_duration(self):
    #     self.__test_user_query('am i free on Sunday at 15:30?', self.CHECK_AVAILABILITY, '15:30', 'NA', True)
    #
    # # C   V   u   u
    # def test__check_availability__start_verbal__no_end__no_duration(self):
    #     self.__test_user_query('am i free on Sunday at half three in the afternoon?', self.CHECK_AVAILABILITY, '15:30', 'NA', True)
    #
    # # C   u   12h u
    # def test__check_availability__no_start__end_12hr__no_duration(self):
    #     self.__test_user_query('am i free on Sunday till 1pm?', self.CHECK_AVAILABILITY, '8:00-13:00', 'NA', True)
    #
    # # C   12h 12h u
    # def test__check_availability__start_12hr__end_12hr__no_duration(self):
    #     self.__test_user_query('am i available Monday 9am till 1pm?', self.CHECK_AVAILABILITY, '9:00-13:00', 'NA', True)
    #
    # # C   24h 12h u
    # def test__check_availability__start_24hr__end_12hr__no_duration(self):
    #     self.__test_user_query('am i available Monday 7:30 till 1pm?', self.CHECK_AVAILABILITY, '7:30-13:00', 'NA', True)
    #
    # # C   V   12h u
    # def test__check_availability__start_verbal__end_12hr__no_duration(self):
    #     self.__test_user_query('am i available Tuesday from seven in the morning till 1pm?', self.CHECK_AVAILABILITY, '7:00-13:00', 'NA', True)
    #
    # # C   u   24h u
    # def test__check_availability__no_start__end_24hr__no_duration(self):
    #     self.__test_user_query('am i free on Sunday till 14:45?', self.CHECK_AVAILABILITY, '8:00-14:45', 'NA', True)
    #
    # # C   12h 24h u
    # def test__check_availability__start_12hr__end_24hr__no_duration(self):
    #     self.__test_user_query('am i free on Sunday 11:15am till 14:45?', self.CHECK_AVAILABILITY, '11:15-14:45', 'NA', True)
    #
    # # C   24h 24h u
    # def test__check_availability__start_24hr__end_24hr__no_duration(self):
    #     self.__test_user_query('am i free on Sunday 11:15 till 14:45?', self.CHECK_AVAILABILITY, '11:15-14:45', 'NA', True)
    #
    # # C   V   24h u
    # def test__check_availability__start_verbal__end_24hr__no_duration(self):
    #     self.__test_user_query('am i free on Sunday from six thirty in the morning till 20:15?', self.CHECK_AVAILABILITY, '6:30-20:15', 'NA', True)
    #
    # # C   u   V   u
    # def test__check_availability__no_start__end_verbal__no_duration(self):
    #     self.__test_user_query('am i available this Wednesday till quarter after five in the afternoon?', self.CHECK_AVAILABILITY, '8:00-17:15', 'NA', True)
    #
    # # C   12h V   u
    # def test__check_availability__start_12h__end_verbal__no_duration(self):
    #     self.__test_user_query('am i available this Wednesday from 10:20am till half past five in the afternoon?', self.CHECK_AVAILABILITY, '10:20-17:30', 'NA', True)
    #
    # # C   24h V   u
    # def test__check_availability__start_24h__end_verbal__no_duration(self):
    #     self.__test_user_query('am i available this Wednesday from 15:50am till half past four in the afternoon?', self.CHECK_AVAILABILITY, '15:50-16:30', 'NA', True)
    #
    # # C   V   V   u
    # def test__check_availability__start_verbal__end_verbal__no_duration(self):
    #     self.__test_user_query('am i available this Wednesday from seven thirty till twenty to four in the afternoon?', self.CHECK_AVAILABILITY, '7:30-15:40', 'NA', True)
    #
    # # C   u   u   hrs
    # def test__check_availability__no_start__no_end__duration_hrs(self):
    #     self.__test_user_query('am i available this Wednesday for 2 hours?', self.CHECK_AVAILABILITY, '8:00-20:00', '2', True)
    #
    # # C   12h u   hrs
    # def test__check_availability__start_12hrs__no_end__duration_hrs(self):
    #     self.__test_user_query('am i available this Monday from 2:30pm for an hour?', self.CHECK_AVAILABILITY, '14:30-15:30', '1', True)
    #
    # # C   24h u   hrs
    # def test__check_availability__start_24hrs__no_end__duration_hrs(self):
    #     self.__test_user_query('am i available this Monday from 15:25 for an hour?', self.CHECK_AVAILABILITY, '15:25-16:25', '1', True)
    #
    # # C   V   u   hrs
    # def test__check_availability__start_verbal__no_end__duration_hrs(self):
    #     self.__test_user_query('am i free for breakfast next Monday from nine fifteen in the morning for an hour and a half?', self.CHECK_AVAILABILITY, '9:15-10:45', '1.5', True)
    #
    # # C   u   12h hrs
    # def test__check_availability__no_start__end_12hr__duration_hrs(self):
    #     self.__test_user_query('can i have a meeting next Saturday until 10am for an hour and a half?', self.CHECK_AVAILABILITY, '8:00-10:00', '1.5', True)
    #
    # # C   12h 12h hrs
    # def test__check_availability__start_12hr__end_12hr__duration_hrs(self):
    #     self.__test_user_query('can i have a 1 hour meeting next Friday between 10am and 2pm?', self.CHECK_AVAILABILITY, '10:00-14:00', '1', True)
    #
    # # C   24h 12h hrs
    # def test__check_availability__start_24hr__end_12hr__duration_hrs(self):
    #     self.__test_user_query('can I schedule a 2-hours meeting tomorrow between 14:30 and 6pm?', self.CHECK_AVAILABILITY, '14:30-18:00', '2', True)
    #
    # # C   V   12h hrs
    # def test__check_availability__start_verbal__end_12hr__duration_hrs(self):
    #     self.__test_user_query('am I available next Monday for 2 hours from nine in the morning till 6pm?', self.CHECK_AVAILABILITY, '9:00-18:00', '2', True)
    #
    # # C   u   24h hrs
    # def test__check_availability__no_start__end_24hr__duration_hrs(self):
    #     self.__test_user_query('am I free tomorrow till 13:00 for half an hour?', self.CHECK_AVAILABILITY, '8:00-13:00', '0.5', True)
    #
    # # C   12h 24h hrs
    # def test__check_availability__start_12hrs__end_24hr__duration_hrs(self):
    #     self.__test_user_query('do I have time for a quick lunch of half an hour with mom day after tomorrow between 12pm and 14:00?', self.CHECK_AVAILABILITY, '12:00-14:00', '0.5', True)
    #
    # # C   24h 24h hrs
    # def test__check_availability__start_24hrs__end_24hr__duration_hrs(self):
    #     self.__test_user_query('do I have time for a quick lunch of half an hour with mom day after tomorrow between 12:00 and 14:00?', self.CHECK_AVAILABILITY, '12:00-14:00', '0.5', True)
    #
    # # C   V   24h hrs
    # def test__check_availability__start_verbal__end_24hr__duration_hrs(self):
    #     self.__test_user_query('can I schedule a 3 hours session from noon till 21:00?', self.CHECK_AVAILABILITY, '12:00-21:00', '3', True)
    #
    # # C   u   V   hrs
    # def test__check_availability__no_start__end_verbal__duration_hrs(self):
    #     self.__test_user_query('can I schedule a 3 hours session from noon till ten in the evening?', self.CHECK_AVAILABILITY, '12:00-22:00', '3', True)
    #
    # # C   12h V   hrs
    # def test__check_availability__start_12h__end_verbal__duration_hrs(self):
    #     self.__test_user_query('am I free for a 2.5 hrs conference tomorrow from 12:30pm till eight thirty in the evening?', self.CHECK_AVAILABILITY, '12:30-20:30', '2.5', True)
    #
    # # C   24h V   hrs
    # def test__check_availability__start_24h__end_verbal__duration_hrs(self):
    #     self.__test_user_query('am I free for a 2.5 hrs conference tomorrow from 12:30 till eight thirty in the evening?', self.CHECK_AVAILABILITY, '12:30-20:30', '2.5', True)
    #
    # # C   V   V   hrs
    # def test__check_availability__start_verbal__end_verbal__duration_hrs(self):
    #     self.__test_user_query('am I free for a 4 hrs conference tomorrow from noon till midnight?', self.CHECK_AVAILABILITY, '12:00-23:59', '4', True)

    # # C   u   u   min
    # def test__check_availability__no_start__no_end__duration_min(self):
    #     self.__test_user_query('am i available this Wednesday for 120 minutes?', self.CHECK_AVAILABILITY, '8:00-20:00', '2', True)
    #
    # # C   12h u   min
    # def test__check_availability__start_12hrs__no_end__duration_min(self):
    #     self.__test_user_query('am i available this Monday from 2:30pm for 60 mins?', self.CHECK_AVAILABILITY, '14:30-15:30', '1', True)
    #
    # # C   24h u   min
    # def test__check_availability__start_24hrs__no_end__duration_min(self):
    #     self.__test_user_query('am i available this Monday from 15:25 for an 60 minutes?', self.CHECK_AVAILABILITY, '15:25-16:25', '1', True)
    #
    # # C   V   u   min
    # def test__check_availability__start_verbal__no_end__duration_min(self):
    #     self.__test_user_query('am i free for breakfast next Monday from nine fifteen in the morning for ninety minutes?', self.CHECK_AVAILABILITY, '9:15-10:45', '1.5', True)
    #
    # # C   u   12h min
    # def test__check_availability__no_start__end_12hr__duration_min(self):
    #     self.__test_user_query('can i have a meeting next Saturday until 10am for an 90 minutes?', self.CHECK_AVAILABILITY, '8:00-10:00', '1.5', True)
    #
    # # C   12h 12h min
    # def test__check_availability__start_12hr__end_12hr__duration_min(self):
    #     self.__test_user_query('can i have a sixty minutes meeting next Friday between 10am and 2pm?', self.CHECK_AVAILABILITY, '10:00-14:00', '1', True)
    #
    # # C   24h 12h min
    # def test__check_availability__start_24hr__end_12hr__duration_min(self):
    #     self.__test_user_query('can I schedule a 120 mins meeting tomorrow between 14:30 and 6pm?', self.CHECK_AVAILABILITY, '14:30-18:00', '2', True)
    #
    # # C   V   12h min
    # def test__check_availability__start_verbal__end_12hr__duration_min(self):
    #     self.__test_user_query('am I available next Monday for 120 minutes from nine in the morning till 6pm?', self.CHECK_AVAILABILITY, '9:00-18:00', '2', True)
    #
    # # C   u   24h min
    # def test__check_availability__no_start__end_24hr__duration_min(self):
    #     self.__test_user_query('am I free tomorrow till 13:00 for thirty minutes?', self.CHECK_AVAILABILITY, '8:00-13:00', '0.5', True)
    #
    # # C   12h 24h min
    # def test__check_availability__start_12hrs__end_24hr__duration_min(self):
    #     self.__test_user_query('do I have time for a quick lunch of thirty minutes with mom day after tomorrow between 12pm and 14:00?', self.CHECK_AVAILABILITY, '12:00-14:00', '0.5', True)
    #
    # # C   24h 24h min
    # def test__check_availability__start_24hrs__end_24hr__duration_min(self):
    #     self.__test_user_query('do I have time for a quick lunch of thirty minutes with mom day after tomorrow between 12:00 and 14:00?', self.CHECK_AVAILABILITY, '12:00-14:00', '0.5', True)
    #
    # # C   V   24h min
    # def test__check_availability__start_verbal__end_24hr__duration_min(self):
    #     self.__test_user_query('can I schedule a 180 minutes session from noon till 21:00?', self.CHECK_AVAILABILITY, '12:00-21:00', '3', True)
    #
    # # C   u   V   min
    # def test__check_availability__no_start__end_verbal__duration_min(self):
    #     self.__test_user_query('can I schedule a one hundred and eighty minutes session from noon till ten in the evening?', self.CHECK_AVAILABILITY, '12:00-22:00', '3', True)
    #
    # # C   12h V   min
    # def test__check_availability__start_12h__end_verbal__duration_min(self):
    #     self.__test_user_query('am I free for a 150 mins conference tomorrow from 12:30pm till eight thirty in the evening?', self.CHECK_AVAILABILITY, '12:30-20:30', '2.5', True)
    #
    # # C   24h V   min
    # def test__check_availability__start_24h__end_verbal__duration_min(self):
    #     self.__test_user_query('am I free for a 150 minutes conference tomorrow from 12:30 till eight thirty in the evening?', self.CHECK_AVAILABILITY, '12:30-20:30', '2.5', True)
    #
    # # C   V   V   min
    # def test__check_availability__start_verbal__end_verbal__duration_min(self):
    #     self.__test_user_query('am I free for a 240 mins hrs conference tomorrow from noon till midnight?', self.CHECK_AVAILABILITY, '12:00-23:59', '4', True)

    def __test_user_query(self,
                          user_query,
                          expected_intention,
                          expected_target_time_frame,
                          expected_target_slot_duration_hrs,
                          debug = False):
        intention_actual_json_str = self.__openai_client_wrapper.resolve_intention(user_query)
        intention_actual_json = json.loads(intention_actual_json_str)
        self.__assert_intention_response(user_query, expected_intention, expected_target_time_frame, expected_target_slot_duration_hrs, intention_actual_json, debug)

    def __assert_intention_response(self,
                                    expected_query,
                                    expected_intention,
                                    expected_target_time_frame,
                                    expected_target_slot_duration_hrs,
                                    actual,
                                    debug = False):
        if debug:
            print(f'[D] actual = {actual}')
        assert expected_query == actual["query"], "query mismatch"
        assert expected_intention == actual["intention"], "intention mismatch"
        assert expected_target_time_frame == actual["target_time_frame"], "target_time_frame mismatch"
        assert expected_target_slot_duration_hrs == actual["target_slot_duration_hrs"], "target_slot_duration_hrs mismatch"

