# Don't Just Trust Your Memory: Evidence-Linked Memory Reduces Memory-Induced Degradation in LLM Agents

- **作者**：Yukyeong Lee、Yumin Choi、Jinheon Baek、Sung Ju Hwang
- **首次公开日期**：2026-11-11
- **版本日期**：2026-11-11（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.14320
- **代码**：https://github.com/yukyeongleee/wikitrace
- **标识符**：arXiv:2611.14320

## 一句话结论

【论文原文】把轨迹压成无来源 lesson 会导致 Agent 因错误、误用或误读记忆而退化；WikiTrace 将每条 insight 链接到成败说明和原始轨迹，让 Agent 在行动前向下追溯证据。

## 真正新增的内容

【论文原文】既有 memory distillation 通常只用任务成败标记生成 lesson，部署时却不再提供生成 lesson 的轨迹。WikiTrace 把简洁 insight、为何成功/失败的摘要和原始 trace 组成可逐层展开的证据链，使 Agent 能检查而不是盲信记忆。

## 核心方法

- 为每条经验保存 concise insight。
- 链接 trajectory outcome 的解释摘要和原始完整轨迹。
- 新任务先读取全部 insight。
- 当 lesson 缺少行动细节、与其他 lesson 冲突或来自失败任务时，通过 terminal tool 沿链接下钻，补全或纠正后再行动。

## 关键实验结果

【论文原文】在五个 Agent benchmark 上，WikiTrace 一致超过既有 memory 方法和“只给相同 insight、不提供证据链”的基线，同时减少 memory-induced degradation。公开摘要未给出绝对提升、额外 token 成本或下钻频率。

## 证据质量与局限

【论文原文】同 insight 对照较好地隔离了证据链接本身的价值，且覆盖五个 benchmark。局限是证据仍来自旧轨迹，不等于当前环境真值；原始 trace 可能包含错误或隐私信息，检索成本及错误证据的传播需要单独审计。

## 最接近的相关工作

最接近 Grounding Agent Memory、RSIAgent、SkillAA、MDSKILL 与 DENSE。WikiTrace 的区别是保留可回溯的多层 provenance，而非仅在写入时给 lesson 一个分数。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】student-generated critique state 可采用同样结构：结论、证据摘要、原始轨迹指针、环境版本和适用范围。verifier student 不仅预测 critique 是否正确，还预测“是否需要下钻原始证据”的选择性分布。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：teacher score 必须链接原始证据；无法追溯的记忆降权。
- **A/B/T 与序数分布**：冲突 lesson 先标 T/待核验，比较证据后再转 A/B。
- **程序化/环境真值**：下钻后用当前环境重新验真，旧成功标签不能直接复用。
- **student-generated critique states**：使用 insight→摘要→raw trace 的三级 provenance 与延迟准入。
- **高熵分叉**：保留相互冲突但证据充分的多个 lesson，避免过早合并。
- **sealed eval**：最终任务不向 memory writer 泄露；报告有/无记忆及下钻成本。