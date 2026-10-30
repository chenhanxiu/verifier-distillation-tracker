# TESD：让 Self-Teacher 在蒸馏过程中持续进化

## 基本信息

- **论文标题**：On-Policy Self-Distillation with Teacher Evolution
- **作者**：Shufan Shen, Zhongni Hou, Chao Bi, Yufei Zhang, Guojun Yin, Shuhui Wang
- **首次公开日期**：2026-10-28
- **版本日期**：2026-10-28（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2610.38637
- **DOI**：https://doi.org/10.48550/arXiv.2610.38637
- **代码**：未见作者公开代码链接

## 一句话结论

TESD 不把 privileged self-teacher 当成静态真值：它让 teacher 自己 rollout、接受任务正确性与 context-independence 环境反馈，再一边提升 teacher、一边按可靠性降权 student 更新。

## 真正新增的内容

**论文原文结论**：

1. 将 OPSD 后期停滞归因于 self-teacher 在部分样本上的指导不可靠。
2. teacher 在带特权上下文的条件下生成 rollout，并接收任务正确性与“脱离上下文仍成立”的环境反馈。
3. 用这些 reward 做 teacher-oriented optimization，持续增强 self-teaching；同时估计指导可靠性，对 student-oriented optimization 做样本级自适应降权。
4. 多数据集与模型规模上持续优于代表性的 token-level 和 sequence-level 方法。

**分析推断**：

- 这是“teacher 信号也要 on-policy 验真”的直接方案，适合把程序/环境反馈嵌入 verifier 蒸馏。
- teacher 与 student 同步更新会提高共适应风险；必须保留冻结 anchor teacher 与 sealed evaluator 才能判断是真进步还是闭环漂移。

## 核心方法

1. 从当前模型构造带 privileged context 的 self-teacher。
2. teacher 自行生成 rollout，环境返回 correctness 与 context-independence reward。
3. 优化 teacher 的监督能力。
4. 由上述 reward 估计样本级 guidance reliability，可靠样本强蒸馏、不可靠样本降权。
5. student 继续在自身生成分布上训练。

## 关键实验结果

**论文报告**：TESD 在多个数据集、模型规模上稳定优于代表性 token-level 与 sequence-level self-distillation 方法，支持“提高监督质量”而非仅增加监督量。公开摘要未给出具体绝对分数或成本，需以正文表格为准。

## 证据质量与局限

- **优点**：teacher 更新与 student 可靠性门控共享可验证环境反馈，问题—方法闭环清晰。
- **局限**：摘要没有说明 context-independence reward 的覆盖率、误报率与跨域稳定性。
- teacher/student 同源且共同演化，可能学会利用 reward specification。
- 尚无长时程 Agent、工具副作用或独立 evaluator 家族的直接证据。

## 最接近的相关工作

- **RISE / RetireOPD**：动态 teacher 与 teacher 退出机制。
- **Coupled Calibration and Learning**：用有真值源域持续校准目标域 teacher。
- **Proof-Carrying Cognition / GLARE**：用 on-policy 现实结算或当前策略负样本更新 reward estimator。

## 如何复用或推进 LLM-as-a-Verifier

让 verifier teacher 在当前 student 轨迹上生成“判断 + 证据 + 可执行检查”；环境分别给 correctness、evidence sufficiency、context independence 三个 reward。只把三者都可靠的样本蒸馏给 student；其余样本保留为 T/abstain 或送到更强 verifier。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：以环境 reward 校准 teacher score，并按 guidance reliability 调整蒸馏权重。
- **pairwise A/B/T 与序数分布**：teacher 可靠性不足时输出 T，不把噪声 pair 强制二分；序数分布保留环境与 soft teacher 的分歧。
- **程序化/环境真值门控**：把 correctness 和 context independence 设为两个独立硬门。
- **student-generated critique states**：让 teacher 对 student critique 做环境重放；只有能独立复现的 critique 才进入训练。
- **高熵分叉与探索**：低可靠性状态降低 teacher 权重并扩大采样，而不是压低策略熵。
- **sealed eval**：冻结评测环境、reward spec 和 evaluator；另设不参与 teacher evolution 的 anchor 监控共适应。