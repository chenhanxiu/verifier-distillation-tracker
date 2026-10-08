# SpecGuard: Proving a Task Is Broken Before the Agent Cheats

- 作者：Param Biyani、Krishnamurthy Dvijotham
- 首次公开日期：2026-10-06
- 版本日期：2026-10-06（v1）
- 原始论文：https://arxiv.org/abs/2610.09159
- Canonical URL：https://arxiv.org/abs/2610.09159
- 代码：https://github.com/prmbiy/specguard

## 一句话结论

【论文原文】SpecGuard 在 Agent 执行前分别形式化任务意图与测试，并由 Lean 4 kernel 证明二者是否不可同时满足，从源头识别会诱发改测试、硬编码或删除安全防线的 reward-hacking 机会。

## 真正新增的内容

【论文原文】不是观察 Agent 是否作弊，而是在任何行为发生前生成机器可检查的不一致证书；任务规范与测试规范独立生成，降低同源解释把冲突抹平的风险。

## 核心方法

【论文原文】只读取任务描述与代码库，将期望行为自动形式化为 Lean 4 specification；测试被独立形式化，kernel 检查是否存在同时满足两者的实现，冲突时输出 certificate。

## 关键实验结果

【论文原文】在 conflicted SWE-bench 任务上最多检测 72.8% 冲突、正式认证 51.1%，冲突漏检率比 model-based judgment 低近五倍。认证覆盖仍不完整。

## 证据质量与局限

【论文原文】形式 kernel 提供强证书，并与模型判断比较。【分析推断】autoformalization 仍可能遗漏意图；51.1% 认证率意味着多数冲突尚无证书，且编程任务外迁移需新的形式语言和工具。

## 最接近的相关工作

【分析推断】接近 MAGS、ContrAgent、GCAC、ImpossibleRubrics 和 executable-contract audit；本文把形式检查前移到 Agent 行动之前。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】在 verifier teacher 前增加“任务是否自洽”的硬层；若规范冲突，轨迹不进入 A/B 训练，而标为 T/BROKEN。生成式 verifier 只能解释证书，不能覆盖 kernel verdict。

## 对 Agent verifier × OPD 实验路线的具体影响

- 【分析推断】score-level OPD：broken task 的 score 不回传给 student。
- 【分析推断】A/B/T：形式冲突直接标 T/BROKEN，不将“作弊成功”当 A。
- 【分析推断】真值门控：Lean certificate 是不可覆盖硬信号。
- 【分析推断】critique states：critique 应引用冲突公式与证书，而非猜测意图。
- 【分析推断】高熵分叉：在冲突解除前停止执行分叉，避免探索危险捷径。
- 【分析推断】sealed eval：独立保存规范、测试和 proof artifact，防止 evaluator 共适应。