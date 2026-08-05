# On-Policy Context Distillation for Language Models

> 来源：历史研究计划 privileged/context 条目（2026-07-27 整理）

## 论文信息

- **标题**：On-Policy Context Distillation for Language Models
- **作者**：Tianzhu Ye, Li Dong, Xun Wu, Shaohan Huang, Furu Wei
- **首次公开/版本**：2026-02-12（v2：2026-03-23）
- **arXiv**：[2602.12275](https://arxiv.org/abs/2602.12275)
- **HTML 全文**：[arxiv.org/html/2602.12275](https://arxiv.org/html/2602.12275)

## 一句话结论

OPCD 展示了如何把额外上下文中的知识内化到无上下文 student，同时保持 on-policy state matching。

## 真正新增的内容与核心方法

student 在自身轨迹上训练，与看到经验历史或优化 system prompt 的 context-conditioned teacher 做 reverse KL；应用包括经验知识蒸馏和 system prompt distillation。

## 关键实验、证据质量与局限

在数学、文本游戏和领域任务上优于基线，并更好保持 OOD 能力，也支持跨尺寸 teacher/student。局限是主要迁移行为知识，而非 verifier 的不确定性或客观正确性。

## 与 LLM-as-a-Verifier 及 Agent verifier × OPD 的关系

可把 privileged context 设为完整工具日志、环境状态、gold evidence 或多 verifier critique，再让部署时不可见这些信息的 student 学评分分布。必须验证 PI 是否泄漏答案或压制合理探索。

## 建议定位

这篇论文应作为当前研究路线的历史基线或邻近工作保存。以上“论文方法/结果”与“对现有方案的迁移判断”已分开表述；迁移建议属于研究分析，不代表原论文已在长时程 Agent verifier 场景完成验证。
