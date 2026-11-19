# Learning through Discernment: when a small language model learns from user feedback on the job, and when it decays

- **作者**：Sirisilp Kongsilp
- **首次公开日期**：2026-11-18
- **版本日期**：2026-11-18（v1）
- **原始论文**：https://arxiv.org/abs/2611.23716
- **代码与数据**：https://github.com/kratai-desci/research/tree/discernment/discernment
- **标识符**：arXiv:2611.23716；DOI: 10.48550/arXiv.2611.23716

## 一句话结论

【论文原文】持续从 Judge 接受的用户反馈学习会先改善再衰退；只有当 Judge 能把失败挡在训练集外且用户真正看得到结果时，在线学习才较稳定。

## 真正新增的内容

【论文原文】在 WebShop 与 τ²-bench 上模拟 127 条最长一年的 Agent“生命”，每天用被 Judge 接受的尝试夜间微调 LoRA；比较环境真值、用户明示 verdict、自判断和冻结 feedback sense，直接测量长期 evaluator 误差如何累积为能力衰退。

## 核心方法

1. Qwen3 0.6B/1.7B 每日执行任务，Judge 选择进入下一晚训练的 lesson。
2. 冻结 feedback sense 读取用户反应，并比较不同“是否先判断用户给出明确 verdict”的设计。
3. 追踪 lesson 中失败比例、长期任务效果与适配器演化。

## 关键实验结果

【论文原文】模型自评路线均先升后降。把礼貌放弃误判为成功的 sense 在 5 条生命中崩溃 3 条；discernment sense 使 5 条中 4 条在两周内接近 oracle，但到第 60 天退化至自评水平。τ²-bench 中用户看不到真实结果时，80% 被接受 lesson 实际失败。97 条生命中失败 lesson 占比与结果 Spearman ρ=-0.81。

## 证据质量与局限

【论文原文】时间跨度长、包含多种 Judge 与 oracle 对照，直接观察 feedback loop；但主要是模拟生活、单作者、模型较小。冻结 Judge 仍会遇到分布漂移，且“礼貌反馈”机制未必代表其他部署域。

## 最接近的相关工作

接近 continual self-training、reward model feedback loops、online RLHF、user-reaction learning、PROSE/GLARE 与 evaluator co-adaptation。其关键贡献是把长期 lesson 污染率与最终衰退关联起来。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】对生产 Agent 的用户点赞/感谢先建“用户是否能观察真实结果”的 applicability head；只有明示且可见的反馈进入 soft teacher。持续监控 oracle 抽检失败率，一旦超阈值暂停蒸馏并回滚，而不是把所有积极语言当奖励。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：teacher score 必须乘以 outcome-visibility 与 verdict-clarity 门控，并报告长期污染率。
- **pairwise A/B/T 与序数分布**：礼貌感谢但无可见结果应标 T/unknown，不能转为 A 或高分。
- **程序化/环境真值门控**：有 oracle 时强制覆盖用户反馈；无 oracle 时降低或拒绝更新。
- **student-generated critique states**：自评与用户反应均不得直接成为 lesson，需 frozen sense/抽检双重准入。
- **高熵分叉探索**：保留 Judge 不确定和用户不可见 outcome 的样本用于诊断，不投入主训练。
- **sealed eval**：使用持续冻结的 oracle panel 和跨时间留出集，检测 evaluator 与 policy 的共同漂移。
