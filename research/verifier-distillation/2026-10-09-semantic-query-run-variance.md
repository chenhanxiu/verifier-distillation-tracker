# Same Query, Different Answer: Run-to-Run Variance in Semantic Query Processing

- **作者**：Oktie Hassanzadeh；Dharmashankar Subramanian
- **首次公开日期**：2026-10-09
- **版本日期**：2026-10-09（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2610.13823
- **Canonical URL**：https://arxiv.org/abs/2610.13823
- **代码**：未发现公开代码链接

## 一句话结论

temperature=0 不能保证 LLM 判决可复现：单行算子仅有少量翻转也会被长查询计划放大到约三分之二答案变化，说明长轨迹 evaluator 必须把逐步波动传播到最终不确定性，而不能只复跑整条结果。

## 真正新增的内容

【论文原文】作者通过原 benchmark harness 重跑 SemBench、LRO-Bench 和 UDA-Bench，记录 120 万次模型调用，并建立 possible-worlds 模型解释为何逐行小概率变化会随计划暴露的行数呈指数放大。

【分析推断】这与 Agent 轨迹完全同构：每一步 Judge、工具抽取或状态判断的小波动会沿控制流累积；三 Judge 投票如果共享相同 endpoint/提示，并不能消除这种相关误差。

## 核心方法

1. 在 temperature=0 下对同一 semantic operator 多次重复执行。
2. 分别测量行级输出、查询答案和系统比较结论的变化。
3. 通过 possible-worlds 模型描述计划长度/暴露行数对波动的放大。
4. 分析 decision margin、reasoning length、模型间分歧与易变行之间的关系。
5. 比较 voting 和 calibrated cascade 对方差及覆盖保证的影响。

## 关键实验结果

【论文原文】五次执行中，单行 operator 输出变化率随模型在 0.07%–10.2% 之间，单项任务最高 24.0%；UDA-Bench 只有少量抽取值变化，却有约三分之二最终答案改变。SemBench 已发表结果中 21% 的文本结果在重跑后质量变化；LRO-Bench 的 28 项实现建议检验中有 16 项不能由原执行次数确定。投票降低但未消除方差，校准 cascade 的保证可以保持，但返回的具体行仍变化。

## 证据质量与局限

【论文原文】120 万次调用、三个 benchmark、原生 harness 和已发表结果复分析，使证据很强。  
【局限】semantic query 计划与自主 Agent 的动作—环境反馈仍有差异；temperature=0 的后端非确定性来源未必完全可见。重复执行估计的是部署时方差，不直接判断哪次输出正确。

## 最接近的相关工作

与 Black-Box Judge 测量不稳定性、All Verdicts are Not Equal、Agents Are Systems, Not Models、Who Judges Matters、Agreement Overstates Evidence、A Trust Layer for Agent Evaluation 和 Robust Conformal Consensus 最接近。

## 如何复用或推进 LLM-as-a-Verifier

将 Agent evaluator 拆成步骤级随机算子，记录每个状态抽取、rubric 判决和聚合节点的重跑分布；使用误差传播或 bootstrap 得到轨迹级区间。对于高影响、低 margin 的节点，触发环境 oracle、异构 Judge 或人工复核，而不是平均所有步骤。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：teacher score 使用重复调用后验和方差权重；单次 temperature=0 分数不得作为确定标签。
- **A/B/T 与序数分布**：重复/顺序/endpoint 变化导致等级翻转时输出 T；保留完整频率而非只取多数票。
- **程序化/环境真值门控**：高影响节点优先调用确定性工具或状态检查器，减少随机判断沿轨迹传播。
- **student-generated critique states**：critique 的证据抽取与结论分别复跑；引用对象变化时拒绝准入。
- **高熵分叉**：区分策略熵与 evaluator 方差；后者应触发重测，不能被误当成值得探索的行为分支。
- **sealed eval**：冻结调用快照仍不足，需规定重复次数、报告 run-to-run 区间，并把 harness/endpoint 波动纳入误差条。

总体判断：【分析推断】这篇论文对用户现有 pass@3/pass³ 体系有直接价值：除模型轨迹波动外，还应单独报告 Judge/operator 的重复波动及其对最终结论的放大。