# Counting Moves, Weighing Voices: Bayesian Dialectical Argumentation for Calibrated Multi-LLM Councils under Persistent Adversaries

- **作者**：Ionel Eduard Stan, Paolo Napoletano
- **首次公开日期**：2026-10-01
- **版本日期**：2026-10-01（v1）
- **原始论文**：https://arxiv.org/abs/2610.02005
- **代码**：未发现公开代码链接

## 一句话结论

BDA 从“提出、挑战、让步”等带类型的讨论动作估计每个 Judge 的持续可靠性，输出校准后的答案后验，而非把多数强度误当正确概率。

## 真正新增的内容

【论文原文】现有 council confidence 往往衡量 decisiveness 而非 correctness，也无法识别持续不可靠成员。BDA 把讨论轨迹视为经典 annotator model 的观测，对每个 agent 建模可靠性；持续敌对 agent 可被反向利用而非仅被少数票淹没。

【分析推断】这为三 Judge 投票升级为概率聚合提供直接方案，但必须注意 Judge 错误相关性，不能默认每个成员条件独立。

## 核心方法

解析谁对哪个答案做 proposal/challenge/concession；用贝叶斯 annotator model 联合推断候选答案 posterior 与 per-agent reliability，再按可靠性加权证据。

## 关键实验结果

【论文原文】在二分类与多分类 benchmark 上，BDA 在无需额外 LLM 调用的 council aggregation 方法中校准最佳；面对持续敌对联盟更稳健，干净设置下仍具竞争力。摘要未提供绝对数值。

## 证据质量与局限

有多类任务和敌对 coalition 对照，但摘要未说明 Judge 家族相关性、长轨迹 Agent 或真实人工 gold 的覆盖；推断依赖 annotator model 假设。

## 最接近的相关工作

VStress、Agreement Overstates Evidence、Robust Conformal Consensus、JuryFlow、多 Judge 面板有效规模。

## 如何复用或推进 LLM-as-a-Verifier

把三模型输出从最终分数扩展为 typed verdict trace，并学习每个模型在不同 rubric 维度上的可靠性；最终保存 posterior 而非高置信多数票。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- **score-level OPD**：用校准 posterior 期望和方差控制蒸馏幅度。
- **A/B/T 与序数分布**：天然输出 A/B 后验；后验接近时设 T，序数任务可扩展为多类别。
- **硬真值门控**：per-agent reliability 必须由独立环境/人工 gold 更新。
- **student-generated critique states**：按 critique 类型和 Judge 可靠性聚合，不把让步当真值。
- **高熵分叉**：posterior 高熵时保留分支并追加互补 verifier。
- **sealed eval**：可靠性校准集、讨论 prompt 与最终 evaluator 分离。
