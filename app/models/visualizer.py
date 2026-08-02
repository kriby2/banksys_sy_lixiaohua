"""数据分析可视化逻辑 — 数据聚合与统计计算."""

import pandas as pd


def compute_overview(df: pd.DataFrame) -> dict:
    """计算数据概览统计.

    Returns:
        dict with keys: total_records, feature_count, subscribe_count,
        subscribe_rate, no_subscribe_count.
    """
    total = len(df)
    sub_count = int((df["subscribe"] == "yes").sum())
    no_count = int((df["subscribe"] == "no").sum())
    rate = sub_count / total if total > 0 else 0.0
    return {
        "total_records": total,
        "feature_count": len(df.columns) - 2,  # exclude id and subscribe
        "subscribe_count": sub_count,
        "no_subscribe_count": no_count,
        "subscribe_rate": round(rate, 4),
    }


def compute_age_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """年龄分组分布."""
    age_bins = [18, 25, 35, 45, 55, 65, 100]
    age_labels = ["18-25", "26-35", "36-45", "46-55", "56-65", "65+"]
    age_group = pd.cut(df["age"], bins=age_bins, labels=age_labels, right=True)
    return age_group.value_counts().reset_index(name="count")


def compute_job_subscribe_rate(df: pd.DataFrame) -> pd.DataFrame:
    """各职业认购率."""
    result = (
        df.groupby("job")["subscribe"]
        .apply(lambda x: (x == "yes").mean())
        .reset_index(name="subscribe_rate")
        .sort_values("subscribe_rate", ascending=False)
    )
    result["subscribe_rate"] = result["subscribe_rate"].round(4)
    return result


def compute_education_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """教育水平分布."""
    return df["education"].value_counts().reset_index(name="count")


def compute_marital_subscribe(df: pd.DataFrame) -> pd.DataFrame:
    """婚姻状况 vs 认购关系."""
    result = df.groupby("marital")["subscribe"].value_counts().unstack(fill_value=0).reset_index()
    return result


def compute_month_subscribe_rate(df: pd.DataFrame) -> pd.DataFrame:
    """各月份营销认购率."""
    month_order = ["mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    result = (
        df.groupby("month")["subscribe"]
        .apply(lambda x: (x == "yes").mean())
        .reset_index(name="subscribe_rate")
    )
    result["month"] = pd.Categorical(result["month"], categories=month_order, ordered=True)
    result = result.sort_values("month")
    result["subscribe_rate"] = result["subscribe_rate"].round(4)
    return result


def filter_dataframe(
    df: pd.DataFrame, job: str | None = None, marital: str | None = None
) -> pd.DataFrame:
    """按条件筛选数据."""
    result = df.copy()
    if job and job != "全部":
        result = result[result["job"] == job]
    if marital and marital != "全部":
        result = result[result["marital"] == marital]
    return result
