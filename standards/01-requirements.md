# 01 · 需求 / 活 PRD 〔本项目活记忆 · AI 维护〕

> **作用**:这是本项目唯一的需求文档。所有新功能、缺陷、技术债都追加到这里,不要另起多个 PRD 文件。
> **更新时机**:每次有新需求、需求变更、验收标准变化时更新。

---

## 1. 项目背景

银行营销团队希望通过历史客户数据（21 个特征）分析营销效果，并离线训练模型后构建在线预测系统——营销人员通过点选式表单输入客户特征，即可预测该客户是否会认购定期存款。

**交付目标**: 跑通 CI，本地 Docker 部署，启动后提供 URL 给用户验证。

---

## 2. Issue 生命周期

| 阶段 | 状态 | 动作 |
|---|---|---|
| 提出 | Open | 写清场景、目标、验收标准 |
| 排期 | Backlog / Todo | 决定优先级和负责人 |
| 开发 | In Progress | 从 main 开 feature 分支 |
| 评审 | In Review | 提 PR,等待 CI 和 Review |
| 合并 | Done | PR 合并 main,自动关闭 Issue |
| 验收 | Verified | 按验收标准确认 |

**追踪规则**: 分支名带 Issue 号,PR 描述写 `closes #<编号>`。

---

## 3. 用户故事模板

```text
### US-<编号> <一句话标题> · 状态: Backlog
作为 <角色>,
我想要 <能力>,
以便 <价值>。

验收标准:
- AC1: Given <前提>,When <动作>,Then <可验证结果>。
- AC2: ...

技术备注:
- <可选:约束、边界、风险>
```

---

## 4. 需求清单

### US-1 初始化项目工程化与 CI · 状态: Backlog

作为 **项目开发者**,
我想要 项目具备基础工程结构、测试与 CI 流水线,
以便 后续每次开发都能自动检查代码质量。

验收标准:
- AC1: Given 项目骨架（app/tests/data/standards），When 初始化完成，Then 包含 `app/`、`tests/`、`data/`、`Dockerfile`、`.github/workflows/ci.yml`、`pyproject.toml`、`requirements.txt`、`requirements-dev.txt`。
- AC2: Given PR 提交，When CI 触发，Then 至少包含 ruff 格式检查、ruff 静态检查、pytest 单元测试、docker build 构建检查。
- AC3: Given CI 全部通过，When 状态为绿，Then 允许合并；任意一项失败则红灯禁止合并。
- AC4: Given Docker 镜像构建成功，When `docker run -d --name banksys_sy_lixiaohua -p 8888:8501 banksys_sy_lixiaohua` 启动，Then `curl -fsS http://localhost:8888/_stcore/health` 返回 200。
- AC5: Given 项目初始化完成，When 更新 `standards/PROGRESS.md`，Then 记录已完成事项与下一步 TODO。

技术备注:
- 仓库名称及 Docker 容器名称均为 `banksys_sy_lixiaohua`。
- 端口固定 8888（主机）→ 8501（容器内 Streamlit 默认端口）。
- **仅 CI，不做 CD**；本地部署由开发者在本地执行 `docker` 命令完成验证。

---

### US-2 数据加载与预处理模块 · 状态: Backlog

作为 **开发者**,
我想要 一个可复用的数据加载模块,
以便 支持数据分析页面和模型训练的数据需求。

验收标准:
- AC1: Given `data/train.csv` 存在,When 调用 `load_train_data()`,Then 返回 pandas DataFrame 且行数 > 0、列包含 21 个特征及目标变量 `subscribe`。
- AC2: Given `data/test.csv` 存在,When 调用 `load_test_data()`,Then 返回 pandas DataFrame 且列结构与训练数据一致（允许缺少目标变量）。
- AC3: Given 数据加载,When 处理数据,Then 正确处理缺失值（如标记为 `unknown`/`nonexistent`）。
- AC4: Given 数据加载模块,When 编写单元测试,Then 覆盖正常加载、文件不存在、空文件场景。
- AC5: Given 函数接口,When 调用方使用,Then 提供清晰的中文/英文列名映射与数据类型说明。

技术备注:
- 数据文件为 UTF-8 编码 CSV。
- 训练数据 `train.csv`（约 2.8 MB），测试数据 `test.csv`（约 0.9 MB）。
- 目标变量：`subscribe`（yes/no 二分类）。

---

### US-3 数据分析交互页面 · 状态: Backlog

作为 **业务分析师**,
我想要 通过可视化界面探索银行营销数据,
以便 快速理解客户特征分布和营销效果。

验收标准:
- AC1: Given 访问应用首页或导航到"数据分析"页面,When 页面加载完成,Then 显示数据概览（总记录数、认购率、特征数量等关键指标）。
- AC2: Given 数据分析页面,When 选择分析维度,Then 展示对应可视化图表（至少包含：年龄分布饼图、职业认购率柱状图、教育水平分布图、婚姻状况与认购关系图）。
- AC3: Given 数据分析页面,When 用户进行筛选操作（如选择特定月份、特定职业）,Then 图表实时更新,交互响应流畅。
- AC4: Given 页面功能,When 编写测试,Then 核心可视化逻辑函数（数据聚合、统计计算）有单元测试覆盖。
- AC5: Given Docker 容器运行,When 访问数据分析页面,Then 页面正常渲染无报错。

技术备注:
- 使用 Streamlit 原生组件：`st.metric`、`st.pyplot`、`st.plotly_chart`、`st.selectbox` 等。
- 图表建议：年龄分布饼图、职业 vs 认购率柱状图、教育水平热力图/条形图、婚姻状况与认购关系图。
- 页面通过 Streamlit 多页机制自动发现 `app/pages/` 目录。

---

### US-4 离线模型训练脚本 · 状态: Backlog

作为 **开发者**,
我想要 一个可复现的离线训练脚本,
以便 从历史数据中训练出认购预测模型。

验收标准:
- AC1: Given `data/train.csv` 存在,When 执行 `python -m app.ml.train`,Then 在 `app/ml/model/` 目录输出模型文件（`model.pkl` 及配套 encoder）。
- AC2: Given 训练完成,When 查看日志/终端输出,Then 打印关键指标：AUC、准确率（Accuracy）、分类报告（precision/recall/f1）。
- AC3: Given 模型文件已存在,When 再次执行训练,Then 支持 `--overwrite` 参数覆盖或默认跳过。
- AC4: Given 训练脚本,When 在任意环境执行,Then 训练结果可复现（固定 `random_state`）。
- AC5: Given 模型产物目录,When 提交代码,Then `app/ml/model/` 在 `.gitignore` 中,不进 Git。
- AC6: Given Docker 构建,When 执行 `docker build`,Then 构建过程中自动运行训练脚本生成模型,使镜像自包含模型文件。

技术备注:
- 使用 scikit-learn（LogisticRegression / RandomForest 任选其一）。
- 处理类别特征（OneHotEncoder / LabelEncoder）。
- 固定 `random_state=42` 保证可复现。
- Docker 构建时用 `RUN python -m app.ml.train --overwrite` 将模型烤进镜像。

---

### US-5 预测服务核心逻辑 · 状态: Backlog

作为 **系统**,
我想要 一个预测服务模块,
以便 根据输入客户特征返回认购预测结果。

验收标准:
- AC1: Given 模型文件存在,When 调用 `predict(features_dict)`,Then 返回字典包含 `subscribe`（bool）、`probability`（float）、`confidence`（string）。
- AC2: Given 合法特征输入,When 调用预测,Then 特征编码与训练时一致,预测结果正确（高认购特征得高概率,低认购特征得低概率,端到端验证）。
- AC3: Given 缺失/非法特征输入,When 调用预测,Then 返回明确错误信息,不崩溃。
- AC4: Given 模型文件不存在,When 调用预测,Then 返回友好提示"模型未找到,请先运行训练"。
- AC5: Given 预测模块,When 编写测试,Then 覆盖正常预测、模型缺失、缺失特征、非法值、未知类别、响应时间（<1s）场景。

技术备注:
- 特征编码必须与训练时一致（建议保存 encoder 与模型一起）。
- 模型加载使用 `lru_cache` 避免重复加载。
- 返回格式示例：`{"subscribe": true, "probability": 0.85, "confidence": "high"}`。

---

### US-6 在线预测交互页面 · 状态: Backlog

作为 **营销人员**,
我想要 通过点选式表单输入客户特征,
以便 快速预测该客户是否会认购定期存款。

验收标准:
- AC1: Given 访问"预测系统"页面,When 页面加载,Then 显示点选式输入表单（每个特征对应一个选择器,选项值从训练数据中动态获取）。
- AC2: Given 表单所有必填项填写完成,When 点击"预测"按钮,Then 页面显示预测结果：是否认购标签、概率进度条、置信度、建议文案。
- AC3: Given 预测结果显示,When 用户查看,Then 提供"重置"按钮清空表单,支持重新输入与预测。
- AC4: Given 模型文件缺失,When 页面加载,Then 显示友好错误提示而非崩溃。
- AC5: Given Docker 容器运行,When 访问预测页面,Then 页面正常渲染,预测功能端到端可用。

技术备注:
- 使用 Streamlit 的 `st.selectbox`、`st.number_input`、`st.button` 组件构建点选式表单。
- 类别型特征的选项从训练数据中提取唯一值,而非硬编码。
- 结果展示包括：预测标签（认购/不认购）、概率进度条、置信度（high/medium/low）、建议文案。

---

### US-7 测试覆盖与质量门禁 · 状态: Backlog

作为 **CI 流水线**,
我想要 核心逻辑有充分的测试覆盖,
以便 保证代码质量,防止回归。

验收标准:
- AC1: Given 核心业务逻辑,When 运行 `pytest --cov=app/models --cov=app/ml --cov-fail-under=80`,Then 覆盖率 ≥80% 且全部通过。
- AC2: Given CI 触发,When PR 提交,Then CI 依次执行 ruff format check、ruff check、pytest with coverage、docker build。
- AC3: Given 任意检查失败,When CI 红灯,Then PR 禁止合并。
- AC4: Given 本地开发,When 提交前,Then 开发者本地执行 ruff + pytest 自检并全绿。

---

## 5. 非功能需求

- **安全**: 密钥只进 Secrets,不进 Git。本项目为教学数据,数据可入库。
- **可维护**: 一需求一小 PR,避免大爆炸式提交。
- **可测试**: 核心逻辑必须有单元测试,UI 页面按 Streamlit 惯例不计入覆盖率。
- **可部署**: 本地 Docker 启动后健康检查通过方可交付。
- **性能**: 单次预测响应 <1s,页面首屏加载 <3s。
- **交付方式**: 仅 CI（GitHub Actions）,不做 CD。本地 `docker build && docker run` 后提供 URL 给用户验证。
