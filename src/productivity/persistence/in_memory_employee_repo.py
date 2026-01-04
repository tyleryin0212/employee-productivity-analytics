from __future__ import annotations

from typing import Dict, Optional
from uuid import uuid4

from productivity.domain.employee_base import AbstractEmployee


class InMemoryEmployeeRepository:
    def __init__(self):
        self._store: Dict[str, AbstractEmployee] = {}

    def save(self, employee: AbstractEmployee) -> AbstractEmployee:
        if not employee.id:
            employee.id = str(uuid4())

        self._store[employee.id] = employee
        return employee

    def get(self, employee_id: str) -> Optional[AbstractEmployee]:
        return self._store.get(employee_id)
