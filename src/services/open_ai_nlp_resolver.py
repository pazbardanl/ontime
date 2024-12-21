from .interfaces import NLPResolverInterface
from .interfaces import OpenAIClientWrapperInterface
from ..model import IntentionDTO
import json

class OpenAINLPResolver(NLPResolverInterface):

    def __init__(self, openai_client_wrapper:OpenAIClientWrapperInterface):
        self.__openai_client_wrapper = openai_client_wrapper

    def resolve_intention(self, user_query: str) -> IntentionDTO:
        print(f'resolving intention for user_query = {user_query}')
        intention_json_str = self.__openai_client_wrapper.resolve_intention(user_query)
        print(f'intention_json_str = {intention_json_str}')
        return self.__get_intention_dto(intention_json_str)

    def __get_intention_dto(self, intention_json_str):
        intention_data = json.loads(intention_json_str)
        return IntentionDTO(
            query = intention_data.get("query"),
            today_date = intention_data.get("today_date"),
            today_weekday = intention_data.get("today_weekday"),
            intention = intention_data.get("intention"),
            target_date = intention_data.get("target_date"),
            target_time_frame = intention_data.get("target_time_frame"),
        )