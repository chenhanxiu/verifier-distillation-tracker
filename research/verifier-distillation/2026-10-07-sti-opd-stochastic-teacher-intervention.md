# Stochastic Teacher Intervention for Agentic On-Policy Distillation

- **作者**：Junnan Liu；Linhao Luo；Zhijun Chen；Qianren Mao；Thuy-Trang Vu；Gholamreza Haffari
- **首次公开日期**：2026-10-07
- **版本日期**：2026-10-07（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2610.10878
- **Canonical URL**：https://arxiv.org/abs/2610.10878
- **代码**：未发现公开代码链接

## 一句话结论

STI-OPD 在多轮 Agent rollout 中只在 teacher–student 高分歧处随机接管动作，并用重要性加权修正混合策略偏差，为“保留 student 探索、又避免灾难性后缀”提供了直接方法。

## 真正新增的内容

【论文原文】方法根据 teacher–student KL 差异映射干预概率，在交互中随机以 teacher 动作替换 student 动作；随后用 Importance-Weighted Reverse KL 校正来自 student/teacher 混合行为策略的采样错配。

【分析推断】这比固定阈值 teacher forcing 更适合高熵分叉：干预概率可由 verifier 的序数不确定性、环境风险和可恢复性共同决定。

## 核心方法

1. student 在多轮环境中生成动作，实时计算 teacher–student KL。
2. 通过概率映射决定是否由 teacher 接管当前动作，而非确定性地全部纠正。
3. rollout 因此来自混合策略，既保留 student 状态又减少进入无意义失败后缀。
4. 用重要性权重的 reverse-KL 训练，校正采样策略和目标策略不一致。

## 关键实验结果

【论文原文】作者报告 STI-OPD 在所有测试的工具使用/长时程基准和 student 尺度上均超过最强先前 OPD 基线。摘要未给出统一绝对提升值，故此处不臆造数字。

## 证据质量与局限

【论文原文】跨多个 agentic benchmark 与尺度的一致收益支持方法普适性。  
【局限】干预依据仍主要是 teacher–student KL，而非环境真值；teacher 错误时可能把 rollout 引向一致但错误的区域。重要性权重在长序列上可能高方差，摘要未说明 sealed evaluator 或不可逆工具副作用的处理。

## 最接近的相关工作

最接近 Persistent Teacher Anchoring、AC-OPD、STRIDE、Belief-Shift Branching、DDO 与 Unified Per-Token OPD Gating。区别是 STI-OPD 直接改变环境交互中的行为策略，并显式校正混合采样偏差。

## 如何复用或推进 LLM-as-a-Verifier

将干预概率从 token KL 扩展为风险函数：A/B/T 分布熵、程序化约束违规概率、状态可恢复性、teacher 可靠性和动作副作用。teacher 接管后仍应执行环境验真，并把“student 原动作—teacher 动作—结果差异”保存为生成式 critique 训练对。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：把 verifier 分数差作为干预门控，同时用重要性权重校正被干预轨迹的训练偏差。
- **A/B/T 与序数分布**：T/高熵触发随机路由而非硬否决；A/B 的 margin 决定干预概率。
- **程序化/环境真值门控**：有副作用的工具动作必须在执行前先过硬约束，KL 仅作为软门控。
- **student-generated critique states**：对每次干预生成“为何接管、替代动作、环境结果”的 critique state，并经重放验真后入库。
- **高熵分叉**：保留非零 student 行动概率，避免 teacher 全接管导致探索坍缩。
- **sealed eval**：最终评测禁用训练期自适应 evaluator，分别报告无干预能力、带干预系统能力和 teacher 调用成本。

总体判断：【分析推断】STI-OPD 是将 verifier 蒸馏落到真实 Agent 交互的强基线，但应把 KL 干预器升级成“硬真值优先、分布式软信号调概率”的安全路由器。