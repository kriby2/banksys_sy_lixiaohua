"""离线训练脚本 — 产出模型文件到 app/ml/model/."""

import argparse
import sys
from pathlib import Path

import joblib
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from app.models.data_loader import CATEGORICAL_COLS, NUMERICAL_COLS, load_train_data

MODEL_DIR = Path(__file__).resolve().parent / "model"
MODEL_PATH = MODEL_DIR / "model.pkl"

RANDOM_STATE = 42
AUC_THRESHOLD = 0.85


def build_pipeline() -> Pipeline:
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_COLS),
            ("num", "passthrough", NUMERICAL_COLS),
        ],
        remainder="drop",
    )
    return Pipeline(
        [
            ("preprocessor", preprocessor),
            (
                "classifier",
                RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE, n_jobs=-1),
            ),
        ]
    )


def train() -> dict:
    """训练模型并保存.

    Returns:
        dict with keys: auc, accuracy, report.
    """
    df = load_train_data()
    X = df.drop(columns=["subscribe"])
    y = (df["subscribe"] == "yes").astype(int)

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )

    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_val)
    y_proba = pipeline.predict_proba(X_val)[:, 1]

    auc = roc_auc_score(y_val, y_proba)
    acc = accuracy_score(y_val, y_pred)
    report = classification_report(y_val, y_pred, target_names=["no", "yes"])

    cv_scores = cross_val_score(pipeline, X, y, cv=5, scoring="roc_auc")
    cv_auc = float(cv_scores.mean())

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)

    return {
        "auc": round(float(auc), 4),
        "cv_auc_5fold": round(cv_auc, 4),
        "accuracy": round(float(acc), 4),
        "report": report,
    }


def main():
    parser = argparse.ArgumentParser(description="训练银行认购预测模型")
    parser.add_argument("--overwrite", action="store_true", help="覆盖已有模型文件")
    parser.add_argument("--check-auc", action="store_true", help=f"检查 AUC >= {AUC_THRESHOLD}")
    args = parser.parse_args()

    if MODEL_PATH.exists() and not args.overwrite:
        print(f"模型已存在: {MODEL_PATH}")
        print("使用 --overwrite 覆盖已有模型")
        sys.exit(0)

    result = train()

    print(f"AUC: {result['auc']:.4f}")
    print(f"CV AUC (5-fold): {result['cv_auc_5fold']:.4f}")
    print(f"Accuracy: {result['accuracy']:.4f}")
    print(f"\n分类报告:\n{result['report']}")
    print(f"模型已保存: {MODEL_PATH}")

    if args.check_auc and result["auc"] < AUC_THRESHOLD:
        print(f"AUC {result['auc']:.4f} 低于阈值 {AUC_THRESHOLD}")
        sys.exit(1)


if __name__ == "__main__":
    main()
