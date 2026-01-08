from __future__ import annotations

import random
from datetime import date, timedelta
from pathlib import Path
from typing import List, Dict, Any

import pandas as pd

from productivity.domain.contact_info import ContactInfo
from productivity.domain.name import Name
from productivity.domain.enums import EducationLevel, EmploymentLevel
from productivity.domain.employee_fulltime import Manager, IndividualContributor
from productivity.domain.employee_parttime import HourlyEmployee, BenefitsEligibleEmployee

from ml.features import employee_to_features
from ml.schema import FEATURE_COLUMNS, TARGET_COLUMN


def _rand_date(start_year: int = 2010, end_year: int = 2025) -> date:
    start = date(start_year, 1, 1)
    end = date(end_year, 12, 31)
    return start + timedelta(days=random.randint(0, (end - start).days))


def _fake_contact(i: int) -> ContactInfo:
    # make it deterministic-ish and unique enough
    return ContactInfo(
        name=Name(first_name=f"Test{i}", last_name="User"),
        address="123 Main St",
        phone_number="555-555-5555",
        email=f"test{i}@example.com",
        emergency_contact=Name(first_name="Emergency", last_name="Contact"),
    )


def _choice_enum(enum_cls):
    return random.choice(list(enum_cls))


def _make_employee(i: int):
    emp_type = random.choice(["manager", "individual_contributor", "hourly", "benefits_eligible"])

    common = dict(
        id="",
        contact=_fake_contact(i),
        employment_date=_rand_date(2010, 2025),
        education_level=_choice_enum(EducationLevel),
        employment_level=_choice_enum(EmploymentLevel),
        last_year_earnings=max(1.0, random.gauss(120_000, 40_000)),
        overtime_earnings=max(0.0, random.gauss(4_000, 3_000)),
        bonus=max(0.0, random.gauss(7_000, 5_000)),
    )

    if emp_type == "manager":
        base_pay = max(30_000.0, random.gauss(140_000, 35_000))
        return Manager(
            **common,
            base_pay=base_pay,
            last_promotion_date=_rand_date(2010, 2025),
            num_projects=max(0, int(random.gauss(3, 2))),
            num_employees=max(0, int(random.gauss(10, 6))),
        )

    if emp_type == "individual_contributor":
        base_pay = max(30_000.0, random.gauss(130_000, 30_000))
        return IndividualContributor(
            **common,
            base_pay=base_pay,
            last_promotion_date=_rand_date(2010, 2025),
            num_projects=max(0, int(random.gauss(3, 2))),
            num_patents=max(0, int(random.gauss(2, 2))),
            num_publications=max(0, int(random.gauss(4, 3))),
            num_external_collaborations=max(0, int(random.gauss(2, 2))),
        )

    if emp_type == "hourly":
        contractual = max(5.0, random.gauss(20, 8))
        actual = max(0.0, random.gauss(22, 10))
        return HourlyEmployee(
            **common,
            contractual_work_hours=contractual,
            actual_work_hours=actual,
            hourly_earnings=max(5.0, random.gauss(18, 6)),
        )

    # benefits_eligible
    contractual = max(5.0, random.gauss(20, 8))
    actual = max(0.0, random.gauss(20, 10))
    return BenefitsEligibleEmployee(
        **common,
        contractual_work_hours=contractual,
        actual_work_hours=actual,
    )


def main(out_path: str = "src/ml/employees_training.csv", rows: int = 500, noise_std: float = 0.15) -> None:
    """
    Generates a grounded synthetic dataset:
    - Features come from the domain object
    - Target label comes from emp.estimate_productivity()
    - Add small Gaussian noise so ML isn't perfectly deterministic
    """
    random.seed(42)

    records: List[Dict[str, Any]] = []
    for i in range(rows):
        emp = _make_employee(i)
        x = employee_to_features(emp)
        y = float(emp.estimate_productivity()) + random.gauss(0.0, noise_std)

        # enforce column order
        record = {col: x.get(col) for col in FEATURE_COLUMNS}
        record[TARGET_COLUMN] = y
        records.append(record)

    df = pd.DataFrame.from_records(records, columns=FEATURE_COLUMNS + [TARGET_COLUMN])

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)

    print(f"Wrote {len(df)} rows to {out.resolve()}")
    print(df.head(5).to_string(index=False))


if __name__ == "__main__":
    main()
