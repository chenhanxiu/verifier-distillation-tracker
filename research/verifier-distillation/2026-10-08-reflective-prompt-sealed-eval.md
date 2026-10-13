# Reflective Prompt Optimization of a Deep-Research Agent: A Topic-Disjoint, Multi-Seed Protocol for Measuring Transferable Gains and Prompt-Level Overfitting

- **作者**：Elias Lumer；Sahil Sen；Vamse Kumar Subbiah；Kevin Paul
- **首次公开日期**：2026-10-08
- **版本日期**：2026-10-08（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2610.12601
- **Canonical URL**：https://arxiv.org/abs/2610.12601
- **DOI**：10.48550/arXiv.2610.12601
- **代码/材料**：论文称公开候选 prompts、lineage diffs、图表与分析；arXiv 页面未提供独立代码链接

## 一句话结论

该研究用 topic-disjoint、多随机种子和 verifier 替换实验表明，Agent prompt 优化的表面验证集增益可能来自 noisy Judge 的小样本选择，而真正可迁移收益依赖分维度反馈而非单一标量奖励。

## 真正新增的内容

【论文原文】在深度研究 Agent 的两个 system prompt 上运行 GEPA，并系统区分“答案记忆”“Judge 噪声选择”和“可迁移行为规则”；近半获胜 prompt 是答案表，但消融发现答案表本身并不贡献奖励。  
【分析推断】对 verifier/OPD 而言，最危险的不只是训练集泄漏，还包括在固定 Judge 噪声上挑中偶然高分的 teacher/critic 版本。

## 核心方法

1. 训练、验证、测试按 topic 完全隔离。
2. 使用多 seed 重复 prompt 演化。
3. 对获胜 prompt 做答案表删除和手写规则复现。
4. 替换 out-of-family Judge，并比较分维度反馈与单标量奖励。

## 关键实验结果

【论文原文】held-out citation reward 从 0.702 提升到 0.781，增量 0.079，bootstrap 95% CI 为 [0.051, 0.107]；三 seed 平均增益 0.107。分维度反馈是迁移的因果成分，压成单一标量后 held-out transfer 变为负；收益在异家族 Judge 下保持。

## 证据质量与局限

有 topic 隔离、置信区间、多 seed、verifier swap 与机制消融，证据较强；但对象是单个深度研究 Agent 和 citation reward，结论不能直接外推到所有工具 Agent 或参数级 OPD。

## 最接近的相关工作

最接近 AutoTuneBench、Beyond Aggregate Scores、Black-Box Judge 测量不稳定性、Who Judges Matters、Reward Score 残差化审计和 Gains and Collapse in OPD。

## 如何复用或推进 LLM-as-a-Verifier

对 prompt、rubric、critic 或 verifier 的任何自动优化都保存 lineage；训练/选择集、调参集和 sealed 集按主题与任务源双重隔离；至少使用三 seed、异家族 Judge 和分维度消融，报告选择前后分布而非单点赢家。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：不要只用聚合总分选 checkpoint，应保留各维 teacher 分数和迁移曲线。
- **A/B/T 与序数分布**：分维度后验应保留；维度冲突或跨 Judge 不稳定时输出 T。
- **程序化/环境真值门控**：引用存在性、页面可达性等确定性检查独立于 LLM Judge。
- **student-generated critique states**：critique 规则需在 topic-disjoint 任务上复现，而不是凭训练内增益入库。
- **高熵分叉**：多 seed 选择防止把偶然高分分支误作有效探索方向。
- **sealed eval**：直接采用 topic-disjoint、Judge swap、lineage audit 和手写规则复现四项验收。