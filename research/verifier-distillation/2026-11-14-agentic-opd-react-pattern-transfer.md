# Agentic On-Policy Distillation Implicitly Reshapes LLMs' ReAct Patterns

- **作者**：Deyang Kong、Zhaoyi Li、Sijian Ren、Yuan Wei、Ying Wei、Defu Lian、Shikun Zhang、Wei Ye
- **首次公开日期**：2026-11-14
- **版本日期**：2026-11-14（v1）
- **原始论文**：https://arxiv.org/abs/2611.19244
- **代码**：未发现公开代码
- **标识符**：arXiv:2611.19244；DOI: 10.48550/arXiv.2611.19244

## 一句话结论

【论文原文】Agentic OPD 不只迁移能力，还会重塑 reasoning、tool action 与 observation acquisition 的 ReAct 模式；错误源域监督可让跨域准确率从 41.5% 降至 6.6%。

## 真正新增的内容

【论文原文】论文跨数学、ALFWorld 与 tau²-bench 分析 OPD 后的交互行为，显示同一监督会改变工具尝试、家庭动作和用户信息依赖。作者进一步用 domain-specific RL 前后 teacher preference change 选择性保留蒸馏位置，只依赖源域轨迹缓解负迁移。

【分析推断】这证明 score-level OPD 的“副作用”应在行为轨迹层审计，而不能只看源域正确率。teacher–student score 对齐可能同时蒸馏不适用的工具习惯和观察策略。

## 核心方法

1. 在三类任务上比较 OPD 前后 reasoning/action/observation 的 ReAct 统计。
2. 用不同领域 teacher 监督测量能力迁移与行为模式偏移。
3. 根据 teacher 在 domain RL 前后的 token preference change 筛选 OPD 位置。

## 关键实验结果

【论文原文】通用推理监督使数学工具尝试率从 70.4% 降到 14.4%，准确率从 16.7% 升到 38.0%；代码解释器监督改善 ALFWorld 动作与零售查询。ALFWorld 监督却使 tau²-bench 从 41.5% 降到 6.6%。选择性 OPD 保留 top 95% 位置后，tau² 准确率从 11.5% 回升到 29.9%，但伴随源域学习折衷。

## 证据质量与局限

【论文原文】包含跨三域行为分析、显著负迁移案例和选择性修复实验。

【分析推断】top-95% 阈值仍是经验选择；只用源域轨迹估计安全迁移不能覆盖目标域新工具与新依赖。ReAct 统计变化也不等于因果机制，需要 frozen harness 和环境重放进一步验证。

## 最接近的相关工作

最接近 Agentic-OPD、STRIDE、IWD、RoboDrop 与 RetireOPD；本文区别是把跨域负迁移具体定位到 ReAct 行为模式，而非仅报告最终分数。

## 如何复用或推进 LLM-as-a-Verifier

为 verifier 增加行为轴：工具必要性、观察充分性、用户信息依赖与恢复性。蒸馏前后都运行轨迹级 auditor，若 outcome 提升但行为轴恶化，则降低对应 token/turn 的 teacher 权重。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：score 必须按 reasoning/action/observation 分解，不能只蒸馏 outcome。
- **pairwise A/B/T 与序数分布**：同一结果下比较工具依赖与观察完整性；跨域证据不足标 T。
- **环境真值门控**：工具前置条件和用户信息依赖由环境/规范硬门控。
- **student-generated critique states**：critique 要指出行为模式何处被源域 teacher 误导。
- **高熵探索**：对 preference change 小或跨域不稳定的位置保留 student 分布。
- **sealed eval**：加入未见工具、未见 harness 与跨域任务，独立报告行为转移和终局成功。

