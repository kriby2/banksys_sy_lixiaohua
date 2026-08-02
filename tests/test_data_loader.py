"""测试 data_loader 模块."""

import tempfile
from pathlib import Path

import pandas as pd
import pytest

from app.models.data_loader import (
    CATEGORICAL_COLS,
    DATA_DIR,
    NUMERICAL_COLS,
    REQUIRED_TRAIN_COLS,
    get_column_info,
    load_test_data,
    load_train_data,
)

# ── load_train_data ──


def test_load_train_data_default_path():
    df = load_train_data()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert list(df.columns) == REQUIRED_TRAIN_COLS
    assert "subscribe" in df.columns


def test_load_train_data_custom_path():
    df = load_train_data(DATA_DIR / "train.csv")
    assert len(df) > 0


def test_load_train_data_file_not_found():
    with pytest.raises(FileNotFoundError, match="训练数据文件不存在"):
        load_train_data("/nonexistent/path/train.csv")


def test_load_train_data_empty_file():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        pass
    try:
        with pytest.raises(ValueError, match="训练数据为空"):
            load_train_data(f.name)
    finally:
        Path(f.name).unlink()


def test_load_train_data_missing_columns():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("a,b,c\n1,2,3\n")
    try:
        with pytest.raises(ValueError, match="训练数据缺少必要列"):
            load_train_data(f.name)
    finally:
        Path(f.name).unlink()


def test_load_train_data_row_count():
    df = load_train_data()
    assert len(df) == 22500


def test_load_train_data_has_subscribe_values():
    df = load_train_data()
    assert set(df["subscribe"].unique()) == {"yes", "no"}


# ── load_test_data ──


def test_load_test_data_default_path():
    df = load_test_data()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "subscribe" not in df.columns


def test_load_test_data_custom_path():
    df = load_test_data(DATA_DIR / "test.csv")
    assert len(df) > 0


def test_load_test_data_file_not_found():
    with pytest.raises(FileNotFoundError, match="测试数据文件不存在"):
        load_test_data("/nonexistent/path/test.csv")


def test_load_test_data_empty_file():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        pass
    try:
        with pytest.raises(ValueError, match="测试数据为空"):
            load_test_data(f.name)
    finally:
        Path(f.name).unlink()


def test_load_test_data_missing_columns():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("a,b,c\n1,2,3\n")
    try:
        with pytest.raises(ValueError, match="测试数据缺少必要列"):
            load_test_data(f.name)
    finally:
        Path(f.name).unlink()


def test_load_test_data_row_count():
    df = load_test_data()
    assert len(df) == 7500


# ── get_column_info ──


def test_get_column_info_returns_dict():
    info = get_column_info()
    assert isinstance(info, dict)
    assert info["total_features"] == 21
    assert info["target"] == "subscribe"
    assert info["target_values"] == ["no", "yes"]


def test_column_info_categorical_count():
    info = get_column_info()
    assert len(info["categorical"]) == len(CATEGORICAL_COLS)


def test_column_info_numerical_count():
    info = get_column_info()
    assert len(info["numerical"]) == len(NUMERICAL_COLS)


# ── data integrity ──


def test_train_data_no_null_values():
    df = load_train_data()
    assert df.isnull().sum().sum() == 0


def test_test_data_no_null_values():
    df = load_test_data()
    assert df.isnull().sum().sum() == 0


def test_categorical_cols_exist_in_data():
    df = load_train_data()
    for col in CATEGORICAL_COLS:
        assert col in df.columns


def test_numerical_cols_exist_in_data():
    df = load_train_data()
    for col in NUMERICAL_COLS:
        assert col in df.columns
