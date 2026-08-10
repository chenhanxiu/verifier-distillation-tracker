# TRACE：长时程 Agent 的边界局部、成对闭环 Verifier

## 基本信息

- **论文标题**：Toward Reliable Context Compression for Long-Horizon Agents: An Empirical Study of Execution Instability
- **作者**：Guanghui Min、Liang Wu、Mayank Darbari、Chen Chen、Liangjie Hong
- **首次公开日期**：2026-08-06
- **版本日期**：2026-08-06（arXiv v1）
- **arXiv ID**：2608.06503
- **DOI**：https://doi.org/10.48550/arXiv.2608.06503
- **原始论文**：https://arxiv.org/abs/2608.06503
- **代码**：截至记录时未发现公开代码
- **记录类型**：新论文（2026-08-10 新列表检出）

## 一句话结论

TRACE 从同一环境状态分别续跑压缩前后的 Agent，利用新增阻塞动作与重复探索构造边界局部偏好；它为 Agent verifier × OPD 提供了比终局成败更干净的 student-state A/B 信号，但目前 verifier 只覆盖显式执行退化，不能检测静默状态损坏或长期不可恢复错误。

## 真正新增的内容

**论文原文结论：**上下文压缩可能削弱最近交互的影响，引发 blocked actions、重复工具调用及跨运行不稳定。TRACE 不把最终任务结果回填给所有摘要，而在每个 compaction boundary 上，从完全相同的环境状态成对执行 PRE（未压缩上下文）和 POST（候选摘要上下文）闭环续跑，以二者短期执行负担差生成摘要偏好，再只把偏好反馈给冻结 proposer 来优化自然语言压缩模板。

**分析推断：**这是一种可直接迁移到 verifier distillation 的反事实局部 teacher：将“是否压缩”替换为“student 分叉 A/B”或“有/无 critique”，同状态续跑产生环境可审计的偏好与可恢复性信号。它比只看 teacher–student KL 更能定位高价值蒸馏状态。

## 核心方法

1. 在压缩边界保存同一环境状态与压缩前上下文。
2. 固定 Agent、工具和解码设置，分别从 PRE 上下文和候选摘要 POST 上下文执行 K 步闭环续跑。
3. 将 AppWorld 原生执行错误记为 blocked action；将已执行过的规范化 tool-call signature 记为 repeated action。
4. 计算压缩额外负担 ΔG = E[G(POST)] − E[G(PRE)]，分数 Q = −ΔG。
5. 每个边界保留最高与最低分摘要形成 contrastive preference；proposer 只看到偏好，不看到后续动作、观察、错误或 verifier 分解。
6. 用少量边界偏好迭代自然语言压缩 prompt；所有模型参数保持冻结。

## 关键实验结果

**论文报告：**

- AppWorld test-normal 的 168 个任务上，TRACE 相比最佳既有压缩 baseline Prompting-O，平均准确率从 **71.4 提升至 77.1**，两次均成功的 Pass² 从 **59.5 提升至 67.3**，至少一次成功的 Pass@2 从 **83.3 提升至 86.9**。
- hard 任务上达到 Acc **63.5**、Pass² **52.4**、Pass@2 **74.6**，三项均优于所有压缩 baseline。
- 不压缩仍更强：总体 Acc **85.7**、Pass² **77.4**，表明 TRACE 只是缩小而非消除压缩损失。
- hard 任务的峰值 context 少于 full-context 一半，同时平均执行步数接近 full-context。
- 用 MiniMax-M3 优化出的模板迁移到 Kimi-K2.7-Code 后仍优于压缩 baselines；论文称总体 Acc 与 Pass² 甚至超过该模型的 full-context 设置，但这属于单 benchmark 的迁移结果。

## 证据质量与局限

- **优点**：同环境状态的 PRE/POST 成对控制能减少 Agent 自身随机性；模型、工具和解码冻结；同时报告平均成功、两次均成功和至少一次成功，能看到可靠性而非单次 pass。
- **局限**：论文明确称是 preliminary empirical study，只测试 AppWorld 与有限模型组合。
- verifier 只观察 blocked/repeated actions，无法捕捉静默状态污染、错误但可执行的操作、延迟很久才显现的损害或语义目标偏移。
- 只选择 12 个边界作为偏好优化样本，样本量小；没有参数级 verifier/student 蒸馏。
- PRE 只是局部控制而非最优轨迹；较高 Q 只说明相对未增加所定义的执行负担，并不等于最终任务正确。
- 尚无独立人类或另一 verifier 对 boundary preference 的大规模校准。

## 最接近的相关工作

- ACON：也优化固定 Agent 的自然语言压缩指南，但用终局成功/失败轨迹反馈。
- ReSum、SUPO：联合优化摘要或下游行为，而 TRACE 固定下游系统。
- Counterfactual Recoverability / SPOT：同样通过分叉续跑判断状态价值，而非仅依赖局部 divergence。
- process reward model、temporal credit assignment：为长轨迹提供稠密信号，但通常缺少同状态 paired control。
- pairwise reward modeling：TRACE 的 boundary-matched best/worst 摘要就是天然偏好对。

## 如何复用或推进 LLM-as-a-Verifier

把 Q 从单一 blocked/repeat 差值扩成序数 posterior：结合终局成功、约束违反、恢复成本、重复探索和状态不一致，输出“明显变差—轻微变差—不确定/等价—轻微变好—明显变好”的概率。若 PRE/POST 置信区间重叠，保留 T，不强制 A/B。再把反事实续跑 teacher 的分布蒸馏到只看当前轨迹前缀的轻量 verifier，使昂贵环境 rollouts 转化为部署时廉价 score。

## 对 Agent verifier × OPD 实验路线的具体影响

1. **Score-level on-policy verifier distillation**：在 student 实际访问的边界生成反事实 teacher score，再蒸馏到 student verifier；这是比离线轨迹更严格的 on-policy 状态覆盖。
2. **Pairwise A/B/T 与序数分布**：PRE/POST 或多个 candidate summary 天然构成同状态 pair；统计不显著时设 T，并学习完整序数分布。
3. **程序化/环境真值门控**：blocked、重复调用和环境状态差分是可审计 teacher signal；语义 judge 只能补充不能覆盖程序事实。
4. **Student-generated critique states**：可比较加入 student critique 前后的闭环续跑；只有 critique 实际减少负担或提升终局结果时才作为 privileged teacher context。
5. **高熵分叉保留探索**：多个候选续跑均成功且动作不同，应标为等价并保留；只压低经重复 rollout 稳定表现更差的分支。
6. **Sealed eval**：优化 proposer 不能看到 verifier 分解是良好隔离；仍应另留任务、环境 seed 和最终 judge，避免围绕 blocked/repeat proxy 共适应。

## 建议的最小实验

在 50 个 AppWorld 任务的 student 高熵分叉点，对 A/B 各续跑 4 次；以环境终态、blocked/repeat 和状态差分产生 5 档 posterior。训练一个只看 prefix + student critique 的 verifier，并比较 scalar KL、ordinal KL 与 A/B/T loss。sealed eval 报告成功率、Pass²、ECE、pairwise accuracy、tie recall、分叉熵和 silent-corruption 率。
