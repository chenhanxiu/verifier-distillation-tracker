# How to Post-Train on a Surrogate: Envelope Sampling Mitigates Reward Hacking

- **作者**：Sanjit Dandapanthula；Shuvom Sadhuka；Samir Khan；Michael Oberst；Aaditya Ramdas；Alexandra Chouldechova
- **首次公开日期**：2026-10-08
- **版本日期**：2026-10-08（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2610.11281
- **Canonical URL**：https://arxiv.org/abs/2610.11281
- **代码**：未发现公开代码链接

## 一句话结论

少量 ground-truth 若从普通 on-policy 样本中抽取，往往看不到罕见但可被优化放大的 verifier 错误；Envelope Sampling 主动覆盖 reward 不确定包络，从而更有效发现并抑制 reward hacking。

## 真正新增的内容

【论文原文】作者假设真实人工/校准 reward 位于以 LLM Judge 为中心的 L2 邻域，构造最小化最坏情形 regret 上界的采样分布；再通过拒绝采样或修改 reward 的训练方案降低对 surrogate 漏洞的利用。

【分析推断】这为高熵分叉提供了比策略熵更直接的采样准则：应优先探索“不同可能真值函数会强烈改变排序”的状态。

## 核心方法

1. 以现有 Judge 为 surrogate reward，并用少量 ground-truth 校准。
2. 建立真实 reward 相对 surrogate 的 L2 不确定集合。
3. 计算覆盖该不确定集合的 envelope sampling 分布，聚焦最坏情形误差可被策略利用的区域。
4. 用 rejection sampling 或 modified reward fine-tuning 降低 regret 与 hacking。

## 关键实验结果

【论文原文】在临床笔记与谄媚（sycophancy）场景中，Envelope Sampling 能缓解 reward hacking，而从 base-model 样本做普通 recalibration 会失败。摘要未报告统一绝对提升，故不补造数值。

## 证据质量与局限

【论文原文】理论目标与两个不同应用场景相互支持，并直接比较常用的 base-model/on-policy 校准方案。  
【局限】L2 邻域是否覆盖真实偏差是关键假设；临床和 sycophancy 不是完整长时程 Agent 环境。ground-truth 的成本与错误、动态策略漂移及高维序数 reward 的扩展仍需验证。

## 最接近的相关工作

与 Proof-Carrying Cognition、GLARE、Monitoring and Discovering Reward Hacking、ImpossibleRubrics、Reward Score 残差化审计、IWD 和 Robust Conformal Consensus 最接近。区别是它从最坏情形后悔界出发设计数据采样。

## 如何复用或推进 LLM-as-a-Verifier

对每个 Agent 状态维护一组与现有真值一致的候选 verifier，估计它们对 A/B/T 或序数分布的分歧包络；优先请求环境重放/人工真值标注这些状态，再用新真值校准 teacher。这样采样目标直接对应“最可能被策略利用的盲区”。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：将 envelope score 加入样本权重，专门补齐 surrogate reward 最脆弱的 on-policy 区域。
- **A/B/T 与序数分布**：在候选真值模型下排序会翻转的样本标为 T，并优先获取硬标签；不把均值分数当确定答案。
- **程序化/环境真值门控**：有限 oracle 预算按最坏情形 regret 分配，而不是均匀或只按策略概率分配。
- **student-generated critique states**：优先审计能让多个 plausible verifier 产生相反判断的 critique，防止语言包装投机。
- **高熵分叉**：用 reward-model ambiguity 与策略熵的乘积/并集分配分叉预算，保留潜在 verifier 漏洞区域。
- **sealed eval**：用独立、隐藏的真值函数/规则和未用于 envelope 构造的任务测试，防止采样器与 evaluator 共适应。

总体判断：【分析推断】这项工作应直接影响数据预算分配：把昂贵环境真值集中到“奖励模型最可能被优化攻破”的状态，比随机复核更有价值。