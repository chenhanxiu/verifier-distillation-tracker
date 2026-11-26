# EvoLink-Bench：评估自演化 Agent 的长时程跨任务依赖

- **论文标题**：EvoLink-Bench: A Benchmark for Evaluating Self-Evolving Agents in Long-Horizon Interdependent Task Streams
- **作者**：Wei Chen, Xiaodong Lu, Weihao Shen, Gongxun Li, Xingyu Guo, Qihang Sun, Fuwei Zhang, Zhao Zhang, Yikun Ban, Shuang Li, Deqing Wang, Fuzhen Zhuang
- **首次公开日期**：2026-11-25
- **版本日期**：2026-11-25（v1）
- **原始论文**：https://arxiv.org/abs/2611.34400
- **DOI**：https://doi.org/10.48550/arXiv.2611.34400
- **代码链接**：未见公开代码

## 一句话结论

EvoLink-Bench 将长时程评价拆为任务内恢复、持久状态更新和后续经验复用，避免把单次成功误当成真正的 Agent 演化。

## 真正新增的内容

**论文原文结论**：基准包含持久工作区和跨任务依赖，并区分可语言化知识修订（L1）与执行能力演化（L2）。**分析推断**：distributional verifier 应对这三类结果分别建模，尤其不能把记忆写入后的即时收益当作长期有效。

## 核心方法

覆盖办公、多轮对话和 AutoResearch 流程；在三种持久化条件下比较 5 个 Agent 框架、3 种 backbone，评测 19,635 个 task slots，并分别统计恢复、状态更新和跨任务复用。

## 关键实验结果

没有框架在 L1/L2 同时稳定最佳；重试只能恢复有限失败，持久状态更新不必然改善后续任务；知识级与能力级演化呈现不同规律，局部提升也常不能迁移到其他任务流。

## 证据质量与局限

大规模 task-slot、持久状态和跨任务依赖比独立短任务更接近真实长时程 Agent。局限是 benchmark 仍无法证明 grader 对开放式路径完备，且没有直接训练 reward model。

## 最接近的相关工作

与 DynSTEER 的阶段评价、DENSE 的证据化捷径树、Continual Search for Long-Horizon RCA 及 SealedLoop 相关。

## 如何复用或推进 LLM-as-a-Verifier

为每个状态输出“当前完成、恢复可能、记忆有效、后续迁移”的联合序数分布；critique/memory 写入后必须在后续任务上复验，失败则回滚。

## 对现有 Agent verifier × OPD 实验路线的具体影响

**分析建议**：score-level OPD 不只优化即时 verdict，还加入跨任务延迟回报；高熵分叉保留不同记忆策略。sealed eval 使用隐藏后续任务测试 evaluator 与 memory 是否共同过拟合，并分报 L1/L2 与恢复指标。
