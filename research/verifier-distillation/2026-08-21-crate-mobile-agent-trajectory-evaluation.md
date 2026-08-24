# CRATE：基于逐步后果推理与聚合的移动 Agent 轨迹评估

- **论文标题**：Automated Trajectory Evaluation for Mobile Agents via Step-Level Consequence Reasoning and Aggregation
- **作者**：Pengshuai Yang，Zijing Gao，Xue Yu，Benhui Zhuang，Bo Yuan，Junlan Feng
- **首次公开日期**：2026-08-21
- **版本日期**：2026-08-21（v1）
- **arXiv ID**：2608.20797
- **原始论文**：https://arxiv.org/abs/2608.20797
- **DOI**：https://doi.org/10.48550/arXiv.2608.20797
- **代码链接**：https://anonymous.4open.science/r/CRATE-D580

## 一句话结论

CRATE 先独立判断每一步动作造成的可见状态变化，再聚合为任务完成度与安全性判断，减少把整条移动 Agent 轨迹一次塞给 Judge 所造成的上下文过载。

## 真正新增的内容

**论文原文结论**：CRATE 是两阶段 VLM-as-Judge：step-level consequence reasoning 从截图中提取任务相关证据并推断动作条件化状态变化，trajectory aggregation 再综合完成度；CRATE-S 进一步评价操作安全。

**分析推断**：这比纯“下一步动作合理性”更接近用户当前可获得的评估信号：即使没有完整未来轨迹，也可以把下一步对状态的局部贡献编码成可累积证据，并在后续得到新状态时更新分布。

## 核心方法

逐步处理移动端视觉状态与动作，生成结构化文本证据；再由轨迹级模块聚合局部后果，分别输出任务完成与安全判断。框架兼容开放和闭源 VLM，避免整轨输入导致的重要证据稀释。

## 关键实验结果

**论文原文**：以 Qwen2.5-VL-72B-Instruct 为核心时，CRATE 在 AndroidWorld 达到 F1 0.833，比 SPA-Bench 高 20%；CRATE-S 在 MobileRisk 达到 F1 0.697。摘要宣称具有有效性和稳健性，但未在摘要中列出跨模型完整方差与成本。

## 证据质量与局限

证据包含两个真实移动 Agent benchmark 和公开匿名代码，质量中等偏上。局限是依赖截图可观察性；后台状态、不可见副作用和延迟后果可能无法由逐帧视觉证据恢复。安全 F1 仍只有 0.697，不能充当单一部署门禁。

## 最接近的相关工作

最接近 SPA-Bench、PRM-as-a-Judge 1.5、TRACE、Thinkingbox 与 LongRCA Bench。CRATE 的区别是把视觉轨迹压缩为动作条件化后果证据，再聚合，而不是直接对整条轨迹做一次整体判断。

## 如何复用或推进 LLM-as-a-Verifier

把下一步评估输出设计为状态转移分布：已完成子目标、引入风险、可恢复性、信息增益和不可见状态待验证项。后续观察到新截图或工具结果时，对这些预测做校准；蒸馏目标应是该分布和证据摘要，而非只有一个 pass/fail。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

- **score-level OPD**：直接蒸馏 step consequence 的多维分数，再用轨迹聚合器生成最终 reward。
- **pairwise A/B/T 与序数分布**：同一状态下比较两个候选动作的预期后果；证据不足或差异小则输出 Tie，并保留序数概率。
- **真值门控**：截图证据需与 UI tree、工具返回和后台状态校验结合，防止视觉上“像完成”。
- **student-generated critique states**：student 先生成“动作将改变什么”的 critique state，teacher 只纠正错误后果预测。
- **高熵探索**：对安全且可能推进任务的多个动作保留分支，不用单一路径一致性压平探索。
- **sealed eval**：独立冻结任务、设备状态和安全违规样例，且 sealed evaluator 不复用训练时的 consequence prompt。
