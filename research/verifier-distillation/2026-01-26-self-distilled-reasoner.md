# Self-Distilled Reasoner: On-Policy Self-Distillation for Large Language Models

> 来源：历史研究计划 privileged/context 条目（2026-07-27 整理）

## 论文信息

- **标题**：Self-Distilled Reasoner: On-Policy Self-Distillation for Large Language Models
- **作者**：Siyan Zhao, Zhihui Xie, Mengchen Liu, Jing Huang, Guan Pang, Feiyu Chen, Aditya Grover
- **首次公开/版本**：2026-01-26（v3：2026-03-20）
- **arXiv**：[2601.18734](https://arxiv.org/abs/2601.18734)
- **HTML 全文**：[arxiv.org/html/2601.18734](https://arxiv.org/html/2601.18734)

## 一句话结论

OPSD 用同一模型的 privileged teacher 与无特权 student，降低了额外 teacher 成本。

## 真正新增的内容与核心方法

teacher 看到 verified reasoning traces，student 只看问题；两者在 student 自己的 rollout 上做逐 token 分布匹配，使模型“教会较弱上下文中的自己”。

## 关键实验、证据质量与局限

多个数学 benchmark 上比 RL 更 token-efficient，并优于 off-policy distillation，且有代码。局限是数学 gold trace 质量高，无法代表 noisy Agent critique；同模型 teacher 也可能共享盲点。

## 与 LLM-as-a-Verifier 及 Agent verifier × OPD 的关系

可把同一 verifier 在“完整证据/简化证据”下视为 teacher/student，先做低成本验证。但需要与独立强 teacher 比较，并用环境真值识别 self-distillation 的共同错误。

## 建议定位

这篇论文应作为当前研究路线的历史基线或邻近工作保存。以上“论文方法/结果”与“对现有方案的迁移判断”已分开表述；迁移建议属于研究分析，不代表原论文已在长时程 Agent verifier 场景完成验证。
