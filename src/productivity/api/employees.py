from __future__ import annotations
from flask import Blueprint, request

from productivity.services.employee_service import EmployeeService
from productivity.persistence.in_memory_employee_repo import InMemoryEmployeeRepository

bp = Blueprint("employees", __name__, url_prefix="/employees")

#wiring
_repo = InMemoryEmployeeRepository()
_service = EmployeeService(repo=_repo)


@bp.post("")
def create_employee():
    payload = request.get_json(silent=True) or {}

    #minimal validation
    if "type" not in payload:
        return {"error": "Missing required field: type"}, 400
    
    try:
        employee = _service.create_employee(payload)
        return employee, 201
    except ValueError as e:
        return {"error": str(e)}, 400
    

@bp.get("/<employee_id>")
def get_employee(employee_id: str):
    employee = _service.get_employee(employee_id)
    if employee is None:
        return {"error": "Employee not found"}, 404
    return employee, 200
