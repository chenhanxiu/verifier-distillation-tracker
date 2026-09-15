# Vibe Patenting: Evaluating LLM Judges for Professional Patent-Drafting Agents

## 基本信息

- **作者**：Toshiaki Koike-Akino；Vlad Blaykhman；Ye Wang；Jing Liu；Gene V. Vinokur
- **首次公开日期**：2026-09-11
- **版本日期**：2026-09-11（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2609.13422
- **代码**：未发现公开代码链接

## 一句话结论

【论文原文】独立 LLM Judge 的结构化反馈能指导专利起草 Agent 迭代改进，使低推理预算 Agent 接近昂贵模型，但与专业律师的一致性强烈依赖评价维度并存在系统性校准差异。

## 真正新增的内容

【论文原文】论文把 LLM-as-a-Judge 放进高专业度、长文档的 draft–judge–revise 闭环，并用专业专利律师做独立验证；结果同时展示 Judge 反馈的优化价值和“总体相关不等于各维度可靠”的测量风险。

【分析推断】这提供了 student-generated critique states 的真实专业场景：critique 可以提升产物，但不应因此自动成为可信训练标签。

## 核心方法

1. Agent 生成专利草稿。
2. 独立 LLM Judge 按专业维度输出结构化评价与修改建议。
3. Agent 根据反馈进行多轮修订。
4. 将 Judge 结果与专业专利律师评价比较，分析一致性与校准差异。
5. 比较不同推理预算 Agent 在 judge-guided revision 后的表现。

## 关键实验结果

【论文原文】Judge 引导的迭代能持续改善草稿；低推理预算 Agent 可接近更昂贵的高推理模型。LLM Judge 与律师具有有意义的一致性，但一致程度随指标显著变化，并出现系统性校准偏差。

【证据边界】摘要没有支持“LLM 可替代律师”的结论；这是特定专业任务上的相关与改进证据，而非法律正确性的完整 oracle。

## 证据质量与局限

- **质量**：引入真实领域专家作为外部锚点，优于仅用另一个 LLM 自证。
- **局限**：专业专家样本通常昂贵且规模有限；长文档评价可能受格式、语言流畅度和遗漏盲区影响。
- **风险**：同一 Judge 同时生成 critique 和衡量改进，会高估闭环收益；专利质量的真实结果还包含审查、权利要求范围和后续法律过程。

## 最接近的相关工作

Human-Aligned Judge for Agentic Drug Discovery、RecurSE 的独立锚定、LLM Judge 遗漏盲区、Draft-Verify-Revise 的指示语漂移，以及 UniRRM 的动态 rubric 评价。本文独特价值在于专业律师验证的长文档闭环。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】将各专业维度建模为序数概率而非总分，并用少量专家标签做分维度校准；要求 generative verifier 为 critique 引用具体权利要求和证据位置。无法覆盖的义务返回 Inconclusive，而不是给中性总分。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- score-level OPD 应按维度校准，禁止把高流畅度补偿硬性遗漏。
- 对修订前后版本构造 A/B/T；律师无显著偏好或义务覆盖相同则标 Tie。
- 可程序化检查的编号一致性、引用、依存关系先硬门控，LLM Judge 评估软质量。
- student-generated critique 只有在独立 Judge 或专家复核后才进入记忆/蒸馏池。
- 对高分歧专业维度保留多个草案分支，避免过早顺从单一 Judge 风格。
- sealed eval 使用未参与提示设计的专家、隐藏案例和冻结 Judge 快照，分别报告优化 Judge 与律师分数。