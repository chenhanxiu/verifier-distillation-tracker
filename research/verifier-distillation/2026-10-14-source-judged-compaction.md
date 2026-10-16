# Source-Judged Compaction：用来源证据过滤长时程 Agent 摘要

- **论文标题**：Prune the Summary, Not the History: Source-Judged Compaction for Long-Horizon Agents
- **作者**：Guanghui Min, Chen Chen
- **首次公开日期**：2026-10-14
- **版本日期**：2026-10-14（v1）
- **原始论文**：https://arxiv.org/abs/2610.20927
- **代码**：https://github.com/GuanghuiMin/sjc

## 一句话结论

长轨迹 compaction 会把环境事实与 compressor 自己的推断混在一起；SJC 用低成本非生成式 judge 逐条判断摘要是否有环境/历史来源并删除无来源项，跨运行可靠性提高 2.1%–8.9%。

## 真正新增的内容

**论文原文**：把 summary entry 的“是否有 source”单独建模，而不是重新生成整份摘要；Jev 输出带校准概率的非生成式判定，每次 compaction 只增加一次请求，不改 Agent 或 compressor。

**分析推断**：这是 student-generated critique/memory state 的最直接准入门之一：先验证出处，再允许其影响未来动作或进入蒸馏数据。

## 核心方法

将结构化摘要拆成条目，逐条与环境输出和上一版摘要对齐；来源概率低于阈值的条目删除，保留原始历史不动。判定器不生成改写文本，降低二次幻觉。

## 关键实验结果

**论文原文**：对一种广泛使用的结构化 compressor，83% 的失败运行可追溯到执行某个具体摘要条目，且多数无环境输出支持。在 AppWorld 与 OfficeBench、两个 Agent 模型上，SJC 比原 compressor 的跨运行可靠性提高 2.1%–8.9%，不增加 Agent token 使用量。

## 证据质量与局限

优点是有失败归因、两个环境和两个 Agent；局限是 source support 不保证结论正确或决策有用，阈值错误可能删除必要推断。Jev 本身在 unsupported acceptance 上的盲区也要求独立校准。

## 最接近的相关工作

与 Grounding Agent Memory、RSIAgent、DENSE、PaperDoctor 的证据指针，以及 Draft–Verify–Revise 的指称漂移审计最接近。

## 如何复用或推进 LLM-as-a-Verifier

将 critique/memory 拆成“观察、推断、建议、未完成义务”四类；观察必须有环境 source，推断必须显式标注不确定性，建议不能伪装成事实。source judge 输出概率可直接形成 T/INCONCLUSIVE 区间。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：仅在 critique 条目通过 source gate 后才计算 teacher–student score shift。
- **A/B/T 与序数分布**：有明确来源为可评 A/B；无来源默认 T，不当作负例。
- **真值门控**：环境日志和上一版已验证状态是唯一硬来源。
- **critique states**：把 source probability、证据指针和条目类型一起写入状态。
- **高熵探索**：删除无来源断言，但保留标明“假设”的多个候选，不把 pruning 变成过早收敛。
- **sealed eval**：用隐藏日志扰动、伪来源和过期状态测试 source judge，且 final evaluator 不复用训练阈值。
