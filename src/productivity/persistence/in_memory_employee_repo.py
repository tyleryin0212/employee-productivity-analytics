from __future__ import annotations

from typing import Any, Optional, Dict
from uuid import uuid4


class InMemoryEmployeeRepository:
    def __init__(self):
        self._store: Dict[str, Any] = {}

    def save(self, employee: Any) -> Any:
        # supports dict placeholder OR your domain object once added
        if isinstance(employee, dict):
            emp_id = employee.get("id") or str(uuid4())
            employee["id"] = emp_id
            self._store[emp_id] = employee
            return employee

        # If domain object, assume it has .id
        emp_id = getattr(employee, "id", None) or str(uuid4())
        setattr(employee, "id", emp_id)
        self._store[emp_id] = employee
        return employee

    def get(self, employee_id: str) -> Optional[Any]:
        return self._store.get(employee_id)