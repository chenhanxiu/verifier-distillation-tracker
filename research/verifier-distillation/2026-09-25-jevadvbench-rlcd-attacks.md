# JevAdvBench: A Benchmark and Black-Box Attacks for Reinforcement Learning for Calibrated Decisions Models

- **作者**：Jianyi Hu, Hangtao Zhang, Yi Liu, Yeqi Zeng, Li Zeng, Xianlong Wang, Rui Wang, Leo Yu Zhang
- **首次公开日期**：2026-09-25
- **版本日期**：2026-09-25（v1）
- **原始论文**：https://arxiv.org/abs/2609.31142
- **代码与数据**：https://github.com/JevAdvBench/JevAdvBench
- **项目页**：https://jevadvbench.github.io/JevAdvBench/

## 一句话结论

【论文原文】对 RLCD/Jev 这类直接输出概率、类别或分数的模型，无指令性的“旁观者意见”写入 state 就能使 12.1% 的决策翻转，并使 38% 的高置信答案跌破人工复核阈值，因此 state 必须被视为不可信、带论点的输入。

## 真正新增的内容

【论文原文】JevAdvBench 是面向 typed calibrated-decision model 的首个系统性黑盒攻击基准：812 个问题、66 个场景、9,744 个单编辑变体；用“攻击结果相对同一模型 clean decision 的变化”并对照完全相同请求的 rerun 噪声，而不依赖多数由模型自产的标签。

## 核心方法

1. 覆盖 Noul、Choice、Score 三种输出类型，分别攻击 question、state、injection 与结构字段。
2. 每个变体只做一个可逆编辑，并以 billed input tokens 验证编辑是否真正到达模型。
3. 以 clean 自身决策为参照，报告 flip、无 flip 的 shift、target hit 与 confidence-gate 影响。
4. 使用 66 场景聚类 bootstrap、Holm 校正和 identical-rerun noise floor。

## 关键实验结果

【论文原文】jev-1.13.0 的重述攻击仅在 rerun 基线的 1.2 个百分点内，schema 外字段完全未到达模型；但 state 中一条未验证意见使 12.1% 决策翻转，与最强注入命令的 10.1% 统计上相当。它还把 38% 的高置信 Choice/Score 答案压到 0.8 复核阈值以下；相同重跑总体 flip noise floor 为 1.0%（95% CI 0.3–1.9）。

## 证据质量与局限

【论文原文】发布原始响应、校验和、攻击代码和可离线复算结果，且显式验证输入是否送达，证据透明度高。局限是只测 jev-1.13.0、固定单次模板、无自适应搜索；82.4% 标签来自模型自身，因此论文主要度量鲁棒性而非独立真值准确率，也未评估任何防御。

## 最接近的相关工作

最接近 JEV-as-a-Judge、JEV 与 LLM Judge 的非等价性研究、MAWILE 及语义保持扰动审计。区别是它专门针对可被软件直接消费的 typed probability/choice/score，并把 API 预处理是否送达纳入实验。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】现有序数 probabilistic verifier 应增加 state-provenance 通道：把环境事实、用户陈述、其他 Judge 意见和 critique 明确分槽；用干净/攻击成对样本蒸馏不变性，并单独预测“需要人工复核”的风险，不能把原始 confidence 当作攻击检测器。

## 对 Agent verifier × OPD 实验路线的具体影响

- **Score-level OPD**：在 clean/perturbed 同义或无事实增量输入上约束分数分布稳定，而不只拟合均值。
- **A/B/T 与序数分布**：同时审计决策翻转、概率位移和阈值穿越；T 应覆盖 provenance 不可信。
- **真值门控**：环境事实须通过可验证来源进入独立字段，未经验证的 state 意见不能改变硬 verdict。
- **Critique states**：student critique 视为潜在攻击面，写入前要验真并标注来源。
- **探索**：不要因攻击诱导的低置信而无限扩展分叉；路由应结合环境证据。
- **Sealed eval**：锁定模型/API 版本并记录 token billing 与 rerun noise floor，防止服务变化冒充鲁棒性。
