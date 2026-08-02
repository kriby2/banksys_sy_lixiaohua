"""数据分析交互页面."""

import matplotlib.pyplot as plt
import streamlit as st

from app.models.data_loader import load_train_data
from app.models.visualizer import (
    compute_age_distribution,
    compute_education_distribution,
    compute_job_subscribe_rate,
    compute_marital_subscribe,
    compute_month_subscribe_rate,
    compute_overview,
    filter_dataframe,
)

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

df = load_train_data()

st.title("数据分析")

# ── 筛选栏 ──
col1, col2 = st.columns(2)
with col1:
    selected_job = st.selectbox("职业筛选", ["全部"] + sorted(df["job"].unique().tolist()))
with col2:
    selected_marital = st.selectbox(
        "婚姻状况筛选", ["全部"] + sorted(df["marital"].unique().tolist())
    )

filtered_df = filter_dataframe(df, job=selected_job, marital=selected_marital)

# ── 数据概览 ──
st.subheader("数据概览")
overview = compute_overview(filtered_df)
cols = st.columns(5)
cols[0].metric("总记录数", overview["total_records"])
cols[1].metric("特征数量", overview["feature_count"])
cols[2].metric("认购人数", overview["subscribe_count"])
cols[3].metric("未认购人数", overview["no_subscribe_count"])
cols[4].metric("认购率", f"{overview['subscribe_rate']:.2%}")

st.divider()

# ── 图表区 ──
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("年龄分布")
    age_dist = compute_age_distribution(filtered_df)
    fig, ax = plt.subplots()
    ax.pie(age_dist["count"], labels=age_dist["age"], autopct="%1.1f%%")
    ax.set_title("Age Distribution")
    st.pyplot(fig)
    plt.close(fig)

with chart_col2:
    st.subheader("职业认购率")
    job_rate = compute_job_subscribe_rate(filtered_df)
    fig, ax = plt.subplots()
    ax.barh(job_rate["job"], job_rate["subscribe_rate"])
    ax.set_xlabel("Subscription Rate")
    ax.set_title("Subscribe Rate by Job")
    st.pyplot(fig)
    plt.close(fig)

chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    st.subheader("教育水平分布")
    edu_dist = compute_education_distribution(filtered_df)
    fig, ax = plt.subplots()
    ax.bar(edu_dist["education"], edu_dist["count"])
    ax.set_xlabel("Education Level")
    ax.set_ylabel("Count")
    ax.set_title("Education Distribution")
    ax.tick_params(axis="x", rotation=45)
    st.pyplot(fig)
    plt.close(fig)

with chart_col4:
    st.subheader("婚姻状况 vs 认购")
    marital_data = compute_marital_subscribe(filtered_df)
    fig, ax = plt.subplots()
    x = range(len(marital_data))
    width = 0.35
    yes_counts = marital_data.get("yes", [0] * len(marital_data))
    no_counts = marital_data.get("no", [0] * len(marital_data))
    ax.bar([i - width / 2 for i in x], list(yes_counts), width, label="Subscribed")
    ax.bar([i + width / 2 for i in x], list(no_counts), width, label="Not Subscribed")
    ax.set_xticks(x)
    ax.set_xticklabels(marital_data["marital"])
    ax.set_ylabel("Count")
    ax.set_title("Marital Status vs Subscription")
    ax.legend()
    st.pyplot(fig)
    plt.close(fig)

st.divider()

# ── 月份认购率趋势 ──
st.subheader("各月份营销认购率")
month_rate = compute_month_subscribe_rate(filtered_df)
fig, ax = plt.subplots()
ax.plot(month_rate["month"].astype(str), month_rate["subscribe_rate"], marker="o")
ax.set_xlabel("Month")
ax.set_ylabel("Subscription Rate")
ax.set_title("Monthly Subscription Rate Trend")
ax.tick_params(axis="x", rotation=45)
st.pyplot(fig)
plt.close(fig)
