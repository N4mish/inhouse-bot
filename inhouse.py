import datetime
from enum import Enum

class InhouseBotType(Enum):
    IC = 0
    INHOUSE = 1


class Inhouse:
    
    def __init__(self, id: str, type: InhouseBotType, time: datetime.datetime) -> None:
        self.id = id
        self.type = type
        self.time = time
        self.next = None
        self.prev = None

    