# G-CARL: Grounded Checklist-Aligned Reward Learning for Patient-Oriented Medical Report Interpretation

## 基本信息

- **作者**：Shiao Xie、Siyu Chen、Jianwei Lv、Bo Yuan、Yujin Wang、Xiandong Li
- **首次公开日期**：2026-08-20
- **版本日期**：2026-08-20（v1）
- **arXiv ID**：2608.20331
- **DOI**：10.48550/arXiv.2608.20331
- **原始论文**：https://arxiv.org/abs/2608.20331
- **代码**：截至该版本未发现公开代码

## 一句话结论

开放式回答中的不同目标应按可验证性边界分配 verifier：外部可核验的事实用检索证据逐 claim 检查，主观且实例相关的需求覆盖用动态加权 checklist 评分，而不是交给一个整体 LLM Judge。

## 真正新增的内容

**论文原文结论**：G-CARL 将患者导向医疗报告解释拆为 claim-level factuality、case-specific checklist coverage 和格式三类奖励，并用 GRPO 联合优化；事实分支检索报告及多源医疗知识，checklist 分支由 MLLM 生成后经临床专家规则细化。

**分析推断**：其最可复用贡献不是医疗模型本身，而是“按可验证性边界选择 verifier”的 reward architecture：Agent 轨迹中的工具/状态事实、用户需求满足和表达质量不应共享一个整体标量。它是 reward-guided RL，不是直接的 reward model distillation，但可作为 teacher reward 分解模板。

## 核心方法

1. 将模型回答分解为原子医疗 claim。
2. 从上传报告和多源医疗数据库检索证据，分别判断 claim 与报告是否相关、是否被外部证据支持，得到细粒度 factuality reward。
3. 针对每个病例、问题和对话历史生成动态 checklist，并为条目赋权；经临床规则修订后计算覆盖奖励。
4. 加入格式奖励，以 0.4/0.3/0.3 权重组合 factuality/checklist/format，并用 GRPO 对每个输入的 8 个 rollout 更新策略。
5. verifier 使用 Qwen3.5-35B-A3B；最终还通过临床专家盲评和非专业用户可理解性评价验证。

## 关键实验结果

**论文原文结果**：

- MMedReport 含 2,450 个经质量控制、去标识和人工核验的真实咨询实例。
- Qwen3-VL-8B 上，相比 MLLM-as-a-Judge reward，G-CARL 的综合指标由 1.670 提高到 1.739，claim precision 由 93.72 提高到 95.42，checklist recall 由 58.06 提高到 64.57。
- 奖励消融中，完整三奖励组合达到 Overall 1.829、Accuracy 1.141、Precision 96.62、Recall 72.18；去掉检索或改用静态 rubric 均退化。
- 与 DPO、PROMETHEUS、RAR、MedRepBench、CapRL、FactScore 比较，G-CARL 的 Overall 1.829 为最高。
- 250 个 held-out 病例的盲评中，临床专家在医疗准确性和需求满足上分别以 136:85、106:64 的票差偏好 G-CARL；50 名非医疗参与者也给出更高可理解性评价。

## 证据质量与局限

- **证据质量：中高（域内）。** 有多 backbone、3 个随机种子、奖励消融、跨数据集迁移、临床专家盲评和用户研究。
- 医疗域高风险且高度专门化，不能直接外推到通用 Agent 轨迹；retrieval 质量和医疗知识库覆盖决定 factuality verifier 上限。
- checklist 由 MLLM 生成并经规则细化，仍可能遗漏真实用户目标；训练 verifier 与评价模型之间的相关性需进一步审计。
- 训练与评估的部分指标来自相近的结构化奖励设计，可能高估泛化；独立临床评价缓解但未完全消除共适应。
- 未报告将 35B verifier 蒸馏为小型 verifier 后的校准保持情况，也未处理长时程状态转移。

## 最接近的相关工作

最接近 Rubrics as Rewards、FactScore/VeriScore、PROMETHEUS、CapRL、MedRepBench 与多目标 GRPO。区别在于显式区分外部可核验 claim 和仅能通过实例 checklist 判断的需求满足，而不是用一个 holistic Judge 同时承担全部目标。

## 如何复用或推进 LLM-as-a-Verifier

- 对 Agent 轨迹先做 verifier 路由：工具参数、数据库状态和副作用走程序化/检索核验；意图满足和沟通质量走实例 checklist。
- 将每个 checklist 条目输出为 Bernoulli/序数概率并校准，而不是只返回加权总分。
- 用独立人工审计检查动态 checklist 是否遗漏目标，并将遗漏类型反馈给 checklist generator，而非直接奖励策略。
- 将大型 evidence-grounded verifier 的 claim/checklist 分布蒸馏到轻量模型，保留分项置信度和证据引用。

## 对 Agent verifier × OPD 路线的具体影响

**分析推断**：

- **score-level OPD**：teacher 提供分项 reward vector，student verifier 分别蒸馏 factual state、goal coverage 和 response quality，最后再按任务动态组合。
- **A/B/T 与序数分布**：同状态两条轨迹可按每个 checklist 条目比较；当证据不足或差异小则输出 T，而不是强迫 A/B。
- **程序化/环境真值门控**：可执行状态和检索证据优先决定事实维度，LLM Judge 不得覆盖硬真值。
- **student-generated critique states**：学生先将轨迹拆成原子 claim/需求条目，teacher 只验证这些结构化 critique。
- **高熵探索**：事实错误应强门控；主观 checklist 高不确定项只做软奖励，避免压掉多样但合理的解决路线。
- **sealed eval**：最终评估应使用独立知识源、隐藏 checklist、不同 Judge 与人工审计，避免 reward generator、policy 和 evaluator 共享偏差。