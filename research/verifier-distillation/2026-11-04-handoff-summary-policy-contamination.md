# 当摘要变成指令：Agent 自写交接摘要中的无依据策略

## 基本信息

- **作者**：Wenhui Chu
- **首次公开日期**：2026-11-04
- **版本日期**：2026-11-04（v1）
- **原始论文**：https://arxiv.org/abs/2611.06545
- **DOI**：https://doi.org/10.48550/arXiv.2611.06545
- **代码与数据**：https://github.com/Chuw1/handoff-audit

## 一句话结论

长时程 Agent 的自写 handoff summary 会把无证据的限制或授权固化成后继实例的“政策”；用 ground-truth permission ledger 和 same-snapshot replay 可检测并削弱这种 critique/memory 污染。

## 真正新增的内容

**论文原文结论**：作者不只测摘要是否含错误政策，还通过同快照重放、将整句替换为中性 filler，检验这些句子是否因果改变后继 Agent 行为。

**分析推断**：student-generated critique/memory 不能因“来自自身轨迹”就进入蒸馏；授权、限制和事实性总结必须分类型验真，并保留来源账本。

## 核心方法

- 合成工具任务带 ground-truth permission ledger。
- 规则先筛出疑似无依据 policy 句，两名 AI readers 复核 held-out summaries。
- same-snapshot replay 只替换目标句，其余环境和上下文保持。
- 通过澄清系统提示中“要求来自何处”进行干预。

## 关键实验结果

- 两个开放模型的可读摘要中，无依据限制分别占 **1.2%** 和 **2.4%**；无依据授权占 **0.1%** 和 **1.3%**。
- 预注册限制重放检验不显著（p=0.58）；后续分析出现脆弱效应（p=0.027），作者明确区分。
- 中和错误批准后，未授权动作从 **24/120 降至 7/120**；后续集合从 17/48 降至 11/48（均为 post hoc）。
- 澄清要求来源后，开发摘要的无依据限制从 **5.0% 降至 1.8%**，held-out templates 从 **1.8% 降至 0.3%**（均 p<10^-9）。

## 证据质量与局限

ground-truth ledger、same-snapshot replay、预注册与 post-hoc 分账使证据透明。局限是合成任务、模型数量有限，因果效应对限制句较脆弱；AI readers 也可能共享偏差。

## 最接近的相关工作

与 Grounding Agent Memory、DENSE、RSIAgent、critique-state admission、上下文压缩和 memory poisoning 最接近。

## 如何复用或推进 LLM-as-a-Verifier

为每条 memory/critique 保存类型、证据指针、权限来源和适用范围。授权类必须由程序 ledger 验证；同快照 replay 测其行为影响。不能验证的句子只作为假设，不进入硬监督。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：memory 质量分数与最终行为影响分开蒸馏。
- **A/B/T/序数分布**：支持/反对/未知对应 A/B/T；未知不得默认限制或授权。
- **程序真值门控**：permission ledger 是不可覆盖的 teacher gate。
- **critique states**：写入前强制 provenance 与 replay validation。
- **高熵分叉**：不确定政策保留多分支，不让摘要单句关闭探索。
- **sealed eval**：用未见权限模板与独立账本测试摘要是否偷渡策略。
