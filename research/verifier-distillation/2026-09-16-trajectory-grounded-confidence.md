# The Mirage of Calibrated Confidence：轨迹无关的口头置信度

## 元数据

- **论文标题**：The Mirage of Calibrated Confidence: Trajectory-Independence of Verbalized Confidence in Vision-Language Models
- **作者**：Jisoo Yang、Jaeho Han、Trung X. Pham、Junyeong Kim
- **首次公开日期**：2026-09-16
- **版本日期**：2026-09-16（v1）
- **原始论文**：https://arxiv.org/abs/2609.18453
- **代码链接**：未发现公开代码链接
- **状态**：EMNLP 2026 Main

## 一句话结论

仅校准“答案是否正确”的置信度不足以得到可靠的 distributional verifier；必须额外检查置信度是否真正依赖轨迹内容，并用受控好/坏轨迹对做 sealed calibration。

## 真正新增的内容

**论文原文结论**：作者提出 Trajectory-Grounding Score（TGS），区分 TGS-self（有无自身轨迹时置信度变化）与 TGS-pair（正确轨迹是否比受控错误轨迹得到更高置信度），并构建覆盖 10 个基准的 TGS-Bench。传统 ECE/AUROC 排名与轨迹 grounding 排名可能明显分离，已有校准训练甚至会加剧脱钩。

**分析推断**：这不是新的 OPD 损失，但给 score-level verifier distillation 增加了关键验收条件：学生复现 teacher 的分数分布之前，应证明该分布对轨迹证据敏感，而非只复现答案先验或语言化自信风格。

## 核心方法

- 对轨迹内容做受控变化、token masking，并利用模型自身的犹豫标记检查置信度响应。
- TGS-self 比较同一问题在提供/移除模型自身轨迹时的置信度。
- TGS-pair 在视觉、推理、答案三个轴上构造好/坏轨迹对，检查正确轨迹是否得到更高置信度。
- 将轨迹 grounding 与常规 ECE、AUROC 分开评价。

## 关键实验结果

**论文报告**：TGS-Bench 覆盖 10 个基准；多个 VLM 的口头置信度对实际推理轨迹内容不够敏感，常规校准排序与 TGS 排序不一致。论文摘要未给出统一的数值提升幅度，因此此处不外推具体增益。

## 证据质量与局限

- 优点：受控好/坏轨迹对比比只看最终正确率更接近因果诊断；跨 10 个基准；论文已被 EMNLP 2026 Main 接收。
- 局限：研究对象是 VLM，尚未直接验证工具型长时程 Agent；口头置信度不是完整的序数概率模型；受控扰动的生态有效性仍需在真实 agent trace 上复核。

## 最接近的相关工作

最接近本仓库中的 Rethinking Verbalized Confidence、RoboRMBench、Robust Conformal Consensus，以及以反事实轨迹衡量步骤贡献的 Legibility is Not Interpretability。区别在于本文把“置信度是否由轨迹驱动”本身定义为独立测量轴。

## 如何复用或推进 LLM-as-a-Verifier

可在每个高熵分叉构造 A/B/T：A 为真实成功分支，B 为受控错误分支，T 为证据不足或不可区分；除序数分数外，同时蒸馏 score distribution 对轨迹替换的响应。将 TGS 作为 verifier 训练后的必要校验，而不是优化目标本身。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：增加 trajectory-sensitivity 正则或反事实一致性测试，避免只蒸馏答案先验。
- **pairwise A/B/T 与序数分布**：用 TGS-pair 生成成对监督；当置信区间重叠时标 T，而非强制排序。
- **程序化/环境真值门控**：好/坏轨迹必须由可执行结果或环境重放确认。
- **student-generated critique states**：检查加入 critique 前后分数变化是否与真实纠错一致。
- **高熵探索**：置信度高但 TGS 低的状态不得提前剪枝。
- **sealed eval**：保留未参与校准的轨迹扰动、模型族和任务，防止 evaluator 学会固定扰动模板。