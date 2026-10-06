# Asking Earns Nothing: Scoring the Decision to Act in BFCL Multi-Turn

- 作者：Yangze Liu、Zhongyi Han
- 首次公开日期：2026-10-03
- 当前版本日期：2026-10-03（v1）
- arXiv：2610.04429
- 原始论文：https://arxiv.org/abs/2610.04429
- Canonical URL：https://doi.org/10.48550/arXiv.2610.04429
- 代码/数据：论文称发布 turn-level scorer、配对样本与 31 条人工核验坏例；摘要页未提供直接仓库链接

## 一句话结论

【论文原文】BFCL Multi-Turn 在本应评价“信息不足时询问、信息完整时行动”的关键回合跳过评分，导致猜测不受罚、询问不获益，官方排名可能与真实决策能力相反。

## 真正新增的内容

【论文原文】作者利用 should-ask 样本与其完整信息 base twin 构成受控配对，仅用存储轨迹和确定性 turn-level scorer 评价是否尝试改变世界的调用，无需 LLM Judge。

## 核心方法

【论文原文】对 223 对同回合索引、仅缺一项信息的 twin，分别检查完整条件下是否行动、缺失条件下是否克制；“总行动”与“总询问”都只能得 50 分，从而隔离真正的条件决策。

## 关键实验结果

【论文原文】gpt-5.4 在完整回合行动率 83.4%、缺失回合克制率 78.0%，七模型中决策准确率最高 80.7%，但官方分数排第六。加入“不要询问”提示后，真实决策准确率无可检测变化，官方两类分数却上升 13.5–23.5 点。

## 证据质量与局限

【论文原文】配对设计强、评分确定性且含 31 条人工核验坏例。局限是针对 BFCL 特定类别与实现；二元“是否尝试调用”不能覆盖询问质量、后续恢复和工具参数正确性；需确认发布 scorer 的版本与官方数据版本匹配。

## 最接近的相关工作

最接近 Executable-Contract Audit、Harness or Model、Interface-Induced Trajectory Censoring，以及 Agent 轨迹可诊断性/abstention。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】将“问还是做”设为独立 verifier 维度：同一任务构造 complete/incomplete twins，由程序判断该回合是否允许副作用动作；这比只看最终成功更能测不确定性处理与可恢复性。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：【分析推断】对 twin 状态蒸馏“行动许可概率”，而非复用整轨迹总分。
- **A/B/T 与序数分布**：【分析推断】完整/缺失信息下的动作构成条件 A/B；信息可选时允许 T。
- **硬真值门控**：【分析推断】缺失必要槽位时，程序门控禁止世界改变调用。
- **critique states**：【分析推断】critique 需指出缺失字段和最小澄清问题。
- **高熵探索**：【分析推断】允许多种询问表述，但不把猜测动作当探索。
- **sealed eval**：【分析推断】加入隐藏 twin 和 scorer 审计，防止模型针对公开“应问”模板。
