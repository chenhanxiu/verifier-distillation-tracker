# LLM-as-a-Verifier: A General-Purpose Verification Framework

> 来源：历史研究计划核心条目（2026-07-27 整理）

## 论文信息

- **标题**：LLM-as-a-Verifier: A General-Purpose Verification Framework
- **作者**：Jacky Kwok, Shulu Li, Pranav Atreya, Yuejiang Liu, Yixing Jiang, Chelsea Finn, Marco Pavone, Ion Stoica, Azalia Mirhoseini
- **首次公开/版本**：2026-07-06（v2：2026-07-07）
- **arXiv**：[2607.05391](https://arxiv.org/abs/2607.05391)
- **HTML 全文**：[arxiv.org/html/2607.05391](https://arxiv.org/html/2607.05391)

## 一句话结论

把离散 Judge 分数升级为评分 token 概率分布的期望值，是现有 Agent verifier × OPD 路线最直接的 verifier 侧基础。

## 真正新增的内容与核心方法

从评分 token logits 计算连续期望分数，并从评分粒度、重复采样、准则分解三个维度扩展验证计算；还提出更省成本的候选排序，并把连续分数用于任务进度估计与密集 RL 反馈。

## 关键实验、证据质量与局限

在 Terminal-Bench V2、SWE-Bench Verified、RoboRewardBench、MedAgentBench 上分别报告 86.5%、78.2%、87.4%、73.3%，并在机器人和数学任务展示密集反馈可提高 SAC/GRPO 样本效率。证据覆盖面强且有代码，但性能仍依赖底座模型、提示和评分 token 设计。

## 与 LLM-as-a-Verifier 及 Agent verifier × OPD 的关系

它直接提供 teacher 评分分布的读取方式。建议把期望分数、完整评分分布、criterion-wise 分布同时保存，比较单次高粒度与多次低粒度的成本/校准权衡；独立 sealed eval 应使用不同提示或不同 verifier，防止 evaluator 共适应。

## 建议定位

这篇论文应作为当前研究路线的历史基线或邻近工作保存。以上“论文方法/结果”与“对现有方案的迁移判断”已分开表述；迁移建议属于研究分析，不代表原论文已在长时程 Agent verifier 场景完成验证。
