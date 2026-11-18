# Streaming On-Policy Distillation: Decoupling Three Clocks for Stage-Wise Supervision Consumption

- **作者**：Yun Zhu Da Wang
- **首次公开日期**：2026-11-17
- **版本日期**：2026-11-17（v1）
- **原始论文**：https://arxiv.org/abs/2611.22298
- **代码链接**：未发现公开代码
- **标识符**：arXiv:2611.22298；DOI: 10.48550/arXiv.2611.22298

## 一句话结论

【论文原文】OPD 不必把响应完成、监督到达与参数更新锁在同一节拍；分段消费新生成监督可降低供给等待，但在相同更新数下尚未证明端到端加速。

## 真正新增的内容

【论文原文】提出 streaming OPD，将三个“时钟”解耦：生成可继续时交付新片段、每次保留完整因果前缀、只在新增位置计损失；并用 consumption protocol 显式管理预算、位置覆盖、陈旧度与更新调度。论文把“质量恢复”和“供给侧吞吐”分开报告，避免把异步系统收益误当算法收益。

## 核心方法

1. 同一 response 以多个 stage 交付，监督片段附带完整 prefix，避免截断上下文改变 teacher 条件分布。
2. 只对本次新增 token 计算蒸馏损失，防止重复消费早期位置。
3. 通过预算匹配、freshness filter、disagreement-overlap 选点及版本滞后控制，使同步、预算匹配和流式方案可比较。

## 关键实验结果

【论文原文】在 GSM8K、Qwen3-4B→Qwen3-0.6B、VERL 设置中，监督预算匹配把七个共同候选的早期最佳测试差距从 4.55 缩至 2.42 点。同步 continuation 达 73.39%，同步基线 74.30%，预算匹配 71.95%；一条不可配对的延长记录达 76.12%。freshness 与 disagreement-overlap 改善局部峰值，但未建立持续优势。系统原型降低供给等待，未证明 equal-update speedup。

## 证据质量与局限

【论文原文】论文主动区分算法质量与系统等待，且报告负结果，证据口径较谨慎；但仅覆盖单一数学任务和 teacher/student 组合，延长记录不可与主实验配对，尚无长时程工具 Agent、verifier score 或多轮环境真值实验。

## 最接近的相关工作

最接近异步/在线 OPD、阶段式 rollout 消费、staleness-aware distributed RL，以及 token-level OPD gating。与只改变 KL 方向或 teacher 路由的方法不同，本工作主要改变监督何时、以何种粒度被消费。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】可把每个 Agent 决策段的 verifier 结果作为独立 supervision stage：先消费已结算的局部约束与 critique，终局环境结果到达后再补充 outcome/ordinal 分布；完整 trace prefix 始终保留，只对新结算区间更新。这样能把 verifier latency 与 rollout latency 解耦，同时记录 teacher/version lag。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level on-policy verifier distillation**：增加“同步整轨迹 / 预算匹配 / streaming”三臂，并按等监督 token、等更新数、等墙钟时间分别比较。
- **pairwise A/B/T 与序数评分分布**：同一分叉的 A/B/T 可延迟到证据齐备后消费；不得把未结算片段重复计权。
- **程序化/环境真值门控**：局部硬约束先到先用，终局成功只在环境结算后补写，不让软 teacher 提前覆盖硬真值。
- **student-generated critique states**：critique 可作为新的 stage，但需绑定其生成时的完整 causal prefix 与 verifier 版本。
- **高熵分叉下保留探索**：优先流式消费 disagreement-overlap 区域，但论文只支持局部峰值，不能据此宣称稳定收益。
- **独立 sealed eval**：冻结独立 evaluator 与更新预算；同时报告 equal-update、equal-supervision 和 wall-clock 三套结果，防止系统吞吐掩盖共适应。
