# Arena-Hard Judge 的聚合分数稳定，不代表逐样本 Verdict 稳定

- **论文标题**：Behind Aggregate Scores: What Systematically Varying Arena-Hard's LLM Judge Reveals
- **作者**：Louise Yorke
- **首次公开日期**：2026-10-21
- **版本日期**：2026-10-21（v1）
- **原始论文**：https://arxiv.org/abs/2610.30512
- **DOI / canonical URL**：https://doi.org/10.48550/arXiv.2610.30512
- **代码与数据**：https://github.com/Yorkel/llm-judge-release

## 一句话结论

固定模型版本、温度 0 和近乎不变的 aggregate score 仍可掩盖 21.2% 的逐 prompt A/B/T 翻转，因此偏好蒸馏必须审计样本级重测一致性。

## 真正新增的内容

**论文原文结论**：作者固定 500 个 Arena-Hard v2.0 prompts 和两模型答案，系统改变 criteria、output format、task framing 的 8 种组合，并在 pinned GPT-4.1、temperature 0 下重复每种设置，将自然重测波动与指令变更效应分离。

**分析推断**：对 verifier distillation 而言，聚合 win rate 可稳定并不意味着训练标签可靠；样本级 label noise 可能在 student 更新中累积而不会反映在 benchmark 总分。

## 核心方法

1. 固定 prompt、候选答案、judge model revision、量化/解码设置。
2. 对 criteria、输出格式与任务 framing 做全因子变化。
3. 每种设置原样重跑，估计基线不稳定性。
4. 同时报告 aggregate score 变化与逐 prompt win/tie/loss agreement。
5. 将指令效应与 unchanged rerun 的自然波动比较。

## 关键实验结果

**论文原文结论**：默认设置重跑仅使 aggregate score 移动约 1 点，却让 21.2% prompts 的 win/tie/loss 变化。一个移除 reasoning 和若干指令的设置，超出自然重测波动的 prompt 变化达 28.2 个百分点，aggregate score 下降 4.09；强调 accuracy 的设置额外改变 6.7 个百分点，但 aggregate score 几乎不动。

## 证据质量与局限

实验控制严格、代码数据公开，并显式校正重复运行基线。局限是单一 judge 家族、单一 arena 数据和 500 prompts；不能推出所有 judge 都有同样翻转率，也未直接测量这些标签对 downstream policy 的影响。

## 最接近的相关工作

最接近 Black-Box Judge Measurement Instability、Who Judges Matters、Agreement Overstates Evidence、MAWILE 与 Rethinking Verbalized Confidence。它的新意在于将 prompt 级重测波动与 instruction ablation 分离。

## 如何复用或推进 LLM-as-a-Verifier

对每个候选 A/B/T 标签存储重复 judge 分布，而非单次 verdict；用重测频率构造序数概率或 Dirichlet 后验。高翻转样本用于 T/abstain、人工或环境验真，不直接形成强蒸馏梯度。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

- **score-level OPD**：teacher score 应包含重测方差，更新强度与稳定性反比。
- **A/B/T**：T 由重复 verdict 分布定义，而不是单次 judge 输出；A/B 需达到预设稳定阈值。
- **硬真值门控**：有环境真值时由真值决定方向，judge 重测仅估计幅度和解释。
- **critique states**：只接纳跨 prompt 模板与重复运行都稳定、且有证据指针的 critique。
- **高熵探索**：高翻转标签应保留候选分支，避免把 judge 随机性误当确定偏好。
- **sealed eval**：冻结 judge snapshot、prompt、解码与重复次数，同时报告 aggregate 与逐样本 agreement。
