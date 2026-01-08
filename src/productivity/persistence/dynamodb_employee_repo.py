from __future__ import annotations

from decimal import Decimal
from typing import Optional, Any, Dict
import os
from uuid import uuid4

import boto3

from productivity.domain.employee_base import AbstractEmployee
from productivity.factories.employee_factory import EmployeeFactory

class DynamoDBEmployeeRepository:

    _TYPE_BY_CLASS = {
        "HourlyEmployee": "hourly",
        "BenefitsEligibleEmployee": "benefits_eligible",
        "Manager": "manager",
        "IndividualContributor": "individual_contributor",

    }
    def __init__(self, table_name: str | None = None, region_name: str | None = None):

        self._table_name = table_name or os.environ["EMPLOYEES_TABLE_NAME"]
        dynamodb = boto3.resource("dynamodb", region_name=region_name)
        self._table = dynamodb.Table(self._table_name)

    def save(self, employee: AbstractEmployee) -> AbstractEmployee:
        #ensure server-generated id exists, if not, generate one
        if not employee.id:
            employee.id = str(uuid4())
        
        item = self._employee_to_item(employee)
        self._table.put_item(Item=item)
        return employee
    
    def get(self, employee_id: str) -> Optional[AbstractEmployee]:
        resp = self._table.get_item(Key={"employee_id": employee_id})
        item = resp.get("Item")
        if not item:
            return None

        payload = dict(item["payload"])
        payload["id"] = employee_id
        payload["type"] = item["type"]

        return EmployeeFactory.from_payload(payload)
    
    def _employee_to_item(self, employee: AbstractEmployee) -> Dict[str, Any]:
        """
        Store:
          employee_id (PK)
          type (class/type string)
          payload (Map): JSON-safe fields to rebuild the domain object
        """
        
        payload = self._to_payload(employee)
        payload.pop("id", None)  

        payload = self._to_decimal(payload)

        emp_type = self._TYPE_BY_CLASS.get(employee.__class__.__name__)
        if not emp_type:
            raise ValueError(f"Unsupported employee class: {employee.__class__.__name__}")

        return {
            "employee_id": employee.id,
            "type": emp_type,
            "payload": payload, 
        }
    
    def _to_payload(self, employee: AbstractEmployee) -> Dict[str, Any]:
        # simple, local conversion; mirrors your service’s approach
        from dataclasses import asdict
        from datetime import date
        from enum import Enum

        def json_safe(obj: Any) -> Any:
            if isinstance(obj, date):
                return obj.isoformat()
            if isinstance(obj, Enum):
                return obj.value
            if isinstance(obj, dict):
                return {k: json_safe(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [json_safe(v) for v in obj]
            return obj

        return json_safe(asdict(employee))
    
    def _to_decimal(self, value):
        if isinstance(value, float):
            return Decimal(str(value))  # str avoids float precision bugs
        if isinstance(value, dict):
            return {k: self._to_decimal(v) for k, v in value.items()}
        if isinstance(value, list):
            return [self._to_decimal(v) for v in value]
        return value
