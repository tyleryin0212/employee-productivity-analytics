# contact info for employees

from __future__ import annotations
from dataclasses import dataclass
from .name import Name

@dataclass(eq=True)
class ContactInfo:

    name: Name
    address: str
    phone_number: str
    email: str
    emergency_contact: Name

    