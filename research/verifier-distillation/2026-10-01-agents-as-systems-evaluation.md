# Agents Are Systems, Not Models: Rethinking Agentic Evaluation

- **作者**：Luis Wiedmann, Leander Girrbach, Cordelia Schmid, Zeynep Akata
- **首次公开日期**：2026-10-01
- **版本日期**：2026-10-01（v1）
- **原始论文**：https://arxiv.org/abs/2610.01618
- **代码/数据**：论文称发布 benchmark 与 18,000+ 条轨迹，摘要页未给出链接

## 一句话结论

Agent 结果约 54% 的方差来自同一配置重复运行，而非配置差异；评测对象应是模型、信息、预算、自验证与 harness 的完整系统。

## 真正新增的内容

【论文原文】作者在四项科学任务上系统改变 task information、reasoning、self-verification、time budget 和 backbone。提供给 Agent 的信息影响最大，超过时间和模型尺寸；提示“自验证”作用很小，而专用 verification tool 明显改变行为。

【分析推断】这直接支持把“模型能力榜”和“系统能力榜”拆开，并要求 verifier 蒸馏实验报告 scaffold/configuration，而非只标模型名。

## 核心方法

在同一科学 benchmark 上做五类系统配置消融与重复运行；用 trajectory taxonomy 分析不同配置如何改变验证行为、成本、稳定性和成功率。

## 关键实验结果

【论文原文】约 54% outcome variance 来自相同配置的重复；信息供给是最大影响因素，同时降低成本并改善校准。更多时间只有在信息充分或模型能力足够时才有帮助。数据含 18,000+ Agent trajectories。

## 证据质量与局限

大规模轨迹与系统级因子设计很有价值，但只覆盖四个科学任务；配置因素仍可能交互，摘要未给完整方差分解置信区间。

## 最接近的相关工作

Harness or Model?、How Do Agent Harnesses Create Value?、AutoTuneBench、Black-Box Judge 测量不稳定性。

## 如何复用或推进 LLM-as-a-Verifier

对每条 verifier 结论记录完整运行配置和重复 seed；把验证行为作为可观察过程指标，并区分“提示要求验证”与“系统提供验证工具”。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- **score-level OPD**：score 必须条件化 harness、预算和信息配置，避免跨配置混训。
- **A/B/T 与序数分布**：配置间差异小于重复波动时判 T。
- **硬真值门控**：专用 verification tool 优先于 prompt 自我检查。
- **student-generated critique states**：记录 critique 是 prompt 诱导还是工具证据产生。
- **高熵分叉**：同时报告 pass@k 与稳定成功率，不能只展示最佳分支。
- **sealed eval**：模型榜固定系统配置；系统榜允许最优配置，但分别冻结协议。
