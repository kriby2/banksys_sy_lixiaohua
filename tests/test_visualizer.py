"""测试 visualizer 模块."""

import pandas as pd
import pytest

from app.models.visualizer import (
    compute_age_distribution,
    compute_education_distribution,
    compute_job_subscribe_rate,
    compute_marital_subscribe,
    compute_month_subscribe_rate,
    compute_overview,
    filter_dataframe,
)


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5, 6],
            "age": [25, 35, 45, 55, 30, 40],
            "job": ["admin.", "blue-collar", "technician", "admin.", "services", "blue-collar"],
            "marital": ["single", "married", "divorced", "married", "single", "divorced"],
            "education": [
                "high.school",
                "university.degree",
                "basic.9y",
                "high.school",
                "professional.course",
                "university.degree",
            ],
            "default": ["no", "no", "no", "yes", "no", "no"],
            "housing": ["yes", "yes", "no", "yes", "no", "yes"],
            "loan": ["no", "yes", "no", "no", "yes", "no"],
            "contact": ["cellular", "telephone", "cellular", "cellular", "telephone", "cellular"],
            "month": ["may", "jun", "jul", "aug", "may", "jun"],
            "day_of_week": ["mon", "tue", "wed", "thu", "fri", "mon"],
            "duration": [100, 200, 300, 400, 500, 600],
            "campaign": [1, 2, 1, 3, 2, 1],
            "pdays": [999, 999, 5, 999, 10, 999],
            "previous": [0, 0, 1, 0, 1, 0],
            "poutcome": [
                "nonexistent",
                "nonexistent",
                "success",
                "nonexistent",
                "failure",
                "nonexistent",
            ],
            "emp_var_rate": [1.4, -0.9, 1.4, -1.8, -2.9, -1.8],
            "cons_price_index": [93.9, 92.8, 93.2, 93.0, 92.1, 94.4],
            "cons_conf_index": [-42.7, -46.2, -38.1, -40.0, -35.4, -41.8],
            "lending_rate3m": [4.2, 4.9, 1.3, 3.9, 5.0, 2.1],
            "nr_employed": [5191.0, 4991.6, 5076.2, 5099.1, 4963.6, 5228.1],
            "subscribe": ["no", "no", "yes", "no", "yes", "no"],
        }
    )


# ── compute_overview ──


def test_compute_overview_keys(sample_df):
    result = compute_overview(sample_df)
    assert "total_records" in result
    assert "subscribe_rate" in result
    assert "subscribe_count" in result
    assert "no_subscribe_count" in result
    assert "feature_count" in result


def test_compute_overview_counts(sample_df):
    result = compute_overview(sample_df)
    assert result["total_records"] == 6
    assert result["subscribe_count"] == 2
    assert result["no_subscribe_count"] == 4
    assert result["feature_count"] == 20


def test_compute_overview_rate(sample_df):
    result = compute_overview(sample_df)
    assert result["subscribe_rate"] == round(2 / 6, 4)


def test_compute_overview_empty():
    empty_df = pd.DataFrame(columns=["id", "subscribe"])
    result = compute_overview(empty_df)
    assert result["total_records"] == 0
    assert result["subscribe_rate"] == 0.0


# ── compute_age_distribution ──


def test_age_distribution_returns_df(sample_df):
    result = compute_age_distribution(sample_df)
    assert isinstance(result, pd.DataFrame)
    assert "age" in result.columns
    assert "count" in result.columns


def test_age_distribution_sum_matches(sample_df):
    result = compute_age_distribution(sample_df)
    assert result["count"].sum() == len(sample_df)


# ── compute_job_subscribe_rate ──


def test_job_subscribe_rate_columns(sample_df):
    result = compute_job_subscribe_rate(sample_df)
    assert "job" in result.columns
    assert "subscribe_rate" in result.columns


def test_job_subscribe_rate_range(sample_df):
    result = compute_job_subscribe_rate(sample_df)
    assert (result["subscribe_rate"] >= 0).all()
    assert (result["subscribe_rate"] <= 1).all()


# ── compute_education_distribution ──


def test_education_distribution_columns(sample_df):
    result = compute_education_distribution(sample_df)
    assert "education" in result.columns
    assert "count" in result.columns


def test_education_distribution_sum(sample_df):
    result = compute_education_distribution(sample_df)
    assert result["count"].sum() == len(sample_df)


# ── compute_marital_subscribe ──


def test_marital_subscribe_has_marital_col(sample_df):
    result = compute_marital_subscribe(sample_df)
    assert "marital" in result.columns


def test_marital_subscribe_row_count(sample_df):
    result = compute_marital_subscribe(sample_df)
    assert len(result) <= sample_df["marital"].nunique()


# ── compute_month_subscribe_rate ──


def test_month_subscribe_rate_columns(sample_df):
    result = compute_month_subscribe_rate(sample_df)
    assert "month" in result.columns
    assert "subscribe_rate" in result.columns


def test_month_subscribe_rate_range(sample_df):
    result = compute_month_subscribe_rate(sample_df)
    assert (result["subscribe_rate"] >= 0).all()
    assert (result["subscribe_rate"] <= 1).all()


# ── filter_dataframe ──


def test_filter_no_filter(sample_df):
    result = filter_dataframe(sample_df)
    assert len(result) == len(sample_df)


def test_filter_by_job(sample_df):
    result = filter_dataframe(sample_df, job="admin.")
    assert len(result) == 2
    assert (result["job"] == "admin.").all()


def test_filter_by_job_all(sample_df):
    result = filter_dataframe(sample_df, job="全部")
    assert len(result) == len(sample_df)


def test_filter_by_marital(sample_df):
    result = filter_dataframe(sample_df, marital="single")
    assert len(result) == 2
    assert (result["marital"] == "single").all()


def test_filter_by_both(sample_df):
    result = filter_dataframe(sample_df, job="admin.", marital="married")
    assert len(result) == 1


def test_filter_no_match(sample_df):
    result = filter_dataframe(sample_df, job="nonexistent")
    assert len(result) == 0
