# When Evaluators of AI Agents Disagree: An Empirical Study of Native Scoring, LLM Judges, and Commit-Boundary Checks on tau2-bench

- **作者**：Sungbin Im
- **首次公开日期**：2026-11-10
- **版本日期**：2026-11-10（v1）
- **原始论文**：https://arxiv.org/abs/2611.14581
- **复现包（代码、轨迹、提示与标签）**：https://doi.org/10.5281/zenodo.23683806
- **标识符**：arXiv:2611.14581；DOI: 10.48550/arXiv.2611.14581

## 一句话结论

【论文原文】LLM Judge 的重复性很高却可能与环境真值严重不一致；一个无模型调用的 commit-boundary 规则检查，在 tau2-bench 的禁写案例上比多个 Judge 更可靠。

## 真正新增的内容

【论文原文】在同一 2,160 条工具轨迹上并列比较 native gold-state scoring、普通 LLM Judge、带 policy 的 Judge 和最小边界检查，并加入人工标注。该设计直接测量“终态真值、轨迹 Judge、规则检查”并非可互换的评价通道。

【分析推断】这是程序化/环境真值门控 teacher 信号的强证据：Judge 一致性或自洽性不能作为正确性替代；对 Agent verifier 蒸馏，应把写操作边界 checker 设为不可被软分数覆盖的硬门。

## 核心方法

1. 在 tau2-bench 航空与零售域运行 2,160 个 episode，记录每次数据库写入。
2. 使用四种 evaluator 对同一 episode 评分。
3. 两名标注者独立标注 120 条轨迹的任务正确性、政策合规和 commit 正确性。
4. 检查 verification、correction、safe-termination gates 是否减少禁写。

## 关键实验结果

【论文原文】Judge 重复同一 verdict 的比例为 98.2%，但与 native scoring 仅有 56.2% 一致。在 11 个实际执行禁写的 episode 中，Judge 通过 10–11 个，强 Judge 仍通过 6 个，而 boundary evaluator 捕获全部 11 个；三类 gate 未显著降低禁写。无 gate 时禁写率为 11.1%。

## 证据质量与局限

【论文原文】样本量大、同轨迹多 evaluator 对照、含人工标注，且公开复现材料。

【分析推断】11 个禁写案例的绝对数量仍小，人工标注仅覆盖 120 条；boundary checker 针对 commit 语义，不能替代开放式质量评价。结果支持“硬门优先”，不支持“完全弃用 LLM Judge”。

## 最接近的相关工作

最接近 Ground-truth-as-code、ContrAgent、GCAC、GameLogicBench、MAWILE 与 Judge panel dependence 研究。区别在于直接对齐真实数据库写入边界，并展示 evidence digest 丢失关键状态会让 gate 反而拒绝合法请求。

## 如何复用或推进 LLM-as-a-Verifier

构造双通道 verifier：commit/permission/state transition 由程序规则给硬 verdict，LLM 只评价意图、证据充分性和非结构化质量。序数分数必须以硬 verdict 为条件；硬失败不可被平均高分抵消。对 digest 做字段覆盖审计，并把缺失状态显式标 T。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：硬边界失败将 distillation direction 设负或屏蔽，不由 Judge 幅度翻转。
- **A/B/T**：同一动作前后的 commit state 可直接构造 A/B；身份、状态等关键字段缺失时标 T。
- **环境真值门控**：把数据库 diff、权限与期望写集合纳入 teacher certificate。
- **critique states**：critique 必须引用未被 digest 丢弃的状态字段。
- **高熵探索**：边界内的多个合法写法继续保留，不让规则 checker 误充完整策略。
- **sealed eval**：使用隐藏写操作断言和独立人工抽检，且禁止训练 Judge 访问 sealed labels。
