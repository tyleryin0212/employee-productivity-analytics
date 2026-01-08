from __future__ import annotations

from dataclasses import fields
from datetime import date
from typing import Any, Mapping, Dict, Type

from productivity.domain.employee_base import AbstractEmployee
from productivity.domain.employee_fulltime import Manager, IndividualContributor
from productivity.domain.employee_parttime import HourlyEmployee, BenefitsEligibleEmployee

from productivity.domain.contact_info import ContactInfo
from productivity.domain.name import Name
from productivity.domain.enums import EducationLevel, EmploymentLevel


class EmployeeFactory:
    TYPE_MAP: Dict[str, Type[AbstractEmployee]] = {
        "manager": Manager,
        "individual_contributor": IndividualContributor,
        "hourly": HourlyEmployee,
        "benefits_eligible": BenefitsEligibleEmployee,
    }

    @classmethod
    def from_payload(cls, data: Mapping[str, Any]) -> AbstractEmployee:
        emp_type = str(data.get("type", "")).strip().lower()
        if not emp_type:
            raise ValueError("Missing required field: type")

        model_cls = cls.TYPE_MAP.get(emp_type)
        if model_cls is None:
            raise ValueError(f"Unsupported employee type: {emp_type}")

        kwargs: dict[str, Any] = dict(data)
        kwargs.pop("type", None)  # not a dataclass field
        kwargs.setdefault("id", "")

        # --- nested dataclasses ---
        if "contact" in kwargs and isinstance(kwargs["contact"], dict):
            kwargs["contact"] = cls._parse_contact(kwargs["contact"])

        # --- enums ---
        if "education_level" in kwargs and isinstance(kwargs["education_level"], str):
            kwargs["education_level"] = EducationLevel(kwargs["education_level"])

        if "employment_level" in kwargs and isinstance(kwargs["employment_level"], str):
            kwargs["employment_level"] = EmploymentLevel(kwargs["employment_level"])

        # --- dates (ISO strings) ---
        for key in ("employment_date", "last_promotion_date"):
            if key in kwargs and isinstance(kwargs[key], str):
                kwargs[key] = date.fromisoformat(kwargs[key])
        
        init_field_names = {f.name for f in fields(model_cls) if f.init}
        kwargs = {k: v for k, v in kwargs.items() if k in init_field_names}

        return model_cls(**kwargs)

    @staticmethod
    def _parse_contact(payload: Mapping[str, Any]) -> ContactInfo:
        p = dict(payload)

        # ContactInfo.name and emergency_contact are Name dataclasses
        if "name" in p and isinstance(p["name"], dict):
            p["name"] = Name(**p["name"])

        if "emergency_contact" in p and isinstance(p["emergency_contact"], dict):
            p["emergency_contact"] = Name(**p["emergency_contact"])

        return ContactInfo(**p)
