# MemGuard: Persisting Verifier Signals for LLM-Agent Memory Governance

## 基本信息

- 作者：Haoyu Wang、Guangyuan Dong、He Liang、Zijing Zhang、Jiachen Luo、Chuang Liu、Chao Xue、Hao Tang
- 首次公开日期：2026-08-22
- 版本日期：2026-08-22（v1）
- arXiv：2608.21867
- 原始论文：https://arxiv.org/abs/2608.21867
- DOI：https://doi.org/10.48550/arXiv.2608.21867
- 代码：https://github.com/whyyyyy123/MemGuard

## 一句话结论

Verifier 信号不应只用于一次性筛选轨迹；将奖励、置信度、标签和不确定性作为持久元数据贯穿 Agent 记忆的准入、检索、冲突消解和归档，可稳定提升长任务成功率并减少步骤。

## 真正新增的内容

**论文原文结论：** MemGuard 把多准则 score-token verifier 输出持久绑定到每条候选记忆，并在整个生命周期复用，而不是验证后丢弃。

**分析推断：** 这提供了一个把 distributional verifier 输出转成可复用 Agent 状态的工程接口，也可作为 student-generated critique state 的可信度层。

## 核心方法

候选轨迹先经过多准则验证，生成 reward、confidence、label、uncertainty 描述符；记忆随后在 provisional、active、summary、archived 状态间迁移，检索重排、重复合并、冲突处理和预算归档都读取这些描述符。

## 关键实验结果

在 Terminal-Bench 2.0、SWE-Bench Verified、WebArena、Mind2Web，4 个 backbone、5 个随机种子和匹配运行预算下，MemGuard 在 16 个组合中均取得最佳成功指标和最低平均步骤；相对最强记忆基线 ReasoningBank，WebArena 最大提升 7.9 个成功率点，Mind2Web 提升 5.6 个 step-success-rate 点，终端与软件工程任务提升 2.4–3.5 点。

## 证据质量与局限

证据质量中高：跨四类 Agent benchmark、多个 backbone、五个种子且有 verifier-only control。局限是公开仓库只含治理核心，不含完整 benchmark harness、数据、Agent runtime 和模型客户端；摘要也未证明 verifier 元数据在分布外长期漂移下仍保持校准。

## 最接近的相关工作

最接近 ReasoningBank、经验/技能记忆、verifier-gated replay 与不确定性感知检索。相较一次性 outcome filtering，MemGuard 的差异是让 verifier 状态持续参与后续生命周期决策。

## 如何复用或推进 LLM-as-a-Verifier

可把现有五维 Agent Judge 的完整序数分布、置信度和硬门槛结果写入轨迹记录，而非只保存最终分数；后续抽样、回放和 critique 生成都以这些字段作为条件。

## 对 Agent verifier × OPD 实验路线的具体影响

- **Score-level OPD：** 训练样本可携带历史 verifier 分布与置信度，按生命周期阶段加权蒸馏。
- **A/B/T 与序数分布：** 保留完整分布比单标签更适合冲突记忆比较与不确定性传播。
- **真值门控：** 环境终态可决定准入，LLM verifier 负责软质量与冲突解释。
- **Student critique states：** critique 作为记忆条目时应继承产生它的证据与不确定性。
- **高熵探索：** 高不确定条目进入 provisional 区而非立即删除，待更多回放证据更新。
- **Sealed eval：** 评测时冻结独立 verifier 和记忆快照，避免治理策略与训练 Judge 共适应。
