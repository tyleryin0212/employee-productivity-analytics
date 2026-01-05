from __future__ import annotations

from dataclasses import asdict, is_dataclass
from datetime import date
from enum import Enum
from typing import Any, Mapping, Optional, Dict

from productivity.factories.employee_factory import EmployeeFactory
from productivity.domain.employee_base import AbstractEmployee
from productivity.persistence.employee_repo import EmployeeRepository


class EmployeeService:
    def __init__(self, repo: EmployeeRepository):
        self._repo = repo

    # -------------------------
    # Use cases
    # -------------------------

    def create_employee(self, payload: Mapping[str, Any]) -> Dict[str, Any]:
        """
        JSON payload -> domain employee -> repo -> JSON response dict
        """
        employee: AbstractEmployee = EmployeeFactory.from_payload(payload)

        saved: AbstractEmployee = self._repo.save(employee)

        return self._to_dict(saved)

    def get_employee(self, employee_id: str) -> Optional[Dict[str, Any]]:
        emp = self._repo.get(employee_id)
        if emp is None:
            return None
        return self._to_dict(emp)

    # -------------------------
    # Serialization helpers
    # -------------------------

    def _to_dict(self, employee: AbstractEmployee) -> Dict[str, Any]:
        """
        Convert domain employee object to a JSON-safe dict for API responses.
        """
        if not is_dataclass(employee):
            raise TypeError("Employee must be a dataclass to serialize cleanly")

        data = asdict(employee)
        data["type"] = employee.__class__.__name__  # helpful for client/UI

        return self._json_safe(data)

    def _json_safe(self, obj: Any) -> Any:
        """
        Recursively convert non-JSON types:
        - date -> ISO string
        - Enum -> .value
        """
        if isinstance(obj, date):
            return obj.isoformat()

        if isinstance(obj, Enum):
            return obj.value

        if isinstance(obj, dict):
            return {k: self._json_safe(v) for k, v in obj.items()}

        if isinstance(obj, list):
            return [self._json_safe(v) for v in obj]

        return obj

    # get employee productivity
    def get_productivity(self, employee_id: str) -> Optional[Dict[str, Any]]:
        emp = self._repo.get(employee_id)
        if emp is None:
            return None
        return {
            "employee_id": emp.id,
            "type": emp.__class__.__name__,
            "productivity": emp.estimate_productivity(),
        }