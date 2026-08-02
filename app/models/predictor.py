"""预测服务模块 — 加载模型并提供 predict 接口."""

import time
from functools import lru_cache
from pathlib import Path

import pandas as pd
from sklearn.pipeline import Pipeline

from app.models.data_loader import CATEGORICAL_COLS, NUMERICAL_COLS

MODEL_PATH = Path(__file__).resolve().parent.parent / "ml" / "model" / "model.pkl"

FEATURE_COLS = CATEGORICAL_COLS + NUMERICAL_COLS


@lru_cache(maxsize=1)
def load_model() -> Pipeline:
    """加载已训练的模型，带内存缓存.

    Raises:
        FileNotFoundError: 模型文件不存在.
    """
    import joblib

    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"模型文件未找到: {MODEL_PATH}，请先运行训练脚本")
    return joblib.load(MODEL_PATH)


def predict(features: dict) -> dict:
    """预测客户认购意愿.

    Args:
        features: 包含 20 个特征值的字典，键为列名，值为对应的值.

    Returns:
        dict with keys: subscribe (bool), probability (float), confidence (str).

    Raises:
        FileNotFoundError: 模型文件不存在.
        ValueError: 输入特征不完整或包含未知类别.
    """
    start = time.perf_counter()

    model = load_model()  # noqa: F841 (used below)

    missing = set(FEATURE_COLS) - set(features.keys())
    if missing:
        raise ValueError(f"缺少特征: {missing}")

    extra = set(features.keys()) - set(FEATURE_COLS)
    if extra:
        raise ValueError(f"未知特征: {extra}")

    input_df = pd.DataFrame([features])[FEATURE_COLS]

    for col in CATEGORICAL_COLS:
        val = input_df.loc[0, col]
        if isinstance(val, (int, float)):
            input_df.loc[0, col] = str(val)

    proba = model.predict_proba(input_df)[0, 1]
    proba = float(proba)

    subscribe = proba >= 0.5
    if proba >= 0.7:
        confidence = "high"
    elif proba >= 0.5:
        confidence = "medium"
    else:
        confidence = "low"

    elapsed = time.perf_counter() - start

    return {
        "subscribe": subscribe,
        "probability": round(proba, 4),
        "confidence": confidence,
        "response_time_ms": round(elapsed * 1000, 2),
    }
