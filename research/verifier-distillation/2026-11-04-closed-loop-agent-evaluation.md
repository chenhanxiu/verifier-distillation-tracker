# Closed-Loop Agent Evaluation: Layered Measurement and Self-Calibration

- **作者**：Ruifeng Ren, Gun Ahn
- **首次公开日期**：2026-11-04
- **版本日期**：2026-11-04（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.07051
- **DOI**：https://doi.org/10.48550/arXiv.2611.07051
- **代码**：论文页面未给出公开代码链接

## 一句话结论

该框架把 Agent 评价拆为 span、trace、conversation、engagement 四层，并要求结论追溯到原子证据与版本化规则；证据与规则式判断比 holistic score 一致性更高。

## 真正新增的内容

它显式把 biased raters、censored outcomes、provenance 与 adjudication 纳入部署期评价，并设计内循环审计 evaluator、外循环用分组件回归推动 Agent 改进。

## 核心方法

沿 Execution、Substance、Trajectory、Results 主轴分层测量，以 Conduct 作全程约束；Agent Factory 生成带领域知识包和 adapter harness 的 evaluator agent；所有指标追溯到 atomic data。

## 关键实验结果

SharpInsight 与公开对话数据案例中，evidence-and-rule judgment 相较 holistic scoring 达到更高一致性：**ICC 0.86 vs. 0.81；κ 0.81 vs. 0.63**。

## 证据质量与局限

框架覆盖完整，但论文仅 7 页，实证主要是案例研究；一致性提高不等于与真实 outcome 的有效性提高，闭环还可能让 evaluator 与 policy 共适应。

## 最接近的相关工作

最接近 AutoTuneBench、Benchmarks as Software、PaperDoctor、DENSE 与 continuous evaluator monitoring。

## 如何复用或推进 LLM-as-a-Verifier

将 generative verifier 输出拆成原子证据、规则适用性、分层 verdict 与不确定性；训练 evaluator 和 sealed evaluator 使用分离的规则版本与反馈管线。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

1. score-level OPD 同时蒸馏 span/trace/outcome 分量，避免一个总分掩盖来源。
2. A/B/T 在每层单独判断，再组合为分布。
3. critique state 必须带 provenance 与 adjudication 状态。
4. 高熵层触发局部分叉而非整轨迹重跑。
5. 内循环可校准训练 verifier，但 sealed eval 必须冻结、隔离且只向外发布汇总结果。