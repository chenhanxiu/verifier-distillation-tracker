# APEx：Agent 程序化经验蒸馏与测试时自适应

## 基本信息

- **论文标题**：APEx: Distillation of Agent Procedural Experience for Adaptive Deep Research Question Answering
- **作者**：Jie Ding, Rui Sun, Xinyuan Zhang, Zeyu Zhang, Xin Liu
- **首次公开日期**：2026-09-02
- **当前版本日期**：2026-09-02（v1）
- **arXiv**：[2609.02253](https://arxiv.org/abs/2609.02253)
- **DOI**：[10.48550/arXiv.2609.02253](https://doi.org/10.48550/arXiv.2609.02253)（DataCite 注册待完成）
- **代码**：[J-Ding519/APEx](https://github.com/J-Ding519/APEx)

## 一句话结论

APEx 用下游奖励优化“轨迹→程序化 skill”的 Distiller，并把 skill 作为测试时 Planner 更新的正则先验，直接连接了长轨迹经验蒸馏、student critique/skill state 与在线自适应。

## 真正新增的内容

**论文原文结论**：APEx 将经验分为实例级轨迹 memory 与类别级程序 skill，通过 Executor、Distiller、Planner 的三阶段交替 GRPO 闭环训练，使 skill 生成由下游效用驱动而非固定 prompt。测试时以多 Judge 的无真值奖励更新 Planner，并用历史 skill 的可靠度和支持样本数调节 alignment regularization，抑制策略漂移。

真正新增点是把“经验压缩是否好”转化为可训练目标，并让压缩后的 skill 不只是上下文提示，而是测试时 RL 的策略先验。

## 核心方法

实例 memory 保存 query、workflow summary、结果与复用胜率；类别 skill 保存推荐步骤、常见失败、支持数和成功率。三阶段分别冻结其他模块训练 Executor、Distiller、Planner。Planner 可依据首轮执行结果决定是否重规划。测试时三个 LLM Judge 分别检查推理一致性、轨迹证据支持、答案有效完整性，经 arbiter 聚合；skill alignment 权重随该 skill 的胜率与证据量增长。

## 关键实验结果

**论文报告**：7 个域内/域外基准平均 64.4%，高于 GPT-5.4 的 49.7%（+14.7 点）及最强 memory baseline MIA 的 61.4%（+3.0 点）；各基准分数为 68.7、67.8、75.2、66.3、42.4、66.9、63.8。skill-only 版本减少注入 token。论文同时做 skill sufficiency、上下文效率、泛化与消融分析。

## 证据质量与局限

覆盖 7 个基准、强 baseline 与公开代码，证据中等偏强。但测试时“ground-truth-free”更新依赖多 LLM Judge 和 arbiter，且伪奖励继续进入 memory consolidation，存在 evaluator 共适应与错误 skill 累积风险；结果主要是 QA/deep research，不等价于真实可执行 Agent。与 GPT-5.4 的比较还混合了 agent scaffold 和测试时更新收益。

## 最接近的相关工作

最接近 MemP、ExpeL、Memento、MIA、LongWoF-Bench、RubricEM、ARISE-RL 与 latent/on-policy self-distillation。相较普通 procedural memory，APEx 直接训练 Distiller；相较 token-level OPD，它蒸馏的是可读 skill，再用 RL 内化。

## 如何复用或推进 LLM-as-a-Verifier

**分析推断**：把 skill 的单一胜率改为条件序数分布（成功、部分推进、无效、造成回归），并记录环境/任务簇后验；Distiller 同时生成可检验 rubric 与 critique。只有独立执行或 sealed Judge 证明 skill 提高后续轨迹时，才把该 skill 蒸馏进 Planner。三 Judge 的分歧可保留为不确定性，而非由 arbiter 压成单分。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：对“有/无 skill”同前缀 rollout 的 verifier 分布做 on-policy 蒸馏，以实际增益门控。
- **A/B/T 与序数分布**：A/B 为两种 skill/plan，效果不可区分时保留 T；按成功、部分推进、回归建等级分布。
- **真值门控**：工具有效性和最终状态优先；多 Judge 只补充开放式质量。
- **critique states**：类别 skill 可作为 student-generated critique state，但必须携带支持轨迹、失败模式和可靠度。
- **高熵探索**：低支持数或高分歧 skill 只作弱先验，不应强制收缩动作分布。
- **sealed eval**：冻结独立 Judge、任务簇与 memory；同时报告在线伪奖励和不参与更新的真实指标。