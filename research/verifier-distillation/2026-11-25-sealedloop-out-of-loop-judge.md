# SealedLoop：用闭环外独立 Judge 决定自改进策略的提交或回滚

- **论文标题**：Keep or Roll Back? Out-of-Loop Judges for Self-Improving VLA and End-to-End Embodied Policies
- **作者**：Zilin Huang, Zhengyang Wan, Kangan Qian, Zihao Sheng, Sikai Chen
- **首次公开日期**：2026-11-25
- **版本日期**：2026-11-25（v1）
- **原始论文**：https://arxiv.org/abs/2611.33794
- **DOI**：https://doi.org/10.48550/arXiv.2611.33794
- **项目页**：https://www.huang-zilin.com/SealedLoop/

## 一句话结论

SealedLoop 把 evaluator 移到自改进闭环之外，并用序贯检验控制误保留劣化策略的概率，直接给出 sealed eval 的实证模板。

## 真正新增的内容

**论文原文结论**：即使 in-loop Judge 在自己的数据上完全正确，策略改进也可能无法迁移到未见条件；框架把假增益分为 judge error 与 transfer gap。**分析推断**：现有 Agent verifier × OPD 不能用训练 Judge 的分数决定 checkpoint 晋级，必须保留不可优化的外部证据通道。

## 核心方法

训练闭环继续使用原 critic，但候选策略只有通过 sealed judge 上的序贯假设检验才被保留；测试保证以有界概率接受更差策略。相同改进循环分别由闭环内外 Judge 决策，以隔离判错和分布转移。

## 关键实验结果

LIBERO 中成功分类器把 196 个失败中的 65 个判为成功；驾驶中即使闭环 Judge 精确，仍会保留 8/15 个在未见城市退化的策略。sealed test 在已知增益对上接受 11/12 个真实提升、拒绝全部 59 个退化；最终 PDMS 为 0.674，高于闭环 critic 决策的 0.649（起点 0.638）。

## 证据质量与局限

覆盖模拟操控、自动驾驶和真实车辆，并显式控制错误接受概率，证据质量较高。局限是 sealed judge 的构造成本、独立性和长期保密性仍需工程保证；真实车辆实验仅 6 个盲配对。

## 最接近的相关工作

与 AutoTuneBench 的冻结测量、Harness or Model? 的隔离 oracle、Reality Is the Final Verifier 和 failure-driven sealed test 最接近。

## 如何复用或推进 LLM-as-a-Verifier

训练可继续使用 generative/ordinal verifier，但 checkpoint 提交只参考冻结的环境结果与独立 Judge；将 Judge 输出保留为完整序数分布，并用序贯检验而非单次均值阈值作决策。

## 对现有 Agent verifier × OPD 实验路线的具体影响

**分析建议**：把实验拆成 proposer、train verifier、sealed verifier 三套互不共享提示和数据的角色；score-level OPD 与 critique states 只能影响 proposer。高熵分叉在闭环内探索，最终晋级由 sealed 环境执行决定，并分别报告 judge error、transfer gap 和误接受上界。
