# Same Judgement, Different Scores: Numerical Scoring Topology in LLM-as-a-Judge Evaluation

- **作者**：Doyun Kim, Chanwoo Kim, Jiwoo Kum, Minsoo Song, Chanjun Park
- **首次公开日期**：2026-11-19
- **版本日期**：2026-11-19（v1）
- **原始论文**：[arXiv:2611.26077](https://arxiv.org/abs/2611.26077)
- **DOI**：[10.48550/arXiv.2611.26077](https://doi.org/10.48550/arXiv.2611.26077)
- **代码**：论文页面未提供公开代码链接
- **发表信息**：EACL 2027 Findings（论文页面标注）

## 一句话结论

【论文原文】同一语义判断仅因数值量表的宽度、粒度、偏移、对称性或边界改变，就会产生系统性分数、校准和鲁棒性差异；【分析推断】ordinal verifier 训练前必须冻结 scoring topology，并优先蒸馏概率或阈值事件，而非把不同量表的标量直接混合。

## 真正新增的内容

【论文原文】工作定义“numerical scoring topology”作为独立设计变量，并系统比较其对多种 benchmark 与 Judge 模型的影响。它把常被视为提示细节的量表设计提升为评价协议的一部分。

【分析推断】对 verifier distillation 的新增价值是指出：teacher 分数的几何坐标系本身会改变标签分布；跨 teacher、跨轮次或跨 prompt 的 score-level OPD 若不统一坐标系，可能蒸馏的是格式偏差。

## 核心方法

【论文原文】

1. 用五个维度描述数值量表：scale width、granularity、offset、symmetry、boundary placement；
2. 在多种 benchmark 和不同 Judge 模型上保持语义评价任务不变，仅改变 scoring topology；
3. 比较分数偏移、校准、判别效度与鲁棒性；
4. 分析模型规模/能力与 topology 敏感性的关系。

## 关键实验结果

【论文原文】

- scoring topology 对 Judge 分数、校准与鲁棒性产生系统性影响。
- 在高判断负荷任务上影响更明显。
- 平移后的范围和较窄量表在许多设置中造成最大的 score deviation。
- 更强、更大的 Judge 一般具有更高判别效度，也更能抵抗 topology 变化。

## 证据质量与局限

【论文原文】优点是跨 benchmark、跨 Judge 的系统操纵，并明确拆分量表结构维度。摘要未给出各设置的具体效应量、人工真值覆盖和对训练后策略的下游影响；结论主要针对 zero-shot Judge 评价，不自动证明所有 reward model 都同样敏感。

【分析推断】更大模型“更稳健”仍不能替代 protocol normalization；若训练阶段量表固定但 sealed eval 量表变化，模型可能学到量表特定阈值。

## 最接近的相关工作

- Rethinking Verbalized Confidence：比较 verbalized confidence 与 logprob 作为 Judge 信号。
- MAWILE：用应不变/应下降的扰动审计多轴 Judge。
- ordinal probabilistic reward model：保留类别顺序及分布。
- Reward Score 残差化审计：提醒表面校正不等于构念有效。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】建立 topology-invariance 测试：对同一轨迹用 0–4、1–5、0–10、带负值对称量表和文字等级重复评分。主训练标签采用规范化阈值事件的累计概率，例如 P(score≥k)，并用等距/有序 logit 映射回统一序数空间；将 topology 方差作为 epistemic uncertainty。

## 对现有 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- **score-level on-policy verifier distillation**：固定 teacher prompt 与量表；跨 teacher 分数先做 ordinal calibration，不直接平均原始数值。
- **pairwise A/B/T 与序数评分分布**：pairwise 与 ordinal 共用潜在效用，但分别建模；T 阈值需在统一坐标系中定义。
- **程序化/环境真值门控**：用真值锚点拟合每种 topology 的映射，并监控映射随 policy 漂移。
- **student-generated critique states**：critique 准入使用量表不变性；对 topology 高敏感的样本标记不确定。
- **高熵分叉保留探索**：把量表变体产生的分歧计入熵，避免错误低置信被单一量表掩盖。
- **独立 sealed eval**：冻结一套主量表，同时用未参与训练的 topology 变体做鲁棒性压力测试。
