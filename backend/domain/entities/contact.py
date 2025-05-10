from dataclasses import dataclass
from typing import Optional

@dataclass
class Contact:
    id: Optional[int]
    name: str
    phone: Optional[str]
    email: Optional[str]