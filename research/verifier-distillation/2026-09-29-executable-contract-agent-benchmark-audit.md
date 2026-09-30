# Do Agent Benchmarks Do What They Say? An Executable-Contract Audit of Tool-Using Agent Environments

- **作者**：Rohith Reddy Bellibatlu, Zichong Wang, Wenbin Zhang
- **首次公开日期**：2026-09-29
- **版本日期**：2026-09-29（v1）
- **原始论文**：https://arxiv.org/abs/2609.37315
- **代码**：未发现公开代码链接

## 一句话结论

四个 Agent benchmark 的工具实现与接口承诺存在可确认偏差，甚至会让 evaluator 奖励未真实发生的状态变化，说明“环境真值”本身也必须做可执行契约审计。

## 真正新增的内容

【论文原文】作者把工具公开接口写成 executable contract，检查实现并沿任务文件和 evaluator 代码追踪 score provenance；审计 34 个会修改状态的工具，确认 7 个工具缺陷和 1 个 evaluator 属性。

【分析推断】这补上了 verifier × OPD 路线常忽略的一层：程序化 grader 并非天然真值，若环境实现错误，硬门控会系统性蒸馏错误信号。

## 核心方法

静态检查接口/实现一致性，动态 probe 工具行为，再将缺陷传播到具体 task、状态写入和最终 verdict；使用 pinned commit 保证可复查。

## 关键实验结果

【论文原文】注入缺陷测试中 25 个 flag 无假阳性，但 5 个 negative control 中标出 2 个，且漏掉多数缺陷；33 个 scored miss 中 29 个虽有契约条款却无 probe 暴露。静态部分单独命中 17 个确认位置中的 14 个。AgentDojo 25 个 mutating tools 至少 5 个偏离其 advertised surface；tau2-bench 的隔离路径显示 evaluator 会奖励错误实现并惩罚修复实现。

## 证据质量与局限

【论文原文】证据来自 pinned commit、逐项复现和 provenance tracing，因果链较强；但只覆盖四个 benchmark，动态检测召回率有限，契约解释也可能有争议。

## 最接近的相关工作

Ground-truth-as-code Agent Evaluation、AutoTuneBench、Harness or Model?、GameLogicBench、GCAC。

## 如何复用或推进 LLM-as-a-Verifier

在把环境 outcome 用作 teacher 前，为每个 mutating tool 建立前置条件、状态转换和后置条件；verifier 输出必须引用真实状态差分，而非工具自然语言回执。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- **score-level OPD**：未通过契约审计的任务不得贡献蒸馏权重。
- **A/B/T 与序数分布**：环境实现不确定时标 T/INVALID，而不是据假回报排 A/B。
- **硬真值门控**：增加“oracle 自身验证”层，锁定环境 commit、probe 和 score provenance。
- **critique states**：critique 引用工具回执时必须与实际状态 diff 对账。
- **高熵探索**：避免把环境 bug 造成的奖励差异误判为高价值分叉。
- **sealed eval**：sealed 不只隐藏任务，还要冻结并审计工具实现与 evaluator；修复后需版本化重跑。
