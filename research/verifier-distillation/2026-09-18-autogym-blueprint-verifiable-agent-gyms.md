# AutoGym：先定义解空间与 Verifier，再生成 Agent Gym

- 论文标题：AutoGym: Blueprint-First Generation of Verifiable Agent Gyms
- 作者：Aarati Andrea Noronha；Kavya Ravikumar；Carly Xiaoyu Lin
- 首次公开日期：2026-09-18
- 当前版本日期：2026-09-18（v1）
- arXiv：https://arxiv.org/abs/2609.22592
- DOI：https://doi.org/10.48550/arXiv.2609.22592
- 代码：截至 v1 未见公开代码仓库

## 一句话结论

AutoGym 先冻结有效解空间、环境要求和验证标准，再实例化任务与工具环境，并用失败轨迹主动调节课程，直接提供了“任务—环境—程序化 verifier”联合生成的工程模板。

## 真正新增的内容

- 【论文原文】将 solvability 和 verifier correctness 从生成后的筛选项前移为 blueprint 构造约束。
- 【论文原文】用显式参数控制任务拓扑、交互深度、能力轴、问题混淆和 distractor，使难度变化不只来自表述复杂化。
- 【论文原文】从历史模型失败轨迹提取薄弱能力，动态调整生成分布，形成主动课程而非静态合成集。

## 核心方法

1. 输入最小领域 seed 或旧 Agent 轨迹，先生成包含 solution space、环境状态、可执行验收条件的 blueprint。
2. 从 blueprint 物化工具、数据库、任务和隐藏 verifier，并通过迭代 repair 排除不可解或验证不一致的样本。
3. 对目标模型进行多次 rollout，按能力维分析失败，同时单独检查环境与 verifier 缺陷。
4. 成功率低于 0.30 的维度放宽、超过 0.80 的维度加强；有界更新参数以避免课程振荡。

## 关键实验结果

- 【论文原文】生产力 gym 的两种配置各生成 350 个候选，repair 后保留 297 和 280 个；更难配置使 Claude Opus 4.6 的 hard 任务占比达到 39%。
- 【论文原文】从 gpt-oss-120b 的时间推理失败生成 100 个任务，保留 92 个；其中 41.4% 对该模型为中/高难度，而 89.1% 对 Opus 4.6 为 easy。
- 【论文原文】另生成六领域 600 题，十小时内完成，repair 后保留率 86%；并在 600 题 instruction-following gym 上为 8B 模型产生了清晰 GRPO 学习信号。
- 【论文原文】时间推理 gym 的 groundedness、scalability、task realism、environment realism 分别为 93.4、97.0、98.0、96.3。

## 证据质量与局限

- 证据中等：有两个详细场景、多模型与八次 rollout、人工检查困难样本和结构化认证，但论文是 workshop 投稿，未提供公开实现。
- 论文承认生产力 gym 的 interface realism 仅 78.0，mock 工具与真实 API 有差距；distractor 的接入也可能不自然。
- 【分析推断】由同一生成管线产出 blueprint、环境和 verifier 仍可能共享规格盲区，因此不能取代独立 sealed eval。

## 最接近的相关工作

最接近 Agent World Model、ToolGate、Ground-truth-as-code Agent Evaluation、GameLogicBench、Terminal-Universe 和 Harness-of-Harness；AutoGym 的区别是把任务、环境、verifier 与能力课程放在同一个可调生成闭环中。

## 如何复用或推进 LLM-as-a-Verifier

- 先把当前 37 个子能力转为 blueprint 字段：任务义务、允许路径、状态不变量、终止条件、可恢复性和验收函数，再生成 case。
- 让 LLM Judge 只负责解释失败证据和生成 critique，程序化 verifier 对成功/失败拥有不可覆盖的否决权。
- 用已有 3,800 case 的失败轨迹反向调节生成参数，补充成功率过高或过低的能力格，而非只增加 prompt 数量。

## 对现有 Agent verifier × OPD 路线的具体影响

- 【分析推断】AutoGym 可成为 on-policy 数据生产器：从 student 失败状态生成同 blueprint 的 A/B/T 分支，以隐藏 verifier 提供方向，序数 Judge 提供幅度。
- 【分析推断】高熵分叉应保留多种符合 blueprint 的有效路径，避免 verifier 将单一参考轨迹固化成唯一正确策略。
- 【分析推断】训练时可动态生成 gym，但最终结论必须在冻结 blueprint 生成器、隐藏验收函数和未见环境的 sealed suite 上复测，防止课程生成器与 evaluator 共适应。
