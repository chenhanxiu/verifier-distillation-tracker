# Agreement Overstates Evidence：LLM Judge 共识中的相关错误

- 论文标题：Agreement Overstates Evidence: Error Dependence in LLM Judge Consensus
- 作者：Elias Hossain；Niloofar Yousefi；Ser-Nam Lim
- 首次公开日期：2026-09-18
- 当前版本日期：2026-09-18（v1）
- arXiv：https://arxiv.org/abs/2609.22512
- DOI：https://doi.org/10.48550/arXiv.2609.22512
- 代码：https://github.com/eliashossain001/Automatic-Jury-Consensus

## 一句话结论

十个 LLM Judge 的有效独立信息量可能只有 3.51 个；多模型一致并不是独立证据，必须用少量可信真值估计共错结构，再决定投票、A/B/T 聚合和训练数据准入。

## 真正新增的内容

- 【论文原文】把 Judge bank 的错误相关性、有效集成规模与统计显著性放进同一测量框架，不只报告平均一致率。
- 【论文原文】区分“全局共错”和“特定子群共错”，证明相同的总体相关程度可能偏好不同聚合规则。
- 【论文原文】验证共识保留的污染会进入 DPO 数据并降低 held-out reward margin，连接了 evaluator 共错与后续策略训练。

## 核心方法

1. 在带可信标签的 calibration panel 上收集每个 Judge 的逐题错误向量。
2. 估计误差相关矩阵、平均相关系数、特征谱和 effective ensemble size；以题目而非单次投票作为统计推断单位。
3. 对比普通多数票、相关性过滤、偏差簇过滤和学习式规则选择器，并在等保留率下评估。
4. 用控制性共错注入、跨数据集与 frontier/open-weight Judge bank 测试结论稳健性。

## 关键实验结果

- 【论文原文】主实验十 Judge bank 在 1,133 个 RewardBench 项目上的平均错误相关为 0.206，有效规模仅 3.51/10；扩展到 16 个 Judge 时有效规模约 4.71。
- 【论文原文】在最高 28% 的比较中，忽略共享错误会得出“系统显著更优”，而按题目级相关性推断后该结论不成立。
- 【论文原文】跨 GPT、Claude、Grok 的 frontier bank 虽单 Judge 准确率为 91%–93%，残余错误相关仍高达 0.56。
- 【论文原文】没有一种相关性感知过滤器在所有设置稳定优于多数票；严格协议下学习选择器增益仅 +0.12 个百分点且置信区间跨零。

## 证据质量与局限

- 证据较强：有可信标签、多个数据集、open/frontier bank、bootstrap、控制注入和下游 DPO 实验；代码公开。
- 局限：自然环境中的共错流行度不能由控制注入直接推出；深入分析的共同漏洞主要是位置偏差；自适应方法约需 100 个可信标签；结果不能直接外推到新的 Judge 组合和 Agent 任务。
- 【分析推断】论文支持校准现有三 Judge 系统，但不支持简单换成某一种“更高级”投票公式。

## 最接近的相关工作

最接近仓库中的 How Many Humans Is a Judge Panel Worth?、Who Judges Matters、Robust Conformal Consensus 和 Black-Box Judge Measurement Instability；本论文额外强调错误的联合结构以及错误统计如何改变显著性和下游偏好优化。

## 如何复用或推进 LLM-as-a-Verifier

- 为三 Judge 评测保存逐题错误矩阵，而非只保存最终票数；报告 nominal vote、有效票数和共错簇。
- 对五维 0–3 分分别估计相关性，避免“总分一致”掩盖某一维度的系统共错。
- 由程序/环境真值样本构成约 100 条 sealed calibration panel，选择多数票、置信度加权或 A/B/T 聚合规则；Judge/任务变化后重新校准。

## 对现有 Agent verifier × OPD 路线的具体影响

- 【分析推断】三模型投票不能默认等于三份独立监督；OPD loss 应按有效证据量而非票数缩放，并保留 Judge 分歧分布。
- 【分析推断】pairwise A/B/T 中，三者一致也需检查是否属于历史共错簇；共识但无环境真值的样本不应自动进入高权重蒸馏集。
- 【分析推断】sealed eval 需要与训练 Judge bank 在模型家族、提示模板和数据来源上隔离，并以题目级 bootstrap 判断改进，防止 evaluator 共适应制造虚假显著性。
