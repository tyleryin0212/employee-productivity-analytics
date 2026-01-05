from __future__ import annotations

from datetime import date
from typing import Literal, Union

from pydantic import BaseModel

# import your enums
from productivity.domain.enums import EducationLevel, EmploymentLevel


class NameSchema(BaseModel):
    first_name: str
    last_name: str


class ContactInfoSchema(BaseModel):
    name: NameSchema
    address: str
    phone_number: str
    email: str
    emergency_contact: NameSchema


class BaseEmployeeCreate(BaseModel):
    # id intentionally omitted: server generates it
    contact: ContactInfoSchema
    employment_date: date
    education_level: EducationLevel
    employment_level: EmploymentLevel
    last_year_earnings: float
    overtime_earnings: float = 0.0
    bonus: float = 0.0


class HourlyEmployeeCreate(BaseEmployeeCreate):
    type: Literal["hourly"]
    contractual_work_hours: float
    actual_work_hours: float
    hourly_earnings: float


class BenefitsEligibleEmployeeCreate(BaseEmployeeCreate):
    type: Literal["benefits_eligible"]
    contractual_work_hours: float
    actual_work_hours: float


class ManagerCreate(BaseEmployeeCreate):
    type: Literal["manager"]
    base_pay: float
    last_promotion_date: date
    num_projects: int
    num_employees: int


class IndividualContributorCreate(BaseEmployeeCreate):
    type: Literal["individual_contributor"]
    base_pay: float
    last_promotion_date: date
    num_projects: int
    num_patents: int
    num_publications: int
    num_external_collaborations: int


CreateEmployeeRequest = Union[
    HourlyEmployeeCreate,
    BenefitsEligibleEmployeeCreate,
    ManagerCreate,
    IndividualContributorCreate,
]
