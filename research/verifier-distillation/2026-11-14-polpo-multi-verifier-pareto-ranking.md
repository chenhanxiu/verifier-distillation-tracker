# Policy Optimization With Multiple Verifiers via Pareto Rankings

- **作者**：Kai Yamashita、Shohei Taniguchi、Hiroki Furuta、Masahiro Suzuki、Yutaka Matsuo
- **首次公开日期**：2026-11-14
- **版本日期**：2026-11-14（v1）
- **原始论文**：https://arxiv.org/abs/2611.19064
- **代码**：未发现公开代码
- **标识符**：arXiv:2611.19064；DOI: 10.48550/arXiv.2611.19064

## 一句话结论

【论文原文】POLPO 不把多个 verifier 的结果压成标量，而以 Pareto dominance 只学习确定的偏序关系，并让相互冲突的部分成功保持不可比。

## 真正新增的内容

【论文原文】论文指出 complete-success 奖励丢弃部分解之间的差异，而计数或加权和会人为规定“满足不同约束集合”的优劣。POLPO 直接从 verifier 建立的偏序学习：若一个回答满足额外要求且未丢失已有要求，它支配另一个回答；冲突结果不强行排序。

【分析推断】这是现有 pairwise A/B/T 与序数评分分布路线的直接算法化版本：A/B 只来自可证明支配，T 对应不可比；比把多维 Judge 分数平均成单一 reward 更能保留高熵分叉。

## 核心方法

1. 将每个回答表示为多 verifier 的通过/失败向量。
2. 用 Pareto dominance 构造部分顺序，保留冲突解的不可比性。
3. 扩展 DPO 的 listwise likelihood，对所有与偏序一致的完整排序的总概率做最大化。

## 关键实验结果

【论文原文】在代码生成和指令遵循任务上，POLPO 相比标量 reward 训练具有更高学习效率和更高的完整要求满足率，并能在尚无全通过回答时从已验证的局部改进学习。摘要未披露具体绝对提升和置信区间。

## 证据质量与局限

【论文原文】方法覆盖两个多约束任务族，并直接与标量聚合训练比较。

【分析推断】Pareto 关系依赖每个 verifier 本身可靠，且 verifier 数增大后可比样本可能迅速变少；二元通过向量也没有表达 verifier 置信度和严重性。需要报告不可比率、有效样本量及错误 verifier 对偏序的敏感性。

## 最接近的相关工作

最接近多 Judge 面板的分布恢复、Agreement Overstates Evidence、MAWILE 和 UECR-GRPO。不同点是 POLPO 不先聚合 Judge，而把偏序直接写入 policy objective。

## 如何复用或推进 LLM-as-a-Verifier

把程序测试、环境断言与软 Judge 各自保留为独立轴；只有硬轴一致支配时产生确定偏好。对软轴使用通过概率分布或置信区间，并把无法支配的样本送往主动取证 Judge，而不是强行标量化。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：保留每个 verifier 的独立 score，蒸馏 Pareto 改进而非加权总分。
- **pairwise A/B/T 与序数分布**：支配关系生成 A/B；冲突与重叠区间标 T，并保留多轴分布。
- **环境真值门控**：程序或环境 verifier 决定不可违反的轴，软 Judge 只细化可行集合。
- **student-generated critique states**：critique 必须指出改善了哪个约束且未破坏哪些约束。
- **高熵探索**：不可比响应继续保留，避免权重选择导致单一模式坍缩。
- **sealed eval**：冻结 verifier 集与权重无关的偏序规则，报告各轴、全通过率和不可比率。

