# On-Policy Delta Distillation

> 来源：历史研究计划 OPD 条目（2026-07-27 整理）

## 论文信息

- **标题**：On-Policy Delta Distillation
- **作者**：Byeongho Heo, Jaehui Hwang, Sangdoo Yun, Dongyoon Han
- **首次公开/版本**：2026-07-16
- **arXiv**：[2607.15161](https://arxiv.org/abs/2607.15161)
- **HTML 全文**：[arxiv.org/html/2607.15161](https://arxiv.org/html/2607.15161)

## 一句话结论

OPD² 不蒸馏 teacher 全分布，而蒸馏 reasoning tuning 相对 base model 的增量，减少无关底座知识的干扰。

## 真正新增的内容与核心方法

把 teacher 与其 instruction/reasoning tuning 前 base model 的分布差定义为 delta signal，只转移后训练新增能力。

## 关键实验、证据质量与局限

在数学、科学、代码推理中一致优于传统 OPD，并以较短后训练获得强表现。局限是需要可访问匹配的 teacher base，且 delta 可能同时包含任务能力、风格和安全变化。

## 与 LLM-as-a-Verifier 及 Agent verifier × OPD 的关系

对 verifier 蒸馏可定义 teacher verifier 相对 base/judge 的 score-distribution delta，或有证据/无证据提示的 delta。建议比较 full distribution 与 delta-only，并监测校准和通用判断能力是否受损。

## 建议定位

这篇论文应作为当前研究路线的历史基线或邻近工作保存。以上“论文方法/结果”与“对现有方案的迁移判断”已分开表述；迁移建议属于研究分析，不代表原论文已在长时程 Agent verifier 场景完成验证。
