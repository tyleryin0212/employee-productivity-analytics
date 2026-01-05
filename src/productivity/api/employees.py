from flask import Blueprint, request, current_app

bp = Blueprint("employees", __name__, url_prefix="/employees")

bp = Blueprint("employees", __name__, url_prefix="/employees")

def _service():
    return current_app.config["EMPLOYEE_SERVICE"]

@bp.post("")
def create_employee():
    payload = request.get_json(silent=True) or {}
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