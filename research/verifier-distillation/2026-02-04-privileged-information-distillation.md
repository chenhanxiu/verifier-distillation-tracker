# Privileged Information Distillation for Language Models

> 来源：历史研究计划 privileged/context 条目（2026-07-27 整理）

## 论文信息

- **标题**：Privileged Information Distillation for Language Models
- **作者**：Emiliano Penaloza, Dheeraj Vattikonda, Nicolas Gontier, Alexandre Lacoste, Laurent Charlin, Massimo Caccia
- **首次公开/版本**：2026-02-04（v3：2026-02-16）
- **arXiv**：[2602.04942](https://arxiv.org/abs/2602.04942)
- **HTML 全文**：[arxiv.org/html/2602.04942](https://arxiv.org/html/2602.04942)

## 一句话结论

这是与长时程 Agent 最直接的 privileged distillation 工作之一：只有 action trajectory 可见时仍能转移 PI-conditioned 能力。

## 真正新增的内容与核心方法

π-Distill 联合训练 PI-conditioned teacher 与无条件 student；另给出 OPSD，用 reverse-KL penalty 把 student 拉向 PI teacher，专门面向隐藏 CoT、只暴露动作轨迹的多轮环境。

## 关键实验、证据质量与局限

跨多个 agentic benchmark、模型和 PI 类型，π-Distill 及部分场景下 OPSD 优于依赖完整 CoT 的 SFT+RL。证据相关性高；但训练 teacher/student 的耦合可能造成 evaluator 共适应。

## 与 LLM-as-a-Verifier 及 Agent verifier × OPD 的关系

可将 PI 设为工具执行真值、完整页面状态、错误定位和 rubric；部署 student 只看可用轨迹。建议保留独立 sealed verifier，比较 joint π-Distill 与 frozen-teacher score OPD。

## 建议定位

这篇论文应作为当前研究路线的历史基线或邻近工作保存。以上“论文方法/结果”与“对现有方案的迁移判断”已分开表述；迁移建议属于研究分析，不代表原论文已在长时程 Agent verifier 场景完成验证。
