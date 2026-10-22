# B-CARE: Blind Classwise Assessment of Relative Evidence for Stance Error Ranking

- **作者**：Meysam Sabbaghan、Doina Caragea
- **首次公开日期**：2026-10-21
- **版本日期**：2026-10-21（v1）
- **原始论文**：https://arxiv.org/abs/2610.29350
- **arXiv ID**：2610.29350
- **DOI**：https://doi.org/10.48550/arXiv.2610.29350
- **代码/项目**：未发现公开链接

## 一句话结论

让 verifier 在看不到 base model 预测与置信度时，对所有候选标签输出序数证据分布，可形成跨模型复用的相对风险分数并减少自我确认偏差。

## 真正新增的内容

提出 prediction-blind 的 classwise evidence profile：同一个固定 LLM verifier 独立评分每个候选标签，再用最强替代标签证据与预测标签证据之差排序错误风险。

## 核心方法

输入只含目标与文本，不暴露 base model 的选择或 confidence；verifier 输出所有 stance 类别的 ordinal evidence，构造比较风险并跨不同 base LLM 共用，无需为每个模型训练独立 error detector。

## 关键实验结果

四个 stance benchmark、三个异构 base LLM，共 12 个设置与 5,206 个唯一实例；平均 AUROC 0.735、AUPRC 0.524，最高风险 20% 的样本捕获 41.06% 错误。

## 证据质量与局限

跨模型、跨数据集并同时报告排序与 selective prediction 指标；但任务是短文本 stance 分类，不是长轨迹 Agent，且序数证据由单一 LLM 产生，尚无程序真值或决策后果验证。

## 最接近的相关工作

最接近 Ordinal Probabilistic Reward Model、Robust Conformal Consensus、Our Own Jev、JEV-as-a-Judge 与 Who Judges Matters。

## 如何复用或推进 LLM-as-a-Verifier

对共享 Agent 状态的候选动作盲评，不向 verifier 暴露 student 选择；保留每个候选的序数证据分布，再由环境真值校准差值与 abstention 阈值。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】A/B/T 可改为“对 A、B 逐项盲评后比较”：差值小或多档后验重叠时标 T，高置信差值仅控制 OPD 幅度，执行真值控制方向。该设计可减少 Judge 对 student 已选动作的确认偏差，但需在长轨迹 shared-prefix 分叉上重新验证。

## 结论边界

除明确标注“分析推断”的段落外，上述方法与实验结论来自论文原文或公开摘要；推断部分是面向现有研究路线的可检验假设，不应视为论文作者已经证明的结论。
