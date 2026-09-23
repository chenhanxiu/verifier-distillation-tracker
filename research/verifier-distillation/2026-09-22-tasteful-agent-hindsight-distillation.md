# The Tasteful Agent: Measuring and Improving Taste in Long-Horizon Tasks

- **作者**：Wenbo Pan, Zhichao Liu, Shujie Liu, Jingying Zeng, Chin-Yew Lin, Xianfeng Tang, Yan Lu, Qi He, Xiaohua Jia
- **首次公开日期**：2026-09-22
- **版本日期**：2026-09-22（v1）
- **原始论文**：https://arxiv.org/abs/2609.25804
- **Canonical URL**：https://arxiv.org/abs/2609.25804
- **DOI**：10.48550/arXiv.2609.25804（arXiv DataCite，待注册）
- **代码**：https://github.com/wbopan/tastebench
- **数据集**：https://huggingface.co/datasets/wenbopan/taste-bench
- **arXiv ID**：2609.25804

## 一句话结论

【论文原文】将长时程 Agent 的真实轨迹切成“看不到后果的决策分叉”，再把能看到后果的 privileged teacher 判断蒸馏给 student，可使 Qwen3.6-27B 在任务不重叠的分叉上提升 17.9 个百分点，并改善 held-out SWE-bench Pro 的端到端成功率；这是目前最直接的“未来结果 teacher → 当前状态 verifier”蒸馏原型之一。

## 真正新增的内容

【论文原文】Taste-Bench 不只问任务是否最终成功，而是从平行 rollout 和单轨迹 detour 中自动挖掘 502 个真实决策分叉：给模型任务、分叉前缀和两个候选方向，隐藏后续结果，要求其提前选中最终更优方向。标签由后续测试、实验结果或恢复路径产生，不依赖大规模专家标注。论文进一步用“已知正确方向”的同一基座模型生成推理，再以 token-level forward KL 蒸馏到只看分叉前缀的 student。

【分析推断】其新增价值不是一般的 outcome prediction，而是把长时程延迟后果转化为可训练的 pairwise A/B 状态，并展示 privileged hindsight 可以被压缩进在线决策模型。

## 核心方法

1. 从 2,677 条软件工程 rollout 和 1,132 条研究 Agent 轨迹中对齐平行分支或检测“错误方向—失败—恢复”的 detour。
2. 对候选分叉做双重过滤：只看候选文本即可猜中的样本删除；完整记录下 Judge 仍不同意标签的样本删除。
3. 评测时将 A/B 顺序互换两次，只有两次都选对才计正确，抑制位置偏差。
4. 蒸馏时 teacher 获得正确方向提示并生成完整推理，student 只见正常分叉上下文；在 teacher continuation 上最小化 token-level forward KL，使用任务不重叠交叉折。
5. 端到端实验把 student 的分叉判断写成 advice，由固定 executor 独立完成任务。

## 关键实验结果

- 14 个前沿模型中最佳准确率仅 59.7%；需要更多后续工作才能显现优劣的分叉，平均准确率从 62.3% 降到 21.0%，接近该双顺序协议下的随机水平 25%。
- 增加推理预算几乎无效：两个模型从最低到最高 reasoning effort 分别变化 -0.2 和 +2.2 个百分点。
- 人工复核 172 个明确 A/B 判断时，170 个与自动标签一致（98.8%）；两名复核者在共同明确的 74 题上 Cohen’s κ=0.973。
- 任务不重叠评测中，distilled student 从 30.0% 提升到 47.9%；按单次顺序平均则从 42.7% 提升到 62.4%。
- 41 个 held-out SWE-bench Pro 任务中，固定 executor 无 advice 成功率为 14.6%，全正确 advice 的上界为 39.0%；论文报告 student advice 带来端到端提升，但样本规模较小。

## 证据质量与局限

【论文原文】优点包括真实 Agent 轨迹、任务不重叠折、官方 SWE-bench Pro 执行评价、双顺序协议和人工标签核验。局限是 4,657 个候选分叉仅 502 个通过 Judge 过滤，筛选过程会偏向现有 Judge 能确认的样本；平行分支仍可能同时受到后续执行质量影响；端到端评测只有 41 个任务，且 advice 来自同任务早期轨迹。

【分析推断】teacher continuation 来自已知标签后的“解释”，未证明其因果推理忠实；若直接当作 critique state，可能把事后合理化一并蒸馏。需要独立 sealed eval 和环境重放验证其跨 Agent、跨 harness 迁移。

## 最接近的相关工作

最接近的是 outcome-conditioned/privileged on-policy distillation、STRIDE 的首错定位、Belief-Shift Branching 与 EPIG-Tree 的高价值分叉选择，以及 EDGE/DRACO/BATON 的长轨迹信用分配。相比只预测终局奖励，本方法把后果压缩成“当前分叉应选哪条路”的 pairwise 判断；相比普通 OPD，它不是在 student token 前缀上直接匹配 teacher 分布，而是蒸馏 hindsight reasoning。

## 如何复用或推进 LLM-as-a-Verifier

- 将分叉标签从硬 A/B 扩展为 A/B/T：当两条分支终局差异落入执行噪声或置信区间时标 Tie，而不是强迫二选一。
- 保留 teacher 的分布而非单一标签，训练序数评分分布（立即可验证、下一步可验证、需更多工作、不足以判断），并对“more work”高熵状态触发环境分支。
- 把 student-generated critique 作为第三候选状态；只有 critique 能预测后续可执行证据且在重放中改善结果时，才写入 memory。
- 让硬测试、实验指标或环境结算决定方向，LLM teacher 只提供解释与幅度。

## 对现有 Agent verifier × OPD 路线的具体影响

【分析推断】优先新增“hindsight fork distillation”实验臂：在同一 on-policy student 状态生成 A/B（必要时 T）分支，使用程序/环境终局结果确定方向，再比较 label-only、teacher rationale forward-KL、score-distribution distillation 三种训练。高熵分叉不应立即压成单一路径，应保留多个分支到足够后果出现；训练集可使用 privileged future，sealed eval 必须隐藏未来、冻结 executor/harness，并使用未参与筛选的独立 oracle，防止 evaluator 与分叉生成器共适应。