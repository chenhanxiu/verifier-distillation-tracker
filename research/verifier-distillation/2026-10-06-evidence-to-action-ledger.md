# From Evidence to Action: How Tool-Using Agents Fail

- 作者：Hongzhan Lin、Shidong Cao、Ziyang Luo、Wenhao Chai、Mong-Li Lee、Wynne Hsu
- 首次公开日期：2026-10-06
- 版本日期：2026-10-06（v1）
- 原始论文：https://arxiv.org/abs/2610.07753
- Canonical URL：https://arxiv.org/abs/2610.07753
- 代码：未发现公开代码链接

## 一句话结论

【论文原文】工具 Agent 的主要失败常发生在执行前：调查不完整或尚未建立所需证据就行动；一旦证据充分，单步执行通常可靠，多步工作流则暴露未满足前置条件与未完成闭环。

## 真正新增的内容

【论文原文】SafeActBench 用 Evidence Ledger 把“何时知道什么”与动作时序绑定，并以确定性轨迹 evaluator 检查下游依赖；这把结果正确性拆成调查、证据、决策、执行和完成声明。

## 核心方法

【论文原文】656 个案例覆盖六类运营域、五种协议，从静态动作判断、调查后不行动到单步和多步工作流；provenance-bound ledger 记录已建立事实、动作发生时点及依赖是否满足。

## 关键实验结果

【论文原文】十个 model–harness 配置中，静态动作评估强并不保证交互执行强；错误常始于证据未完备时停止或行动。证据齐备后单动作成功率通常较高，多动作任务仍受前置条件和未完成执行影响。摘要未给统一百分比。

## 证据质量与局限

【论文原文】规模为 656 案例且有确定性 evaluator，证据链比纯 LLM Judge 强。【分析推断】六个运营域仍不足以覆盖开放世界工具使用；ledger 的本体和“所需证据”规范可能漏掉隐含条件。

## 最接近的相关工作

【分析推断】接近 GCAC、Ground-truth-as-code、ContrAgent、PaperDoctor 与 TwinCheck；本文突出 evidence-before-action 的时序约束。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】把 verifier 输出分为 evidence sufficiency、action permission、execution completeness 三个序数头，并由 ledger 生成硬门控；生成式 critique 必须指出缺失证据或未闭合依赖，不能只给总体失败解释。

## 对 Agent verifier × OPD 实验路线的具体影响

- 【分析推断】score-level OPD：分别蒸馏证据充分度、动作合法性、完成度，不用单一总分。
- 【分析推断】A/B/T：证据充分才比较 A/B；未调查到关键状态时标 T。
- 【分析推断】真值门控：ledger 与确定性依赖检查决定方向，LLM 只补语义判断。
- 【分析推断】critique states：critique 需引用 ledger 条目和时间点。
- 【分析推断】高熵分叉：在证据缺口最大的节点分叉调查动作，而非直接分叉执行。
- 【分析推断】sealed eval：隐藏依赖图并冻结 evaluator，防止 Agent 针对 rubric 共适应。