# WISD：通过“弱化自身”构造无特权信息的 OPD 信号

## 基本信息

- **论文标题**：Weaken to Strengthen: Weakening-Induced On-Policy Self-Distillation for Large Reasoning Models
- **作者**：Yecheng Wu, Song Han, Han Cai
- **首次公开日期**：2026-10-28
- **版本日期**：2026-10-28（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2610.38681
- **DOI**：https://doi.org/10.48550/arXiv.2610.38681
- **代码**：https://github.com/jet-ai-projects/WISD （论文列出；本次检查时链接返回 404）

## 一句话结论

WISD 不再依赖答案、参考推理等 privileged context，而是用量化或剪枝制造“较弱自我”，再从原模型与弱化模型的分布差中提取 on-policy 自蒸馏方向。

## 真正新增的内容

**论文原文结论**：

1. 提出 Weakening-Induced OPD：当外部 teacher 和特权信息都不可用时，以原模型相对其弱化副本的能力差作为监督。
2. 研究两种弱化方式：低比特量化和 magnitude pruning。
3. 数学与代码推理中，量化/剪枝版本相对原模型平均提升 4.0/5.5 个百分点。

**分析推断**：

- 这提供了“行为抵消”视角：稳定能力可从原模型与受控退化模型的 logit 差中提取，类似用负孪生暴露哪些判断真正依赖关键能力。
- 对 verifier student，可构造输入/工具/记忆受损的 weak verifier；但必须证明弱化只移除能力而未引入新的系统偏差。

## 核心方法

1. 从当前模型得到量化或剪枝的 weaker counterpart。
2. 学生在自身分布下采样状态。
3. 比较原模型与弱模型的 token 分布，把相对差异作为无需参考答案的自蒸馏信号。
4. 在不同模型架构、规模、数学与代码任务上评估两类弱化方式。

## 关键实验结果

**论文报告**：

- 量化与剪枝平均提升分别为 +4.0 和 +5.5 个百分点。
- 剪枝使 Qwen3.5-4B 在 HMMT 2025 从 57.7% 提升到 70.5%，LiveCodeBench v6 从 39.1% 提升到 56.7%。
- 量化使 Qwen3.6-35B-A3B 在同两项任务从 68.5%/61.8% 提升到 74.6%/69.5%。

## 证据质量与局限

- **优点**：覆盖不同架构与规模，改进幅度较大；明确测试无 privileged information 的困难设置。
- **局限**：作者标注为 work in progress；代码链接当前不可访问，复现性暂受限。
- 弱化差分不天然等同“正确方向”：量化/剪枝可能改变校准、长度偏好和稀有 token，而不是只降低推理能力。
- 结果仍集中于可自动判分的数学/代码，尚无长时程 Agent verifier 实验。

## 最接近的相关工作

- **对比式自蒸馏（behavior cancellation）**：同样用正负模型差分分离能力与行为偏置。
- **Low-Bit OPD**：在真实量化部署路径上做 OPD，但目的不是把量化副本作为负 teacher。
- **TwinCheck / IWD**：分别用负孪生与不变性衡量判断可靠性。

## 如何复用或推进 LLM-as-a-Verifier

构造三类弱 verifier：去掉环境观察、屏蔽关键工具结果、压缩/污染记忆；让完整 verifier 与弱 verifier 对同一轨迹输出序数分布。只有差异与程序真值一致时，才把差分蒸馏给 student；若差异主要来自文风、长度或 family bias，则拒绝更新。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：增加“完整 verifier − 受控弱化 verifier”的残差分数基线。
- **pairwise A/B/T 与序数分布**：弱化前后若排序翻转但无环境证据，标 T 并保留两种分布，不把翻转自动视为监督。
- **程序化/环境真值门控**：用单元测试、状态断言或终局奖励验证弱化差分方向。
- **student-generated critique states**：让 student 生成 critique，再分别给完整/弱 verifier；只收录由关键证据支撑的差异。
- **高熵分叉与探索**：把弱化差分作为探索优先级而非硬剪枝信号。
- **sealed eval**：使用未参与弱化设计的任务与独立 oracle，审计差分是否只是量化伪影。