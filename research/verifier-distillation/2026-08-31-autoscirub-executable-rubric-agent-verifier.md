# Learning to Evaluate Before Improving: Automatic Rubric Induction for Automatic Research Agents

## 基本信息

- **方法名**：AutoSciRub
- **作者**：Xuehai Wang, Haowei Qin, Tongxin Liu, Junkai Li, Buqiang Xu, Jintian Zhang, Yijun Chen, Zirui Xue, Shumin Deng
- **首次公开日期**：2026-08-31
- **版本日期**：2026-08-31（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2608.31076
- **DOI**：https://doi.org/10.48550/arXiv.2608.31076
- **代码**：https://github.com/zjunlp/AutoSciRub

## 一句话结论

AutoSciRub 先从模糊任务自动诱导“有证据、可执行、原子化”的 task-specific rubric，再逐项验证并修订长时程研究 Agent，是 generative verifier 构造与 critique-state 闭环的直接工程模板。

## 真正新增的内容

**论文原文结论**：面对没有明确方法和成功标准的开放研究任务，AutoSciRub 在执行前将目标分解为原子科学准则，并用文献、网页证据、任务可见数据和环境约束进行 grounding；执行后逐准则核对报告与 supporting artifacts，生成定向修订反馈。

**分析推断**：对 Agent verifier 的核心启发是“先生成评价程序，再执行任务”。相比用一个固定 Judge 直接读完整轨迹，动态 rubric 可显式暴露该任务真正需要的证据和状态变化，也更适合蒸馏成 criterion-level score distribution 与 critique state。

## 核心方法

1. 从 underspecified instruction 分解原子科学目标。
2. 检索并绑定相关文献、web evidence、任务数据与环境约束。
3. 生成具体、可行动、可验证的 task-specific rubric。
4. Agent 执行研究工作并产生报告及实验 artifacts。
5. verifier 逐项检查证据，定位未满足准则。
6. 将缺口转成 targeted critique，驱动迭代修订。

## 关键实验结果

**论文报告**：

- ResearchClawBench 全部 40 个任务上，固定 Codex harness、三种 backbone 的平均增益为 **+2.08**。
- 固定 DeepSeek-V4-Flash、比较三种 Agent harness 时平均增益为 **+2.95**。
- AstaBench E2E Discovery 随机固定的 20 任务子集上，三个 Agent harness 平均提升 **+16.8**，同时保持或增加成功完成的任务数。
- 结果覆盖固定 harness/变模型与固定模型/变 harness 两种控制方式。

## 证据质量与局限

- **证据质量：中**。有跨模型、跨 harness、两个 benchmark 的结果和开源代码，但论文明确标注为 work in progress。
- AstaBench 只评测 20 个随机样本，统计稳定性和任务选择敏感性仍需验证。
- rubric 的生成器、执行 Agent 和最终评分器可能共享模型家族或证据源，存在相关错误与共适应。
- “可执行”主要表示逐项可验证工作流，并非所有准则都由程序真值决定。
- 论文关注最终研究报告与 artifacts，未直接评估每一步动作的因果贡献。

## 最接近的相关工作

- PaperGym：从论文构造 rubric，并用 privileged OPSD + GRPO 训练。
- ExecRubrics：把 rubric 编译为可审计程序。
- G-CARL：按可验证性边界拆分硬事实奖励与动态 checklist。
- CRATE：先提取 step-level consequence evidence，再做轨迹级聚合。
- AgenticRAG-FP / Coding Agent 三层过程评估：强调证据与因果贡献不能混同。

## 如何复用或推进 LLM-as-a-Verifier

- 在评估“下一步动作”前，先基于当前用户目标、可用工具和环境状态生成原子 rubric。
- 每项 rubric 必须带：需要的证据、可观察状态、硬约束、未知项和可接受替代路径。
- verifier 输出每项的序数分布、证据引用和 critique，而不是单一总分。
- 用后续工具结果或环境重放验证 critique 是否真实提高目标推进，再将有效 critique 蒸馏给 student verifier。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：teacher 输出应从总分改为“准则 × 序数等级”的分布，student 在自身下一步动作上学习。
- **pairwise A/B/T**：以相同动态 rubric 比较动作 A/B；证据不足或互有优劣时允许 tie，不强造排序。
- **程序化真值门控**：工具 schema、权限、安全约束、状态更新等规则先作硬门槛，LLM rubric 仅评价剩余开放部分。
- **student critique states**：AutoSciRub 的“未满足准则 + supporting evidence”可直接作为 critique state；仅保留经重放证实能改善后续行为的 critique。
- **高熵分叉**：动态 rubric 应描述多个可接受路径，避免把生成器偏好的单一路线当成唯一答案。
- **sealed eval**：最终评测使用冻结 rubric、独立证据源、不同 Judge 家族与环境终态；另外报告 rubric 生成错误率，防止评价程序和 Agent 一起自洽但偏离目标。
