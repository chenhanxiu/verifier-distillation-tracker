# RL Starts before RL：把 OPD 作为强化学习前置阶段

## 基本信息

- 论文标题：RL Starts before RL: On Policy Distillation for Better Reinforcement Learning
- 作者：Shuai Dong；Yongfu Zhu；Yuqi Xu；Weichu Xie；Liuwenpu；Ziyue Wang；Kaiwen Tuo；Congcong Wang；Siyuan Wang；Wenqi Shao；Shuai Yang；Ji Zhao；Caoyuan Ma；Wenzheng Chang；Taiqiang Wu；Xinlei Yu；Hongrui Wu；Xiaoxuan He；Fangke Chen；Dianyi Wang；Kanghui Tian；Sirry Chen；Xingyu Liu；Xiangnan Wu；Jiawei Guo；Haowen Hou；LingHan Chen；Zhongyu Wei；Jiaqi Wang
- 首次公开日期：2026-09-23
- 版本日期：2026-09-23（v1）
- arXiv：2609.28145
- DOI：https://doi.org/10.48550/arXiv.2609.28145
- 原始论文：https://arxiv.org/abs/2609.28145
- 代码：截至 2026-09-24，论文页面未提供作者代码链接

## 一句话结论

OPD 的价值不能只看蒸馏结束时的准确率：它可改变随后 RL 的可学习状态分布，而且最佳 KL 方向取决于轨迹来源和后续训练阶段。

## 真正新增的内容

【论文原文】论文在共享 RL 设置下比较 OPD 初始化、直接 RL 与 SFT→RL，发现 OPD 即使不立即提高准确率，也可能带来更高的最终 RL 性能；并系统比较 student/teacher 轨迹来源与 forward/reverse KL 在“蒸馏后”和“再 RL 后”的排序变化。

【分析推断】这要求 Agent verifier × OPD 路线把 sealed eval 的观察点后移：不仅测 verifier/student 当下拟合，还要测经过真实环境优化后是否保留可恢复、多样且可继续改进的策略分布。

## 核心方法

1. 在 RL 前以 on-policy distillation 初始化 student。
2. 统一后续 RL 配置，比较不同前置训练策略。
3. 对比 student-generated 与 teacher-generated 蒸馏轨迹。
4. 对比 forward KL 与 reverse KL，并分别在 OPD 后和 RL 后评价。

## 关键实验结果

【论文原文】OPD 初始化的 student 在共享 RL 设置下最终优于直接 RL 或 SFT 后再 RL；这一优势可在 OPD 阶段准确率几乎不变时出现。student on-policy 轨迹上，reverse KL 在 RL 前更好、forward KL 在 RL 后反超；teacher-generated 轨迹上，reverse KL 在两个阶段均领先。论文摘要未给出统一的绝对增益数字。

## 证据质量与局限

【论文原文】关键比较控制了后续 RL 设置，并对轨迹来源和散度目标做交叉分析。

【分析推断】当前证据主要来自推理任务，尚未验证多轮工具 Agent、verifier 共适应或环境非平稳性。论文把“分布对齐有利于后续 RL”作为行为解释，尚非严格因果机制证明。

## 最接近的相关工作

与 One-Shot OPD、Data-free OPD、SuRe、RouteOPD、RetireOPD 和 γOPD 最接近。不同之处在于把 OPD 视作 RL 的状态分布预条件器，并以最终 RL 表现而非即时蒸馏分数选择目标。

## 如何复用或推进 LLM-as-a-Verifier

先用 verifier teacher 对 student on-policy 轨迹做分布蒸馏，再在环境真值下继续 RL；同时保存蒸馏前后策略熵、分叉覆盖和恢复率。将 verifier 的序数分布作为软初始化，而非永久替代环境奖励。

## 对现有 Agent verifier × OPD 路线的具体影响

【分析推断】

- score-level OPD：新增“OPD→环境 RL”两阶段基线，不能只比较蒸馏后分数。
- A/B/T：保留 teacher 不确定或近似打平的 T 状态，作为后续 RL 的探索储备。
- 真值门控：OPD 负责塑形，最终方向由程序化/环境回报纠偏。
- critique states：比较 student-generated critique 轨迹与 teacher-generated 轨迹对后续 RL 的不同影响。
- 高熵探索：把 KL 方向作为变量；预期 forward KL 可能在后续 RL 中更好保留可改进的次优模式。
- sealed eval：至少在 OPD 后、RL 中途和 RL 结束三个冻结检查点独立评测，防止以即时增益选错方案。