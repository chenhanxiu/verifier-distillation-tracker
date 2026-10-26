# Tampered ML：最小反事实实验设计审计

- **论文标题**：Tampered ML: Evaluating LLM Judgment of Machine Learning Research
- **作者**：Soroush Ebadian、Parand A. Alamdari、Joe Benton、Hailey Joren
- **首次公开日期**：2026-10-23
- **版本日期**：2026-10-23（v1）
- **原始论文**：https://arxiv.org/abs/2610.32114
- **DOI / canonical URL**：https://doi.org/10.48550/arXiv.2610.32114
- **代码/公开数据子集**：https://github.com/tamperedml/tamperedml

## 一句话结论

用 1,858 对“原实验—最小缺陷反事实”测试后，最强 Judge 仍仅 77.9%，且受展示顺序和“更具体、更透明、更常规”的表面线索影响，说明 pairwise verifier 必须做双顺序与最小反事实 sealed 审计。

## 真正新增的内容

**论文原文结论**：从已发表 ML 论文重建实验提案，再做最小编辑注入单一方法学缺陷；模型需在两种展示顺序中选出更可靠的设计。

**分析推断**：这种 construction 比随机错误注入更接近 Agent verifier 的“局部动作看似合理、但破坏因果有效性”难例，可直接用于 A/B/T 评测。

## 核心方法

1. 以发表论文实验为源，生成最小方法学 tamper。
2. 多重过滤确保原案忠实、改动确实削弱有效性。
3. 双顺序 pairwise 评价，测准确率、位置敏感与偏好线索。
4. 人工抽样验证数据对是否成立。
5. 发布带污染 canary 的数据子集，剩余数据按申请提供。

## 关键实验结果

**论文原文结论**：共 1,858 对；人工分层样本估计 86% 条目有效（95% CI 81%–91%）；Opus 5 最高为 77.9%。模型偏好看起来更具体、透明或常规的缺陷设计，并对 A/B 顺序高度敏感。

## 证据质量与局限

数据规模和双顺序设计较好，含人工有效性区间；但约 14% 条目可能无效，来源偏向顶会 oral/spotlight，构造流水线不公开，公开子集不完整。高分只代表识别此类 tamper，不构成通用科学可靠性认证。

## 最接近的相关工作

接近 MAWILE、SANE、Beyond Aggregate Scores、ImpossibleRubrics、Who Judges Matters 与 Judge Reliability Harness。

## 如何复用或推进 LLM-as-a-Verifier

为每类 Agent 轨迹生成最小反事实：删除必要检查、替换工具结果、交换动作顺序、伪造更详细理由或遗漏约束；要求 verifier 双顺序判断，并用环境重放确认 tamper 的真实影响。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

- **score-level OPD**：只有通过 tamper sensitivity 的 verifier score 才可作 teacher。
- **A/B/T**：两顺序 verdict 一致且有硬真值时给 A/B；翻转或样本无效时给 T。
- **真值门控**：tamper 是否破坏任务由程序/环境验证，不由语言偏好决定。
- **critique states**：critique 必须指出被 tamper 的具体因果环节。
- **探索保留**：不要因“更常规”而淘汰新颖但正确分支。
- **sealed eval**：保留未公开 tamper 类型与 canary，避免 evaluator 针对测试集共适应。
