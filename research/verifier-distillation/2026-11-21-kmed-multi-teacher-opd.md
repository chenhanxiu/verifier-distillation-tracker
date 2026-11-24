# KMed-31B Technical Report

- **作者**：KMed Team at NAVER
- **首次公开日期**：2026-11-21
- **版本日期**：2026-11-21（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.28719
- **DOI**：https://doi.org/10.48550/arXiv.2611.28719
- **代码**：未见作者在 arXiv 摘要页给出独立代码链接

## 一句话结论

按“是否有唯一答案 × 可用反馈类型”训练四个 specialist，再以 Multi-teacher On-policy Delta Distillation 合并，可在提升 rubric 任务的同时维持可验证 MCQA 能力。

## 真正新增的内容

**论文原文结论**：提出 MOPD²，将四类医疗任务各自适配的 specialist 通过 on-policy delta distillation 整合进单一 31B student。  
**分析推断**：这为 heterogeneous verifier 路线提供了比统一 reward 更稳的做法：蒸馏 teacher 相对 base 的能力位移，而不是不可比的绝对分数。

## 核心方法

按输出是否唯一、反馈是否为 reference/rubric 划分任务；为每类训练 specialist，然后在 student on-policy 状态上迁移多 teacher 的 delta。另构建 Synthetic Health Dialogue 支撑临床问询。

## 关键实验结果

相对 base，HealthBench Hard/Professional 非思考模式从 22.95/37.92 提升到 41.87/50.20，思考模式从 23.80/41.97 提升到 51.48/59.18；四个医疗选择题 benchmark 维持或小幅提升。配方迁移到 Qwen3.8-27B 后两项 HealthBench 亦上升。

## 证据质量与局限

跨 base 复现实验增强可信度，但 HealthBench 含 LLM/rubric 评价，且报告主要面向医疗域；未证明多个 specialist 的错误独立，也未给独立 sealed clinical outcome。

## 最接近的相关工作

最接近 Lightning Weave 与 CompassOPD 的相对能力位移、VG-OPD 的多专家选择、Coupled Calibration and Learning 的 teacher 偏差校准。

## 如何复用或推进 LLM-as-a-Verifier

为 Agent verifier 分成：可执行终局、过程合规、证据质量、恢复性四个 specialist；各自只使用其可靠反馈训练，再蒸馏相对基线的 score delta 与 ordinal distribution。

## 对 Agent verifier × OPD 实验路线的具体影响

将 score-level OPD 从单一 teacher 改为按信号类型路由的 delta 蒸馏：程序真值 teacher 决定方向，rubric teacher 只调幅度；A/B/T 保留 specialist 分歧而不先平均。sealed eval 分别报告每类能力，避免综合分掩盖退化。