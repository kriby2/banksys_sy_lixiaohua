"""银行营销数据加载模块."""

from pathlib import Path

import pandas as pd
from pandas.errors import EmptyDataError

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"

REQUIRED_TRAIN_COLS = [
    "id",
    "age",
    "job",
    "marital",
    "education",
    "default",
    "housing",
    "loan",
    "contact",
    "month",
    "day_of_week",
    "duration",
    "campaign",
    "pdays",
    "previous",
    "poutcome",
    "emp_var_rate",
    "cons_price_index",
    "cons_conf_index",
    "lending_rate3m",
    "nr_employed",
    "subscribe",
]

REQUIRED_TEST_COLS = [
    "id",
    "age",
    "job",
    "marital",
    "education",
    "default",
    "housing",
    "loan",
    "contact",
    "month",
    "day_of_week",
    "duration",
    "campaign",
    "pdays",
    "previous",
    "poutcome",
    "emp_var_rate",
    "cons_price_index",
    "cons_conf_index",
    "lending_rate3m",
    "nr_employed",
]

CATEGORICAL_COLS = [
    "job",
    "marital",
    "education",
    "default",
    "housing",
    "loan",
    "contact",
    "month",
    "day_of_week",
    "poutcome",
]

NUMERICAL_COLS = [
    "age",
    "duration",
    "campaign",
    "pdays",
    "previous",
    "emp_var_rate",
    "cons_price_index",
    "cons_conf_index",
    "lending_rate3m",
    "nr_employed",
]


def load_train_data(path: str | Path | None = None) -> pd.DataFrame:
    """加载训练数据.

    Returns:
        pd.DataFrame with 22 columns (21 features + subscribe target).

    Raises:
        FileNotFoundError: 数据文件不存在.
        ValueError: 数据为空或缺少必要列.
    """
    filepath = Path(path) if path else (DATA_DIR / "train.csv")
    if not filepath.exists():
        raise FileNotFoundError(f"训练数据文件不存在: {filepath}")
    try:
        df = pd.read_csv(filepath)
    except EmptyDataError:
        raise ValueError("训练数据为空") from None
    if df.empty:
        raise ValueError("训练数据为空")
    missing = set(REQUIRED_TRAIN_COLS) - set(df.columns)
    if missing:
        raise ValueError(f"训练数据缺少必要列: {missing}")
    return df


def load_test_data(path: str | Path | None = None) -> pd.DataFrame:
    """加载测试数据.

    Returns:
        pd.DataFrame with 21 columns (features only, no target).

    Raises:
        FileNotFoundError: 数据文件不存在.
        ValueError: 数据为空或缺少必要列.
    """
    filepath = Path(path) if path else (DATA_DIR / "test.csv")
    if not filepath.exists():
        raise FileNotFoundError(f"测试数据文件不存在: {filepath}")
    try:
        df = pd.read_csv(filepath)
    except EmptyDataError:
        raise ValueError("测试数据为空") from None
    if df.empty:
        raise ValueError("测试数据为空")
    missing = set(REQUIRED_TEST_COLS) - set(df.columns)
    if missing:
        raise ValueError(f"测试数据缺少必要列: {missing}")
    return df


def get_column_info() -> dict:
    """返回数据集的列信息."""
    return {
        "total_features": 21,
        "categorical": CATEGORICAL_COLS,
        "numerical": NUMERICAL_COLS,
        "target": "subscribe",
        "target_values": ["no", "yes"],
    }
