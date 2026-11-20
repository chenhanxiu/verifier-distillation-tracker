# Bradley-Terry Training Can Distort Outcome Probabilities of Initially Accurate Language World Models

- **作者**：Xinze Shi, Litian Zhang, Zhenjie Su, Zelong Yu, Yuting Zhang, Qihua Feng, Zifeng Kang, Chaozhuo Li, Zhengxuan Hu
- **首次公开日期**：2026-11-19
- **版本日期**：2026-11-19（v1）
- **原始论文**：[arXiv:2611.25594](https://arxiv.org/abs/2611.25594)
- **DOI**：[10.48550/arXiv.2611.25594](https://doi.org/10.48550/arXiv.2611.25594)
- **代码**：论文页面未提供公开代码链接

## 一句话结论

【论文原文】即使 pairwise 比较本身正确，Bradley–Terry 目标也可能把原本准确的 outcome 概率推向物理上不可能的分支；【分析推断】A/B/T 偏好不能无条件当作 distributional verifier 的概率监督，必须显式建模 Judge 选择规则并用环境枚举/结算锚定分布。

## 真正新增的内容

【论文原文】作者把问题从“偏好标签是否有噪声”推进到“偏好似然是否识别真实 outcome distribution”：在结果可枚举的机器人推物环境中，直接计算 Bradley–Terry 最优点，并预测训练后概率会向哪里偏移；另一个了解 Judge 规则的 likelihood 使用相同比较却不会产生同样扭曲。

【分析推断】这为现有 pairwise A/B/T → 序数/概率分布的转换提供了明确反例：排序一致不等于概率可恢复。

## 核心方法

【论文原文】

1. 构造可枚举真实 outcome distribution 的模拟 robot push；
2. Judge 比较两个候选 outcome 哪个更接近已发生结果；
3. 用 Bradley–Terry 目标训练原本已校准的 language world model；
4. 在训练前解析/数值求出目标最优点，并与训练终点对照；
5. 用显式知道 Judge 规则的 likelihood 作为修正对照；
6. 从 probability、readout、response 到 action 审计误差传递。

## 关键实验结果

【论文原文】

- 初始模型在未见 layout 上 hazard error 为 2.4 个百分点。
- Bradley–Terry 训练把 33–43 个百分点概率移到该条件枚举分支从未产生的 outcome。
- 在去掉物理不可能事件后仍残留约 29 个百分点偏移。
- 继承训练前阈值时，含不可能事件的设置每次决策效用约损失 3 点；未见条件损失 1–2 点，主要来自 false reject。
- 无不可能事件时，六个随机种子的平均效用损失低于 1 点，但动作选择仍有小幅 regret。

## 证据质量与局限

【论文原文】优点是有枚举真分布、目标最优点预测、替代 likelihood 和跨多种 candidate law/更密枚举的稳健性检查，因果归因较强。局限是单一模拟机器人任务、10 页规模，结论针对 outcome probability，并不说明 Bradley–Terry 在纯排序目的下普遍无效。

【分析推断】对 Agent verifier 的风险取决于下游是否把 pairwise logit 当成校准概率；若只做排序，伤害可能较小，但一旦用于阈值、风险预算或探索裁剪就会放大。

## 最接近的相关工作

- Bradley–Terry reward modeling 与 pairwise preference learning。
- distributional verifier / ordinal probabilistic reward model：目标是恢复评分或 outcome 分布。
- MAWILE：用受控扰动审计 pairwise 与 ordinal Judge。
- Agreement Overstates Evidence：说明相关 Judge 投票会夸大证据。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】将 A/B/T 数据生成过程写入概率模型：Judge 是比较“与观察到的结果更近”、比较“任务效用更高”，还是比较“更像参考轨迹”，三者对应不同 likelihood。可枚举环境中直接做 proper scoring rule；不可枚举环境中至少用部分 outcome certificate 和保留集校准。

## 对现有 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- **score-level on-policy verifier distillation**：不要把 pairwise logit 直接解释为绝对 score；先验证其与环境 outcome 概率的可识别性。
- **pairwise A/B/T 与序数评分分布**：A/B/T 作为观测，序数/概率分布作为潜变量，显式建模 Judge 选择规则；T 不能简单等于 0.5。
- **程序化/环境真值门控**：用枚举分支、执行回执或不可达证书约束概率质量，禁止给不可能 outcome 分配质量。
- **student-generated critique states**：critique 的 pairwise 偏好只用于排序，是否写入记忆仍需 outcome 验真。
- **高熵分叉保留探索**：概率扭曲可能制造假低熵；以环境可行分支熵而非 Bradley–Terry 熵决定探索。
- **独立 sealed eval**：单独报告 ranking、calibration、impossible-mass 和 decision utility，避免“排序变好”掩盖分布退化。
