from __future__ import annotations

import os
from flask import Flask

from productivity.api.employees import bp as employees_bp
from productivity.services.employee_service import EmployeeService

from productivity.persistence.in_memory_employee_repo import InMemoryEmployeeRepository

def create_app() -> Flask:
    app = Flask(__name__)

    # choose repository implementation
    repo_type = os.getenv("REPO_TYPE", "memory").lower()

    if repo_type == "dynamodb":
        from productivity.persistence.dynamodb_employee_repo import DynamoDBEmployeeRepository

        # DynamoDBEmployeeRepository reads table name from env by default,
        # but you can also pass it explicitly.
        repo = DynamoDBEmployeeRepository(
            table_name=os.getenv("EMPLOYEES_TABLE_NAME"),
            region_name=os.getenv("AWS_REGION"),
        )
    else: 
        repo = InMemoryEmployeeRepository()
    
    # dependency injection
    app.config["EMPLOYEE_SERVICE"] = EmployeeService(repo=repo)

    # routes:

    app.register_blueprint(employees_bp)

    #basic health check
    @app.get("/health")
    def health():
        return {"status": "ok"}, 200
    
    return app