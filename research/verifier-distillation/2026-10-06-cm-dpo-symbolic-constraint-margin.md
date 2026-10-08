# CM-DPO: Constraint-Margin Direct Preference Optimization for LLM Planning

- 作者：Rabimba Karanjai、Qun Gu、Hemanth Hegadehalli Madhavarao、Wenhuan Sun、Xiaojiao Yu 等
- 首次公开日期：2026-10-06
- 版本日期：2026-10-06（v1）
- 原始论文：https://arxiv.org/abs/2610.09219
- Canonical URL：https://arxiv.org/abs/2610.09219
- 代码：未发现公开代码链接

## 一句话结论

【论文原文】CM-DPO 用确定性符号 verifier 给出的连续违规幅度替代二元偏好，并以词典序目标保证硬约束不被软偏好交易掉，实现“硬真值定方向、违规程度定幅度”。

## 真正新增的内容

【论文原文】区分 1 美元与 1000 美元超预算等不同严重度；同时通过程序化约束画像和 reasoning teacher 的 minimal-edit distillation 生成偏差更小的训练对。

## 核心方法

【论文原文】从 symbolic verifier 计算 constraint margin，并按违规严重度缩放 DPO 信号；硬约束和软约束分层词典序优化；DCCG 生成约束，RT-MED 产生最小编辑偏好对。

## 关键实验结果

【论文原文】8B 模型在 TravelPlanner、NaturalPlan 与域外 PlanBench 达 89.2% pass rate、93.4% solve rate；以低 13 倍延迟匹配多 Agent 系统，并在未见 Blocksworld 上超过 GPT-4o 9.2 点。

## 证据质量与局限

【论文原文】有多规划基准、域外测试和效率比较。【分析推断】依赖符号化约束正确完备；若 verifier misspecified，连续 margin 只会更精确地优化错误目标，需审计 grader/contract。

## 最接近的相关工作

【分析推断】最接近 TV-Regulated OPD、DCSD、ContrAgent、GCAC 与 executable-contract audit；不同点是将连续违规幅度直接嵌入 preference objective。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】把五维 Agent rubric 中可程序化部分转换为 margin distribution：硬 fail 决定不可交易方向，LLM ordinal verifier 只在可行集合内评价目标推进、效率和恢复性。

## 对 Agent verifier × OPD 实验路线的具体影响

- 【分析推断】score-level OPD：以 verifier margin 替代统一 ±1 权重。
- 【分析推断】A/B/T：同为 B 的轨迹保留违规严重度序数分布；不可比较为 T。
- 【分析推断】真值门控：硬约束先词典序过滤，soft teacher 不得覆盖。
- 【分析推断】critique states：critique 必须指出具体约束与 margin 变化。
- 【分析推断】高熵分叉：在硬可行集合内保留多种软最优路径。
- 【分析推断】sealed eval：冻结独立契约与隐藏约束，审计 specification gap。