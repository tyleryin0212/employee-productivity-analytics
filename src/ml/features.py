from __future__ import annotations

from datetime import date
from typing import Any, Dict

from productivity.domain.employee_base import AbstractEmployee
from productivity.domain.employee_fulltime import AbstractFullTimeEmployee, Manager, IndividualContributor
from productivity.domain.employee_parttime import AbstractPartTimeEmployee, HourlyEmployee, BenefitsEligibleEmployee
from ml.schema import FEATURE_COLUMNS

# single source of truth for type strings
TYPE_BY_CLASSNAME = {
    "HourlyEmployee": "hourly",
    "BenefitsEligibleEmployee": "benefits_eligible",
    "Manager": "manager",
    "IndividualContributor": "individual_contributor",
}

def _full_years_between(start: date, end: date) -> int:
    years = end.year - start.year
    if (end.month, end.day) < (start.month, start.day):
        years -= 1
    return max(years, 0)

def _employee_type(emp: AbstractEmployee) -> str:
    return TYPE_BY_CLASSNAME.get(emp.__class__.__name__, emp.__class__.__name__.lower())

def employee_to_features(emp: AbstractEmployee) -> Dict[str, Any]:
    """
    Domain employee -> flat feature row.
    Uses getattr(...) for optional subtype fields to avoid lots of isinstance checks.
    """
    # start with None for everything (=> NaN in pandas)
    row: Dict[str, Any] = {c: None for c in FEATURE_COLUMNS}

    # categoricals (always present)
    row["employee_type"] = _employee_type(emp)
    row["employment_level"] = emp.employment_level.value
    row["education_level"] = emp.education_level.value

    # common numerics (always present)
    row["last_year_earnings"] = float(emp.last_year_earnings)
    row["overtime_earnings"] = float(emp.overtime_earnings)
    row["bonus"] = float(emp.bonus)

    # numeric fields that may or may not exist depending on subtype
    # (no branching needed)
    optional_numeric_fields = [
        "base_pay",
        "num_projects",
        "num_employees",
        "num_publications",
        "num_patents",
        "num_external_collaborations",
        "contractual_work_hours",
        "actual_work_hours",
        "hourly_earnings",
    ]
    for f in optional_numeric_fields:
        v = getattr(emp, f, None)
        if v is None:
            continue
        # cast ints cleanly; everything else to float
        row[f] = int(v) if isinstance(v, int) else float(v)

    # computed field derived from date (only if last_promotion_date exists)
    last_promo = getattr(emp, "last_promotion_date", None)
    if last_promo is not None:
        row["years_since_promotion"] = _full_years_between(last_promo, date.today())

    return row