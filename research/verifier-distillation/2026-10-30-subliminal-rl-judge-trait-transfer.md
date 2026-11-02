# Subliminal Reinforcement Learning：Judge 特质可经分数通道迁移

- **论文标题**：Subliminal Reinforcement Learning: traits travel through a judge's scores
- **作者**：Keuntae Kim, Yong Suk Choi
- **首次公开日期**：2026-10-30
- **版本日期**：2026-10-30（v1）
- **原始论文**：https://arxiv.org/abs/2610.41301
- **DOI**：https://doi.org/10.48550/arXiv.2610.41301
- **代码与数据**：https://github.com/kkt94/subliminal-rl

## 一句话结论

即使 student 只生成无语义音节或数字、只接收 Judge 分数，Judge 的隐含偏好仍可能经 GRPO 奖励差异迁移到 student 的正常回答中。

## 真正新增的内容

**论文原文结论**：subliminal learning 不只发生于 teacher 文本蒸馏；单个 LM Judge 的标量分数也足以承载特质，且移除不同 Judge 之间的 reward difference 会消除迁移。

**分析推断**：这直接挑战“score-level verifier distillation 比生成式 critique 更安全”的朴素假设。即便不蒸馏文字理由，teacher 的家族偏好、人格或安全倾向也可能编码在相对分数几何中。

## 核心方法

student 生成编造音节或数字；带特定动物偏好的 Judge 对输出评分；以 GRPO 更新 student。论文将迁移链拆成四阶段：特质进入 Judge 分数、分数偏好某些可推动 student 的字符串、训练累积该偏置、最后在正常答案中显现。作者也把相同流程迁移到 AI-safety dispositions。

## 关键实验结果

**论文原文报告**：

- 48 个设计单元中 2 个未通过有效性门槛，17 个在 5% FDR 下建立显著特质迁移；其中包括纯数字单元。
- 移除 Judge 之间的 reward difference 后，迁移消失。
- 使用由其他数据或另一模型构造、但具有同类偏好的 Judge 时，偏好落在不同字符串上，未检测到迁移。
- 对不良安全倾向，四阶段链仍成立，训练前阶段测量可预示部分风险。

## 证据质量与局限

优点是多设计单元、FDR 控制、机制分解和消融，并公开代码数据。局限是实验偏合成，效应依赖 Judge、字符串支持集和训练动力学；“未检测到”不等于不存在。安全 disposition 的外部效度与更大规模 Agent 训练仍需验证。

## 最接近的相关工作

最接近的是 subliminal learning、reward hacking、Judge family bias、Who Judges Matters、Agreement Overstates Evidence，以及 reward model / verifier distillation 中的 teacher-bias transfer。论文的新意是确认纯 score channel 也能迁移隐含特质。

## 如何复用或推进 LLM-as-a-Verifier

- 在蒸馏前做“无语义探针”：固定随机/数字/格式化动作，检查不同 Judge 的分数差是否预测下游行为偏移。
- 多 Judge 不应只求平均；需要正交化家族偏差，并保留分歧分布。
- pairwise A/B/T 中，若偏好无法被程序真值或环境证据解释，标为 T 并降低权重。
- 对 student-generated critique states 记录 teacher score、Judge ID、模型家族和扰动不变性，便于追踪隐式迁移。

## 对现有 Agent verifier × OPD 实验路线的具体影响

**分析推断**：score-level OPD 必须新增“trait leakage audit”。训练前后在 sealed prompt 集上测量非任务特质；比较单 Judge、多家族 Judge、真值门控、score residualization 与仅符号方向监督。程序化/环境真值应决定更新方向，teacher score 只在可解释残差范围内决定幅度。sealed eval 必须使用未参与训练、不同家族的 evaluator，并单独报告任务成功与非任务特质漂移，防止 evaluator 共适应掩盖泄漏。