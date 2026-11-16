# Soteria: Formally Verified Planning with Runtime Enforcement for Safe LLM Agents

- **作者**：Mike He、Ankush Desai、Sharad Malik、Aarti Gupta
- **首次公开日期**：2026-11-13
- **版本日期**：2026-11-13（v1）
- **原始论文**：https://arxiv.org/abs/2611.17880
- **代码**：未发现公开代码
- **标识符**：arXiv:2611.17880；DOI: 10.48550/arXiv.2611.17880

## 一句话结论

【论文原文】Soteria 在任何工具调用前形式验证层级计划，并在运行时强制执行规范；被阻止后仍用已验证计划指导恢复，平均任务成功率达到最佳基线的 1.7 倍且无策略违规。

## 真正新增的内容

【论文原文】不同于只在运行时拒绝不安全动作，Soteria 先验证完整结构化计划，再让该计划同时充当安全证书与恢复指南，从而缓解“阻止违规后 Agent 被困住”的 utility–safety 张力。

【分析推断】对 Agent verifier × OPD，它提供了不可被软 Judge 覆盖的硬真值层：形式规范决定可行动作集合，score-level verifier 只在集合内排序。已验证计划还可生成反事实负分支和精确的首个违规状态。

## 核心方法

1. Agent 在执行前生成层级结构化计划。
2. 形式验证器检查计划满足领域策略与正确性规范；未通过则不调用工具。
3. 运行时 enforcement 约束每步动作，并在阻断时依据已验证计划恢复或重规划。

## 关键实验结果

【论文原文】在覆盖多种工具使用任务的多个基准上，Soteria 的平均任务成功率是最佳基线的 1.7 倍，同时报告零 policy-specification violation；论文获 NeurIPS 2026 Oral。摘要未给出逐基准样本量和验证耗时。

## 证据质量与局限

【论文原文】同时报告 utility 和 safety，且与多基准最佳基线比较，证明“形式阻断必然牺牲成功率”并非必然。

【分析推断】零违规仅相对于已编码规范，不能排除 specification gap；真实环境状态、工具副作用或规范翻译错误仍可能逃逸。形式验证的成本和对开放式任务的可扩展性需单独测量，且应避免把验证器本身纳入策略可优化的反馈闭环。

## 最接近的相关工作

最接近 MAGS 的冻结形式安全层、ContrAgent 的 LTLf/DFA 约束、GCAC 的可执行工作流契约和 Reality Is the Final Verifier 的 specification/reality gap。Soteria 的区别是让已验证层级计划同时支持运行时恢复，而不只作拒绝门。

## 如何复用或推进 LLM-as-a-Verifier

形式验证器输出 hard feasible mask、失败规范和最早违规节点；generative verifier 再解释失败、估计可恢复性并给可行分支排序。蒸馏时只传递可行集合内的 teacher 分布，任何与规范冲突的 teacher 偏好都被截断。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：先应用形式可行 mask，再对合法动作做 score-level 蒸馏；硬门决定方向。
- **pairwise A/B/T 与序数分布**：合法/非法形成确定 A/B；两个合法恢复计划保留序数分布；规范不完备时标 T。
- **环境真值门控**：形式证明与运行时状态断言成为不可覆盖的 teacher anchor。
- **student-generated critique states**：critique 需引用具体规范和违规节点，并经验证器复现。
- **高熵探索**：只裁掉已证明非法分支，在多个合法计划间保持探索和可恢复性差异。
- **sealed eval**：冻结规范、验证器和隐藏副作用测试；另设现实结算检查 specification gap，防止策略只优化可见规则。
