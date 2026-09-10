# OnPoKD：面向低质量多模态数据的自适应 On-Policy Distillation

- **论文标题**：On-Policy Distillation for Vision-Language Model Adaptation, an Effective Paradigm on Low-Quality Multimodal Data
- **作者**：Hongyuan Zhang, Xianda Guo, Yanlun Peng, Qianlong Yang, Yubin Guo, Pinhan Fu, Mulin Chen, Xiaozhen Qiao, Ping Luo
- **首次公开日期**：2026-09-09
- **版本日期**：2026-09-09（v1）
- **原始论文**：https://arxiv.org/abs/2609.10321
- **代码**：截至本次记录未发现公开代码

## 一句话结论

OnPoKD 不把 teacher 预测视为固定真值，而让轻量 controller 根据 teacher、student 与零样本 prior 的可靠性和分歧逐样本构造受限目标，并用验证集反馈更新该决策。

## 真正新增的内容

**论文原文结论**：作者将 VLM 蒸馏目标构造表述为训练期 policy decision；controller 在 teacher、冻结零样本 prior 与 hard label 之间动态混合，并限制动作幅度，推理时完全移除。

**分析推断**：对 verifier 蒸馏最有价值的不是视觉分类本身，而是“teacher 信号也是需要被验证和路由的动作”。它可直接转成 Agent 轨迹上按状态选择 pointwise、pairwise、程序真值或拒绝监督的 gating policy。

## 核心方法

两层 MLP controller 读取 teacher/student/prior 的可靠性与分歧特征，输出有界动作，改变目标混合、样本权重和温度；controller 由 base/source validation feedback 优化，初始化为保守的 teacher-dominant 策略。Student 推理结构不变。

## 关键实验结果

11 个 base-to-novel 数据集平均 HM 从 PromptKD 的 83.73 提升到 84.62；novel 类提升 1.40 点。跨数据集平均准确率从 71.33 提升到 72.66，其中 EuroSAT +5.69、DTD +3.11，但 Caltech101、Food101、UCF101 有小幅下降。代表数据集训练时间增加 19%–25%，显存增加 51%。

## 证据质量与局限

覆盖 11 个数据集、跨域迁移和多项消融，且无推理开销，证据中等偏强。局限是任务仍为分类而非生成式或长时程 Agent；controller 依赖验证反馈和 hard label，可能把 validation 选择偏差带入闭环；收益均值不大且部分目标域退化。

## 最接近的相关工作

PromptKD、自适应知识蒸馏、teacher reliability weighting，以及 reward-gated OPD（如 OPDVR、RA-OPD、SAGE）最接近。OnPoKD 的差异是把目标构造本身作为可学习且有界的策略。

## 如何复用或推进 LLM-as-a-Verifier

将 controller 输出扩展为：调用哪个 verifier、使用何种协议（score/A-B-T/critique）、是否以硬真值否决、以及蒸馏温度。输入包含 student entropy、不同 verifier 的分布差异、执行结果与历史校准误差；动作必须有界并允许 abstain。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：比较固定 teacher score 与验证反馈驱动的逐状态混合。
- **A/B/T 与序数分布**：controller 选择 pointwise、pairwise 或 tie，不把所有状态压成同一种标签。
- **真值门控**：环境真值拥有不可覆盖的方向权；软 teacher/prior 只影响幅度。
- **critique states**：把 student critique 的证据覆盖、teacher 分歧作为 controller 特征。
- **高熵探索**：高熵且 teacher 不可靠时降低蒸馏权重或 abstain，而非强行收缩。
- **sealed eval**：controller 的训练 validation 与独立 sealed eval 必须隔离，并报告每个域的负迁移而非只报平均值。
