# Overcoming Scaling Limits in On-Policy Self-Distillation for LLM Reasoning

- **作者**：Md. Ismail Hossain, Humaira Kousar, Isidora Chara Tourni
- **首次公开日期**：2026-09-29
- **版本日期**：2026-09-29（v1）
- **原始论文**：https://arxiv.org/abs/2609.37915
- **代码**：未发现公开代码链接

## 一句话结论

OASIS 发现“student scaffold 是否被真值验证”比 privileged context 是否正确更关键，并仅用最终答案标签维持大模型上的 OPSD 收益。

## 真正新增的内容

【论文原文】作者将 scaffold correctness 与 teacher context correctness 做因子分解，发现前者对下游准确率影响更大；未验证 scaffold 会产生 teacher 使用 student 不可得信息的 imitation gap。OASIS 主要在标签验证通过的 on-policy 轨迹上蒸馏，同时允许 teacher 上下文只是未验证的模型尝试。

【分析推断】这为“硬真值决定哪些 student states 可接受，软 teacher 只在其上给稠密位移”提供了清晰证据。

## 核心方法

保留 OPSD 目标，但用最终答案标签筛选 on-policy scaffold；teacher 的 privileged context 不再依赖人工书写解答，可使用模型生成的尝试。

## 关键实验结果

【论文原文】Qwen3 1.7B、4B、8B 在 AIME 2024/2025 与 HMMT 2025 上相对 base 平均提升 3.2–3.8 点；标准 OPSD 增益从 1.7B 的 3.05 点降到 8B 的 0.14 点，而 8B OASIS 比 OPSD 高 3.05 点。

## 证据质量与局限

【论文原文】有尺寸因子分析和三个数学基准，但“最终答案正确”不保证中间过程有效，尚未在长时程工具 Agent 上验证。【分析推断】若把终局标签直接推广到 trajectory，仍可能奖励投机或错误但碰巧成功的路径。

## 最接近的相关工作

OPSD、SIGNBALANCE、PROSE、Ground-truth-as-code Agent Evaluation、ContrAgent。

## 如何复用或推进 LLM-as-a-Verifier

将“verified scaffold”从最终答案扩展为可执行轨迹前缀：满足状态断言、权限和不可逆操作约束后，才允许 generative verifier 产生 critique 与稠密分数。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- **score-level OPD**：先二元硬门控 state，再在通过样本上应用 score-level 权重。
- **A/B/T 与序数分布**：硬真值冲突时直接负类；真值不足时标 T，而非让 teacher 强行排序。
- **硬真值门控**：是该论文最直接的迁移点，优先验证 scaffold 而非美化 teacher context。
- **critique states**：只蒸馏来自已验证前缀的 critique，并记录验证证书。
- **高熵探索**：保留所有真值通过的多样路径，不把“正确”压成唯一示范。
- **sealed eval**：筛选标签与最终 evaluator 分离，防止按同一答案规则过拟合。
