# RLDS：面向长轨迹 Agent 的子任务分解信用分配

## 基本信息

- 论文标题：Reinforcement Learning with Decomposed Subtasks
- 作者：Mattie Terzolo；Mikolaj Sacha；Ayan Sinha；Andrew Rabinovich
- 首次公开日期：2026-09-22
- 版本日期：2026-09-22（v1）
- arXiv：2609.27035
- DOI：https://doi.org/10.48550/arXiv.2609.27035
- 原始论文：https://arxiv.org/abs/2609.27035
- 代码：截至 2026-09-24，论文页面未提供作者代码链接

## 一句话结论

RLDS 不再把整条多轮轨迹压成一个 GRPO 标量，而是先按子任务拆分回报，再把每个子任务的相对优势集中到反思所标记的关键步骤。

## 真正新增的内容

【论文原文】Subtask-Decomposed Advantage Estimation（SDAE）在固定技能分类上分割轨迹奖励，分别计算组内相对优势，并依据子任务重要性把信用分配到相关 token，尤其集中到 reflection 标注为关键的执行步骤。

【分析推断】这为长时程 score-level verifier distillation 提供了二维分解：先在轨迹间比较同一子任务，再在轨迹内定位责任步骤，可避免终局成败把有效前缀和无关查询一起奖惩。

## 核心方法

1. 用固定 taxonomy 将复合任务拆为子任务。
2. 把终局或 rubric 回报分成子任务份额。
3. 对每个子任务独立计算 group-relative advantage。
4. 由 reflection 标识该子任务在哪一步产生实质影响，并据重要性向 token 分配信用。

## 关键实验结果

【论文原文】方法在 FrozenLake、HotpotQA、ScienceWorld 和 DeepResearch 四个 Agent 基准上评测。高异质性任务收益最大：ScienceWorld 提升 11.5 个百分点（95% CI +9.8 至 +13.3），FrozenLake 提升 9.8 个百分点（+7.0 至 +12.8）；HotpotQA 和 DeepResearch 的变化处于噪声范围。ScienceWorld 每步墙钟时间下降 10.9%。

## 证据质量与局限

【论文原文】论文提供配对 bootstrap 区间，并明确报告两个任务无显著收益，证据表达较克制。

【分析推断】固定 taxonomy 和由模型生成的 reflection 都可能成为新偏差源；回报“分份额”的正确性未必有环境真值。结果跨四类任务但尚未验证超长生产轨迹、不同 taxonomy 或 sealed evaluator 下的共适应。

## 最接近的相关工作

与 BATON 的“轨迹内归因 × 轨迹间权重”、PGPO 的状态势能、DRACO 的动态 rubric 信用、Key-Step Supervision 及 RECAP 最接近。RLDS 的独特之处是直接替换 GRPO 标量优势为子任务级组内优势，并在真实多轮 Agent 基准上验证。

## 如何复用或推进 LLM-as-a-Verifier

将 verifier 输出从单分数改为“子任务 × 序数等级”的分布矩阵，并为每个分量附证据步骤。只在环境日志能确认子任务完成或 reflection 与独立标注一致时，把对应信用送入 student；无法定位时保留 T/INCONCLUSIVE。

## 对现有 Agent verifier × OPD 路线的具体影响

【分析推断】

- score-level OPD：以子任务优势而非整轨迹分数缩放 teacher–student score gap。
- A/B/T：在同一子任务内比较两条轨迹或两个动作；跨子任务不可比时标 T。
- 真值门控：可执行检查器负责判定子任务是否完成，LLM reflection 只负责候选归因。
- critique states：student 反思必须绑定子任务、责任步骤和可重放证据后才进入训练。
- 高熵探索：对已成功但实现路径不同的子任务分别保留优势，避免总分将多样策略压平。
- sealed eval：冻结 taxonomy、重要性权重与终局 checker，并单独报告每个子任务的迁移和误归因率。