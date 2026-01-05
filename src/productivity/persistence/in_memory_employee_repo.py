from __future__ import annotations

from typing import Dict, Optional
from uuid import uuid4

from productivity.domain.employee_base import AbstractEmployee


class InMemoryEmployeeRepository:
    """
    Dev/test repository.
    Stores domain objects in a dict in memory.
    """

    def __init__(self) -> None:
        self._store: Dict[str, AbstractEmployee] = {}

    def save(self, employee: AbstractEmployee) -> AbstractEmployee:
        # Server-generated id
        if not employee.id:
            employee.id = str(uuid4())

        self._store[employee.id] = employee
        return employee

    def get(self, employee_id: str) -> Optional[AbstractEmployee]:
        return self._store.get(employee_id)
