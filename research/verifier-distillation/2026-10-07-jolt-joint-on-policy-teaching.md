# A Good Self-Teacher Meets the Student Where They Are: Joint On-Policy Learning and Teaching

- 作者：Randy Ardywibowo、Arnav Dalal、Jiantao Jiao
- 首次公开日期：2026-10-07
- 版本日期：2026-10-07（v1）
- 原始论文：https://arxiv.org/abs/2610.10447
- Canonical URL：https://arxiv.org/abs/2610.10447
- 代码：未发现论文专属公开代码链接

## 一句话结论

【论文原文】高表现 privileged self-teacher 仍可能因使用 student 无法复现的捷径而给出有害监督；JOLT 联合训练 teacher 与 student，使 teacher 的局部蒸馏更新与 student reward gradient 对齐。

## 真正新增的内容

【论文原文】论文给出 teacher 局部 distillation update 成为 student reward gradient 正倍数的充要条件，并据此把“teacher 要强”改成“teacher 要强且适配 student 当前能力”。

## 核心方法

【论文原文】同一策略承担 privileged teacher 与 unprivileged student 两个角色；teacher 优化 outcome reward，同时以 token-level KL 向 student 正则；student 在自己的轨迹上接受密集 OPD，并可叠加 student reward。

## 关键实验结果

【论文原文】在数学、代码、工具使用和终端任务上提升训练效率与最终表现；加入 student reward 进一步增益。摘要未提供统一数值，应以各任务表格为准。

## 证据质量与局限

【论文原文】兼有理论刻画与跨四类任务实验。【分析推断】局部梯度对齐不保证长时程全局最优；同一模型双角色可能产生 evaluator 共适应，privileged 信息也可能泄露不可执行捷径。

## 最接近的相关工作

【分析推断】接近 Prep-OPD、Coupled Calibration and Learning、OPD-Aha、PACT 与 privileged-information self-distillation。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】把 verifier teacher 也训练成“适合当前 student”的教学者：终局真值保证方向，向 student 的 KL 保证可吸收性；但独立 sealed verifier 必须保留，不能让共同训练的 teacher 自证正确。

## 对 Agent verifier × OPD 实验路线的具体影响

- 【分析推断】score-level OPD：比较冻结 teacher 与 JOLT teacher 的 reward-gradient 对齐率。
- 【分析推断】A/B/T：teacher 只有在局部更新预测提升真实回报时才给 A/B，否则 T。
- 【分析推断】真值门控：privileged teacher 的方向必须被环境结算确认。
- 【分析推断】critique states：拒绝依赖 student 不可见信息的 critique。
- 【分析推断】高熵分叉：KL-to-student 防止 teacher 过度跳离可达分布。
- 【分析推断】sealed eval：使用完全独立模型与隐藏环境重评，审计 teacher–student 共适应。