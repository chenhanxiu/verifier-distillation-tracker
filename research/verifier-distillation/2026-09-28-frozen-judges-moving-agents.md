# Frozen Judges, Moving Agents: Version-Dependent LLM-Judge Error and the Limits of Judge-Assisted Agent Evaluation

- **作者**：Jiapeng Li
- **首次公开日期**：2026-09-28
- **版本日期**：2026-09-28（v1）
- **原始论文**：https://arxiv.org/abs/2609.34198
- **代码**：未在 arXiv 页面提供

## 一句话结论

【论文原文】固定 Judge 对不同版本 Agent 的错误并不稳定，旧版本校准迁移到新版本会放大比较误差；上线判断应依赖当前输出的成对审计与执行参考，而非 Judge-only 差值。

## 真正新增的内容

【论文原文】论文系统检验 task-conditioned error invariance，并量化同一 Judge 对 agent upgrade 前后的差分错误；它还展示旧版本 calibration transport 在新版本上失效。

## 核心方法

1. 分析 SWE-bench、tau-bench 和 AgentRewardBench 的多版本 Agent 输出。\n2. 在 task 条件下检验 Judge 错误是否随 Agent 版本不变。\n3. 将 Judge-only 改进区间与执行 reward 区间比较。\n4. 评估旧版校准迁移和当前版本 paired audit。

## 关键实验结果

【论文原文】SWE-bench 8,743 个对齐 agent-task cell 中，32/60 个 judge×version-pair 单元存在可检测差分比较成分；8 个 Judge-only 区间宣称提升而执行区间无法确认。旧版校准迁移使平均绝对比较误差从 3.8 升至 19.5 个百分点。tau-bench 中一位 Judge 还反转了 9 点 reference-reward 差距。

## 证据质量与局限

【论文原文】覆盖 35 个 coding-agent submission、20 个预设版本对、250 个 SWE-bench 任务及 tau-bench/AgentRewardBench，证据丰富。局限是部分主分析因上游故障只剩三位 Judge；审计缩窄区间有限，且未给通用修正算法。

## 最接近的相关工作

最接近 Black-Box Judge 测量不稳定性、Harness or Model、AutoTuneBench 与 Who Judges Matters；新增维度是 Agent 版本本身会改变 Judge 错误结构。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】每次候选模型升级都重新抽取同任务 paired trajectories 做人工/执行审计；不要沿用旧模型上的 Judge confusion matrix。把 evaluator version 与 agent version 共同写入结果元数据。

## 对 Agent verifier × OPD 实验路线的具体影响

- **Score-level OPD**：teacher score 校准需随 student policy 版本更新。\n- **A/B/T 与序数分布**：发布差值时报告版本条件下的误差分布。\n- **真值门控**：执行 reference 优先于 Judge-only release decision。\n- **Critique states**：新版本常见行为需重新审计 critique 可靠性。\n- **探索**：不要把 Judge 对新行为的陌生惩罚误当退化。\n- **Sealed eval**：冻结 evaluator 只保证复现，不保证无版本偏差；需当前输出 paired audit。
