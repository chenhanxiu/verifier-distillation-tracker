# EvoRouter：以 Insight 引导的 On-Policy Distillation 学习多 Agent 路由

## 基本信息

- **论文标题**：EvoRouter: Cost-Efficient Multi-Agent Routing via Insight-Guided On-Policy Distillation
- **作者**：Yitao Xiao, Xu Zhang, Ye Cheng, Shaoyong Guo, Yan Sun, Ziyue Zhu, Sitao Xie, Guo Tong, Haoran Luo
- **首次公开日期**：2026-10-26
- **版本日期**：2026-10-26（v1）
- **论文链接**：https://arxiv.org/abs/2610.35690
- **代码链接**：https://github.com/CenYangtze/EvoRouter

## 一句话结论

EvoRouter 把执行轨迹中的性能—成本反馈压缩成可复用 routing insights，再由 privileged teacher 对 router 自己产生的规划轨迹提供逐 token OPD，使多 Agent 配置选择同时提升效果并显著降本。

## 真正新增的内容

**论文原文结论**：工作不是只对“选哪个模型”做分类，而是在模型、协作拓扑、Agent 数、轮数和 skill 的组合空间中闭环学习；历史执行被专家汇总为条件化 insight，teacher 再把 insight 与当前执行反馈转成 dense token supervision。

**分析推断**：它提供了 Agent verifier × OPD 的系统级实例：teacher 信号不再只评答案，而是评价“为何选择这套 harness/Agent 配置”。这比把最终成功率直接广播到整段路由计划更接近 score-level、state-conditional distillation。

## 核心方法

1. Router 在当前策略下生成多 Agent 配置与规划轨迹。
2. 执行后收集任务得分与计算成本；expert 周期性提炼能力需求、扩容边际收益与配置交互。
3. Privileged teacher 结合 insight 与执行反馈，在 student 自己的规划前缀上提供逐 token 监督。
4. 再以 cost-aware RL 联合优化准确率和 Worker FLOPs，形成“执行—总结—蒸馏—再执行”循环。

## 关键实验结果

**论文报告**：覆盖五个域的 19 个域内数据集及两个域外 benchmark；域内平均准确率 68.69%，比最强路由基线高 7.23 个百分点，同时推理计算成本下降 50.95%。

## 证据质量与局限

优点是跨域、含 OOD、公开代码并同时报告效果与成本。局限是收益由 insight、OPD 与 cost-aware RL 共同产生，摘要未隔离每个组件的独立贡献；任务多为可聚合的短周期配置决策，尚不能等同于任意长时程工具 Agent。

## 最接近的相关工作

最接近 AgentRouter、Router-R1、MasRouter，以及多 teacher OPD、VG-OPD、Nash-MOPD。区别在于它将“路由经验”显式写成可复用 insight，再蒸馏到当前 router 的 on-policy 规划状态。

## 如何复用或推进 LLM-as-a-Verifier

可让 verifier 输出配置级序数分布：任务成功、成本、恢复性、安全和冗余度，而不是单一 reward。只有执行真值通过时，才把 insight 作为 teacher context；对多个配置效果后验重叠的状态保留 T。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：直接加入“路由/脚手架选择”这一层，不只蒸馏动作 token。
- **A/B/T 与序数分布**：同一任务可比较两套 Agent 配置；成本—效果不可区分时标 T。
- **硬真值门控**：用真实执行成功、预算与工具错误决定监督方向。
- **critique states**：insight 可作为 student-generated critique/memory，但写入前需回放验证。
- **高熵探索**：不要只保留当前最优配置，应保存近似 Pareto 的多个分支。
- **sealed eval**：冻结独立任务集、执行环境和成本计量，避免 router 与 insight expert 共适应。