# abstractFullTimeEmployee + Manager + IndividualContributor

from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from datetime import date
from typing import ClassVar

from productivity.domain.employee_base import AbstractEmployee

from .contact_info import ContactInfo
from .enums import EducationLevel, EmploymentLevel

@dataclass(eq=True)
class AbstractFullTimeEmployee(AbstractEmployee, ABC):
    PROJECT_BONUS: ClassVar[float] = 1.5
    PROJECT_BONUS_THRESHOLD: ClassVar[int] = 2

    LAST_PROMOTION_PENALTY: ClassVar[float] = -0.8
    LAST_PROMOTION_PENALTY_THRESHOLD: ClassVar[int] = 3

    base_pay: float 
    last_promotion_date: date
    num_projects: int 

    def _base_productivity_full_time(self) -> float:
        return self._f(self.last_year_earnings) / self._f(self.base_pay)
    
    def _project_bonus(self) -> float:
        return self.PROJECT_BONUS if self.num_projects > self.PROJECT_BONUS_THRESHOLD else 0.0
    
    @staticmethod
    def _full_years_between(start: date, end: date) -> int:
        """
        Full year difference.
        If end is before the anniversary in the end year, subtract 1.
        """

        years = end.year - start.year
        if (end.month, end.day) < (start.month, start.day):
            years -= 1
        return years
    
    def _years_since_promotion(self) -> int:
        return self._full_years_between(self.last_promotion_date, date.today())
    
    def _last_promotion_penalty(self) -> float:
        return (
            self.LAST_PROMOTION_PENALTY
            if self._years_since_promotion() > self.LAST_PROMOTION_PENALTY_THRESHOLD
            else 0.0
        )
    
    def estimate_productivity(self) -> float:
        return (
            super().estimate_productivity()
            + self._base_productivity_full_time()
            + self._project_bonus()
            + self._last_promotion_penalty()
        )
    

@dataclass(eq=True)
class Manager(AbstractFullTimeEmployee):
    MANAGER_BONUS: ClassVar[float] = 1.8
    MANAGER_BONUS_THRESHOLD: ClassVar[int] = 8
    num_employees: int

    def _manager_bonus(self) -> float:
        """
        Receives manager bonus if managing more than threshold employees.
        """
        return (
            self.MANAGER_BONUS
            if self.num_employees > self.MANAGER_BONUS_THRESHOLD
            else 0.0
        )
    
    def estimate_productivity(self) -> float:
        """
        Sums base productivity and all applicable manager bonuses.
        """

        return super().estimate_productivity() + self._manager_bonus()
    

@dataclass(eq=True)
class IndividualContributor(AbstractFullTimeEmployee):

    INDIVIDUAL_CONTRIBUTOR_BONUS: ClassVar[float] = 1.3
    INDIVIDUAL_CONTRIBUTOR_BONUS_THRESHOLD: ClassVar[int] = 4

    num_patents: int
    num_publications: int
    num_external_collaborations: int

    def _individual_contributor_bonus(self) -> float:
        return (
            self.INDIVIDUAL_CONTRIBUTOR_BONUS 
            if self.num_publications > self.INDIVIDUAL_CONTRIBUTOR_BONUS_THRESHOLD
            else 0.0
        )
    
    def estimate_productivity(self) -> float:
        return super().estimate_productivity() + self._individual_contributor_bonus()
    
    