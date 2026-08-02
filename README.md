# banksys_sy_lixiaohua

基于银行营销数据的客户认购分析与预测系统。

## 功能

- **数据分析**：交互式可视化探索客户特征分布与营销效果
- **在线预测**：基于机器学习模型，通过点选式表单预测客户认购意愿

## 技术栈

Python 3.11 / Streamlit / scikit-learn / pandas / pytest / ruff / Docker

## 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 启动应用
streamlit run app/main.py
```

## Docker 部署

```bash
docker build -t banksys_sy_lixiaohua .
docker run -d --name banksys_sy_lixiaohua -p 8888:8501 banksys_sy_lixiaohua
```

访问 http://localhost:8888

## CI

PR 触发自动检查：ruff 格式检查、ruff 静态检查、pytest 单元测试、docker build。
