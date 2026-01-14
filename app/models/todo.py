from dataclasses import dataclass, asdict
from datetime import datetime, UTC
from typing import Optional

@dataclass
class Todo:
    id: int
    title: str
    description: Optional[str] = None
    dueDate: Optional[str] = None
    isCompleted: bool = False
    createdAt: str | None = None

    def __post_init__(self):
        if self.createdAt is None:
            self.createdAt = datetime.now(UTC).isoformat()

    def to_dict(self) -> dict:
        return asdict(self)
