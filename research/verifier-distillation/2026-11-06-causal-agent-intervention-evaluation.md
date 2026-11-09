# Knowing When to Intervene: Causal Evaluation of AI Agents

## 基本信息

- **作者**：Ayush Sawarni；Wenqian Xing；Tijana Zrnic；Ramesh Johari；Vasilis Syrgkanis
- **首次公开日期**：2026-11-06
- **版本日期**：2026-11-06（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.09792
- **DOI**：https://doi.org/10.48550/arXiv.2611.09792
- **代码**：截至记录时未检索到可稳定确认的独立公开仓库

## 一句话结论

长轨迹中的 verifier/人工审核是否有价值不能由静态 benchmark 或“被拦截动作看起来更差”判断，而应通过轨迹内随机干预估计对最终结果的动态因果效应。

## 真正新增的内容

**论文原文结论**：提出一个方法学框架，使用少量带随机 verification/screening 干预的 Agent 轨迹，估计丰富的上下文干预策略之动态因果效应，并据此构建动作风险 leaderboard。

**分析推断**：这为 verifier 路由与 student-generated critique 的价值评估提供了比相关性 Judge 分数更干净的估计量，但本身不是 verifier 蒸馏算法。

## 核心方法

1. 在轨迹内的合格决策点随机分配“直接执行”或“验证/筛查”。
2. 记录当前可见状态、后续策略行为与终局结果。
3. 估计不同上下文干预策略的动态因果效应，而非只比较被干预与未干预样本。
4. 用估计的结构参数生成动作风险与审计优先级。

## 关键实验结果

**论文报告**：在 τ-bench Retail、ToolSandbox 和 ImpossibleBench 上，干预效应随动作和状态显著变化；摘要没有给出统一平均提升值，重点是异质性与可识别评估框架。

## 证据质量与局限

- 随机化干预和终局结果比离线轨迹打标签更接近因果证据。
- 横跨三个 Agent benchmark，但摘要未给出样本量、区间覆盖和成本收益细节。
- 依赖随机化协议、可观测状态与后续策略假设；部署分布漂移仍可能破坏估计。
- 估计“干预是否有用”不等同于 verifier 判定本身正确。

## 最接近的相关工作

接近动态处理效应、off-policy evaluation、action-level sentinel、executed counterfactual attribution 和 adaptive oversight。区别在于它把验证/筛查本身当作时序干预来评估。

## 如何复用或推进 LLM-as-a-Verifier

将 verifier 调用视为有成本的 action，而非默认总是执行；在部分轨迹节点随机升级到强 verifier/人工/环境重放，学习“何时调用、调用哪一级”的策略，并以终局任务成功率估计增益。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

- **score-level OPD**：只在随机化数据表明 teacher 干预有正因果效应的状态提高蒸馏权重。
- **A/B/T 与序数分布**：T 可触发随机升级；把升级后的终局增益作为路由标签。
- **真值门控**：环境/程序验证是干预类型之一，应单独估计成本与收益。
- **critique states**：不能只比较有/无 critique 的观察结果，需在同类状态随机插入 critique 后继续执行。
- **高熵分叉**：优先在高熵且估计干预收益大的节点追加 verifier；高熵本身不是充分条件。
- **sealed eval**：使用与训练路由器隔离的随机化轨迹和冻结终局指标，避免 evaluator 与 policy 共适应。