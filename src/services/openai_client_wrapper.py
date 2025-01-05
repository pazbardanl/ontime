from datetime import date
from openai import OpenAI
from .interfaces import OpenAIClientWrapperInterface

class OpenAIClientWrapper(OpenAIClientWrapperInterface):
    MODEL = "gpt-4o-mini"
    DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    def __init__(self):
        self.__openai_client = OpenAI()

    def resolve_intention(self, user_query:str):
        completion = self.__get_nlp_completion(user_query)
        return completion.choices[0].message.content

    def _get_nlp_system_content(self):
        today = date.today()
        day_of_the_week = self.DAYS[today.weekday()]
        print(f"today = {today}, day_of_the_week = {day_of_the_week}")
        return f"""
            You are an intelligent assistant specialized in resolving user queries related to availability and scheduling. Your task is to process queries and respond with a JSON string that includes the following fields (all strings):
            - `today_date`: The current date in "YYYY-MM-DD" format.
            - `today_weekday`: The current day of the week (e.g., "Monday").
            - `intention`: Either "check_availability" or "propose_slots", based on the user query.
            - `target_date`: A specific date mentioned in the query in "YYYY-MM-DD" format.
            - `target_time_frame`: The time range or time of day related to the query.
            - `target_slot_duration_hrs`: The duration of the time slot in hours.
            
            ### Behavior:
            1. For queries about checking availability (e.g., "Am I free on 1.1.2025 from 8 AM till 2 PM"):
               - Set `intention` to "check_availability".
               - Parse the `target_date` from the query.
               - Determine `target_time_frame` based on the scenario:
                 - **Start time only:** Return a single time (e.g., "13:00").
                 - **Explicit start and end time:** Return a pair of times (e.g., "13:00-14:30").
                 - **Start time with duration (hours):** Convert to a time range (e.g., "13:00-14:30").
                 - **Start time with duration (minutes):** Convert to a time range (e.g., "13:00-14:30").
                 - **Time of day:** Return a predefined range (e.g., "8:00-12:00" for "morning").
               - Set `target_slot_duration_hrs` based on the query: if the query specify a target time frame that is larger than the requested slot, then state the slot duration in hours. 
                    If the time frame is smaller than the slot duration then the slot should be ignored ("NA"). if slot duration is not stated in the query then it should be "NA".
            
            2. For queries about proposing time slots (e.g., "When can I meet for 30 minutes on 1.1.2025 between 9 AM and 1 PM"):
               - Set `intention` to "propose_slots".
               - Parse the `target_date` from the query.
               - Determine `target_time_frame` as described above.
               - Parse the slot duration in hours and set it in `target_slot_duration_hrs`.
               - Note propose_slots scenario is relevant only when user explicitly asks to propose, recommend or suggest slots. otherwise default to check_availability
            
            ### Time of Day Mapping:
            - Early morning: "5:00-8:00"
            - Morning: "8:00-12:00"
            - Noon: "12:00-16:00"
            - Afternoon: "16:00-18:00"
            - Evening: "18:00-22:00"
            - Night: "22:00-5:00"
            
            ### Examples:
            
            Example 1:
            Query: "Am I free on 1.1.2025 from 8 AM till 2 PM?"
            Response:
            {{
                "query": "Am I free on 1.1.2025 from 8 AM till 2 PM?",
                "today_date": "2023-12-21",
                "today_weekday": "Thursday",
                "intention": "check_availability",
                "target_date": "2025-01-01",
                "target_time_frame": "8:00-14:00",
                "target_slot_duration_hrs": "NA"
            }}
            
            Example 2: Query: "When can I meet for 30 minutes on 1.1.2025 between 9 AM and 1 PM?" 
            Response:
            {{
                "query": "When can I meet for 30 minutes on 1.1.2025 between 9 AM and 1 PM?",
                "today_date": "2023-12-21",
                "today_weekday": "Thursday",
                "intention": "propose_slots",
                "target_date": "2025-01-01",
                "target_time_frame": "9:00-13:00",
                "target_slot_duration_hrs": "0.5"
            }}
            
            Example 3: Query: "Am I free tomorrow morning?" 
            Response:
            {{
                "query": "Am I free tomorrow morning?",
                "today_date": "2023-12-21",
                "today_weekday": "Thursday",
                "intention": "check_availability",
                "target_date": "2023-12-22",
                "target_time_frame": "8:00-12:00",
                "target_slot_duration_hrs": "NA"
            }}
            
            Example 4: Query: "When can I meet for 1 hour in the evening on 1.1.2025?" 
            Response:
            {{
                "query": "When can I meet for 1 hour in the evening on 1.1.2025?"
                "today_date": "2023-12-21",
                "today_weekday": "Thursday",
                "intention": "propose_slots",
                "target_date": "2025-01-01",
                "target_time_frame": "18:00-22:00",
                "target_slot_duration_hrs": "1"
            }}

            Example 5: Query: "can i meet for 30 minutes next Sunday at noon?" 
            Response:
            {{
                "query": "can i meet for 30 minutes next Sunday at noon?"
                "today_date": "2023-12-21",
                "today_weekday": "Thursday",
                "intention": "propose_slots",
                "target_date": "2025-01-01",
                "target_time_frame": "12:00-16:00",
                "target_slot_duration_hrs": "0.5"
            }}
            Example 6: Query: "am i free on Monday 13-14 for 15mins?"
            Note: this is a tricky one, since this is clearly check_availability and the 15mins slot should be ignored.
            Response:
            {{
                "query": "am i free on Monday 13-14 for 15mins?"
                "today_date": "2023-12-21",
                "today_weekday": "Monday",
                "intention": "check_availability",
                "target_date": "2025-01-01",
                "target_time_frame": "13:00-14:00",
                "target_slot_duration_hrs": "NA"
            }}
            Example 7:
            Query: "Am I free on 1.1.2025 at 2 PM?"
            Note: target_time_frame should have only start time as end time was not specified
            Response:
            {{
                "query": "Am I free on 1.1.2025 at 2 PM?",
                "today_date": "2023-12-21",
                "today_weekday": "Thursday",
                "intention": "check_availability",
                "target_date": "2025-01-01",
                "target_time_frame": "14:00",
                "target_slot_duration_hrs": "NA"
            }}
            Example 8:
            Query: "Am I free on Thursday?"
            Note: no times specified, so needs to take the default day times (8am-8pm) as target_time_frame
            Response:
            {{
                "query": "Am I free on Thursday?",
                "today_date": "2023-12-21",
                "today_weekday": "Thursday",
                "intention": "check_availability",
                "target_date": "2025-01-01",
                "target_time_frame": "8:00-20:00",
                "target_slot_duration_hrs": "NA"
            }}
            Example 9:
            Query: "am i free on Sunday till quarter to three in the afternoon?"
            Note: no start time specified, so default to start 8am. also, end time is described verbally.
            Response:
            {{
                "query": "am i free on Sunday till quarter to three in the afternoon?",
                "today_date": "2023-12-21",
                "today_weekday": "Thursday",
                "intention": "check_availability",
                "target_date": "2025-01-01",
                "target_time_frame": "8:00-14:45",
                "target_slot_duration_hrs": "NA"
            }}
            Example 10:
            Query: "am i free next Tuesday from eight thirty in the morning till twenty to five in the afternoon"
            Response:
            {{
                "query": "am i free next Tuesday from eight thirty in the morning till twenty to five in the afternoon",
                "today_date": "2023-12-21",
                "today_weekday": "Thursday",
                "intention": "check_availability",
                "target_date": "2025-01-01",
                "target_time_frame": "8:30-16:40",
                "target_slot_duration_hrs": "NA"
            }}
            Example 11:
            Query: "am i available this Thursday for 5 hours?"
            Response:
            {{
                "query": "am i available this Thursday for 5 hours",
                "today_date": "2023-12-21",
                "today_weekday": "Thursday",
                "intention": "check_availability",
                "target_date": "2025-01-01",
                "target_time_frame": "8:00-20:00",
                "target_slot_duration_hrs": "5"
            }}
            Example 12:
            Query: "can i meet with Mike on Tuesday until 11am for an hour and a half?"
            Response:
            {{
                "query": "can i meet with Mike on Tuesday until 11am for an hour and a half?",
                "today_date": "2023-12-21",
                "today_weekday": "Thursday",
                "intention": "check_availability",
                "target_date": "2025-01-01",
                "target_time_frame": "8:00-11:00",
                "target_slot_duration_hrs": "1.5"
            }}
            Example 13:
            Query: "can i have a 1 hour meeting next Friday between 10am and 2pm?"
            Note: query phrasing might suggest the request is for 'propose_slots', while it's actually 'check_availability' since the user is merely trying to understand whether they are available for 1 hour within a time frame.
            Response:
            {{
                "query": "can i have a 1 hour meeting next Friday between 10am and 2pm?",
                "today_date": "2023-12-21",
                "today_weekday": "Thursday",
                "intention": "check_availability",
                "target_date": "2025-01-01",
                "target_time_frame": "10:00-14:00",
                "target_slot_duration_hrs": "1"
            }}
            Example 14:
            Query: "can I schedule a two hour meeting next Sunday between 8:30 and 11?"
            Note: query phrasing might suggest the request is for 'propose_slots', while it's actually 'check_availability' since the user is merely trying to understand whether they are available for 2 hour within a time frame.
            Response:
            {{
                "query": "can I schedule a one hour meeting next Sunday between 8:30 and 11?",
                "today_date": "2023-12-21",
                "today_weekday": "Thursday",
                "intention": "check_availability",
                "target_date": "2025-01-01",
                "target_time_frame": "8:30-11:00",
                "target_slot_duration_hrs": "2"
            }}

            Key Notes:
            Always parse the target_date and target_time_frame carefully from the query.
            For ambiguous queries, use predefined ranges for "time of day".
            Ensure the JSON response is well-formed, valid, and includes all required fields.
            Refrain from leading zeros when specifying times (example: 07:30 is wrong, 7:30 is right) 
            Refrain from wrapping the response string with ```json...```
            Make sure to include the query field in the response, with the original user query.
            As default, day starts at 8am and ends 8pm
            Offset your dates considering today is {today}, {day_of_the_week}.
            """

    def __get_nlp_completion(self, user_query):
        completion = self.__openai_client.chat.completions.create(
            model=self.MODEL,
            messages=[
                {"role": "system",
                 "content": self._get_nlp_system_content()},
                {
                    "role": "user",
                    "content": user_query
                }
            ]
        )
        return completion

