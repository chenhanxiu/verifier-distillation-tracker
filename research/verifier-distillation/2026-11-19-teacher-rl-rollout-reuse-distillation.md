# Don't Discard Your Rollouts: Reusing Teacher RL Traces for Student Distillation

- **作者**：Vashisth Tiwari、Emma Strubell、J. Zico Kolter
- **首次公开日期**：2026-11-19
- **当前版本日期**：2026-11-19（v1）
- **原始论文**：https://arxiv.org/abs/2611.26803
- **代码**：截至本记录未发现作者公开代码链接
- **标识符**：arXiv:2611.26803；DOI: 10.48550/arXiv.2611.26803

## 一句话结论

已保存的 teacher GRPO/PPO 轨迹及奖励元数据可以通过“易题 SFT 热身 + 混合成功题 DPO + teacher 似然筛选”接近重新生成数据的经典蒸馏效果，提示 verifier × OPD 应把 rollout 元数据视为可复用课程而非一次性副产物。

## 真正新增的内容

**论文原文**：作者首次系统研究直接复用 teacher RL 训练日志做 student distillation；证明朴素 SFT 不够、朴素 DPO 对弱 student 会崩溃，并用已有 prompt pass rate 与 teacher log-likelihood 组织两阶段课程，无需额外推理构造数据。

**分析推断**：真正有价值的是把 reward、难度与 teacher 兼容性分开使用：reward 决定成功结构，pass rate 决定课程顺序，teacher 似然避免把 student 推向其无法吸收的轨迹。

## 核心方法

- 从 teacher RL 日志保留每题多条 completion、奖励、prompt pass rate 和 teacher log-likelihood。
- 先在最容易、成功率高的题上做 SFT warm start。
- 再在有成功/失败混合的题上构造 DPO 偏好。
- 用 teacher log-likelihood 选择更适合 student 的 completion，减少能力跨度导致的训练不稳。

## 关键实验结果

**论文原文**：在数学推理和 Python 编码任务、多个模型家族的 student 上，两阶段方案平均表现与经典蒸馏相当，同时数据构造不需要新增推理成本。朴素 SFT 明显落后，朴素 DPO 虽可能较强但在较弱 student 上出现坍塌。

## 证据质量与局限

论文被 NeurIPS 2026 接收，比较了多模型家族和两类可验证任务，证据覆盖优于单一模型实验。摘要未给出逐基准完整数值；方法是离线复用 teacher 轨迹，不是严格的 student-on-policy OPD，也未覆盖长时程工具环境、序数 reward 或 evaluator 共适应。

## 最接近的相关工作

最接近经典知识蒸馏、rejection sampling、DPO、GRPO 日志复用、MRPD 的 expert-log curriculum 与 AutoMaster 的 teacher 轨迹改进。与 OPD 的区别是轨迹来自 teacher 训练历史而非当前 student。

## 如何复用或推进 LLM-as-a-Verifier

**分析推断**：为每条历史轨迹保留 outcome、逐步 verifier 分布、teacher 似然、环境证书和采样策略版本；训练轻量 verifier 时先从高证据、低难度轨迹校准，再进入混合成功的 A/B/T 对。teacher 似然只能作为吸收难度代理，不能替代真值。

## 对 Agent verifier × OPD 路线的具体影响

**分析推断**：

- **score-level OPD**：把历史 rollout 的 score 分布用于 verifier warm start，再切到 student 新轨迹做 on-policy 校正。
- **A/B/T 与序数分布**：优先从同题混合成功组构造 A/B；环境证据不足或 reward 并列时保留 T。
- **真值门控**：奖励元数据必须由环境证书复核，避免把 teacher RL 的 reward hacking 继承给 student。
- **critique states**：只复用能指向具体失败步骤、且可由执行结果验证的 critique。
- **探索**：不要只保留最高 reward 轨迹；保留高熵题的多个成功模式和有诊断价值的失败分支。
- **sealed eval**：历史 reward 只能用于训练，最终比较必须用独立冻结任务与 verifier。