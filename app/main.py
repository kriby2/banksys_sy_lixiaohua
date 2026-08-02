"""银行营销数据分析与认购预测系统 — Streamlit 主入口."""

import streamlit as st

st.set_page_config(
    page_title="银行营销分析与预测",
    page_icon=":bank:",
    layout="wide",
)

st.title("银行营销数据分析与认购预测系统")
st.markdown(
    """
    本系统基于银行营销历史数据，提供两大核心功能：

    - **数据分析**：探索客户特征分布、营销效果分析、数据可视化
    - **在线预测**：基于机器学习模型，输入客户特征预测其认购意愿

    请通过左侧导航栏选择功能页面。
    """
)
