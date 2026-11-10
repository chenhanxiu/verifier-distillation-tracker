# ECOS: Environment-Calibrated On-Policy Self-Distillation for Language Agents

- **作者**：Chenhao Zhang、Zhongan Wang、Mingxuan Li、Hehe Fan、Zheng Zhu、Ming Li
- **首次公开日期**：2026-11-10
- **版本日期**：2026-11-10（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.12232
- **代码**：未发现公开代码链接
- **标识符**：arXiv:2611.12232

## 一句话结论

【论文原文】ECOS 不再按 privileged skill 对 token 概率的影响大小盲目自蒸馏，而是用环境结果估计的 command-level advantage 决定 teacher 指导应被信任多少、哪些自写 reflection/skill 值得强化。

## 真正新增的内容

【论文原文】现有 Agent OPSD 会让同一个模型在 privileged skill 条件下充当 teacher，但错误的自写 skill 可能在后续更新中回流。ECOS 将“上下文使 teacher 改变了多少”改成“这种改变是否偏向更高环境优势的命令”，把环境结算直接接到 teacher preference 与 skill 强化上。

## 核心方法

- 在相似 observation 上比较已执行 command，估计 command-level advantage。
- 用该 advantage 缩放 teacher 对 student token/command 的偏好，而不是仅依赖 teacher–student likelihood shift。
- 对 reflection 与 skill 进行选择性强化：只有其诱导偏好更倾向高优势命令时才获得正向更新。
- 推理时移除 privileged skill，验证知识是否已进入参数而非继续依赖检索。

## 关键实验结果

【论文原文】不在推理时提供 skill，3B/7B Agent 在 seen ALFWorld 上达到 **90.5%/93.3%** macro success，在 WebShop 上达到 **75.5%/80.5%**。在 unseen ALFWorld 上，相同协议下分别超过 GRPO **11.0/7.6 个百分点**。消融中，仅监督可执行 command 而非 Actor 全部回复，使 3B WebShop 成功率从 **52.3% 提升到 75.0%**。

## 证据质量与局限

【论文原文】结果覆盖两个经典交互环境和两个模型规模，并包含关键监督粒度消融，证据与 Agent OPSD 主张直接对应。局限是环境相对封闭，command advantage 依赖“相似 observation”的可比性；摘要未给出跨 seed 方差、校准误差或长期 skill 漂移数据，也未证明对开放网页或软件工程轨迹同样有效。

## 最接近的相关工作

最接近的是 Observation-Calibrated Self-Distillation、RSIAgent/SkillAA 的验证后记忆写入，以及 OPDVR/γOPD 中“硬结果定方向、dense teacher 定幅度”的组合。ECOS 更进一步，把环境优势同时用于 teacher preference 和自生成 skill 的准入。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】可将 command-level advantage 换成 verifier 目标：对共享 observation 的候选轨迹生成 A/B/T 与序数分布，程序/环境真值决定偏好方向，generative verifier 的 critique 只提供可解释幅度。若 critique 诱导的 action 偏好与环境优势相反，则 critique 不进入 student 状态池。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：这是最直接的新基线；把每个状态的 teacher score shift 乘以环境校准 advantage。
- **A/B/T 与序数分布**：相似 observation 内做成对比较；差异低于环境噪声时标为 T，而非强制排序。
- **程序化/环境真值**：承担不可覆盖的方向门控，soft teacher 只在方向一致时贡献幅度。
- **student-generated critique states**：reflection/skill 必须通过“是否提升后续 command advantage”的延迟准入。
- **高熵分叉**：保留多个环境上近似等价的高优势命令，避免把单一 teacher 偏好当作唯一最优策略。
- **sealed eval**：冻结独立任务、环境版本和 evaluator；训练所用 advantage estimator 不参与最终评分，以检测 evaluator—policy 共适应。