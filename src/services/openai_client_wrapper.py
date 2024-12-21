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
        return f"""You are an assistant that parses user requests for calendar availability. 
            For each user query, extract the intention (e.g., 'check_availability', 'propose_slots'), 
            the date, time, any relevant time ranges, and optionally the slot duration (if input mentions it). 
            Provide the output as JSON.
            
            Examples: 
            Input: "Am I available the coming Monday at 3 PM?" 
            Output: {{"query":"Am I available the coming Monday at 3 PM?","today_date": 2024-12-21, "today_weekday": Saturday ,"intention": "check_availability", "target_date": "2024-12-23", "target_time_frame": "15:00"}} 
            
            Input: "Can you suggest a slot of 90 minutes for Tuesday morning?" 
            Output: {{"query":"Can you suggest a slot of 90 minutes for Tuesday morning?","today_date": 2024-12-21, "today_weekday": Saturday ,"intention": "propose_slots", "target_date": "2024-12-24", "target_time_frame": "8:00-12:00", "target_slot_duration_hrs": "1.5"}}. 
            
            Early morning is 5am till 8am, morning is 8am till 12pm, noon is 12pm till 4pm, afternoon is 4pm till 6pm, 
            evening is 6pm till 10pm, night is 10pm till 5am. 
            
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

