# RewardWeaver: Long-Horizon Interactive Learning for Language Agents via Self-Evolving Reward Adaptation

- 作者：Hengbo Xiao、Boyao Zhang、Purui Liu、Yuxuan Zheng、Haoran Yin、Haibo Liu、Fan Zhang
- 首次公开日期：2026-10-07
- 版本日期：2026-10-07（v1）
- 原始论文：https://arxiv.org/abs/2610.10120
- Canonical URL：https://arxiv.org/abs/2610.10120
- 代码：未发现公开代码链接

## 一句话结论

【论文原文】RewardWeaver 不固定 process reward，而在每个训练阶段依据低终局回报轨迹的反向归因，动态选择当前真正限制成功率的能力 rubric，同时冻结已接纳 rubric 的语义。

## 真正新增的内容

【论文原文】闭环连接策略优化、任务评价、失败归因和 reward adaptation；只有反复出现、受策略控制的瓶颈才获得下一阶段过程奖励，未被能力空间覆盖的失败通过受控流程扩展 rubric。

## 核心方法

【论文原文】维护经验证的 capability space；每阶段后对低结果轨迹做 outcome-grounded backward attribution，聚合瓶颈并分配对应 process rewards；新能力先验证再准入，既有语义保持固定。

## 关键实验结果

【论文原文】在 SOTOPIA、Amazon HistoryPrice 与新 Sales Benchmark 上取得论文所报 SOTA；消融支持动态奖励分配、失败锚定归因及 rubric 语义稳定性。摘要未给统一绝对增益。

## 证据质量与局限

【论文原文】覆盖社交、议价和销售三类长交互，并有组件消融。【分析推断】reward 适配与 policy 同循环，仍可能发生 evaluator 共适应；新 rubric 的发现与验证依赖归因器质量。

## 最接近的相关工作

【分析推断】接近 DRACO、Dr.Credit、BATON、PROSE、DynSTEER 与 continual failure search；独特点是动态选择 reward 但冻结已接纳语义。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】把五维/八维 Agent rubric 变成“语义冻结、权重可变”的能力空间；环境结果决定当前瓶颈，verifier 只调整各头训练权重，不允许在线改写定义。

## 对 Agent verifier × OPD 实验路线的具体影响

- 【分析推断】score-level OPD：按阶段瓶颈动态重权，但保存原始各维分数。
- 【分析推断】A/B/T：仅对有稳定失败证据的能力生成 A/B，其余 T。
- 【分析推断】真值门控：终局成功和执行日志负责反向归因的锚点。
- 【分析推断】critique states：新 critique 类型需通过受控准入再持久化。
- 【分析推断】高熵分叉：对当前瓶颈状态追加分叉，不全局收紧策略。
- 【分析推断】sealed eval：冻结 rubric 语义和隐藏任务，监控权重适配是否只提高训练闭环分数。