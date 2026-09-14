# SCOPE-OPSD：Fisher 条件化特权子空间用于 On-Policy Self-Distillation

## 基本信息

- **论文标题**：SCOPE-OPSD: Fisher-Conditioned Privileged Subspaces for On-Policy Self-Distillation
- **作者**：Yunmeng Chen, Kunyu Wang, Peihan Li, Yi Wang, Shuyin Xia, Yi Liu, Xinyong Cheng, Dehui Wang, Xiangyong Zhai, Yanxing Liu, Song Liu
- **首次公开日期**：2026-09-11
- **版本日期**：2026-09-11（v1）
- **原始论文**：https://arxiv.org/abs/2609.12579
- **DOI**：https://doi.org/10.48550/arXiv.2609.12579
- **代码**：未发现公开代码链接

## 一句话结论

【论文原文】在标准 next-token OPSD 之外，加入由残差协方差与 LM-head Fisher 敏感度估计的冻结 rank-64 特权子空间，可在不增加 rollout 或推理模块的前提下稳定改善短预算 OPSD。

## 真正新增的内容

【论文原文】现有 OPSD 只通过条件化 self-teacher 的 token 概率传递监督；本文把 teacher–student 最终层残差投影到数据依赖、Fisher 条件化的低秩方向，形成第二条表示级蒸馏通道。随机子空间对照保持秩和非零谱一致，并按每个实验臂校准梯度 RMS，因而较好隔离“方向结构”而非辅助损失强度的贡献。

## 核心方法

1. 在 student 自生成 prefix 上运行普通 solution-conditioned OPSD。
2. 从 teacher–student 最终层残差协方差与输出头 Fisher 敏感度估计 rank-64 因子并冻结。
3. 将表示残差投影到该子空间，和 token-level OPSD 联合优化。
4. 以谱匹配随机子空间和 Pure OPSD 为控制组。

## 关键实验结果

【论文原文】在 Qwen3-1.7B、4B、8B 的 25/50/75/100 步完整轨迹上，Structured 对 Pure OPSD 的 12 个模型—检查点组合中 11 个严格提升、1 个持平；对 matched Random 在 12 个组合中胜出 10 个。1.7B 第 75 步两次独立复跑均高出 Random 1.39 个 Macro Avg@12 点；cross-fit 诊断的 held-out privileged-gap capture 为随机方向的 4.40 倍。

## 证据质量与局限

【论文原文】优点是控制组匹配几何谱与梯度尺度，并报告完整训练轨迹和重复运行。局限是只覆盖 Qwen3 三个规模、短训练预算及 rank-64 单一主设定；摘要未证明对长时程 Agent、环境交互或 sealed OOD 任务有效。

## 最接近的相关工作

Pure OPSD、privileged-information self-teacher、表示蒸馏、Fisher 加权压缩，以及 GC-OPD、DualOPSD、SuRe 和 Unified Per-Token OPD Gating。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】可把 score-level verifier 的 teacher–student 分布误差与此表示子空间联合蒸馏：输出头学习序数评分分布或 A/B/T，低秩通道保存 teacher 对 critique、约束违例和不确定性的隐含表征。程序化真值仍应决定监督方向，子空间损失只调节幅度，避免把 teacher 偏差固化。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】建议新增“token-only / score-only / token+Fisher-subspace”三臂消融，并在 student-generated critique states 与高熵分叉上分别测量收益。用环境真值门控符号、序数分布熵控制子空间权重；sealed eval 必须冻结 task、oracle、teacher 和子空间估计样本，防止 evaluator 共适应。