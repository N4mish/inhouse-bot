import datetime
import discord
from enum import Enum

class Role(Enum):
    TOP = 0
    JGL = 1
    MID = 2
    ADC = 3
    SUP = 4

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
        self.participants = []

    
