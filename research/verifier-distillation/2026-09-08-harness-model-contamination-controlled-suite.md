# Harness or Model？在污染受控私有套件中隔离 Agent Harness 效应

## 基本信息

- **论文标题**：Harness or Model? Isolating the Harness Effect in Agentic Coding with a Contamination-Controlled Private Suite
- **作者**：Mohsen Arjmandi
- **首次公开日期**：2026-09-08
- **版本日期**：2026-09-08（v1；修正早期手稿的 telemetry 成本缺陷）
- **原始论文**：https://arxiv.org/abs/2609.11987
- **DOI**：https://doi.org/10.48550/arXiv.2609.11987
- **代码**：论文称发布 orchestrator、grading oracle、重分析代码与派生聚合，但 arXiv 摘要页未给出可核验 URL

## 一句话结论

【论文原文】在同模型、配对任务和隔离 oracle 下，vendor-native harness 并无稳定平均优势；harness、任务类型、超时与计费遥测会显著改变表面结论。

## 真正新增的内容

【论文原文】用 256 个私有 repository 与 post-cutoff contest 任务控制污染，并对同一模型做 native harness 与 neutral harness 配对比较；评分由隔离 oracle 完成，将“模型能力”和“harness 效应”拆开。论文还公开更正自身 telemetry 缺陷，示范 evaluator 审计。

## 核心方法

对 Claude Opus 4.8 和 GPT-5.5 各取 80 个共享任务，在 native SDK 与 deepagents 下运行；另设 Gemini、DeepSeek side cells。计划 800 次，完成评分 792 次；用 task bootstrap 置信区间、分层对照、冻结价格重算成本。

## 关键实验结果

【论文原文】Opus native 相对 neutral 为 -1.25pp（48.8% vs 50.0%，95% CI [-10.0,+7.5]）；GPT native 为 +1.25pp（55.6% vs 54.4%，CI [-4.4,+6.9]），均未解析出平均优势。Opus 在 61 个 repo 任务落后 9.0pp，却在 19 个 contest 任务领先 23.7pp；该分层为事后选择。81 个超时取消运行中 22 个已产生 passing patch。成本排序受 58 个缺失 usage 记录影响而未定。

## 证据质量与局限

【论文原文】优势是私有、post-cutoff 任务、同模型配对、隔离 oracle 与置信区间。局限包括单作者、任务私有、若干运行缺失、事后分层以及成本 telemetry 不完整；不能据此断言所有 harness 等价。

## 最接近的相关工作

Harness-of-Harness、EvoHarnessBench、Cheap Verifiers Large Blind Spots、Black-Box Judge 测量不稳定性，以及 contamination-controlled coding-agent evaluation。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】Verifier 训练与评测应把 harness 版本、parser、工具 schema、超时策略视为显式协变量。可为同一轨迹保留“动作语义评分”和“harness 执行结果”两层标签，并用隔离 oracle 给出不可覆盖的真值门控。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】所有 OPD A/B/T 比较应采用同模型、同任务、harness 交叉配对；score-level 蒸馏不能把 harness 失败当成策略失败。高熵分叉要记录取消但已成功的分支；sealed eval 应冻结 oracle、任务、价格口径和 telemetry schema，并在另一个 harness 上复测，防止 evaluator/harness 共适应。