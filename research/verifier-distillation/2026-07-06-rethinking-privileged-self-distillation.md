# Rethinking On-Policy Self-Distillation for Thinking Models

> 来源：历史研究计划 privileged/context 条目（2026-07-27 整理）

## 论文信息

- **标题**：Rethinking On-Policy Self-Distillation for Thinking Models
- **作者**：Simran Kaur, Narutatsu Ri, Yinghui He, Liam Fowl, Sanjeev Arora
- **首次公开/版本**：2026-07-06
- **arXiv**：[2607.05184](https://arxiv.org/abs/2607.05184)
- **HTML 全文**：[arxiv.org/html/2607.05184](https://arxiv.org/html/2607.05184)

## 一句话结论

这是一篇必须保留的反例：privileged teacher 可能在高熵自纠错分叉上压制 thinking model，导致能力下降。

## 真正新增的内容与核心方法

系统展示 privileged self-distillation/privileged OPD 对 thinking models 的负迁移，并把问题定位到高熵 fork：teacher 因看到答案而过早确定，反而惩罚 student 的 reconsideration、verification 与 backtracking token。

## 关键实验、证据质量与局限

五个 Qwen3/OLMo thinking model，在 AIME24/AIME25/HMMT25 上 avg@16 最多相对下降 17%，且长 rollout 更严重。证据直接且有诊断，但域仍以数学推理为主。

## 与 LLM-as-a-Verifier 及 Agent verifier × OPD 的关系

目标方案不能在高熵分叉无条件蒸馏 privileged verifier。建议设置 entropy-aware abstention、保留 exploration token、区分 critique 与 policy 更新，并把 fork rate、自纠错率、pass@k 纳入主指标。

## 建议定位

这篇论文应作为当前研究路线的历史基线或邻近工作保存。以上“论文方法/结果”与“对现有方案的迁移判断”已分开表述；迁移建议属于研究分析，不代表原论文已在长时程 Agent verifier 场景完成验证。
