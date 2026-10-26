# DATC：用 Reward-Model 梯度分配逐 Token 信用

- **论文标题**：Direction-Aware Token Credit Assignment with Reward-Model Gradients
- **作者**：Yikuan Hu、Jifeng Zhu、Minle Su、Jiaqin Yue、Gujie Shao、Yanzhe Chen、Haoxuan Jia、Haoran Xu、Wangzhou Dai
- **首次公开日期**：2026-10-23
- **版本日期**：2026-10-23（v1）
- **原始论文**：https://arxiv.org/abs/2610.32772
- **DOI / canonical URL**：https://doi.org/10.48550/arXiv.2610.32772
- **项目页**：https://datc-project.github.io/
- **代码**：未发现公开代码链接

## 一句话结论

DATC 将冻结 reward model 的局部增益方向与 GRPO 实际更新方向做内积，只重分配强度而保持响应级 advantage 的符号与均值，为“终局真值定方向、软 verifier 定 token 幅度”提供了最直接的数学原型。

## 真正新增的内容

**论文原文结论**：DATC 通过 straight-through surrogate 把冻结 RM 的输入梯度映射到 actor logit 空间，计算每个位置的 reward-improvement direction 与 sampled-action update direction 的对齐度，并用 KL 正则化的 softmax 分配 token 权重。

**分析推断**：相较于按熵、注意力或 prefix score 分配信用，DATC 明确问“这一次实际 GRPO 更新是否沿着 reward 上升方向”，因此更适合接入 score-level verifier。

## 核心方法

1. 在真实 sampled response 上保持前向不变，以 straight-through 路径反传冻结 RM。
2. 得到每个位置的 RM logit-space 梯度与 sampled token score direction。
3. 用二者内积估计局部 reward 增益，再乘响应级 advantage 决定强化/抑制强度。
4. 解带 KL 正则的 token 份额优化，保持权重为正且均值为 1。
5. 将 token-level advantage 缓存后代入标准 clipped GRPO 目标。

## 关键实验结果

**论文原文结论**：在 Qwen3-14B 与 Llama-3.1-8B、Base 与 Instruct 共四个设置中，DATC 在四项评测的均值均优于 GRPO；消融支持方向信息和 token—位置对应关系的重要性。训练只额外需要一次 RM 输入反向传播。

## 证据质量与局限

包含推导、四个设置、组件消融和人工评测，证据较强；但实验是一般偏好优化而非长时程 Agent。actor 与 RM 需要 tokenizer/ID 对齐；一阶 surrogate 与冻结 RM 可能继承 reward hacking；额外反向传播增加成本，且离线指标提升不等于 sealed 环境成功。

## 最接近的相关工作

接近 P2T、RED、DelTA、VCORE、MRTPO、UECR-GRPO 与 γOPD。DATC 的区别是显式比较 reward 梯度方向和当前策略更新方向，而非只估计 token 重要性。

## 如何复用或推进 LLM-as-a-Verifier

把多维 verifier 的每个 score head 分别反传，得到目标推进、安全、可恢复性等维度的 token 信用；硬环境 verdict 控制更新符号，软 Judge 梯度只分配幅度。不同 head 方向冲突时保留分布而不是提前压成单分。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

- **score-level OPD**：比较 uniform advantage、entropy weighting 与 DATC-style gradient weighting。
- **A/B/T/序数**：若多个 verifier head 的方向冲突或后验重叠，标 T 并降低权重。
- **真值门控**：执行真值决定正负；RM 梯度不可翻转硬 verdict。
- **critique states**：用 critique-conditioned verifier 梯度定位应修正 token，再由重放验收。
- **高熵探索**：限制最大 token 权重，避免单一 RM 梯度压垮高熵分叉。
- **sealed eval**：冻结未参与梯度生成的执行 evaluator，检查 reward 上升是否对应真实任务成功。
