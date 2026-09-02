# Cheap Verifiers, Large Blind Spots：成本级联中的自验证盲区

## 基本信息

- **论文标题**：Cheap Verifiers, Large Blind Spots: Measuring the Reliability Cost of Cost-Saving Cascades
- **作者**：Dushyant Rajput
- **首次公开日期**：2026-09-01
- **当前版本日期**：2026-09-01（v1）
- **arXiv**：[2609.01345](https://arxiv.org/abs/2609.01345)
- **DOI**：[10.48550/arXiv.2609.01345](https://doi.org/10.48550/arXiv.2609.01345)（DataCite 注册待完成）
- **代码**：截至 v1 未在 arXiv 页面提供公开代码链接

## 一句话结论

论文实证并理论化说明：用同一个 verifier 决定升级、构造纠错数据并计算仪表盘，会让系统在真实错误率恶化时仍显示稳定；这是 verifier 蒸馏闭环必须设置独立 sealed eval 的直接反例。

## 真正新增的内容

**论文原文结论**：廉价 student 先回答，verifier 只把困难尾部升级给 frontier model；进一步用 verifier 拒绝样本微调 student。作者测得 verifier 对 student 错误的接受率（盲区 (eta)）会随 student 变强而增大，并给出两群体守恒关系 (epsilon_inftylesssim q_0eta_0)，说明所有 in-loop 指标都改善时真实质量仍可能不变或恶化。

新增价值是把 verifier 共适应从定性担忧变成可测量变量，并揭示“更强 student 更容易进入 verifier 盲区”的对抗性移动，而非假设错误独立同分布。

## 核心方法

在真实 LLM 级联上测量 student、不同能力 verifier、升级率、真实错误与 verifier 可见错误；再把 verifier 拒绝尾部用于多轮 corrective fine-tuning，观察系统动态。理论模型把输入划分为 verifier 可检测与盲区两群体，并用合成实验验证机制。

## 关键实验结果

**论文报告**：student 从 0.5B 扩到 32B 时，盲区 (eta) 从 0.12 增至 0.55。frontier verifier 可把 (eta) 降至约 0.05，但在 hard-MATH 上升级 46% 请求，而真实错误率为 39%，几乎消耗一半 frontier 成本。对小 student 的 naive corrective fine-tuning 在所有尝试的同族/跨族 teacher 下均退化并最终崩溃。期间 verifier 计算的仪表盘错误率始终约 3%，真实交付错误率最高达到 32%。

## 证据质量与局限

数值、真实模型实验、理论与合成验证相互支撑，证据很有针对性；但 v1 篇幅和任务范围有限，hard-MATH 级联不等于长时程工具 Agent。小 student 微调崩溃可能受数据量、优化和采样策略影响，不能推出所有 reward/verifier distillation 都失败。单作者且尚无代码链接，应把结论视为强警示而非普遍定理。

## 最接近的相关工作

接近 reward hacking、Goodhart 定律、Rubric Dropout、RecurSE、JuryProbe、Judge 共演化和选择性预测/模型级联。与一般 Judge 偏差研究不同，本工作测量偏差如何被闭环训练主动富集。

## 如何复用或推进 LLM-as-a-Verifier

**分析推断**：每轮记录至少三套指标：训练 verifier 分数、不同架构 sealed verifier 分数、程序/人工真值；估计条件盲区 (eta(s)) 随 student 版本、轨迹长度和错误类型的变化。蒸馏数据不能只来自拒绝尾部，应混入独立抽样的接受样本审计，并对 acceptance blind spot 做逆概率校正或保守 abstain。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：禁止用同一 score head 同时筛数据、给梯度和宣布提升；报告按 student 版本分层的 calibration/盲区。
- **A/B/T/序数**：保留 tie/abstain，特别审计 verifier 高置信接受但 sealed truth 失败的轨迹。
- **真值门控**：可执行终态优先于 verifier；对无硬真值项进行随机人工/独立 Judge 抽检。
- **critique states**：不要只训练 verifier 拒绝的 critique；抽查“无问题” critique 以发现遗漏盲区。
- **探索**：被 verifier 接受不等于可停止探索；对高风险或分布漂移状态维持一定随机升级率。
- **sealed eval**：必须完全脱离训练 verifier 与拒绝数据选择机制；持续追踪 in-loop 与 sealed 指标差值，差值扩张即停止闭环更新。