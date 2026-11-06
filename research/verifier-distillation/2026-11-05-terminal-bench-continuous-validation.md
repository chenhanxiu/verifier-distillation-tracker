# Benchmarks as Software: Terminal-Bench and the Case for Continuous Benchmarks

- **作者**：E. Kelly Buchanan, Crystal Zhou, Scott W. Linderman, Christopher Ré
- **首次公开日期**：2026-11-05
- **版本日期**：2026-11-05（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.08417
- **DOI**：https://doi.org/10.48550/arXiv.2611.08417
- **代码/数据**：论文页面未给出单独代码链接；修复以 Terminal-Bench 2.1 形式发布

## 一句话结论

Agent benchmark 会积累“维护债务”：任务、verifier 与资源预算都会过时；Terminal-Bench 连续审计发现约 30% 项目有问题，修复后准确率变化超过 10 点、名次最多移动三位。

## 真正新增的内容

论文把 benchmark 视为持续维护的软件系统，提出结合社区报告、任务 artifact、Agent trace、自动 oracle 检查和人工门控修复的 continuous-validation workflow，并把 wall-clock 等资源参数纳入 measurement specification。

## 核心方法

对 Terminal-Bench 2.0 进行全链路审计：从失败/成功轨迹反查任务与测试，执行自动 oracle 检查，再由人工决定修复；发布 2.1 并重新测量模型、harness、排名和时间预算敏感性。

## 关键实验结果

- 约 **30%** 的 benchmark 项目发现问题。
- 修复后准确率提高 **超过 10 个百分点**，leaderboard 名次最多移动 **3 位**，总体排序仍高度相关（Spearman **ρ=0.958**）。
- 延长时间限制可在 GPT-5.4 上关闭 **20pp** harness gap；在 GPT-5.4 mini 上把 **30pp** gap 缩至 **5pp**。

## 证据质量与局限

**论文原文结论**：真实高影响 benchmark 的逐项审计与修复前后重跑，证据具有工程代表性。  
**局限**：集中于 terminal/coding Agent；持续更新会引入版本可比性问题；人工门控本身也需记录一致性与盲法。

## 最接近的相关工作

最接近的是 AutoTuneBench、Harness or Model、Ground-truth-as-code、GameLogicBench，以及 benchmark contamination、test maintenance 与 evaluator audit。

## 如何复用或推进 LLM-as-a-Verifier

为 verifier 建立“测试套件 + 版本号 + 失败样本回归 + 变异测试 + 人工审批”的软件生命周期。训练 teacher 与 sealed evaluator 必须分别版本化；每次 verifier 修复都重放历史轨迹并记录 score delta。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

1. score-level OPD 实验要锁定 verifier、环境、harness 和资源预算版本，否则跨 checkpoint 曲线不可解释。
2. A/B/T 与序数分布应保留 verifier 版本维度；修复前后排序反转是高价值 T/审计样本。
3. student critique 进入训练前应通过回归测试和人工门控，避免把 benchmark bug 蒸馏进去。
4. 高熵分叉的比较必须控制时间、工具配额和重试预算。
5. sealed eval 不应“一次冻结后永不维护”，而应是独立、版本化、盲修复的连续验证系统；修复不能回写训练集而不做隔离。