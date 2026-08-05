# Scaling Reasoning Efficiently via Relaxed On-Policy Distillation

> 来源：历史研究计划 OPD 条目（2026-07-27 整理）

## 论文信息

- **标题**：Scaling Reasoning Efficiently via Relaxed On-Policy Distillation
- **作者**：Jongwoo Ko, Sara Abdali, Young Jin Kim, Tianyi Chen, Pashmina Cameron
- **首次公开/版本**：2026-03-11
- **arXiv**：[2603.11137](https://arxiv.org/abs/2603.11137)
- **HTML 全文**：[arxiv.org/html/2603.11137](https://arxiv.org/html/2603.11137)

## 一句话结论

REOPOLD 把 teacher/student 对数似然比解释成 token reward，建立了 OPD 与 policy optimization 的明确桥梁。

## 真正新增的内容与核心方法

通过 mixture-based reward clipping、基于 entropy 的 token 动态采样，以及 exploration-to-refinement 统一训练，放松严格模仿以减少不稳定和负迁移。

## 关键实验、证据质量与局限

覆盖数学、视觉与 agentic tool-use，报告比近期 RL 高 6.7–12× 样本效率，7B 在视觉推理上匹配 32B teacher 且推理快约 3.32×。代码当时标注“即将发布”，需谨慎看待复现性与成本口径。

## 与 LLM-as-a-Verifier 及 Agent verifier × OPD 的关系

适合把 verifier dense score 转成 token/step advantage 时参考。建议用 score delta 或 progress delta 而非绝对分数，并对 clipping、entropy sampling、训练阶段切换做消融。

## 建议定位

这篇论文应作为当前研究路线的历史基线或邻近工作保存。以上“论文方法/结果”与“对现有方案的迁移判断”已分开表述；迁移建议属于研究分析，不代表原论文已在长时程 Agent verifier 场景完成验证。
