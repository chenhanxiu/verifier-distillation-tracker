# Jev 式 System One 模型的选项顺序偏差

## 基本信息

- **论文标题**：Understanding Jev-Style System One Models: Does Structure Reduce Selection Bias?
- **作者**：Mingyang Song, Mao Zheng, Zhiyuan Ma, Xinpeng Zhou
- **首次公开日期**：2026-10-26
- **版本日期**：2026-10-26（v1）
- **论文链接**：https://arxiv.org/abs/2610.35826
- **代码链接**：未发现公开代码

## 一句话结论

Jev 的结构化一次前向概率输出并不会自动消除选项顺序偏差；总体准确率几乎不变时，逐样本失败集合仍会大幅扩张，甚至全体一致也经常错误。

## 真正新增的内容

**论文原文结论**：对两个 Jev 版本、12 个复现模型与六个生成式 LLM，将同一问题的候选项进行八种排列并追踪逐样本答案，区分固定顺序重复与等价选项重排。

**分析推断**：distributional verifier 的“稳定概率”不能只用总准确率或重复方差验收；应测试语义等价变换下每个样本的后验与决策是否稳定。对 A/B/T 而言，顺序敏感本身就是进入 T 或降低蒸馏权重的理由。

## 核心方法

- 使用 1,700 道题、两个 benchmark。
- 对每题生成八种选项排列，同时做固定顺序重复对照。
- 追踪首个失败、累计失败集合、重复性、投票和一致判断的正确性。
- 横向比较原生 Jev、Jev 复现和生成式 LLM。

## 关键实验结果

**论文报告**：Jev 总体准确率变化不到两个百分点，但相对原始顺序的累计失败集合扩大 27%–29%；首错持续到最后一种排列。投票仅带来有限改善，且 unanimous verdict 仍频繁错误；Jev 在保持正确选项方面没有普遍优于生成式 LLM。

## 证据质量与局限

多模型、逐样本配对和固定顺序对照使结论可信。局限是两项 benchmark 仍以多选题为主，尚未直接覆盖长轨迹、工具证据和连续序数评分；也没有证明某种训练方法能修复偏差。

## 最接近的相关工作

Our Own Jev、JEV-as-a-Judge、Who Judges Matters、Behind Aggregate Scores、MAWILE。本文聚焦候选顺序这一可控、标签保持不变的变形测试。

## 如何复用或推进 LLM-as-a-Verifier

将 pairwise A/B 同时以 AB、BA 两个顺序运行；ordinal 候选集至少做循环置换。输出完整 posterior，并把顺序造成的方差并入 epistemic uncertainty，而不是只平均成一个分数。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：按置换稳定性门控 teacher score。
- **A/B/T**：AB/BA 不一致直接标 T；一致但低覆盖也不视为真值。
- **硬真值门控**：当程序或环境结算可用时，其方向覆盖 Jev 选择。
- **critique states**：候选 critique 的呈现顺序必须随机化并审计。
- **高熵探索**：保留因排序扰动发生翻转的分支。
- **sealed eval**：冻结隐藏置换集，报告逐样本翻转率而非只有 aggregate accuracy。