"""
Feature Contract Stability
Any change here requires:
1. retraining the ML model
2. redeploying the service

Feature schema shared by:
- offline training
- online inference

DO NOT change without retraining the model.
"""

FEATURE_COLUMNS = [
    # categoricals
    "employee_type",        # hourly / benefits_eligible / manager / individual_contributor
    "employment_level",     # ENTRY / INTERMEDIATE / MID / SENIOR / EXECUTIVE
    "education_level",      # HIGH_SCHOOL_DIPLOMA / ... / PROFESSIONAL

    # common numerics
    "last_year_earnings",
    "overtime_earnings",
    "bonus",

    # full-time numerics
    "base_pay",
    "num_projects",
    "years_since_promotion",
    "num_employees",
    "num_publications",
    "num_patents",
    "num_external_collaborations",

    # part-time numerics
    "contractual_work_hours",
    "actual_work_hours",
    "hourly_earnings",
]

TARGET_COLUMN = "productivity"