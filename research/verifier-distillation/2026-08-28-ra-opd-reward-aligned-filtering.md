# When Teacher Guidance Misleads: Reward-Aligned On-Policy Distillation

## 基本信息

- **作者**：Siyuan Gan, Yuhan Li, Xiran Wang, Linjian Meng, Boyan Wang, Zhen Zhao, Jing Huo, Yang Gao
- **首次公开日期**：2026-08-28
- **版本日期**：2026-08-28（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2608.27960
- **DOI**：https://doi.org/10.48550/arXiv.2608.27960
- **代码**：论文当前未提供公开代码链接

## 一句话结论

RA-OPD 用可验证终局奖励检查“整条轨迹的 OPD 更新方向”是否正确，只保留方向一致的 teacher 信号；它是程序化真值门控 score-level OPD 的一个极简、低额外开销实现。

## 真正新增的内容

**论文原文结论**：现有 token 级可靠性修正仍可能在轨迹层面奖励错误答案或压低正确但不同于 teacher 主模态的答案。RA-OPD 将 token 级 teacher–student log-ratio 聚合成轨迹级 distillation return，再与二值 outcome reward 做绝对方向一致性判断；不同于 Uni-OPD，它不要求同一 prompt 有多个 rollout 或同时出现正负奖励。

**分析推断**：关键增量不是引入新 verifier，而是明确把“teacher 给多大力”与“环境真值允许朝哪个方向更新”分开。这一分工可直接移植到 Agent：环境/程序检查器决定准入方向，teacher 的密集分布只在通过门控后负责信用分配。

## 核心方法

对 student rollout `τ` 的每个 token 计算标准 OPD 信号：

`r_t = log π_T(o_t|s_t) - log π_θ(o_t|s_t)`

并取长度归一化轨迹回报：

`G_OPD = (1/|τ|) Σ_t r_t`

由 outcome verifier 给出 `R∈{0,1}`，使用掩码：

`m = 1[(2R-1)G_OPD ≥ 0]`

因此只保留两类轨迹：

- 正确轨迹且 teacher 相对 student 更认可该轨迹（`G_OPD≥0`）；
- 错误轨迹且 teacher 相对 student 更不认可该轨迹（`G_OPD≤0`）。

掩码作用于整条轨迹，但保留轨迹内部仍使用原始 token 级 OPD 信号。方法复用既有 rollout 和 teacher 概率，不新增 rollout 或 teacher 调用。

## 关键实验结果

**论文报告**：

- Qwen3-4B：七个数学基准的 avg@k 从标准 OPD 的 **40.68** 提升到 **45.88**；pass@k 从 **55.66** 提升到 **61.11**。
- Qwen3-8B：avg@k 从 **44.34** 提升到 **49.43**；pass@k 从 **57.66** 提升到 **61.56**。
- DeepSeek-R1-Distill-Qwen-7B：数学 avg@k 从 OPD 的 **64.43** 提升到 **69.34**。
- 论文还在三个代码基准上报告相对标准 OPD 和其他测试变体的持续增益。

## 证据质量与局限

- **证据质量：中高**。覆盖 Qwen3 与 DeepSeek-R1 系列、数学与代码任务，并比较 OPD、ExOPD、Uni-OPD，含 avg@k/pass@k 与消融。
- 结果依赖可得到可靠二值终局真值的任务；尚未验证 noisy/ordinal verifier。
- 掩码在轨迹层面是硬二值的，不能定位“正确轨迹中的局部坏步骤”或“错误轨迹中的可复用恢复步骤”。
- 主要实验不是长时程工具 Agent；对长轨迹的 credit assignment、状态分布漂移和 verifier 延迟仍待验证。
- 未看到独立 sealed evaluator 对训练后模型进行共适应审计。

## 最接近的相关工作

- OPDVR / Reward-Gated OPD：同样用可验证奖励约束 teacher 信号方向。
- Uni-OPD：比较同 prompt 多条轨迹的 distillation return 与 outcome ordering。
- GC-OPD：用 verifier–teacher 残差校准 token 级 OPD。
- REOPD、SuRe、Prune-OPD：从 token 可靠性、梯度集中或局部截断角度修正 teacher 信号。

RA-OPD 的区别是以每条轨迹独立的“绝对符号一致性”作准入，不依赖组内奖励多样性。

## 如何复用或推进 LLM-as-a-Verifier

1. 对同一 Agent 状态生成若干下一步动作或短后缀，先由环境检查器给出成功/失败、状态增益或约束满足结果。
2. 将 verifier student 的 score-level teacher–student 差异聚合到分支级，再检查其方向是否与环境真值一致。
3. 只有通过方向门控的分支进入蒸馏；未通过者保留为诊断样本，而不是反向学习 teacher。
4. 将硬掩码扩展为置信门控：程序真值为硬门槛，序数评分分布或 A/B/T 后验决定软权重。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level on-policy verifier distillation**：应加入“轨迹/分支级方向一致性 mask”作为最小强基线，而不只做 teacher score 回归。
- **pairwise A/B/T 与序数分布**：可把 `R` 从二值扩展为 A/B/T 或序数后验，要求 teacher 的 pairwise log-odds 与 verifier 后验方向一致；tie/高不确定样本不应被强制更新。
- **程序化/环境真值门控**：论文直接支持“硬真值决定方向，teacher 分布决定幅度”的设计。
- **student-generated critique states**：可在 student 自生成 critique 后重新计算方向一致性，只蒸馏能让环境真值或独立 verifier 改善的 critique 状态。
- **高熵分叉保留探索**：不应删除所有未对齐样本；正确但 teacher 不认可的分支可能正是新模式，应进入探索池而非训练池。
- **sealed eval**：训练门控 verifier 与最终评价器必须分离；至少报告固定独立环境检查、未参与训练的 Judge，以及 best-of-K/分支覆盖率，防止只优化门控可见模式。
