# Stopping and Routing LLM Judge Panels

## 基本信息

- **作者**：Bin Zhu、Yi Xie、Yanghui Rao
- **首次公开日期**：2026-08-20
- **版本日期**：2026-08-20（v1）
- **arXiv ID**：2608.19802
- **DOI**：10.48550/arXiv.2608.19802
- **原始论文**：https://arxiv.org/abs/2608.19802
- **代码**：截至该版本未发现公开代码

## 一句话结论

与其把更多 Judge 无条件加入集成，不如用小规模人工审计集估计每个 Judge 相对当前 panel 的条件增益，将其划分为冗余副本、全局互补者或切片专家，并在验证增益低于阈值时停止调用。

## 真正新增的内容

**论文原文结论**：论文把 Judge panel 从“固定成员的聚合问题”改写为带成本、可路由、可停止的条件分配问题。一个 Judge 的价值不是单体准确率或与其他 Judge 的表面差异，而是其在已有 panel 输出条件下对目标标签风险的剩余降低量；切片专家只在部署时可识别的子群上调用。

**分析推断**：这可以作为 distributional verifier 的外层控制器：程序化 verifier、pairwise Judge、序数评分模型和 critique Judge 不必每条轨迹全调用，而可根据状态、分歧、熵或程序化检查结果动态组合。它不是 verifier distillation 本身，但提供了选择 teacher 信号和控制蒸馏成本的直接机制。

## 核心方法

1. 用小规模带真值的审计集，将候选 Judge 输出规范化为二元、A/B 或连续评分。
2. 对当前 panel 拟合条件校准器，估计加入候选 Judge 后的 held-out squared calibration risk 降幅。
3. 将候选划分为：
   - **copy**：加入后无显著剩余信息；
   - **complement**：对全局风险有稳定增益；
   - **specialist**：只在预先声明且部署时可计算的切片上有增益。
4. 按“验证增益－调用成本”贪心加入 Judge；低于阈值时停止。切片路由不能使用最终人工标签，只能使用元数据、已有 verifier 输出、分类器或已观察到的 Judge 分歧。
5. 构造集、验证集和最终测试集严格分离；最终测试只用于一次性报告。

## 关键实验结果

**论文原文结果**：

- 覆盖 reasoning、代码 public-test 过拟合、安全、偏好、RewardBench/Arena100K、SummEval、MATH-500 等审计场景，结果平均于 10 次随机切分。
- 在 MBPP public-overfit 上，角色路由方案风险为 0.0097、准确率 0.9900，优于单 Judge 的 0.0226/0.9767 和全量 flat panel 的 0.0158/0.9617。
- 在 JailbreakBench-7 上，角色路由达到风险 0.1094、准确率 0.8527，而单 Judge 为 0.1183/0.8349。
- 在包含 10 个近重复 prompt 变体的 LLMBar 压力测试中，角色路由以平均 3.64 次调用达到 0.7143 准确率；全调用 logistic stack 用 10 次调用达到 0.6862。
- 论文也报告某些 RewardBench、MATH 等边界情形仍值得保留广泛集成，并不宣称稀疏路由总是最优。

## 证据质量与局限

- **证据质量：中高。** 有多个任务类型、强基线、成本指标、10 次切分、95% 置信区间，以及构造/验证/最终测试分离。
- 依赖小规模人工审计标签和预先声明的可部署切片；分布漂移后角色与阈值可能失效。
- 当前主要是贪心单 Judge 增益，可能漏掉两个单独无效但联合互补的高阶组合。
- 实验多为静态单样本评价矩阵，并未直接验证长时程 Agent 轨迹中的在线路由稳定性。
- panel 与路由规则仍可能对审计集共适应；最终测试隔离降低但不能消除长期反复调参后的泄漏风险。

## 最接近的相关工作

最接近的是 FrugalGPT/RouteLLM 式成本级联、Dawid–Skene/reliability jury、全调用 stacking，以及针对 LLM-as-a-Judge 的多 Judge 集成与校准。与仅按单体置信度升级调用不同，本工作测量候选 Judge 相对现有 panel 的条件信息增益。

## 如何复用或推进 LLM-as-a-Verifier

- 把程序化 outcome verifier 作为低成本首层；当它饱和时停止，无须再调用 LLM Judge。
- 当程序真值不完整时，根据工具错误类型、任务阶段和 Judge 分歧路由专门的 critique/verifier。
- 将校准器输出保留为分布而非硬投票，为后续 A/B/T 或序数评分分布提供不确定性。
- 定期用新的人类审计样本重新估计角色，避免将历史“强 Judge”永久固化为 teacher。

## 对 Agent verifier × OPD 路线的具体影响

**分析推断**：

- **score-level on-policy verifier distillation**：只在 verifier 对当前 panel 有条件增益的 rollout 上加入其 score，避免重复 teacher 信号放大。
- **pairwise A/B/T 与序数分布**：把 A/B/T、过程分数和 outcome verifier 作为异构 panel 成员，用条件风险增益决定组合，而非强制压成一次多数投票。
- **程序化/环境真值门控**：当可执行 verifier 已决定结果时直接停止；只把剩余不确定样本交给 LLM Judge。
- **student-generated critique states**：critique Judge 可作为只在高分歧或特定失败切片触发的 specialist。
- **高熵分叉探索**：不应把高熵本身等同于失败；可把熵作为路由信号，调用互补 Judge 后再决定是否蒸馏。
- **sealed eval**：沿用构造/验证/最终测试三级隔离，并额外建立长期不参与 panel 选择的 sealed Agent 轨迹集，防止 evaluator 与策略共同适应。