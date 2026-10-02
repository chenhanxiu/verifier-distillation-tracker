# When Harnesses Lose the Signal: Causal Evaluation of Recovery in LLM Agents

- **作者**：Shuyao Xiao, Shengling Wang, Xuan Chen, Ke Chao, Ming Cui, Feifei Qian, Chaoyang Mei, Fanlin Meng, Ziming Yu, Junxi Yin
- **首次公开日期**：2026-09-30
- **版本日期**：2026-09-30（v1）
- **原始论文**：https://arxiv.org/abs/2610.00372
- **代码**：未发现公开代码链接

## 一句话结论

同一种 harness recovery 可能救回失败轨迹，也可能破坏原本会成功的轨迹；CIR 通过同状态有/无干预对照，学习何时恢复值得执行。

## 真正新增的内容

【论文原文】平均成功率掩盖 rescue 与 harm。作者从同一 execution state 分叉，比较 recovery 与 no-recovery 的反事实结果，并训练只使用干预前信息的轻量 Causal Intervention Router。

【分析推断】这为“下一步动作贡献度”提供了更严格定义：不是 Judge 看起来合理，而是与不干预反事实相比对终局成功的因果增量。

## 核心方法

对同一状态执行有/无 recovery 两臂，分离救回和破坏；分析干预价值随时间变化，再以 pre-recovery features 训练选择性路由器。

## 关键实验结果

【论文原文】ALFWorld/Qwen3-14B 上，CIR 将成功率从 70.33% 提升到 73.33%；所有具有正确 observation 的评测轨迹都未被改动。控制实验表明收益不能只由环境返回的新 observation 解释。

## 证据质量与局限

有同状态反事实和针对干扰效应的控制，因果解释强于平均成功率；但仅一个环境/模型，增益为 3 点，摘要未报告置信区间及恢复成本。

## 最接近的相关工作

PivotOPD、REVERSAL-BENCH、HiSentinel、SkillAA、Completed Pairs Hide Capped Failures。

## 如何复用或推进 LLM-as-a-Verifier

为 recovery verifier 建立三类标签：rescue、neutral、harm；通过环境 checkpoint 独立执行双臂，而非让同一 Judge推断反事实。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- **score-level OPD**：使用 recovery 的因果增量而不是绝对成功作为 score。
- **A/B/T 与序数分布**：有/无干预是天然 A/B；差异不显著为 T。
- **硬真值门控**：双臂必须同状态重放并由环境结算。
- **student-generated critique states**：critique 只有造成 rescue 且不增加 harm 才可蒸馏。
- **高熵分叉**：将预算集中在干预价值不确定的状态。
- **sealed eval**：独立执行两臂并报告截断/超时，防止选择性完成偏差。
