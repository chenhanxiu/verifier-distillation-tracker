# Valid Stopping in Adaptive Generator-Verifier Loops

- 作者：Mahmoud Hegazy、Michael I. Jordan、Aymeric Dieuleveut
- 首次公开日期：2026-10-05
- 当前版本日期：2026-10-05（v1）
- arXiv：2610.06432
- 原始论文：https://arxiv.org/abs/2610.06432
- Canonical URL：https://doi.org/10.48550/arXiv.2610.06432
- 代码：未发现公开代码链接

## 一句话结论

【论文原文】当 generator 自适应搜索 cheap verifier 时，假阳性会随尝试次数累积；论文给出控制已接受提案 false discovery rate 的有效停止规则。

## 真正新增的内容

【论文原文】工作将 generator–verifier 循环视为序贯统计检验，引入基于 index betting 的 e-values，并提出适用于非单调损失的 conformal risk control，而不是用固定分数阈值决定何时停止。

## 核心方法

【论文原文】cheap verifier 作为昂贵 ground-truth oracle 的代理；在自适应提案流中累计证据，并在满足风险控制条件时接受/停止，使多次搜索造成的选择偏差被显式纳入保证。

## 关键实验结果

【论文原文】方法在合成设置和蛋白质设计基准上验证；摘要报告能够在自适应搜索中控制已接受提案的错误发现风险，但未给出统一的效果数字。

## 证据质量与局限

【论文原文】理论贡献强，且包含真实科学设计任务。局限是保证依赖校准/交换性等统计条件；蛋白设计与语言 Agent 的相关结构、非平稳 verifier 和状态依赖可能不同；控制 FDR 不等于每个提案均正确。

## 最接近的相关工作

最接近 Robust Conformal Consensus、Certified Selective Automation、VStress，以及 best-of-k/verifier test-time scaling 的认证工作。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】将每次 Agent 重试、候选修复和 critique-revise 循环视为自适应多重检验；停止条件应由风险预算而非“某次分数过阈值”决定，并周期性调用昂贵环境 oracle 更新校准。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：【分析推断】仅在序贯风险上界通过时把高分候选写入蒸馏缓冲区。
- **A/B/T 与序数分布**：【分析推断】未达到统计停止条件的比较统一保留为 T。
- **硬真值门控**：【分析推断】抽样调用 ground-truth oracle 作为风险校准锚点。
- **critique states**：【分析推断】多轮 critique 搜索的累计假阳性必须计入预算。
- **高熵探索**：【分析推断】在风险预算内允许继续分叉，而不是首个高分即停止。
- **sealed eval**：【分析推断】训练外独立复核已接受轨迹，报告选择后 FDR 与覆盖率。
