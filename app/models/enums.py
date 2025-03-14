from enum import Enum as PyEnum

class PriorityEnum(str, PyEnum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class StatusEnum(str, PyEnum):
    PENDING = "Pending"
    COMPLETED = "Completed"

