# DART-SD：面向多轮工具 Agent 菱形拓扑的局部自蒸馏

## 基本信息

- **论文标题**：DART-SD: Diamond-topology Aware Retrieval and Tuning for Self-Distillation of Multi-Turn Tool-Calling Agents
- **作者**：Hangrui Xu、Jiarui Wang、Yang Yang、Chuanbo Zhu、Fangda Chen、Ziqi Wu、Jingming Cai、Yan Song
- **首次公开日期**：2026-08-19
- **版本日期**：2026-08-19（v1）
- **arXiv ID**：2608.18524
- **DOI**：10.48550/arXiv.2608.18524
- **论文**：https://arxiv.org/abs/2608.18524
- **代码**：截至记录时论文未给出公开代码链接。

## 一句话结论

DART-SD 把多轮工具执行建模为可汇合的交互状态图，定位 student 首次离开“经验可恢复区域”的 Critical Topological Breakpoint，只蒸馏恢复后缀并冻结有效前缀，从而避免全轨迹模仿压制顺序不同但同样正确的探索路径。

## 真正新增的内容

### 论文原文结论

多子目标可交换时，成功解并非一条线，而是汇合的 diamond lattice。DART-SD 构造 Interaction-State Transition Graph，联合成功与失败轨迹识别 CTB，再检索有成功支持的 recovery reference；progressive self-distillation 的 loss 仅覆盖 teacher 重采样的恢复步骤。

### 分析推断

这是对“高熵分叉不能按 reference trajectory 做逐步对齐”的直接方法学回答。它比 token divergence 更接近反事实可恢复性，但 CTB 仍由经验图和 teacher recovery 定义，不等于已学习校准的 distributional verifier。

## 核心方法

1. 将环境状态、工具动作与后继状态构成 ISTG，保留不同动作顺序最终汇合的拓扑。
2. 在 student on-policy rollout 中定位首次偏离 success-supported recoverable region 的 CTB。
3. 从 CTB 检索相关成功路径，由 teacher 生成 recovery suffix。
4. 只对恢复 suffix 做监督，保护 CTB 前已正确执行的 student prefix。
5. 迭代更新后重新采样与重建能力边界，使 CTB 逐步向后移动。

## 关键实验结果

### 论文原文

- 在 FTRL 的 2,000+ 可验证工具环境训练，并在 FTRL、BFCL、ToolHop、τ-bench、RoTBench 测试。
- Qwen3-4B/8B 的汇总结果中，DART-SD 为 45.58，最强列出的训练基线 FTRL-GRPO 为 40.33。
- Qwen3-8B 上，DART-SD 在所有五项 benchmark 都优于 base，并在 FTRL、ToolHop、τ-bench 超过 teacher。
- 平均工具调用从迭代 1 的 4.23 降至迭代 5 的 3.55，短于 golden reference 的 4.02。
- 失败轨迹平均 CTB position 从 0.348 后移到 1.452，说明可保护的有效 prefix 变长。

## 证据质量与局限

- **质量**：覆盖两个 student 尺度、五个工具 benchmark、蒸馏与 RL 基线；报告轨迹长度、CTB 演化与 OOD 迁移。
- **局限**：未见公开代码；ISTG/CTB 的构造误差与成本尚难复核；“经验可恢复”依赖已有成功轨迹覆盖；没有明确 A/B/T 校准或人工轨迹质量评估；主要由任务完成指标验证；v1 预印本。
- 更短轨迹不必然更安全或更可解释，尤其在不可逆工具动作中。

## 最接近的相关工作

SOPD、OPSD、SCoRe-SFT、FTRL-GRPO、ToolRL、MatchTIR，以及 counterfactual recoverability / Wrong but Useful 轨迹价值分析。

## 如何推进 LLM-as-a-Verifier

- 将 CTB detector 视为过程 verifier：输出“仍可恢复 / 临界 / 已离开可恢复域”的序数分布，而不是硬断点。
- 以同一环境状态的继续与恢复 suffix 做 pairwise A/B/T；若两者均成功或差异不显著标 T。
- 在图节点上加入程序状态 diff、工具异常与 student critique，使 verifier 判断基于状态而非字符串动作序列。

## 对 Agent verifier × OPD 路线的具体影响

以下为**分析推断**：

- **Score-level OPD**：只在 CTB 后用 verifier score 加权 teacher loss，前缀梯度置零或显著降权。
- **A/B/T 与序数分布**：按共享环境状态比较两个后继，而非比较整条轨迹；建模恢复概率而非单一正确/错误。
- **真值门控**：ISTG 边必须由执行结果、环境状态和工具返回验证；LLM 仅解释断点。
- **Critique states**：让 student 在疑似 CTB 生成反思，验证反思是否提高 recovery success，再决定是否作为蒸馏状态。
- **高熵探索**：对能汇合到同一成功状态的不同路径均保留，不把非 reference 顺序惩罚为错。
- **Sealed eval**：sealed 任务不得进入 ISTG/检索库；使用独立执行器验证 recovery，另报告不可逆误操作和 evaluator 误判。