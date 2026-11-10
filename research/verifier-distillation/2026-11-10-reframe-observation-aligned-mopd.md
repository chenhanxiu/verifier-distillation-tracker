# Reframe: Observation-Aligned Multi-Teacher On-Policy Distillation for Agentic Visual Reasoning

- **作者**：Haozhi Yuan、Handong Li、Yifan Zhang、Qianshan Wei
- **首次公开日期**：2026-11-10
- **版本日期**：2026-11-10（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.12886
- **代码**：未发现公开代码链接
- **标识符**：arXiv:2611.12886

## 一句话结论

【论文原文】Reframe 不只对齐输出分布，还把 tool-returned observation 当作对齐对象：先训练 specialist 真正依赖工具证据，再在 student 选错工具动作时修复 observation 并从修复点继续 MOPD。

## 真正新增的内容

【论文原文】视觉 Agent 的失败既可能来自忽略已返回的证据，也可能来自前一步工具动作太差、根本没有产生可供蒸馏的 observation。Reframe 将两者拆成互补阶段：Ground-Drop-GRPO 提高 observation dependence，Observation-Gated-MOPD 在 rollout 中途替换缺陷工具动作并继续蒸馏，从而把状态修复纳入 MOPD。

## 核心方法

- **GD-GRPO**：以 evidence-aware reward 训练空间/时间 specialist，并随机移除原始视觉输入，迫使模型使用工具返回的 observation。
- **OG-MOPD**：检测不充分的工具动作，用 canonical action 替换，获得修复后的 observation，再从该状态恢复 distillation。
- 两阶段均不要求任务专用 SFT cold start；第二阶段由多个 specialist teacher 提供 on-policy 指导。

## 关键实验结果

【论文原文】在 **14 个图像与视频 benchmark** 上，Reframe 超过 Mix-RL 与 vanilla MOPD；消融显示 GD-GRPO 相比 outcome-only GRPO 提高了 observation dependence 与 tool gain。公开摘要未给出统一的绝对分数或提升幅度，因此此处不推断具体增益大小。

## 证据质量与局限

【论文原文】评测范围广且包含两阶段消融，但摘要未报告方差、修复触发率和 canonical action 的构造成本。中途替换动作会形成反事实/干预后的轨迹；若训练与评估都依赖同一修复器，可能高估端到端自主能力。

【分析推断】修复 observation 很适合构造 critique state，但必须保留原始失败分支和干预 provenance，否则会把 teacher 的纠错能力误记为 student 自主能力。

## 最接近的相关工作

最接近的是 OPD-Aha 的视觉证据差分、Belief-Shift Branching、AC-OPD 的局部 teacher continuation，以及 DENSE/LLM-as-an-Improver 的“失败—修复—再验证”轨迹。Reframe 的新增点是把 canonical tool action 直接注入 rollout，随后在新 observation 上继续多教师 OPD。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】将 verifier 的输入状态拆成“原始轨迹”“修复动作”“修复后 observation”三层，并让 generative verifier 输出证据指针与干预原因。score student 同时学习原始分支的失败概率和修复分支的可恢复性分布，而不是只学习修复后的高分 verdict。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：对 observation 的质量和输出 score 分别建模，避免把坏观察下的低分归因于 reasoning。
- **A/B/T 与序数分布**：原始/修复分支构成成对样本；若修复改变了任务信息，应标记不可直接比较而非强行 A/B。
- **程序化/环境真值**：canonical action 必须通过工具 schema、权限和环境结果验证。
- **student-generated critique states**：优先从真实失败点生成，并附干预 provenance；验证通过后才进入训练。
- **高熵分叉**：保留原始分支及多个合法修复动作，防止 canonical repair 抹平探索。
- **sealed eval**：最终评测禁用训练期修复器，或单独报告“自主”和“允许修复”两条曲线。