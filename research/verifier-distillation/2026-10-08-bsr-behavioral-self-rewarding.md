# Beyond Binary Verifiable Rewards: Behavioral Self-Rewarding for SWE Agents

- **作者**：Yiran Wu；Andrew Zhao；Yurui Chang；Qingyun Wu；Xuan Feng
- **首次公开日期**：2026-10-08
- **版本日期**：2026-10-08（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2610.12598
- **Canonical URL**：https://arxiv.org/abs/2610.12598
- **DOI**：10.48550/arXiv.2610.12598
- **代码**：https://github.com/yiranwu0/behavioral-self-rewarding（作者项目页所列；检查时仓库为空）

## 一句话结论

BSR 在可执行测试的 pass/fail 顺序不变这一硬约束下，用当前策略对同任务、同 verdict 的调试轨迹做成对行为比较并生成有界软奖励，是“环境真值定方向、student verifier 定幅度”的直接实现。

## 真正新增的内容

【论文原文】二元测试奖励无法区分“有实质进展但未通过”和“无效重复”的失败轨迹；BSR 仅在相同任务、相同 verifier 结果内部比较可观察调试行为，经加权 Bradley–Terry 聚合、deadzone 去噪和幅度约束后形成辅助奖励。  
【分析推断】它给现有 A/B/T 方案提供了安全组合方式：A/B 来自组内相对行为质量，硬测试结果保持跨组偏序，无法稳定排序时保留 T。

## 核心方法

1. 同一 issue 采样多条轨迹并执行测试，按 pass/fail 分桶。
2. 当前 policy 作为 Judge，依据动作轨迹、任务、参考补丁和 rubric 做随机顺序的成对比较。
3. 用 Bradley–Terry 得到任务内相对分数，经 deadzone、中心化和有界映射生成行为奖励。
4. 主设置只细分失败桶，并保证任一成功轨迹的总奖励高于任一失败轨迹。

## 关键实验结果

【论文原文】Qwen3-14B、400 步时，SWE-bench Verified 平均准确率由 32.1% 升至 34.7%，SWE-bench-Live Lite Pass@3 由 11.33% 升至 13.67%；各模型规模和训练预算均报告正增益。随机辅助奖励不能复现收益。  
【局限】自我 Judge 与外部 Kimi K2.5 的 macro-F1 约 0.6–0.7，且训练后期有所下降；训练墙钟时间增加 19.86%，尚缺严格等算力比较。

## 证据质量与局限

多模型、两个 SWE 基准、三次运行，并有随机奖励和 reward mapping 消融，证据中等偏强。但 Judge 看到了参考补丁，信号属于 privileged teacher；结果主要限于 coding agent，且同一策略兼任生成器与评判器仍有共适应风险。

## 最接近的相关工作

最接近 Ground-truth-as-code、FLARE、PROSE、GLARE、CM-DPO 与 RewardWeaver。相较这些工作，BSR 的核心差异是先冻结硬 verifier 的跨组顺序，只在硬标签无法区分的组内引入自评价。

## 如何复用或推进 LLM-as-a-Verifier

可将五维 Judge 用于同一终局标签内的轨迹排序：硬门槛维度决定 pass/fail，目标推进、效率和证据质量只做有界残差；同时保留原始 pairwise 概率、顺序反转率和 T 比例用于校准。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：把行为残差作为 teacher score，但总幅度不得跨越硬真值边界。
- **A/B/T 与序数分布**：同任务同 verdict 内做 A/B/T；deadzone 对应 T，Bradley–Terry 后验可转序数分布。
- **程序化/环境真值门控**：测试结果决定符号与上界，软 Judge 只分配组内信用。
- **student-generated critique states**：只接受能指向可观察动作证据、且不改变硬 verdict 的 critique。
- **高熵分叉**：失败桶中保留高质量探索轨迹，不把所有失败统一压低。
- **sealed eval**：用冻结测试、外部 Judge 和未见仓库复核，避免 student 同时优化并定义奖励。