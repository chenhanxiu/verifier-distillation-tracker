# VERA: Verdict-Conditioned Reliability for Adaptive LLM Judges

- 作者：Qiushui Xu、Syamil Mohd Razak、Tao Yuan、Piotr Habas
- 首次公开日期：2026-10-04
- 当前版本日期：2026-10-04（v1）
- arXiv：2610.05452
- 原始论文：https://arxiv.org/abs/2610.05452
- Canonical URL：https://doi.org/10.48550/arXiv.2610.05452
- 代码：未发现公开代码链接

## 一句话结论

【论文原文】VERA 不依赖易过度自信的输出置信度，而是在每个预测 verdict 内从隐藏表示区分正确/错误判断，并用该可靠性轴控制 Judge 的周期性适配。

## 真正新增的内容

【论文原文】可靠性估计按 verdict 条件化，避免把“更像某一类别”误当作“更可能正确”；适配循环同时包含可靠性排序纠错、reliability-residual replay 与可靠性方向周期刷新。

## 核心方法

【论文原文】从已验证反馈学习隐藏激活中的正确/错误方向；按可靠性选择新样本更新，并回放当前可靠性模型尚未解释的旧样本，以减轻遗忘和时序漂移。

## 关键实验结果

【论文原文】在 Chatbot Arena 适配后，8B/14B Judge 在四个 held-out 公共基准上均优于各自最强基线，相对提升最高 23.01%；在独立的私有时序审计任务上，重点类别 recall 相对提升最高 16.1%。

## 证据质量与局限

【论文原文】有跨公共基准和私有时序任务验证，并比较自适应基线。局限是需要模型隐藏状态，不能直接用于黑盒 Judge；可靠性轴依赖已验证反馈质量；持续刷新仍可能与被优化 Agent 共适应，且未给出长轨迹逐步证据。

## 最接近的相关工作

最接近 JEV 式低成本概率 Judge、Frozen Judges Moving Agents、Who Judges Matters，以及 representation monitor 路线。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】将 verdict-conditioned reliability 作为序数 verifier 的第二输出：同一分数等级内再预测“此判断可靠的概率”，用于路由人工/强 Judge，而非把原始 confidence 当真值。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：【分析推断】用 reliability 对 score 蒸馏加权，并对不同 verdict 分别校准。
- **A/B/T 与序数分布**：【分析推断】低可靠 A/B 判断自动转 T；保留 verdict×reliability 联合分布。
- **硬真值门控**：【分析推断】可靠性方向只能由程序/人工已验证反馈更新。
- **critique states**：【分析推断】critique 写入需同时通过内容分数和 verdict-conditioned reliability 阈值。
- **高熵探索**：【分析推断】低可靠但高分歧状态应升级复核而非剪枝。
- **sealed eval**：【分析推断】冻结一套从未参与方向刷新的 hidden-feedback 集，审计时序漂移。
