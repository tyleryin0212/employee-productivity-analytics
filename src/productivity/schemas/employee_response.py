from __future__ import annotations
from pydantic import BaseModel


class ProductivityResponse(BaseModel):
    employee_id: str
    type: str
    productivity: float
