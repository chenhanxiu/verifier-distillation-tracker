# Pairwise Evaluation 遗漏了什么：跨 Prompt 的 Reward Score 可比性

- **论文标题**：What Pairwise Evaluation Misses: Reward Scores across Prompts
- **作者**：Mateusz Modrzejewski, Tomasz Radzikowski
- **首次公开日期**：2026-10-22
- **版本日期**：2026-10-22（v1）
- **原始论文**：https://arxiv.org/abs/2610.31090
- **DOI / canonical URL**：https://doi.org/10.48550/arXiv.2610.31090
- **代码**：未见作者公开代码链接

## 一句话结论

同 prompt 的 pairwise 胜负会抵消 prompt 共享偏置，因此无法证明 reward score 能跨 prompt 比较；这直接限制了将 A/B 偏好无校准地汇总成全局序数分数。

## 真正新增的内容

**论文原文结论**：作者提出以人类评分为参照的跨 prompt 审计，组合 between-prompt variance share、sibling-rating regression 与 prompt substitution，并应用于 18 个 released scorer 和 6 个匹配训练条件。

**分析推断**：该工作填补了 pairwise A/B 与 pointwise/ordinal score 之间的可识别缺口：局部排序正确不代表分数零点和尺度可跨任务共享。

## 核心方法

1. 比较模型 reward score 与同一批人类 rating 的 prompt 间方差。
2. 用同 prompt 的 sibling responses 分离共享 prompt 成分。
3. 替换原始 prompt，测试 scorer 对错误条件的敏感性。
4. 检查去除 prompt mean 后，全局筛选 usefulness 是否下降。
5. 将可比性、条件敏感性与选择效用分开报告。

## 关键实验结果

**论文原文结论**：在 HelpSteer2 上，6 个 reward model 的 between-prompt share 为 0.34–0.64，而人类对应份额接近 0。固定指令替换仍保留明显聚类，却削弱与 prompt-level 人类评分的一致性；直接减去 prompt mean 又会降低全局筛选的 helpfulness，说明该成分并非纯噪声。

## 证据质量与局限

覆盖 18 个 scorer 和 6 个训练条件，审计设计能区分多种解释，证据较强。局限是结论依赖 HelpSteer2 等静态 response 数据与人类 rating；尚未展示长轨迹、on-policy 分布漂移或程序真值下的结果，且简单残差化并非修复方案。

## 最接近的相关工作

最接近 reward-score residualization audit、MAWILE、Robust Conformal Consensus、Who Judges Matters，以及 ordinal probabilistic reward modeling。它与 pairwise RM benchmark 的核心差异是专门审计跨 prompt 的共享分数成分。

## 如何复用或推进 LLM-as-a-Verifier

将 verifier 输出分解为 prompt/任务基线、response 增量和不确定性；pairwise 训练负责局部次序，少量锚定样本或环境真值负责跨任务校准。不要把未经校准的 raw score 直接用于跨任务采样、课程排序或早停。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

- **score-level OPD**：在不同 Agent 任务间比较 teacher score 前，先做任务条件校准并报告原始/校准双轨结果。
- **A/B/T 与序数分布**：A/B 只约束同状态候选次序；T 与序数强度需由锚点把局部尺度连接起来。
- **硬真值门控**：用程序或环境成功率提供跨 prompt 的共同标尺，避免 reward baseline 决定更新强度。
- **critique states**：比较 critique 前后的增量，而非绝对分数；同时测试换 prompt 后增量是否仍成立。
- **高熵探索**：禁止按跨任务 raw score 直接淘汰分支，防止高 baseline 任务占用预算。
- **sealed eval**：独立报告同 prompt 排序、跨 prompt 校准和全局选择效用，不能用单一 pairwise accuracy 代替。
