from __future__ import annotations

from pathlib import Path

import pandas as pd
import joblib

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

from ml.schema import FEATURE_COLUMNS, TARGET_COLUMN


DATA_PATH = Path("src/ml/employees_training.csv")
MODEL_PATH = Path("src/ml/model.pkl")

def main() -> None:
    # 1) Load dataset
    df = pd.read_csv(DATA_PATH)

    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    # 2) Identify column types
    categorical_cols = [
        "employee_type",
        "employment_level",
        "education_level",
    ]

    numeric_cols = [c for c in FEATURE_COLUMNS if c not in categorical_cols]

    # 3) Preprocessing pipelines
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", categorical_pipeline, categorical_cols),
            ("num", numeric_pipeline, numeric_cols),
        ]
    )

    # 4) Model
    model = RandomForestRegressor(
        n_estimators=150,
        random_state=42,
    )

    # 5) Full pipeline
    pipeline = Pipeline(
        steps=[
            ("preprocess", preprocessor),
            ("model", model),
        ]
    )

    # 6) Train / test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 7) Train
    pipeline.fit(X_train, y_train)

    # 8) Evaluate
    preds = pipeline.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    print("Model evaluation")
    print("----------------")
    print(f"MAE: {mae:.3f}")
    print(f"R² : {r2:.3f}")

    # 9) Save model
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)

    print(f"\nSaved model to {MODEL_PATH.resolve()}")


if __name__ == "__main__":
    main()