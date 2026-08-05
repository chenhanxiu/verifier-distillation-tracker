# Breaking the Tokenizer Barrier: On-Policy Distillation across Model Families

> 来源：历史研究计划 OPD 条目（2026-07-27 整理）

## 论文信息

- **标题**：Breaking the Tokenizer Barrier: On-Policy Distillation across Model Families
- **作者**：Yifan Niu, Han Xiao, Dongyi Liu, Zelong Wang, Dihong Gong, Yasheng Wang, Jia Li
- **首次公开/版本**：2026-06-08
- **arXiv**：[2606.09456](https://arxiv.org/abs/2606.09456)
- **HTML 全文**：[arxiv.org/html/2606.09456](https://arxiv.org/html/2606.09456)

## 一句话结论

该工作解决了 token-level OPD 的工程硬约束：teacher/student tokenizer 不同时如何传递高保真概率信号。

## 真正新增的内容与核心方法

提出精确 token mapping，使标准 OPD 能跨模型家族运行，而不是退回只模仿 teacher 文本的 SFT。

## 关键实验、证据质量与局限

论文在多项 benchmark 上报告跨 tokenizer OPD 比基线更算力高效。摘要层面缺少映射误差对长文本和罕见 token 的详细结论，仍需结合代码检验复杂 Agent 轨迹。

## 与 LLM-as-a-Verifier 及 Agent verifier × OPD 的关系

若 Qwen student 与 Kimi/其他 teacher tokenizer 不同，这是 token-level 路线的必要基线；但 score-level A/B/T 或序数分布天然跨 tokenizer，可能以更低工程风险达到目标，应直接比较。

## 建议定位

这篇论文应作为当前研究路线的历史基线或邻近工作保存。以上“论文方法/结果”与“对现有方案的迁移判断”已分开表述；迁移建议属于研究分析，不代表原论文已在长时程 Agent verifier 场景完成验证。
