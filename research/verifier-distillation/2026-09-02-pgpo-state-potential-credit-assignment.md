# PGPO：用跨轨迹状态势能细化失败轨迹信用分配

## 基本信息

- **论文标题**：PGPO: Potential-Guided Policy Optimization for Multi-Turn Agentic Tasks
- **作者**：Yuyao Zheng, Haipeng Sun, Junwei Bao, Lemao Liu, Hongfei Jiang, Yang Song, Dejing Dou
- **首次公开日期**：2026-09-02
- **当前版本日期**：2026-09-02（v1）
- **arXiv**：[2609.02236](https://arxiv.org/abs/2609.02236)
- **DOI**：[10.48550/arXiv.2609.02236](https://doi.org/10.48550/arXiv.2609.02236)（DataCite 注册待完成）
- **代码**：截至 v1 未在 arXiv 页面提供公开代码链接

## 一句话结论

PGPO 从同组 rollout 的锚点状态回报估计经验势能，用相邻状态势能差给每个动作赋 credit，避免把失败轨迹中的有效步骤与错误步骤一并惩罚。

## 真正新增的内容

**论文原文结论**：现有 step-level advantage 仍主要继承各自轨迹终局，失败轨迹内的好动作难以区分。PGPO 在 rollout group 中寻找可对齐的 anchor state，以跨轨迹回报统计估计 state potential，再以相邻势能差生成 action advantage，让成功/失败轨迹之间传播信用。

对 verifier 路线的新增意义在于：局部动作价值不再等于单条轨迹终局标签，而由“到达相似状态后其他分支的结果”共同估计。

## 核心方法

对同一任务采样一组多轮轨迹，识别可共享或匹配的 anchor states；聚合从这些状态继续执行的 return 得到经验势能。每步 advantage 由后继状态势能减前态势能构成，并用于 group-based policy optimization。该设计重点改善失败轨迹内部的局部区分，额外训练开销很小。

## 关键实验结果

**论文报告**：在 ALFWorld 与 WebShop 上，相对近期 group-based RL 方法取得强整体表现；进一步分析显示失败侧 credit 更有信息量且训练开销可忽略。arXiv v1 页面未提供统一数值表或公开代码，因此不外推具体提升幅度，也不把“强表现”解释为跨域稳定。

## 证据质量与局限

证据目前为中等：两个标准交互基准且方法动机清楚，但公开摘要缺少细粒度数值；anchor-state 匹配质量决定势能偏差。在部分可观测、状态别名或随机环境中，表面相似状态可能有不同未来；同组经验势能也不是独立真值，可能随当前 policy 共适应。

## 最接近的相关工作

最接近 GiGPO、CrEST、SOPD、LURE、Wrong but Useful、AgenticRAG-FP 和 process reward/value modeling。区别是 PGPO 用跨轨迹锚点传播终局回报，而非让 LLM Judge 直接为每一步打分。

## 如何复用或推进 LLM-as-a-Verifier

**分析推断**：将势能从单点期望扩展为 ordinal return distribution，记录成功、部分推进、可恢复失败、不可恢复失败的概率；同一锚点下的候选动作自然构成 A/B/T。LLM verifier 可负责语义状态对齐和 critique，环境 rollout 负责校准势能方向。对无法可靠对齐的状态输出 abstain，并保留探索。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：蒸馏 state-potential 分布及相邻差，而非整轨迹总分。
- **A/B/T 与序数分布**：同一 anchor 下比较动作后继分布；置信区间重叠标 T。
- **真值门控**：只有真实 rollout return 决定梯度方向，LLM 相似度只决定候选状态是否可聚合。
- **critique states**：student 解释势能变化对应的进展/风险，再用后续回报验证解释。
- **高熵探索**：高方差势能或低样本 anchor 不做强剪枝；保留可能恢复的失败分支。
- **sealed eval**：用未见任务、独立随机种子及固定环境评估势能校准，防止 anchor 规则适配训练轨迹。