from __future__ import annotations
from typing import Protocol, Optional

from productivity.domain.employee_base import AbstractEmployee

class EmployeeRepository(Protocol):
    def save(self, employee: AbstractEmployee) -> AbstractEmployee: ...
    def get(self, employee_id: str) -> Optional[AbstractEmployee]: ...