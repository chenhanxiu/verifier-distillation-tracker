# Evidence-Governed Adoption of Self-Generated Updates in Autonomous AI Agents

- **作者**：Subodh Lonkar
- **首次公开日期**：2026-11-12
- **版本日期**：2026-11-12（v1）
- **原始论文**：https://arxiv.org/abs/2611.16378
- **代码**：未见公开代码仓库
- **标识符**：arXiv:2611.16378；DOI: 10.48550/arXiv.2611.16378

## 一句话结论

【论文原文】EGE 将自生成更新的“提出”与“采用”分开，用冻结候选、fresh paired audit、独立 evaluator 校准、非劣检验和有界 canary 管理持续 Agent 更新。

## 真正新增的内容

【论文原文】框架为一串自适应产生的候选构造 evaluator-calibrated simultaneous lower bound，并用 candidate-wise Hoeffding 界与独立校准样本纠正 operational evaluator 的乐观偏差；同时形式化 reference 更换的 bridge test 与版本链累计退化上界。

【分析推断】它不是 verifier 蒸馏算法，但为持续更新 verifier/critique/memory 后的 sealed acceptance 提供了目前最贴近实验路线的统计治理层，尤其针对 evaluator 与候选共同适应。

## 核心方法

1. 生成候选后冻结，禁止边评边改。
2. 在 fresh paired samples 上比较候选与 reference。
3. 要求主目标达到预设提升，并对声明能力做 reference-relative non-inferiority。
4. 以独立校准样本修正 evaluator 偏差；通过 bridge test 才更换 reference。
5. 先有界 canary，再决定持续采用。

## 关键实验结果

【论文原文】Monte Carlo stress test 展示在候选依赖的 evaluator 乐观偏差下仍可校准；论文明确说明这只是风格化统计实验，不是已部署 Agent 的实证评测。

## 证据质量与局限

【论文原文】理论条件清楚，并明确限制：有界 paired score、fresh sampling、有效 reference procedure 和预先声明分布；不保证普适安全或任意分布漂移鲁棒性。

【分析推断】证据质量在统计推导上较强、在 Agent 实证上较弱。Hoeffding 界可能保守；若 reference evaluator 本身不具构念有效性，校准只能保证相对一致，不能保证真实正确。

## 最接近的相关工作

最接近 AutoTuneBench、Proof-Carrying Cognition、MAGS、SkillAA、RetireOPD 与 conformal/Judge 校准工作。区别在于把自适应候选序列、evaluator 校准与 reference 版本链统一进采用规则。

## 如何复用或推进 LLM-as-a-Verifier

把 verifier 蒸馏后的每个 checkpoint、prompt 或 rubric 当作候选；在隐藏 paired states 上与当前 reference 比较，并用环境真值/人工 reference 校准 operational Judge。只有主指标改善、关键能力非劣且 canary 通过时才替换 verifier。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：每次 teacher/student 更新后须通过独立 paired audit，不能以训练内分数直接发布。
- **A/B/T 与序数分布**：paired audit 原生支持 A/B；置信下界不足时判 T/不采用。
- **环境真值门控**：reference procedure 优先使用程序测试、环境结算或人工复核，而非同源 Judge。
- **critique states**：新 critique 规则先作为冻结候选评估，未过门不写入持久记忆。
- **高熵探索**：采用门只决定是否发布，不要求训练时消除高熵候选；可保留多分支候选库。
- **sealed eval**：直接采用 fresh、paired、版本化 reference 与 bridge test；把 evaluator calibration set 与优化数据物理隔离。
