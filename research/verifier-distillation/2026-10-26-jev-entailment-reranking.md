# JEV Entailment Reranking：Span Readout 与选择性适配

## 基本信息

- **论文标题**：Improving JEV Entailment Reranking with Span Readouts and Selective Adaptation
- **作者**：Haocheng Mei, Yuchuan Tian, Ye Yuan, Enhua Wu, Chao Xu, Allen Chen, Kai Han, Yunhe Wang
- **首次公开日期**：2026-10-26
- **版本日期**：2026-10-26（v1）
- **论文链接**：https://arxiv.org/abs/2610.35654
- **代码链接**：https://github.com/Mei-TN/Jev-reranking

## 一句话结论

JEV 在跨请求 entailment reranking 中，候选 span 的均值读出配合只适配注意力与 gated DeltaNet，可用更少训练参数获得更稳定的排序准确率。

## 真正新增的内容

**论文原文结论**：direct selection 在单次请求内比较候选，而 entailment reranking 将每个候选拆成独立 NLI 请求；后者需要重新选择 readout 与 adapter 位置。mean-span pooling 不增加 head 参数，selective adaptation 移除 feed-forward adapter。

**分析推断**：对 Agent verifier 而言，“一次比较 A/B”与“分别判断 A、B 是否满足 rubric”不是同一统计问题。独立请求更利于缓存和扩展候选，但跨请求分数必须校准，且会失去同上下文对比带来的共同偏差抵消。

## 核心方法

- 把每个候选转成 premise/hypothesis 与固定 entailment relation 选项。
- 对 NLI 选项内部所有 contextual states 做均值池化。
- 仅在 attention 与 gated DeltaNet projection 保留低秩更新，去除 FFN adapter。
- 用覆盖七个来源、11 种 reranking 配置的 MC11 汇总评价。

## 关键实验结果

**论文报告**：在 NeoHorse-1-4B 上，selective adaptation 相比全模块适配提高 MC11 平均准确率，同时将可训练参数减少一半以上；mean-span pooling 在相同参数量下继续稳定提升。

## 证据质量与局限

公开代码、跨来源多配置评测是优点。局限是摘要没有披露绝对分数和置信区间；任务仍以候选答案/NLI 为主，尚未评测长轨迹的证据遗漏、工具状态或跨步依赖。

## 最接近的相关工作

Jev、Our Own Jev、JEV-as-a-Judge、pointwise/pairwise reward modeling。区别是系统研究独立请求 entailment reranking 的 readout 与参数高效适配。

## 如何复用或推进 LLM-as-a-Verifier

可将五维 rubric 的每一维转成独立 entailment 候选，得到 typed score distribution；对“目标推进/安全/可恢复性”等分别校准，再聚合为 A/B/T，而不是训练一个不透明总分头。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：用分维度 entailment posterior 控制不同 token/segment 的蒸馏幅度。
- **A/B/T**：分别评分后只有在后验差异超过阈值时给 A/B，否则 T。
- **硬真值门控**：执行证据作为 premise，防止只凭文本风格判定。
- **critique states**：critique 必须能被证据 span entail，才允许写入。
- **高熵探索**：后验相近的候选继续保留。
- **sealed eval**：用未参与 adapter 训练的 rubric、候选顺序和模型家族测试迁移。