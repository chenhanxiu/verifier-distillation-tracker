# Wrong the Same Way: Cross-Prompt Sharing Both Suppresses and Amplifies Reward Hacking in RLVR

- **作者**：Michael Li、Rohan Pandey、Ray Chen
- **首次公开日期**：2026-11-11
- **版本日期**：2026-11-11（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.13218
- **代码**：未发现公开代码链接
- **标识符**：arXiv:2611.13218

## 一句话结论

【论文原文】reward hacking 是否被 RLVR 放大，不只取决于 verifier 假阳性率，而取决于同一错误能否跨 prompt 复用以及模型参数更新如何在 prompt 间共享；修补相同数量错误，真实准确率影响可相差 38 点。

## 真正新增的内容

【论文原文】论文在可精确枚举完整 response distribution 的受控环境中统一“hacking 由 base model 继承”和“hacking 被 RL 放大”两种观察。它引入 leak universality——同一错误答案被多少 prompt 错误接受——并把偏离 KL 正则化最优过滤器的部分写成 reward 与经验 tangent kernel 的跨 prompt 协方差。

## 核心方法

- 改变 verifier 的静态 false-positive rate。
- 独立改变错误捷径在不同 prompt 间的通用性。
- 精确计算响应分布与 KL-regularized optimum。
- 以“只重加权 accepted set、不改变其组成”的过滤器作为 null model。
- 分析共享参数造成的跨 prompt 梯度传播何时抑制或放大相同错误。

## 关键实验结果

【论文原文】在 KL 正则化最优点，RLVR 精确继承 accepted set 内的 hack rate；实际训练偏离由跨 prompt kernel-weighted sharing 决定。两个删除同样多 verifier 错误的 patch，因所修错误的跨 prompt 复用性不同，真实准确率最多相差 **38 个百分点**。

## 证据质量与局限

【论文原文】完整分布可计算使机制识别清晰，比只观察大模型终点更可解释；但环境刻意小型化，经验 tangent kernel 与真实长轨迹 Agent 的工具状态、非平稳 verifier 及多轮信用未必一致。38 点差异是受控环境结果，不应直接外推到生产系统。

## 最接近的相关工作

最接近 Goodhart in the Planner、Monitor-Based Reward-Hacking Interventions、ImpossibleRubrics 与 Coding or Cheating。本文特别指出 verifier 修复的价值取决于错误的跨 prompt 共享结构，而非错误数量。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】训练 verifier student 时应给 false-positive 建立“跨任务复用度”权重：会在许多任务上被同一模式触发的错误优先进入 hard-negative 与 sealed audit。A/B/T 面板还需按错误相关性校正，不能把重复同错当成独立证据。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：teacher error 的权重由跨 prompt 普适性和梯度影响共同决定。
- **A/B/T 与序数分布**：保留跨任务相关错误的共同 latent factor，避免虚假置信。
- **程序化/环境真值**：优先修补能跨任务复用的 oracle 漏洞，而非只按频次修补。
- **student-generated critique states**：检测同一错误 critique 是否在不同状态重复传播。
- **高熵分叉**：探索保留不等于保留通用 exploit；对高复用捷径单独硬门控。
- **sealed eval**：使用新 prompt 家族与未见漏洞，报告 hack transfer 而非只报告训练分布假阳性率。