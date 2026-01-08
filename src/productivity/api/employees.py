from flask import Blueprint, request, current_app
from pydantic import ValidationError

from productivity.schemas.employee_create import CreateEmployeeRequest

bp = Blueprint("employees", __name__, url_prefix="/employees")

def _service():
    return current_app.config["EMPLOYEE_SERVICE"]

@bp.post("")
def create_employee():
    raw = request.get_json(silent=True)
    if raw is None:
        return {"error": "Invalid or missing JSON body"}, 400

    try:
        # Pydantic v2
        req = CreateEmployeeRequest.model_validate(raw)
        payload = req.model_dump()
    except AttributeError:
        # Pydantic v1 fallback
        try:
            req = CreateEmployeeRequest.parse_obj(raw)
            payload = req.dict()
        except ValidationError as e:
            return {"error": "ValidationError", "details": e.errors()}, 400
    except ValidationError as e:
        return {"error": "ValidationError", "details": e.errors()}, 400

    employee = _service().create_employee(payload)
    return employee, 201

@bp.get("/<employee_id>")
def get_employee(employee_id: str):
    employee = _service().get_employee(employee_id)
    if employee is None:
        return {"error": "Employee not found"}, 404
    return employee, 200

@bp.get("/<employee_id>/productivity")
def get_productivity(employee_id: str):
    result = _service().get_productivity(employee_id)
    if result is None:
        return {"error": "Employee not found"}, 404
    return result, 200