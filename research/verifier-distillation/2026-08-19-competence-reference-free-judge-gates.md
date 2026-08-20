# Competence, Not Accuracy：Reference-Free Judge Gate 的部署前诊断

## 基本信息

- **论文标题**：Competence, Not Accuracy: A Diagnostic for Reference-Free Judge Gates in Skill Optimization
- **作者**：Chenle Chen、Yangbo Wei、Chao Yao、Shaoqiang Lu、Junhong Qian、Chen Wu、Lei He
- **首次公开日期**：2026-08-19
- **版本日期**：2026-08-19（v1）
- **arXiv ID**：2608.18719
- **DOI**：10.48550/arXiv.2608.18719
- **论文**：https://arxiv.org/abs/2608.18719
- **代码**：截至记录时未发现公开代码链接。

## 一句话结论

在没有参考答案、rubric 或外部证据时，LLM Judge 本质上依赖自身“重解题”能力；论文给出 competence 与 judge ROC-AUC 的闭式上界，并证明 marginal AUC 会被题目难度混淆，因此 Judge 进入 skill/OPD 闭环前应先做同题正负样本的非干预 discriminability screen。

## 真正新增的内容

### 论文原文结论

作者将 reference-free Judge 建模为 latent solver：judge 先形成内部答案，再按候选与内部答案的一致性打分。对 k 选项、solver competence c，模型给出 `AUC=1/2+(ck-1)/(2(k-1))`，必要条件为 `c>1/k`。他们提出在真实优化 episode 上旁路记录 judge score，不改变接受/拒绝决定，并用 within-question AUC 去除题目难度混淆。

### 分析推断

这为 Agent verifier × OPD 提供了一个“先验证 verifier 是否有信号，再允许其参与蒸馏”的最低门槛。它不是 reward model distillation，也没有长轨迹实验；理论仅适用于缺少 rubric/外部证据的单答案任务。

## 核心方法

1. 单独测 Judge 在相同 grading context 下的 closed-book self-solve competence。
2. 在已有优化运行上非干预采集 judge scores 和事后真值。
3. 对同一问题内的正确/错误 episodes 计算 within-question ROC-AUC，避免 marginal AUC 把难题/易题差异当判别能力。
4. 用闭式 competence bound 预判 Judge 的理论可用区间；未过筛时禁止作为 gate。
5. 再用小规模 closed-loop 实验检查预测的 false accept / false reject 类型。

## 关键实验结果

### 论文原文

- 固定 Claude Sonnet judge，覆盖 research math、factual QA、GPQA-Diamond。
- Research math：marginal AUC 0.457，within-question AUC 0.489，近随机。
- Factual QA：marginal AUC 0.855，但 within-question 降至 0.735，约 0.12 来自难度混淆。
- GPQA marginal AUC 0.735，但无同题 strata，作者明确标为可能乐观。
- 多数组合满足理论上界；Haiku/GPQA 出现一个违反项，说明简化假设并非普遍成立。

## 证据质量与局限

- **质量**：有可检验理论、非干预 probe、同题配对估计和 closed-loop 错误类型验证；主动暴露反例。
- **局限**：仅三个任务、两类 Judge；假设错误均匀分散且按内部答案一致性评分；不适用于 rubric/evidence-grounded verifier；无 Agent 轨迹与蒸馏实验；未开源；v1 预印本。
- ROC-AUC 只度量排序，不保证概率校准、序数间距或闭环安全。

## 最接近的相关工作

LLM-as-a-Judge 校准、Dawid–Skene annotator model、Rubric Dropout、Judge–policy reward hacking，以及 reference-free evaluator reliability 研究。

## 如何推进 LLM-as-a-Verifier

- 为每个 task family 单独做同题正负 episode AUC，不用全局 accuracy 代替。
- Judge 若不能独立完成或验证任务，应加入 rubric、工具输出、环境状态或程序 checker，而不是仅扩大 prompt。
- 对 A/B/T 输出，同时测 pairwise accuracy、tie calibration 与 ordinal expected calibration error。

## 对 Agent verifier × OPD 路线的具体影响

以下为**分析推断**：

- **Score-level OPD**：只有通过旁路 probe 的 Judge score 才能进入 loss；低于门槛时权重置零。
- **A/B/T**：优先收集同一 state 的 sibling actions，构成 within-state A/B/T，避免任务难度混淆。
- **真值门控**：可执行真值、状态 diff、测试结果打破 latent-solver 上界，是比纯 reference-free Judge 更可靠的 teacher 信号。
- **Critique states**：先验证 critique 是否提升 judge competence，而非只提高 judge 自信。
- **高熵探索**：低 competence Judge 容易把不同但有效路径当错，应允许 T/abstain。
- **Sealed eval**：probe 与 gate 校准集独立于 sealed eval；最终使用不同 evaluator family，并报告 judge competence、AUC、calibration 与闭环错误。