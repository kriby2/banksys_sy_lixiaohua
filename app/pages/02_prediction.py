"""在线预测页面 — 点选式表单输入客户特征，预测认购意愿."""

import streamlit as st

from app.models.data_loader import CATEGORICAL_COLS, NUMERICAL_COLS, load_train_data
from app.models.predictor import predict as do_predict

st.title("认购预测")

# ── 加载数据获取选项 ──
df = load_train_data()

CATEGORY_OPTIONS = {}
for col in CATEGORICAL_COLS:
    vals = sorted(df[col].unique().tolist())
    CATEGORY_OPTIONS[col] = vals

NUMERICAL_STATS = {}
for col in NUMERICAL_COLS:
    NUMERICAL_STATS[col] = {
        "min": float(df[col].min()),
        "max": float(df[col].max()),
        "mean": float(df[col].mean()),
    }

# ── 表单 ──
st.subheader("客户特征输入")

with st.form("prediction_form"):
    col1, col2, col3 = st.columns(3)

    inputs = {}
    cats = list(CATEGORICAL_COLS)
    nums = list(NUMERICAL_COLS)

    # 分类特征 — 使用 selectbox
    for i, col in enumerate(cats):
        with [col1, col2, col3][i % 3]:
            inputs[col] = st.selectbox(col, CATEGORY_OPTIONS[col])

    # 数值特征 — 使用 number_input
    for i, col in enumerate(nums):
        with [col1, col2, col3][i % 3]:
            stats = NUMERICAL_STATS[col]
            step = 1.0 if col in ("age", "duration", "campaign", "pdays", "previous") else 0.1
            inputs[col] = st.number_input(
                col,
                value=float(stats["mean"]),
                min_value=float(stats["min"]),
                max_value=float(stats["max"]),
                step=step,
            )

    submitted = st.form_submit_button("预测", type="primary", use_container_width=True)

# ── 预测结果 ──
if submitted:
    try:
        result = do_predict(inputs)

        st.divider()
        st.subheader("预测结果")

        res_col1, res_col2, res_col3 = st.columns(3)

        with res_col1:
            if result["subscribe"]:
                st.metric("预测结果", "将认购", delta="Positive")
            else:
                st.metric("预测结果", "不认购", delta="Negative")

        with res_col2:
            prob = result["probability"]
            st.metric("认购概率", f"{prob:.1%}")
            st.progress(prob)

        with res_col3:
            conf_labels = {"high": "高", "medium": "中", "low": "低"}
            st.metric("置信度", conf_labels.get(result["confidence"], result["confidence"]))

        st.caption(f"响应时间: {result['response_time_ms']:.1f} ms")

        # 建议文案
        if result["confidence"] == "high":
            if result["subscribe"]:
                st.success("该客户有**很高**的认购意愿，建议优先跟进营销。")
            else:
                st.warning("该客户**极低**可能认购，可将资源投入其他客户。")
        elif result["confidence"] == "medium":
            if result["subscribe"]:
                st.info("该客户有**一定**认购意愿，可酌情跟进。")
            else:
                st.info("该客户认购意愿**偏低**，建议进一步了解需求。")
        else:
            st.info("模型对此预测置信度较低，建议结合其他信息综合判断。")

    except FileNotFoundError as e:
        st.error(f"模型未找到：{e}")
    except ValueError as e:
        st.error(f"输入错误：{e}")
