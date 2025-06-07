from enum import Enum

class Status(Enum):
    PENDING = "pending"
    FILTERED = "filtered"
    APPROVED = "approved"
    IN_PROGRESS  = "in_progress"
    RESOLVED = "resolved"
    REJECTED = "rejected"