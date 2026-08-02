"""测试 train 模块."""

import subprocess
import sys

import joblib
import numpy as np
import pytest
from sklearn.pipeline import Pipeline

from app.ml.train import MODEL_PATH, build_pipeline, train


@pytest.fixture(scope="module")
def trained_result():
    """模块级 fixture: 训练一次，复用结果."""
    if MODEL_PATH.exists():
        MODEL_PATH.unlink()
    result = train()
    yield result
    if MODEL_PATH.exists():
        MODEL_PATH.unlink()


# ── build_pipeline ──


def test_build_pipeline_returns_pipeline():
    pipe = build_pipeline()
    assert isinstance(pipe, Pipeline)


def test_build_pipeline_has_steps():
    pipe = build_pipeline()
    steps = dict(pipe.named_steps)
    assert "preprocessor" in steps
    assert "classifier" in steps


# ── train ──


def test_train_returns_dict(trained_result):
    assert isinstance(trained_result, dict)
    for key in ("auc", "accuracy", "report", "cv_auc_5fold"):
        assert key in trained_result


def test_train_auc_above_threshold(trained_result):
    assert trained_result["auc"] >= 0.85


def test_train_accuracy_reasonable(trained_result):
    assert 0.5 < trained_result["accuracy"] < 1.0


def test_train_saves_model_file(trained_result):
    assert MODEL_PATH.exists()


def test_train_model_is_loadable(trained_result):
    model = joblib.load(MODEL_PATH)
    assert isinstance(model, Pipeline)


def test_trained_model_can_predict(trained_result):
    model = joblib.load(MODEL_PATH)
    from app.models.data_loader import load_train_data

    df = load_train_data()
    X = df.drop(columns=["subscribe"]).head(5)
    preds = model.predict(X)
    assert len(preds) == 5
    assert set(preds).issubset({0, 1})


def test_trained_model_predict_proba(trained_result):
    model = joblib.load(MODEL_PATH)
    from app.models.data_loader import load_train_data

    df = load_train_data()
    X = df.drop(columns=["subscribe"]).head(3)
    proba = model.predict_proba(X)
    assert proba.shape == (3, 2)
    assert np.allclose(proba.sum(axis=1), 1.0)


# ── reproducibility ──


def test_train_reproducible():
    """固定 random_state 产生相同 AUC."""
    if MODEL_PATH.exists():
        MODEL_PATH.unlink()
    r1 = train()
    if MODEL_PATH.exists():
        MODEL_PATH.unlink()
    r2 = train()
    if MODEL_PATH.exists():
        MODEL_PATH.unlink()
    assert r1["auc"] == r2["auc"]


# ── CLI ──


def test_cli_overwrite_flag():
    """--overwrite 允许覆盖已有模型."""
    train()
    mtime_before = MODEL_PATH.stat().st_mtime
    result = subprocess.run(
        [sys.executable, "-m", "app.ml.train", "--overwrite"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert MODEL_PATH.stat().st_mtime > mtime_before


def test_cli_check_auc_passes():
    result = subprocess.run(
        [sys.executable, "-m", "app.ml.train", "--overwrite", "--check-auc"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_cli_skips_when_model_exists():
    train()
    result = subprocess.run(
        [sys.executable, "-m", "app.ml.train"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
