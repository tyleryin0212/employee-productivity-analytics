# AbstractPartTimeEmployee + HourlyEmployee

from __future__ import annotations
from dataclasses import dataclass
from abc import ABC
from typing import ClassVar

from .employee_base import AbstractEmployee

@dataclass(eq=True)
class AbstractPartTimeEmployee(AbstractEmployee, ABC):
    PRODUCTIVITY_FACTOR: ClassVar[float] = 3.7

    contractual_work_hours: float
    actual_work_hours: float
    extra_earnings: float

    def __post_init__(self) -> None:
        self.extra_earnings = self.bonus + self.overtime_earnings

    def _base_productivity_part_time(self) -> float:
        return (self.actual_work_hours / self.contractual_work_hours) * self.PRODUCTIVITY_FACTOR
    
    def estimate_productivity(self) -> float:
        return super().estimate_productivity() + self._base_productivity_part_time()
     

class HourlyEmployee(AbstractPartTimeEmployee):
    HOURLY_EARNINGS_BONUS: ClassVar[float] = 3.0
    HOURLY_EARNINGS_BONUS_THRESHOLD: ClassVar[float] = 14.0

    hourly_earnings: float

    def _hourly_earnings_bonus(self) -> float:
        return (
            self.HOURLY_EARNINGS_BONUS
            if self.hourly_earnings < self.HOURLY_EARNINGS_BONUS_THRESHOLD
            else 0.0
        )
    
    def estimate_productivity(self):
        return super().estimate_productivity() + self._hourly_earnings_bonus()
    


@dataclass(eq=True)        
class BenefitsEligibleEmployee(AbstractPartTimeEmployee):
    def estimate_productivity(self) -> float:
        return super().estimate_productivity()
    
