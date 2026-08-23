from dataclasses import dataclass
from typing import Optional


@dataclass
class Source:
    url: str
    source_type: str

    title: Optional[str] = None
    domain: Optional[str] = None

    confidence: Optional[float] = None
