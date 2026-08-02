"""测试 predictor 模块."""

from pathlib import Path

import pytest

from app.ml.train import MODEL_PATH, train as do_train
from app.models.predictor import FEATURE_COLS, load_model, predict


@pytest.fixture(scope="module", autouse=True)
def ensure_model():
    """确保预测测试运行前模型文件存在."""
    if MODEL_PATH.exists():
        MODEL_PATH.unlink()
    do_train()
    yield
    # 不主动删除，留给后续测试使用


HIGH_PROFILE = {
    "age": 30,
    "job": "student",
    "marital": "single",
    "education": "university.degree",
    "default": "no",
    "housing": "no",
    "loan": "no",
    "contact": "cellular",
    "month": "oct",
    "day_of_week": "tue",
    "duration": 3600,
    "campaign": 1,
    "pdays": 999,
    "previous": 0,
    "poutcome": "nonexistent",
    "emp_var_rate": -3.0,
    "cons_price_index": 92.5,
    "cons_conf_index": -46.0,
    "lending_rate3m": 1.2,
    "nr_employed": 4900.0,
}

LOW_PROFILE = {
    "age": 60,
    "job": "blue-collar",
    "marital": "divorced",
    "education": "basic.4y",
    "default": "yes",
    "housing": "yes",
    "loan": "yes",
    "contact": "telephone",
    "month": "may",
    "day_of_week": "mon",
    "duration": 30,
    "campaign": 8,
    "pdays": 0,
    "previous": 0,
    "poutcome": "failure",
    "emp_var_rate": 1.4,
    "cons_price_index": 93.5,
    "cons_conf_index": -36.0,
    "lending_rate3m": 5.0,
    "nr_employed": 5220.0,
}


# ── load_model ──


def test_load_model_returns_pipeline():
    model = load_model()
    from sklearn.pipeline import Pipeline

    assert isinstance(model, Pipeline)


def test_load_model_is_cached():
    m1 = load_model()
    m2 = load_model()
    assert m1 is m2


# ── predict normal ──


def test_predict_high_profile():
    result = predict(HIGH_PROFILE)
    assert "subscribe" in result
    assert "probability" in result
    assert "confidence" in result
    assert "response_time_ms" in result
    assert isinstance(result["subscribe"], bool)
    assert 0.0 <= result["probability"] <= 1.0


def test_predict_low_profile():
    result = predict(LOW_PROFILE)
    assert result["confidence"] in ("high", "medium", "low")


def test_predict_high_profile_higher_than_low():
    high_result = predict(HIGH_PROFILE)
    low_result = predict(LOW_PROFILE)
    assert high_result["probability"] > low_result["probability"]


def test_predict_response_time():
    result = predict(HIGH_PROFILE)
    assert result["response_time_ms"] < 1000


# ── error cases ──


def test_predict_missing_features():
    with pytest.raises(ValueError, match="缺少特征"):
        predict({"age": 30})


def test_predict_extra_features():
    with pytest.raises(ValueError, match="未知特征"):
        features = {**HIGH_PROFILE, "unknown_col": 99}
        predict(features)


def test_load_model_file_not_found():
    import app.models.predictor as pm

    pm.load_model.cache_clear()
    original = pm.MODEL_PATH
    pm.MODEL_PATH = Path("/nonexistent/model.pkl")
    try:
        with pytest.raises(FileNotFoundError, match="模型文件未找到"):
            predict(HIGH_PROFILE)
    finally:
        pm.MODEL_PATH = original
        pm.load_model.cache_clear()


# ── feature list ──


def test_feature_cols_count():
    assert len(FEATURE_COLS) == 20


def test_feature_cols_match_loader():
    from app.models.data_loader import CATEGORICAL_COLS, NUMERICAL_COLS

    assert FEATURE_COLS == CATEGORICAL_COLS + NUMERICAL_COLS
