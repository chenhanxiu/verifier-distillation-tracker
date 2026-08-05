# On-Policy Distillation of Language Models: Learning from Self-Generated Mistakes

> 来源：历史研究计划 OPD 基线（2026-07-27 整理）

## 论文信息

- **标题**：On-Policy Distillation of Language Models: Learning from Self-Generated Mistakes
- **作者**：Rishabh Agarwal, Nino Vieillard, Yongchao Zhou, Piotr Stanczyk, Sabela Ramos, Matthieu Geist, Olivier Bachem
- **首次公开/版本**：2023-06-23（v3：2024-01-17；ICLR 2024）
- **arXiv**：[2306.13649](https://arxiv.org/abs/2306.13649)
- **HTML 全文**：[arxiv.org/html/2306.13649](https://arxiv.org/html/2306.13649)

## 一句话结论

GKD 奠定了“student 在自己访问的状态上接受 teacher dense feedback”的标准 OPD 范式。

## 真正新增的内容与核心方法

不再只训练固定 teacher outputs，而是让 student 采样自身序列，再由 teacher 对这些状态给出分布监督；框架允许不同散度，并可与 RLHF 联合。

## 关键实验、证据质量与局限

覆盖摘要、翻译、算术推理和通用 instruction tuning，已被 ICLR 2024 接收。它证明了 on-policy 能缓解 exposure bias，但没有 verifier 门控、序数 score space 或 Agent 长轨迹信用分配。

## 与 LLM-as-a-Verifier 及 Agent verifier × OPD 的关系

这是必须保留的 vanilla OPD baseline。目标方案应只改变监督空间和门控：token KL、score-distribution KL、score OPD + verifier/env gating 三层递进，确保增益不是简单来自更多 on-policy 数据。

## 建议定位

这篇论文应作为当前研究路线的历史基线或邻近工作保存。以上“论文方法/结果”与“对现有方案的迁移判断”已分开表述；迁移建议属于研究分析，不代表原论文已在长时程 Agent verifier 场景完成验证。
