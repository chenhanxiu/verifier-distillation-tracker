# Mitigating Capability Degradation in LLM Self-Improvement via Representation Geometry Regularization

- **作者**：Jiaqi Tian；Ting Long
- **首次公开日期**：2026-10-09
- **版本日期**：2026-10-09（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2610.12855
- **Canonical URL**：https://arxiv.org/abs/2610.12855
- **DOI**：10.48550/arXiv.2610.12855
- **代码**：https://github.com/supermachinelearner/RGR

## 一句话结论

RGR 揭示 OPSD 总体指标上升时仍会逐步遗忘早期已答对样本，并用表征簇内紧致、簇间分离正则缓解这种“净提升掩盖局部退化”的问题。

## 真正新增的内容

【论文原文】把 OPSD 的能力退化与隐藏表征几何恶化联系起来，并提出不改变原蒸馏目标、可插接多种 OPSD 方法的几何保持正则。  
【分析推断】对 verifier 蒸馏而言，仅看平均相关率或总 reward 会掩盖旧 rubric、旧场景和少数错误类型的遗忘，应加入样本级 retention 与表示漂移审计。

## 核心方法

1. 跟踪训练阶段中“此前正确、后来错误”的样本。
2. 测量隐藏表示的簇内紧致度与簇间分离度。
3. 训练时加入 representation geometry regularization。
4. 与原 OPSD/SDPO/SRPO/RLSD 优化联合，不改其核心目标。

## 关键实验结果

【论文原文】在多种 OPSD 方法和多个数学推理 benchmark 上，RGR 普遍降低能力退化，同时保留整体能力提升；公开代码覆盖 Qwen3-1.7B/4B，以及 AIME 2024、AIME 2025、HMMT 等设置。摘要未给出统一绝对增益。

## 证据质量与局限

跨方法验证和公开代码提升了可复现性，但作者仅两人、结果集中数学推理，且表征几何与能力保持之间目前主要是关联加干预证据；尚未证明对 Agent 长轨迹、异构状态或 verifier 输出头同样有效。

## 最接近的相关工作

与 SCOPE-OPSD、Gains and Collapse in OPD、RetireOPD、Unified Per-Token OPD Gating 和 OPD 的梯度信号消失最接近。

## 如何复用或推进 LLM-as-a-Verifier

为 verifier 建立固定 retention slice：旧错误类型、稀有场景、反事实顺序、T 类和高风险动作。每个蒸馏 checkpoint 同时报告新任务增益、旧样本保持率、类别间 margin 与校准变化。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：总分之外增加 per-slice retention loss 或表示几何约束。
- **A/B/T 与序数分布**：重点检查边界样本是否从 T 被错误推向确定 verdict。
- **程序化/环境真值门控**：用固定硬真值锚点防止 representation drift 改写基本判定。
- **student-generated critique states**：新 critique 状态加入后必须回放旧状态，检测灾难性覆盖。
- **高熵分叉**：保护稀有分支的表示间隔，避免被主流成功轨迹挤压。
- **sealed eval**：冻结跨版本 retention set，并按样本迁移矩阵而非平均分验收。