# Parsing the Stream：长时程 Agent 的可审计 Live Trace Model

## 基本信息

- **论文标题**：Parsing the Stream: A Live Trace Model for Long-Horizon Agents and Their Observers
- **作者**：Egor Pakhomov, Erik Nijkamp
- **首次公开日期**：2026-09-01
- **当前版本日期**：2026-09-01（v1）
- **arXiv**：[2609.01466](https://arxiv.org/abs/2609.01466)
- **DOI**：[10.48550/arXiv.2609.01466](https://doi.org/10.48550/arXiv.2609.01466)（DataCite 注册待完成）
- **代码/基准/轨迹**：[SalesforceAIResearch/tracelab](https://github.com/SalesforceAIResearch/tracelab)

## 一句话结论

论文用 append-only 事件账本和确定性 fold 把长轨迹压成类型化状态，在显著降 token/成本的同时保留可审计真值；这可作为 verifier 输入层，但作者也实证说明它不是对所有顺序敏感任务都有效。

## 真正新增的内容

**论文原文结论**：同一份追加式事件账本被增量折叠成 typed run state，再编译为面向 Agent 和人类 observer 的不同视图；所有评测对照确定性真值。其相对 prompt scratchpad 的剩余价值主要是确定性、可审计性以及由同一状态服务多个观察者，而非普遍更高的准确率。

真正新意是把“轨迹摘要”从自由文本生成改为可重放状态变换，并主动给出失效边界：对顺序敏感且无法由当前聚合表示覆盖的任务，fold 不再帮助。

## 核心方法

原始事件保持不可变；fold 将事件逐步投影到显式 schema 中，视图编译器为监控问答或 agent 上下文选择所需字段。测试包含 observer 对运行状态的查询，以及需要维护运行统计量的 120-link 顺序依赖任务；同时比较 raw trace、预算限制阅读、scratchpad 和不同状态分解。

## 关键实验结果

**论文报告**：observer 代理 LLM 在 compiled view 上准确率 0.85–0.87，raw trace 为 0.48；输入 token 减少约 14–15 倍、成本降低 5–7 倍。120-link 任务中，维护每步运行统计的状态机制为 30/30，full-context 为 8/30；但 prompt scratchpad 以更低成本达到相同准确率。作者明确指出问题与 schema 共同设计，因此可迁移结论仅是“schema 覆盖成立时”的 token/成本收益；30 次结果也标为描述性。

## 证据质量与局限

证据透明，公开代码、基准、可重生成语料和所有轨迹，并使用确定性真值。主要局限是合成任务及系统—基准共设计，observer 用 LLM proxy，不代表真实人类监控效果。schema 漏项会导致“压缩后自信遗漏”，且固定 fold 无法自然表达多义、延迟因果和未知依赖。

## 最接近的相关工作

接近 SPARE 的长上下文裁剪、MemGuard 的 verifier 元数据、LongRCA/AgenticRAG-FP 的轨迹归因、事件溯源系统和状态机式 Agent memory。区别在于此工作强调共享、确定性和可审计的在线状态，而非直接学习压缩器或奖励模型。

## 如何复用或推进 LLM-as-a-Verifier

**分析推断**：把 ledger 作为不可变证据层，fold state 作为低成本 verifier 输入，原始轨迹仅在高不确定或争议时回查。每个序数分数应携带支持它的事件 ID、覆盖率与“未知”质量；generative verifier 生成 critique 时引用具体事件，评分头则输出 A/B/T 或等级分布。若不同 fold 视图给出冲突，应升级到原始事件或独立 verifier。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：teacher 可看全 ledger，student 只看 fold view；蒸馏前以可回答覆盖率门控，避免把遗漏压成确定分数。
- **A/B/T/序数**：同一轨迹在多种 view 下评分；分歧或证据缺失标 T/unknown，而非强行排序。
- **真值门控**：所有工具结果、状态转移和终态保留事件 ID，由程序 fold/checker 提供硬事实。
- **critique states**：student critique 追加到 ledger，但不得改写原事件；后续执行验证 critique 的因果价值。
- **探索**：高熵分叉分别维护状态，直到共享事实足以合并；不可因摘要相似过早丢弃分支。
- **sealed eval**：评测采用未见 schema 项、顺序敏感任务和原始轨迹抽查，测量压缩覆盖盲区。