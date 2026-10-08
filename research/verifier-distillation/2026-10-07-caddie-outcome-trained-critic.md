# Training Advisors for LLM Agents from Task Outcomes

- 作者：Sergei Polezhaev、Barys Liskavets、Ori Press、Alexander Golubev
- 首次公开日期：2026-10-07
- 版本日期：2026-10-07（v1）
- 原始论文：https://arxiv.org/abs/2610.09858
- Canonical URL：https://arxiv.org/abs/2610.09858
- 代码：未发现公开代码链接

## 一句话结论

【论文原文】Caddie 不需要步骤标签或参考 critique，只根据 Agent 接受自然语言建议后是否最终成功，用 RL 训练冻结 base model 外部的 critic；4B critic 可跨模型、跨域迁移。

## 真正新增的内容

【论文原文】把 critique 质量定义为“是否实际改善后续任务结果”，而不是与人工 critique 文本相似；Agent 在推理时还能自行决定何时请求帮助。

## 核心方法

【论文原文】保持执行 Agent/base model 冻结，critic 观察进行中的多步轨迹并生成分析与建议；用接受建议后的终局成功作为 critic RL 回报，无需 step-level annotation。

## 关键实验结果

【论文原文】在 MuSiQue 上，Qwen3-4B critic 将 Qwen3-4B 成功率提高超过 25 个百分点，并超过无 critic 的 Kimi K3；同一 critic 对三个未参与训练的模型，以及域外 τ³ 和 DeepDive 均有增益。

## 证据质量与局限

【论文原文】有跨四个 base model 和域外交互基准迁移证据。【分析推断】终局回报仍可能把帮助效果与后续随机性混在一起；未证明 critique 内容本身事实正确或能在更长工具轨迹稳定归因。

## 最接近的相关工作

【分析推断】接近 FLARE、EquiReview-R、PaperDoctor、LLM-as-an-Improver 与 outcome-supervised process verifier；本文直接以建议后的任务结果训练生成式 critic。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】可把 Caddie 作为 generative verifier teacher，再把“建议前状态—critique—建议后轨迹—环境结算”蒸馏给小 student；critique 必须经反事实无建议对照或重放减少混淆。

## 对 Agent verifier × OPD 实验路线的具体影响

- 【分析推断】score-level OPD：用 critique 后成功增量而非文本似然给权重。
- 【分析推断】A/B/T：同状态有/无建议两臂形成 A/B；不可比轨迹为 T。
- 【分析推断】真值门控：环境结算决定 critique 是否可用。
- 【分析推断】critique states：这是直接基线，但需保存证据指针和后续结果。
- 【分析推断】高熵分叉：只在 critic 预计有帮助且不确定性高时请求建议。
- 【分析推断】sealed eval：在未见模型和任务上冻结 critic，防止同循环共适应。