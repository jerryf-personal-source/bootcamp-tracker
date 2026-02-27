from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Drill:
    id: str
    text: str
    done: bool = False


@dataclass
class DayPlan:
    id: str
    date: str
    title: str
    drills: List[Drill] = field(default_factory=list)
    confidence: Optional[int] = None
    reflection: str = ""
