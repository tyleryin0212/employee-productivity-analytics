# Name of a person, containing first name and last name

from __future__ import annotations
from dataclasses import dataclass

@dataclass(eq=True)
class Name:

    first_name: str
    last_name: str

    

