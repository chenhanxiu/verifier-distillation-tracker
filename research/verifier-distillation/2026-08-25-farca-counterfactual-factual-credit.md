# FARCA: Fact-Aligned Reliability-Aware Credit Assignment for Reinforcement Learning with Factual Supervision

## 基本信息

- 作者：Qiming Xie、Wenjie Zheng、Xiangqing Shen、Rui Xia
- 首次公开日期：2026-08-25
- 版本日期：2026-08-25（v1）
- arXiv：2608.24350
- 原始论文：https://arxiv.org/abs/2608.24350
- DOI：https://doi.org/10.48550/arXiv.2608.24350
- 代码：论文公开页未提供

## 一句话结论

FARCA 将事实核验细化到 token 级，并用移除关键证据后的反事实依赖程度估计 verifier 可靠性，从而让事实奖励和局部 advantage 少受不可靠判断影响。

## 真正新增的内容

**论文原文结论：** 把 noisy factual credit assignment 分成定位歧义和可靠性歧义；通过对齐事实验证与 policy update 粒度解决前者，通过 counterfactual evidence attribution 为每个事实信号赋可靠性权重解决后者。

**分析推断：** 该反事实可靠性机制可直接迁移到 Agent 下一步动作 Judge：如果移除关键状态证据后结论仍不变，Judge 可能并未真正使用证据，其 teacher 权重应下降。

## 核心方法

先定位回答中与各可核验事实对应的 token 区间，产生局部事实奖励；再干预或移除关键证据，测量 factual judgment 对证据的依赖，形成可靠性权重，调节 token reward 和局部 policy advantage。

## 关键实验结果

论文报告在多个模型和多项事实推理 benchmark 上显著提高 factuality，同时保持通用推理能力。公开摘要未提供具体数值、置信区间或成本，因此不应扩写为定量领先结论。

## 证据质量与局限

证据质量中等偏低：方法与因果直觉清晰，但摘要证据仅为定性宣称，未提供代码或效应量。证据移除可能改变输入自然性，反事实依赖也只是 verifier 可靠性的经验代理，不等同于真实准确率。

## 最接近的相关工作

最接近 CROP、AgenticRAG-FP、SCAE、CrEST 和事实型 process reward。区别是把“判断是否依赖关键证据”直接用作训练权重。

## 如何复用或推进 LLM-as-a-Verifier

对每个下一步动作构造 evidence ablation：删除工具结果、环境状态或用户约束后重新评分；仅当 Judge 对真正关键证据敏感、对无关表述稳定时，才将其分数用于 verifier 蒸馏。

## 对 Agent verifier × OPD 实验路线的具体影响

- **Score-level OPD：** 用反事实证据依赖度乘以 teacher score，降低无依据高置信信号。
- **A/B/T：** 对同一动作在完整证据、关键证据删除、无关证据删除条件下形成三路校准。
- **真值门控：** 可执行事实与工具结果先给硬标签，反事实权重只调节软评分。
- **Student critique states：** critique 必须引用改变判断的关键证据，无法定位者降权。
- **高熵探索：** verifier 可靠性低时保留分支，不做强剪枝。
- **Sealed eval：** 干预模板和最终证据集分离，避免 Judge 学会表面化 ablation 线索。
