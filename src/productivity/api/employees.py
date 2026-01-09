from flask import Blueprint, request, current_app
from pydantic import TypeAdapter, ValidationError

from productivity.schemas.employee_create import CreateEmployeeRequest

bp = Blueprint("employees", __name__, url_prefix="/employees")


create_employee_adapter = TypeAdapter(CreateEmployeeRequest)

def _service():
    return current_app.config["EMPLOYEE_SERVICE"]

@bp.post("")
def create_employee():
    raw = request.get_json(silent=True) or {}

    try:
        req = create_employee_adapter.validate_python(raw)  
    except ValidationError as e:
        return {"error": "Validation error", "details": e.errors()}, 400

    # If your service expects a dict payload:
    payload = req.model_dump()  # Pydantic v2
    
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

@bp.get("/<employee_id>/productivity/predict")
def predict_productivity(employee_id: str):
    result = _service().predict_productivity(employee_id)
    if result is None:
        return {"error": "Employee not found"}, 404
    return result, 200
