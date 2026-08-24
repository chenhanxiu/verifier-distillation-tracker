# ChatInvent Judge：经专家对齐的 Agentic 科学工作流评估系统

- **论文标题**：Designing a Robust LLM-Based Evaluation System for Agentic AI in Drug Discovery Through Human Alignment
- **作者**：Emma Granqvist，Rocío Mercado，Samuel Genheden
- **首次公开日期**：2026-08-21
- **版本日期**：2026-08-21（v1）
- **arXiv ID**：2608.21057
- **原始论文**：https://arxiv.org/abs/2608.21057
- **DOI**：https://doi.org/10.48550/arXiv.2608.21057
- **代码链接**：论文页面未提供公开代码

## 一句话结论

该工作把确定性的工具调用正确性与四维 LLM 质量 Judge 分开，并用五位领域专家校准与 few-shot 优化 Judge，为开放式工具 Agent 建立了可落地的人类对齐流程。

## 真正新增的内容

**论文原文结论**：面向 AstraZeneca 的 ChatInvent，作者定义完整性、相关性、结构清晰度与范围遵循四维软评价，同时单独检查 Tool Call Correctness；比较四类 Judge，并用专家标注 few-shot 提高与多数专家的一致率。

**分析推断**：它支持“硬工具真值 + 软序数质量”双层 verifier，而不是把工具正确性、任务贡献和语言质量塞入一个总分。对现有下一步动作评估，可把这四维改写为局部贡献维度并保留分布。

## 核心方法

五位专家为评估样本提供人类锚点，比较 Gemini 3.1 Pro、Claude Opus 4.7、GPT-5 与 Llama 3.1 70B 作为 Judge；选出表现最佳者后，以人类标注示例进行 few-shot 优化，再在 70 个 held-out 问题上应用。工具调用正确性采用确定性检查，与 LLM rubric 分离。

## 关键实验结果

**论文原文**：few-shot 人类示例将最佳 Judge 与专家多数票的一致率从 0.80 提高到 0.86。对 70 个 held-out 问题的分析显示，非正式措辞没有系统性降低输出质量；先重写用户问题再交给 Agent 可能有帮助。

## 证据质量与局限

优点是来自真实部署场景、包含五位领域专家并有 held-out 应用。局限是样本量与领域较窄，摘要未报告专家间一致性、置信区间或 sealed evaluator；few-shot 提升可能部分来自对既有 rubric/专家风格的适配，不能等同于真实科学正确性提升。

## 最接近的相关工作

最接近 ProofJudge、DashArena/DashJudge、Competence, Not Accuracy 与 Rubric Dropout。区别在于它明确把确定性工具检查和多维软 Judge 配合，并以领域专家多数票做校准。

## 如何复用或推进 LLM-as-a-Verifier

先用小规模专家锚点验证每个维度，而非只验证总分；保留各 Judge 的混淆模式和专家分歧。下一步动作可按任务推进、范围遵循、证据充分性、表达/结构和工具合法性分别评分，其中工具合法性必须由程序验证。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

- **score-level OPD**：蒸馏四维软分数与一个独立硬工具标记，避免总分掩盖关键错误。
- **pairwise A/B/T 与序数分布**：用专家分歧校准 Tie 阈值，并让每个维度输出序数概率。
- **真值门控**：Tool Call Correctness 先做硬门控，领域内容再由专家对齐 Judge 处理。
- **student-generated critique states**：student critique 可解释各维度扣分，但最终工具事实由确定性检查确认。
- **高熵探索**：多个工具合法且目标贡献相近的动作应保留 Tie，不由语言风格偏好过早排序。
- **sealed eval**：必须保留独立专家集和未进入 few-shot 的问题；最终 evaluator 不应继续使用训练时同一示例池，以防共适应。
