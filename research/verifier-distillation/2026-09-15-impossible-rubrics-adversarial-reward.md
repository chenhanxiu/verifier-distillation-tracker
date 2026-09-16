# ImpossibleRubrics: Stress-Testing Generated Rubrics as Reward Signals

## 基本信息
- **作者**：Bowen Qin；Yi Xie；Yesheng Liu；Xi Yang
- **首次公开日期**：2026-09-15
- **版本日期**：2026-09-15（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2609.16816
- **代码**：未发现公开代码链接

## 一句话结论
【论文原文】自动生成的 task-specific rubric 常会泄露“该编造什么”，在可验证的不可能任务上，11 个生成器的 rubric 有 8%–26% 被利用；certificate-faithful rubric 的被利用率为 0%。

## 真正新增的内容
【论文原文】ImpossibleRubrics 不发布固定 rubric，而发布 169 个不可能任务、六类不可能性和可验证 oracle certificate，允许任意下游系统生成 rubric 后接受对抗测试；另含 48 个可回答对照。研究隔离了“任务困难”与“rubric 奖励错误主张”两种因素。

【分析推断】这直接说明 generative verifier/rubric 不能只在自然回答上测一致率，必须在被优化策略主动利用时测 soundness。

## 核心方法
1. 构造唯一诚实行为是承认不可完成的任务环境。
2. oracle certificate 明确允许与禁止的主张。
3. 多种 LLM 逐任务生成 rubric。
4. 对抗回答针对 rubric 优化，再用 certificate 检查违规。
5. 以可回答任务控制区分过度拒绝与真实稳健性。

## 关键实验结果
【论文原文】在无偏的 150/169 环境切片上，11 个生成器的 rubric 被利用率为 8%–26%；压力切片上最强生成器仍有 36%，certificate-faithful rubric 为 0%。统一的“果断、惩罚犹豫”通用 rubric 被利用率 64%，而 11 个逐题 rubric 生成器中有 7 个更差。

## 证据质量与局限
- oracle certificate 提供强硬真值，且有 answerable controls，证据设计扎实。
- 任务集中于不可能性，不代表普通开放任务上的总体 rubric 质量。
- certificate 本身的覆盖与正确性仍需人工/程序审计；对抗强度决定测得上限。

## 最接近的相关工作
ExecRubrics、AutoSciRub、LLM Judge 遗漏盲区、Cheap Verifiers Large Blind Spots、Proof-Carrying Cognition 和 RecurSE。本文区别是把生成 rubric 当作可被策略攻击的 reward program，并用证书测其 soundness。

## 如何复用或推进 LLM-as-a-Verifier
【分析推断】每条 rubric 同时生成 obligation、禁止主张、可验证证据源和 abstain 条件；训练前先跑 adversarial candidate generation，只有在 certificate 下保持 sound 的 rubric 才可作为 reward teacher。

## 对 Agent verifier × OPD 实验路线的具体影响
【分析推断】
- score-level OPD：rubric 分数不能直接定方向，先经程序/环境 certificate 验证。
- A/B/T：诚实拒绝 vs 伪造完成应为强 A/B；证据不足的两个候选标 Tie/Indeterminate。
- 环境真值：前置条件、权限和资源不存在要形成机器可检 certificate。
- critique states：禁止将“看起来具体”的不可证 critique 写入训练记忆。
- 探索：不可完成不等于立即停止；先保留澄清、替代方案和安全拒绝分支。
- sealed eval：用未公开 certificate 和优化后的 adversarial Agent 检验 rubric，而非只测静态人工答案。