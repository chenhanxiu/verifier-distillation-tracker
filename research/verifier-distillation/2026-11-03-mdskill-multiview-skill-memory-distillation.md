# MDSKILL：通过多视图蒸馏内化技能记忆

## 基本信息

- **作者**：Dian Jin, Jinluan Yang, Kairong Han, Baohong Li, Zijing Hu, Yi He, Wenlin Zhong, Yunze Tong, Minqin Zhu, Linchuan Li, Yanan Niu, Kun Kuang
- **首次公开日期**：2026-11-03
- **版本日期**：2026-11-03（v1）
- **原始论文**：https://arxiv.org/abs/2611.05313
- **DOI**：https://doi.org/10.48550/arXiv.2611.05313
- **代码**：https://anonymous.4open.science/r/MDSKILL-CF53

## 一句话结论

MDSKILL 将自生成技能记忆按状态落地、动作规划和执行控制拆成三种功能视图，筛选后用 OPSD 内化到共享策略，在不依赖更强外部 teacher 的情况下提升长时程 Agent 表现。

## 真正新增的内容

**论文原文结论**：直接蒸馏 self-generated memory 会受噪声、冗余、冲突与功能纠缠影响；多视图组织和动态质量筛选能更有效地把经验性知识内化。

**分析推断**：三视图结构可直接改造成 generative verifier 的 critique schema，并为 critique-state 准入提供比单一总分更可诊断的门控。

## 核心方法

- 将技能记忆分为 state grounding、action planning、execution control 三个互补视图。
- 用动态指标筛选高质量技能。
- 构造 view-specific 与 integrated reasoning branches。
- 在当前策略轨迹上通过 OPSD 将各分支的互补知识合并到同一策略。
- 不使用更强外部 teacher，也不增加额外推理计算开销。

## 关键实验结果

- 在 3 个 Agent 基准上与 RL、skill-augmented 和 self-distillation baselines 比较。
- 在 ALFWorld 与 WebShop 上，相对已有最佳结果最高提升分别为 **7.1%** 与 **8.1%**。
- 消融与演化分析支持多视图组织和技能筛选对知识内化的贡献。

## 证据质量与局限

优点是覆盖多个 Agent 基准、包含消融、代码可用，且不依赖强 teacher。局限是“动态质量指标”仍可能与策略共适应；摘要没有说明独立环境真值覆盖、失败记忆污染率与跨模型泛化。性能提升不能直接证明 verifier 校准更好。

## 最接近的相关工作

与 skill memory、自我演化 Agent、OPSD、经验回放和结构化 critique 蒸馏最接近。相较把整段 memory 作为提示，本工作强调功能解耦后再内化。

## 如何复用或推进 LLM-as-a-Verifier

把三视图改成 verifier 输出头：状态证据是否充分、计划是否满足约束、执行是否闭环。每个头输出 ordinal distribution 与证据指针；只有通过环境验真的视图才进入 student critique buffer，冲突视图保留为 T/高熵样本。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：比较单总分与三视图分数蒸馏，并研究 integrated branch 是否造成负迁移。
- **A/B/T/序数分布**：按视图分别产生 A/B/T，再用依赖感知聚合而非简单多数票。
- **程序真值门控**：state grounding 用环境快照，execution control 用工具/测试结果；planning 仅作为软信号。
- **critique states**：采用“视图—证据—建议动作”结构，并对写入记忆做准入和回滚。
- **高熵分叉**：冲突技能不强行合并，保留多个可成功策略。
- **sealed eval**：用从未参与技能筛选的任务与冻结 evaluator 验证是否真正内化，而非记住 benchmark 模式。
