# Follow the Policy, Fail the Benchmark: Auditing and Revising Policy-Based Decision Benchmarks

- **作者**：Yanru Xiao, Yifei Cai
- **首次公开日期**：2026-11-04
- **版本日期**：2026-11-04（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.07042
- **DOI**：https://doi.org/10.48550/arXiv.2611.07042
- **代码与修订数据**：https://github.com/SugarRuy/BAR-Policy-Decision

## 一句话结论

九个规则决策 benchmark 的 reference、scorer、任务文本和中间答案会互相矛盾；仅修正 scorer 就能让 SARA 三个模型的接受率各提高 80 多个百分点。

## 真正新增的内容

BAR 用来源追踪、程序执行和受控检查形成版本化审计证据与局部修订，不重新生成模型回答即可量化 evaluator 缺陷造成的分数变化。

## 核心方法

审计 policy、case、reference、intermediate answer 与 scoring rule 的一致性；保存原始输出并用修订 scorer 重放；为每项修复记录范围、证据和版本。

## 关键实验结果

- LegalBench SARA 96 个数值题中，修正 scorer 后三个模型接受率均提高 **80+ 个百分点**。
- RuleArena Tax 恢复 zero floor 后，300 个 reference 中 **27 个**改变，模型差距缩小。
- 发现 unsupported targets、可在 replay 中存活的 reference error，以及奖励不完整决策的 evaluator。

## 证据质量与局限

代码、证据索引和修订数据公开，且使用不变模型输出重评分，能清楚隔离 scorer 效应；但审计集中在 policy decision benchmark，并非所有长时程环境。

## 最接近的相关工作

最接近 Benchmarks as Software、Ground-truth-as-code、Harness or Model、AutoTuneBench 与 evaluator mutation testing。

## 如何复用或推进 LLM-as-a-Verifier

为每个程序化 verifier 建立政策来源、可执行 reference、scorer 单测、变异测试和版本化重放；teacher 信号只有在 policy/reference/scorer 一致时才能作为硬真值。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

1. score-level OPD 前先审计 oracle，错误硬标签比软 Judge 偏差更危险。
2. A/B/T 应允许“benchmark inconsistent”作为独立 T 原因。
3. critique state 保存 policy 条款与执行证据，不能只存 reference。
4. 高熵分叉若由 scorer 缺陷引起，不应被当成探索价值。
5. sealed eval 发布 verifier 版本与重评分 delta，并冻结训练前可见的修订范围。