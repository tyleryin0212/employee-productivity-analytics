# protocol + abstractemployee

from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from abc import ABC
from typing import ClassVar, Protocol

from .contact_info import ContactInfo
from .enums import EducationLevel, EmploymentLevel

class ProductivityEstimate(Protocol):
    """Interface-like contract for objects that can estimate productivity."""
    def estimate_productivity(self) -> float:
        ...

@dataclass(eq=True)
class AbstractEmployee(ABC):
    EMPLOYMENT_LEVEL_BONUS: ClassVar[float] = 1.4

    id: str
    contact: ContactInfo
    employment_date: date
    education_level: EducationLevel
    employment_level: EmploymentLevel
    last_year_earnings: float
    overtime_earnings: float
    bonus: float

    def _employee_level_bonus(self) -> float:
        """
        Helper method that calculates employee level bonus.
        """
        if self.employment_level != EmploymentLevel.ENTRY:
            return self.EMPLOYMENT_LEVEL_BONUS
        return 0.0
    
    def estimate_productivity(self) -> float:
        """
        Base productivity estimate
        
        Subclasses (Manager/IC/Hourly/etc.) should typically add to this:
            return: super().estimate_productivity() + extra_terms
        """
        return self._employee_level_bonus()

    