# On-Policy Transition Distillation

- **作者**：Runyang You、Yongqi Li、Tiezheng Yu、Wenjie Li
- **首次公开日期**：2026-10-20
- **版本日期**：2026-10-20（v1）
- **原始论文**：https://arxiv.org/abs/2610.28048
- **arXiv ID**：2610.28048
- **DOI**：https://doi.org/10.48550/arXiv.2610.28048
- **代码/项目**：未公开

## 一句话结论

OPTD 不只匹配最终 logits，还蒸馏 teacher 与 student 层间预测变化，为多域 OPD 增加深度方向的机制监督。

## 真正新增的内容

诊断显示正确回答在多组中间层之间具有更低 transition KL，并将层到层 log-prob 增量用作额外监督。

## 核心方法

在 student-generated rollout 上保留标准终层分布匹配，同时对齐 teacher/student 的中间层预测转移，而非直接强制隐藏状态相同。

## 关键实验结果

三个 backbone、八个数学/代码/指令 benchmark 中，双域和三域蒸馏总体最佳或并列最佳；三域设置恢复约 90% teacher–student 能力差，普通 OPD 约 75%。

## 证据质量与局限

跨 backbone 与多域结果较完整；但 transition agreement 与正确性的诊断主要是相关性，中间层对齐在异构架构或跨 tokenizer teacher 上未必成立。

## 最接近的相关工作

与 OPMD、SCOPE-OPSD、Fisher-projected OPD 和 representation distillation 最接近。

## 如何复用或推进 LLM-as-a-Verifier

可把 verifier 的评分轨迹扩展为层间序数变化，测试“最终 score 相同但内部转移不同”的样本是否预测 OOD 失败；仍需环境真值定方向。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】优先作为同架构 teacher–student 的机制监督消融，不应取代 score-level A/B/T；sealed eval 要检查它是否只是增强同域表示相似。

## 结论边界

除明确标注“分析推断”的段落外，上述方法与实验结论来自论文原文或公开摘要；推断部分是面向现有研究路线的可检验假设，不应视为论文作者已经证明的结论。
