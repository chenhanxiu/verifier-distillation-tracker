# CompassOPD：通过族内似然位移实现跨模型族 On-Policy Distillation

- **论文标题**：CompassOPD: Cross-Family On-Policy Distillation via Within-Family Likelihood Shifts
- **作者**：Naibin Gu, Qingyi Si, Chenxu Yang, Chuanyu Qin, Junhao Zhou, Peng Fu, Zheng Lin, Weiping Wang
- **首次公开日期**：2026-09-09
- **版本日期**：2026-09-09（v1）
- **原始论文**：https://arxiv.org/abs/2609.10154
- **代码**：截至本次记录未发现公开代码

## 一句话结论

跨模型族 OPD 的主要障碍不只是 tokenizer，而是绝对似然中的“族间偏置”；CompassOPD 只迁移强弱同族 teacher 的相对位移，并用冻结 student 锚定更新，在三种 student 家族上均优于普通跨族 OPD。

## 真正新增的内容

**论文原文结论**：作者把跨族 OPD 信号拆成低能力 teacher-family reference 与 student 的族间 offset，以及强 teacher 相对该 reference 的族内 log-likelihood shift；普通 OPD 同时迁移二者，offset 会掩盖能力提升对应的方向。CompassOPD 去掉 offset，仅迁移族内位移；MoE teacher 还可通过减少激活专家构造自参考。

**分析推断**：这提供了 score-level verifier distillation 的“差分 teacher”模板：不要直接对齐异构 verifier 的绝对分数，而应对齐同一 verifier 家族内从弱到强、从无工具到有工具、或从非特权到特权条件的评分变化。

## 核心方法

Student 在自身 on-policy 轨迹上采样；强 teacher 与同族低能力 reference 对齐文本单元并计算 `ΔT = log p_teacher - log p_reference`。Student 端用冻结初始策略计算 `ΔS`，最终 advantage 为 `stopgrad(ΔT - αΔS)`。其隐含目标是以 teacher 族内位移指数重加权 student reference，而非复制跨族绝对概率。

## 关键实验结果

在 Qwen3.5-35B-A3B teacher、Qwen3.5-0.8B reference 下，平均推理准确率：Granite4.1-3B 从 OPD 的 25.36 提升到 30.86（+5.50）；Qwen3-4B 从 34.94 到 37.08；OLMo-3-7B 从 32.93 到 34.74。MoE 自参考版本仍比 OPD 高 3.43 点。强弱跨族 teacher 的能力差原本为 16.7 点，但普通 OPD 后 student 仅差 0.1 点，支持 offset 掩蔽诊断。

## 证据质量与局限

证据包含多 student/teacher 家族、统一 SFT 初始化与消融，因果归因比单一性能表更强。但任务集中于数学推理，需额外弱同族 reference；没有长时程 Agent、reward model 或 sealed eval 实验，也未证明族内位移天然校准。

## 最接近的相关工作

跨 tokenizer 概率对齐、标准 OPD、RouteOPD，以及 GC-OPD/OPRD 等以相对信号修正蒸馏方向的方法最接近。区别在于 CompassOPD 明确消除 teacher-family reference 与 student 的跨族 offset。

## 如何复用或推进 LLM-as-a-Verifier

可为每个异构 verifier 配置冻结 reference，蒸馏 `强 verifier 分布 - reference 分布`；输出保留完整序数评分分布而非只取均值。对于生成式 verifier，可分别计算 critique token 或 rubric 条目的族内位移，再由硬真值决定是否接纳。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：新增“绝对分数蒸馏 vs 族内差分蒸馏”主消融。
- **A/B/T 与序数分布**：对每个候选分支蒸馏差分 logits，并保留 tie 与不确定质量。
- **真值门控**：程序/环境真值决定方向；族内位移只调强度，避免异构 teacher 的刻度偏差翻转更新。
- **critique states**：比较强弱同族 verifier 对 student critique 的增量认可，而非直接复制强模型措辞。
- **高熵探索**：仅在差分信号置信区间明确时收缩分支；reference/teacher 分歧高时保留探索。
- **sealed eval**：固定 teacher、reference、student-anchor 快照并在独立执行评测上验证，防止共同漂移制造虚假增益。
