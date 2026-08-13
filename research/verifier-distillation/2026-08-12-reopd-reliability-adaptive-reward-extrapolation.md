# REOPD：可靠性自适应的 On-Policy Distillation 奖励外推

## 基本信息

- **标题**：REOPD: Reliability-Adaptive Reward Extrapolation for On-Policy Distillation
- **作者**：Yang Sun, Lichao Ma, Houyuan Qin, Yuxin Liu, Hanyang Lu, Yao Zhu, Pinlong Cai, Guohang Yan
- **首次公开/版本日期**：2026-08-12（v1）
- **arXiv**：https://arxiv.org/abs/2608.11698
- **代码**：截至记录时未发现公开仓库

## 一句话结论

REOPD 只对 ExOPD 中“超越 teacher”的残差做 token 与 batch 两级自适应控制，降低固定全局外推系数导致的尖峰拟合和 reward hacking，但其“可靠性”仅是白盒分布兼容性而非结果正确性。

## 真正新增的内容

**论文结论：** 用 (lambda_{b,t}=1+gamma_bq_t) 替代 ExOPD 的固定 (lambda)：(q_t) 根据 student–teacher discrepancy 抑制不兼容 token，(gamma_b) 根据 micro-batch 残差比例与尺度分配有界预算，同时保留标准 teacher-alignment 项。

**分析推断：** 它适合作为 score-level verifier OPD 的优化稳定器，但不能替代环境真值或序数 verifier，因为作者明确指出低 discrepancy 不保证 teacher 正确。

## 核心方法

- 从已有 student、teacher、reference log-probability 构造兼容权重，无需额外 rollout/verifier。
- token 级权重对大 student–teacher discrepancy 的“超越 teacher”残差降权。
- batch controller 用同步统计、EMA 与上界调节外推预算。
- alignment 项始终保留，只控制额外 reward residual。

## 关键实验结果

**论文报告：** 单 teacher 数学 pooled accuracy 为 47.66%，高于 OPD 46.28% 和 ExOPD 47.47%；代码为 63.45%，高于 OPD 62.55% 和固定 (lambda=1.25) 的 ExOPD 61.72%，但仅与 G-OPD 相当。多 teacher 数学/代码均优于 G-OPD。实验涵盖 AIME/HMMT、HumanEval+、MBPP+、LiveCodeBench。

## 证据质量与局限

- 有数学、代码及多 teacher 设置和消融，支持自适应 residual control。
- 增益整体较小，单 teacher 代码未超过 G-OPD。
- “可靠性”不是 outcome reliability；无需 verifier 是成本优点，也是语义正确性盲区。
- 尚无 Agent、多步环境或 sealed evaluator 实验；代码未公开。

## 最接近的相关工作

G-OPD/ExOPD、Prune-OPD、TIP、SCOPE、reward-gated OPD。区别是只调节 beyond-teacher residual，不改基础对齐信号。

## 如何复用或推进 LLM-as-a-Verifier

将 (q_t) 换成或融合 teacher/student 序数评分分布的一致性；(gamma_b) 再由环境真值通过率校准。对于 student-generated critique，可分别计算 critique-conditioned 与 plain teacher 的残差可靠性。

## 对 Agent verifier × OPD 路线的影响

- **Score-level OPD**：作为有界、分层外推控制器，避免少量极端 teacher score 主导更新。
- **A/B/T**：pairwise/tie 分布只用于控制残差强度，不应因分布接近就默认正确。
- **真值门控**：环境结果应位于兼容权重之上，二者冲突时以真值为准。
- **高熵探索**：有界 residual 可防止单一 teacher 峰值过度压缩策略分布。
- **Sealed eval**：必须用独立 evaluator 检查“训练 reward 上升、真实任务下降”的外推 hacking。
