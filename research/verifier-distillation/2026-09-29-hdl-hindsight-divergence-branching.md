# Where the Model Changes Its Mind: Hindsight-Divergence Localization for Efficient Reinforcement Learning with Verifiable Rewards

- **作者**：Fanchao Chen, Hengyu Fu, Shivaram Venkataraman, Jiantao Jiao
- **首次公开日期**：2026-09-29
- **版本日期**：2026-09-29（v1）
- **原始论文**：https://arxiv.org/abs/2609.36864
- **代码**：未发现公开代码链接

## 一句话结论

HDL 用看到终局反馈后 token likelihood 的变化定位“模型改变主意”的位置，再从这些位置分叉，最多减少 2.5 倍生成 token 并让 Agent 任务提升最多 12.5 点。

## 真正新增的内容

【论文原文】不再独立采样整条轨迹，而用 hindsight-induced log-likelihood change 选择关键分叉点；每个分支复用 root prefix，只对新 suffix 更新策略。

【分析推断】它把“策略熵高”替换为“终局证据使模型后验显著移动”，更接近 verifier 应该投入分叉预算的状态价值。

## 核心方法

先生成少量完整 root trajectory；利用终局反馈重新评估前缀 token，按前后 likelihood divergence 选点；从选定位置采样替代 continuation，训练时只计 suffix。

## 关键实验结果

【论文原文】三个模型、数学/代码/Agent 三域均提升；相同 group size 和训练步数下，相对 GRPO 最多减少 2.5 倍生成 token、加速 rollout 1.8 倍，同时 Agent 任务最多提升 12.5 点。

## 证据质量与局限

【论文原文】有跨域与 matched-budget 比较，但摘要未说明分叉覆盖率、失败恢复性和 verifier 噪声敏感性。【分析推断】likelihood change 衡量“后见之明下的惊讶”，不自动等于因果责任或安全重要性。

## 最接近的相关工作

Belief-Shift Branching、EPIG-Tree、DDO、REVERSAL-BENCH、BATON。

## 如何复用或推进 LLM-as-a-Verifier

把 HDL 分叉点送入分布式 verifier，只在这些局部比较 continuation 的序数 outcome、可恢复性与证据质量，降低整轨迹 Judge 成本。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- **score-level OPD**：在高 hindsight divergence 位置提高 verifier 查询和局部 OPD 权重。
- **A/B/T 与序数分布**：共享 prefix 的分支天然形成 A/B/T，T 可覆盖统计不可分或均可成功的分支。
- **硬真值门控**：分支排序应由环境重放结果定方向，likelihood 只分配预算。
- **critique states**：在被定位点生成 critique，并检验它能否改变后续分支 outcome。
- **高熵探索**：比全程强蒸馏更能保留探索，但应联合策略熵与 recoverability 防漏。
- **sealed eval**：分叉选择器可训练，最终性能需在未见任务和冻结 verifier 上评估。
