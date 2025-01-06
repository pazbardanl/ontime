
class IntentionDTO:

    def __init__(self, query:str,
                 today_date: str,
                 today_weekday: str,
                 intention: str,
                 target_date: str,
                 target_time_frame: str,
                 target_slot_duration_hrs: str = '0'
                 ):
        self.__query = query
        self.__today_date = today_date
        self.__today_weekday = today_weekday
        self.__intention = intention
        self.__target_date = target_date
        self.__target_time_frame = target_time_frame
        self.__target_slot_duration_hrs = target_slot_duration_hrs

    @property
    def query(self):
        return self.__query

    @property
    def today_date(self):
        return self.__today_date

    @property
    def today_weekday(self):
        return self.__today_weekday

    @property
    def intention(self):
        return self.__intention

    @property
    def target_date(self):
        return self.__target_date

    @property
    def target_time_frame(self):
        return self.__target_time_frame

    @property
    def target_slot_duration_hrs(self):
        return self.__target_slot_duration_hrs

    def __eq__(self, other):
        if isinstance(other, IntentionDTO):
            return (self.__query == other.__query and
                    self.__today_date == other.__today_date and
                    self.__today_weekday == other.__today_weekday and
                    self.__intention == other.__intention and
                    self.__target_date == other.__target_date and
                    self.__target_time_frame == other.__target_time_frame)
        return False

    def __hash__(self):
        return hash((self.__query, self.__today_date, self.__today_weekday, self.__intention, self.__target_date, self.__target_time_frame))

    def __str__(self):
        return (f"IntentionDTO("
                f"query='{self.query}', "
                f"today_date='{self.today_date}', "
                f"today_weekday='{self.today_weekday}', "
                f"intention='{self.intention}', "
                f"target_date='{self.target_date}', "
                f"target_time_frame='{self.target_time_frame}', "
                f"target_slot_duration_hrs='{self.target_slot_duration_hrs}')")

    def __repr__(self):
        return self.__str__()