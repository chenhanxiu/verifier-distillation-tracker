# PAST：利用完整学生轨迹进行特权适配的 On-Policy Self-Distillation

## 基本信息

- **论文标题**：PAST: Privileged Adaptation from Complete Student Trajectories for On-Policy Self-Distillation
- **作者**：Yangyang Feng, Zhuoyan Feng, Junlan Chen
- **首次公开日期**：2026-08-09
- **当前版本日期**：2026-08-09（v1）
- **arXiv ID**：2608.08726
- **原始论文**：https://arxiv.org/abs/2608.08726
- **代码**：截至记录时未发现公开代码仓库

## 一句话结论

PAST 把学生已完成轨迹及其最终成败作为 teacher 侧特权信息：正确轨迹保持学生行为，失败轨迹才向可验证成功的 teacher 分布适配，在 1.7B 数学推理实验中显著优于 vanilla OPSD。

## 真正新增的内容

**论文原文结论：** 既有 OPSD 通常只让 teacher 看学生前缀，没有充分利用该前缀最终通向成功还是失败的信息。PAST 将完整学生轨迹作为训练期特权变量，并按最终正确性选择不同 teacher 行为：对正确轨迹保持固定点，对失败轨迹做成功导向的适配。

**分析推断：** 新意不只是“增加 outcome 标签”，而是让同一前缀的监督目标依赖其未来轨迹结果；这为长时程 Agent 中“用未来环境结果反向塑造当前 verifier/teacher 信号”提供了直接原型。

## 核心方法

1. 从当前 student 采样完整 on-policy 轨迹，并用最终答案 verifier 判定成功或失败。
2. 对成功轨迹，让 teacher 保持接近 student 的下一 token 分布，避免破坏已经有效的行为。
3. 对失败轨迹，适配 teacher 使其偏向可验证成功，同时加入 student-proximity 正则，避免监督目标脱离 student 当前支持集。
4. 在 student 自己的前缀上以 forward KL 蒸馏适配后的 teacher。
5. 理论分析将该目标解释为：对给定前缀的轨迹条件 teacher 分布求投影平均，从而分离不可迁移的轨迹特异变化与可迁移的平均修正。

## 关键实验结果

**论文报告：**

- 主实验使用 Qwen3-1.7B thinking 模型，训练 100 个 student updates，在 AIME24、AIME25、HMMT25 上以 3 个随机种子评估。
- 三任务宏平均：Base 38.611，SFT 39.877，GRPO 40.494，vanilla OPSD 42.809，SD-Zero 43.981，H2SD 45.432，PAST 48.426。
- PAST 相对 vanilla OPSD 提升 5.617 分，报告的 95% 置信区间为 [2.592, 8.333]。
- PAST 在 AIME24/AIME25/HMMT25 上分别为 63.519/45.833/35.926。
- 2×2 消融中，仅使用轨迹信息为 43.364，仅训练 teacher 为 42.901，两者结合的 PAST 为 48.426；轨迹移除与打乱实验表明，匹配的完整轨迹信息是关键。
- 4B 的单种子扩展宏平均从 47.685 增至 48.519，但并非每项任务都提高。

## 证据质量与局限

**证据较强处：** 有多基线、3 个随机种子、置信区间和针对轨迹匹配的消融，主结果支持“完整 student 轨迹可提高 OPSD”的主张。

**论文明确或实验可见的局限：**

- 主证据集中在 1.7B 数学推理；4B 只有单种子且任务级结果混合。
- verifier 只检查最终答案，没有验证中间推理过程是否可靠。
- 失败分支依赖成功 masking、可变 group size、重试机制；全失败组可能被跳过，因此难以覆盖真正困难且无成功样本的状态。
- 理论结论针对总体目标，不等价于有限样本训练中的无偏保证。

**分析局限：** 尚无长时程工具调用、部分可观测环境或奖励延迟场景的实验证据，不能直接断言可迁移到 Agent。

## 最接近的相关工作

- Vanilla on-policy self-distillation：在 student-generated prefixes 上蒸馏 teacher。
- H2SD：通过分层/异质 teacher 信号强化自蒸馏。
- Distill Where You Fail：把蒸馏预算集中到 RL 失败组。
- SD-Zero：无需外部标注的自蒸馏路线。

PAST 与这些工作的主要区别是把“匹配的完整 student 轨迹”作为 teacher 侧特权变量，而非只按问题、前缀或 group 成败选择训练样本。

## 如何复用或推进 LLM-as-a-Verifier

**分析建议：**

- 将完整 Agent rollout、环境终态、工具执行日志和 student-generated critique 仅提供给 teacher verifier；student verifier 仍只看在线可用前缀。
- 把二元最终正确性扩展为序数分布，例如失败/部分完成/可恢复/成功，并蒸馏完整 score distribution，而非单一标量。
- 对通过程序化或环境真值门控的成功轨迹采用“固定点”约束，降低 verifier 对正确但少见策略的误惩罚。
- 对失败轨迹让 teacher 生成局部 critique 与可恢复性判断，再蒸馏到 student 的前缀级评分。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断：**

- **Score-level on-policy verifier distillation**：把 PAST 的 token-level forward KL 改为 teacher/student 序数评分分布 KL，是最直接的复用方式。
- **Pairwise A/B/T 与序数分布**：同一高熵分叉的两条完整轨迹可由环境结果组成 A/B/T；结果相同则保留 tie 和分布不确定性。
- **真值门控 teacher 信号**：优先使用程序化测试、环境回执或可复现终态作为成功门，而不是 teacher 自评。
- **Student-generated critique states**：让 teacher 看到学生自己的完整 critique/修复轨迹，判断哪些早期状态仍可恢复。
- **保留探索**：正确分支保持 student 固定点；对失败分支也应以 proximity/熵下限约束，避免一次失败就剪除罕见但可恢复的策略。
- **Sealed eval**：训练门控、teacher verifier 与最终评测必须使用隔离的任务与 evaluator；否则 teacher 和 student 可能对共同 verifier 偏差发生共适应。

总体上，PAST 为“未来轨迹作为训练期特权信息”提供了清晰实现，但将其用于 Agent verifier 前，仍需要过程级环境真值、序数不确定性与独立 sealed evaluation。
