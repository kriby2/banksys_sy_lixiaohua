# PROGRESS · banksys_sy_lixiaohua 〔本项目活记忆 · 状态机〕

> **作用**:这是项目的"存档点"。任意 AI、任意重启会话,读它即可知道当前做到哪、下一步做什么、踩过什么坑。
> **更新时机**:每完成一个有意义步骤、每次会话结束前。
> **格式要求**:时间倒序,最新在上;短、准、可接力。

---

## 当前状态 (最后更新: 2026-08-02 · by AI)

- **阶段**: `US-1 开发完成，本地自检全绿，等待推送 PR`
- **六步流程位置**: 第④步（本地 CI 自检）已完成 → 准备第⑤步（推送 + 提 PR）
- **上一步完成**: 项目骨架全部代码（pyproject.toml / Dockerfile / CI workflow / app / tests），ruff + pytest 全绿
- **下一步**: git push → 提 PR → CI 复检 → 人工合并
- **分支**: `feature/1-project-init`
- **阻塞项**: 无

---

## 待办清单 (TODO,按优先级)

### 第一批：初始化项目工程化与 CI（US-1）
- [x] ① 创建 GitHub 仓库 `banksys_sy_lixiaohua`（开源）→ https://github.com/kriby2/banksys_sy_lixiaohua
- [x] ② 初始化项目骨架：`app/`、`tests/`、`Dockerfile`、`.github/workflows/ci.yml`、`pyproject.toml`、`requirements.txt`、`requirements-dev.txt`、`.gitignore`
- [x] ③ 实现 `app/main.py`（Streamlit 入口,首页）+ `app/pages/`（多页占位）
- [x] ④ 配置 ruff（pyproject.toml）+ 排除 pages/ 的 N999 规则
- [x] ⑤ 编写 Dockerfile（python:3.11-slim, ENV PYTHONPATH=/app, Python urllib 健康检查, 无 apt/curl）
- [x] ⑥ 编写 CI workflow（ruff format check + ruff check + pytest --cov + docker build）
- [x] ⑦ 本地自检全绿：ruff format ✓ / ruff check ✓ / pytest 3/3 ✓ / 100% 覆盖率
- [ ] ⑧ git push → 提 PR → CI 复检全绿 → 人工合并
- [ ] ⑨ 本地 `docker build && docker run -p 8888:8501` 验证健康检查

### 第二批：数据加载与预处理模块（US-2）
- [ ] ① 实现 `app/models/data_loader.py`（load_train_data / load_test_data）
- [ ] ② 编写 `tests/test_data_loader.py`（正常/文件不存在/空文件/列验证/缺失值处理）
- [ ] ③ 本地自检 → 提 PR → 人工合并

### 第三批：数据分析交互页面（US-3）
- [ ] ① 实现 `app/models/visualizer.py`（数据聚合/统计函数）
- [ ] ② 实现 `app/pages/01_data_analysis.py`（数据概览/饼图/柱状图/热力图,交互式筛选）
- [ ] ③ 编写 `tests/test_visualizer.py`
- [ ] ④ 本地自检 → 提 PR → 人工合并

### 第四批：离线模型训练脚本（US-4）
- [ ] ① 实现 `app/ml/train.py`（Pipeline: ColumnTransformer + OneHotEncoder + Classifier,固定种子）
- [ ] ② `app/ml/model/` 加入 `.gitignore`
- [ ] ③ 本地执行训练,确认产出 `model.pkl` 及 encoder,AUC ≥ 0.85
- [ ] ④ 编写 `tests/test_train.py`
- [ ] ⑤ 本地自检 → 提 PR → 人工合并

### 第五批：预测服务核心逻辑（US-5）
- [ ] ① 实现 `app/models/predictor.py`（load_model / predict）
- [ ] ② 编写 `tests/test_predictor.py`（正常预测/模型缺失/缺失特征/非法值/未知类别/响应时间）
- [ ] ③ 本地自检 → 提 PR → 人工合并

### 第六批：在线预测交互页面（US-6）
- [ ] ① 实现 `app/pages/02_prediction.py`（点选式表单,选项从数据动态获取）
- [ ] ② 集成 predictor 模块（结果含标签/概率进度条/置信度/建议文案）
- [ ] ③ 本地 Streamlit 验证：两个页面均可访问,预测端到端可用
- [ ] ④ 本地自检 → 提 PR → 人工合并

### 第七批：质量门禁完善（US-7）
- [ ] ① 确保核心模块测试覆盖率 ≥80%（data_loader/visualizer/predictor/train）
- [ ] ② 更新 Dockerfile 使其构建时自动训练模型（`RUN python -m app.ml.train --overwrite`）
- [ ] ③ 最终 docker build + docker run 验证：健康检查通过 + 两页面功能正常
- [ ] ④ 提 PR → CI 全绿 → 人工合并
- [ ] ⑤ 本地启动容器,提供 `http://localhost:8888` 给用户验证

---

## 关键决策记录 (ADR)

| 日期 | 决策 | 理由 |
|---|---|---|
| 2026-08-02 | 选择 Streamlit 作为 Web 框架 | 快速构建数据应用；适合数据分析与模型演示场景；课程指定 |
| 2026-08-02 | 模型训练离线,预测在线 | 训练是重操作不适合实时请求；预测是轻操作需要快速响应 |
| 2026-08-02 | 数据集进 Git,模型产物不进 Git | 教学用公开数据方便复现；模型二进制大文件不应进版本控制 |
| 2026-08-02 | Docker 构建时自动训练模型 | 模型不进 Git,但镜像需自包含；构建时训练保证部署即可用 |
| 2026-08-02 | 端口固定 8888 | 用户指定端口；Streamlit 默认 8501,Docker 映射到主机 8888 |
| 2026-08-02 | 仅 CI,不做 CD | 用户要求：跑通 CI,本地部署验证即可,不需要自动部署到远程服务器 |

---

## 已知坑 (GOTCHAS)

_尚无记录,开发过程中遇到问题后将追加到此处。_

---

## 里程碑 (DONE)

- [x] 2026-08-02：填写项目规范文档（00-project-context.md / 01-requirements.md / PROGRESS.md）
