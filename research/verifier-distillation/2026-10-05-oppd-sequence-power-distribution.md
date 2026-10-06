# Sharpen Without Search: On-Policy Distillation of Sequence-Level Power Distribution

- 作者：Erfan Baghaei Potraghloo、Seyedarmin Azizi、Arya Fayyazi、Saeid Shokoufa、Mehdi Kamal、Souvik Kundu、Massoud Pedram
- 首次公开日期：2026-10-05
- 当前版本日期：2026-10-05（v1）
- arXiv：2610.06804
- 原始论文：https://arxiv.org/abs/2610.06804
- Canonical URL：https://doi.org/10.48550/arXiv.2610.06804
- 代码：https://github.com/ArminAzizi98/OPPD

## 一句话结论

【论文原文】OPPD 将需要多候选搜索才能采样的序列级 power distribution 蒸馏进单次生成，使 student 学会直接输出其自身高概率答案，而无需参考答案。

## 真正新增的内容

【论文原文】方法不只匹配逐 token teacher 分布，而是用 student 生成候选、冻结 teacher 的序列级幂分布加权，再以相同权重做最大似然更新；本质上把 test-time sharpening/search 编译进模型参数。

## 核心方法

【论文原文】以 sequential Monte Carlo 在 on-policy 候选间采样，完整答案概率经幂指数重加权；粒子权重同时进入训练目标。一个损失系数可控制 student 吸收的 sharpening 强度。

## 关键实验结果

【论文原文】相同温度单次生成相对未训练模型在 MATH500、GSM8K 最多提升 23.0、27.3 点；比公开的 64-candidate power sampling 高 2.4、3.5 点。在相同 checkpoint 与预算下，比 verified-reward GRPO 分别高 3.8、4.0、5.4 点；GRPO 后再做 OPPD 最多增加 9.3 点。

## 证据质量与局限

【论文原文】跨模型族、尺度和数学到 HumanEval 的迁移，并公开代码，证据较完整。局限是主要依赖模型自身概率作为“答案质量”代理；高概率错误可能被进一步强化，且数学任务的确定性验真优势不能直接外推到开放式 Agent 轨迹。

## 最接近的相关工作

最接近普通 OPD、sequence-level OPD/GVPO++、best-of-N/power sampling，以及“Gains and Collapse in OPD”的隐式 reward 解释。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】把 power weight 替换为“序列概率 × 独立 verifier 后验”，使 sharpening 只在硬真值或 sealed verifier 支持时发生；对 Agent 可在共享状态的完整 action chunk 上重加权。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：【分析推断】增加 sequence-level score-weighted MLE 基线，并与 token score 蒸馏比较。
- **A/B/T 与序数分布**：【分析推断】同一状态多候选构成排序；概率接近或 verifier 冲突时标 T。
- **硬真值门控**：【分析推断】环境失败候选权重必须归零，防止“自信错误”被 sharpen。
- **critique states**：【分析推断】critique 可作为候选序列，但须由修复后的环境结果确认权重。
- **高熵探索**：【分析推断】幂指数需随 verifier 不确定性降低，避免过早坍缩。
- **sealed eval**：【分析推断】独立报告单次成功率、pass@k 和策略多样性，防止只提升既有高概率模式。
