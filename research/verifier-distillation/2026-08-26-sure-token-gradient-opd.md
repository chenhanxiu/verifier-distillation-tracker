# SuRe：Sampled-Token Reverse-KL OPD 的梯度分配分析

## 基本信息

- **论文标题**：A Token-Level Analysis of Sampled-Token Reverse-KL On-Policy Distillation
- **作者**：Bing Shao、Jiazheng Zhang、Long Ma、Yujiong Shen、Senjie Jin、Xin Guo、Yuming Yang、Mingxu Chai、Zhiheng Xi、Boyang Liu、Junlin Shang、Tao Gui、Qi Zhang、Xuanjing Huang
- **首次公开日期**：2026-08-26
- **版本日期**：2026-08-27（v2；仅增加作者，科学内容不变）
- **原始论文**：[arXiv:2608.25643](https://arxiv.org/abs/2608.25643)
- **DOI**：[10.48550/arXiv.2608.25643](https://doi.org/10.48550/arXiv.2608.25643)
- **代码链接**：论文未提供公开代码仓库

## 一句话结论

论文证明 sampled-token reverse-KL OPD 的梯度天然高度集中在 student 低概率且 teacher–student 差距大的 token，并以 SuRe 进一步放大这种“惊讶 token”分配；这为高熵分叉选择提供了可解释基线，但尚未证明长轨迹中低概率 token 就是高价值步骤。

## 真正新增的内容

**论文原文结论：**

- 推导 K2 reverse-KL estimator 对 student logits 的单 token 梯度，其 L1 范数分解为 teacher–student log-prob gap 与 student softmax 因子。
- 在数学蒸馏中，低 student 概率 token 占据不成比例的梯度质量，同时更常伴随较大的 teacher–student gap。
- 提出 Surprise-aware Reweighting（SuRe）：使用 detached、bounded 权重进一步放大已有的低概率 token 分配。
- SuRe 在若干数学指标上优于 vanilla OPD，所选 OOD 指标未显示明确退化。

**分析推断：**

SuRe 更像“student surprise × teacher disagreement”的 token 采样器，而不是 verifier。迁移到 Agent 轨迹时，应把它与实际目标贡献、环境真值或反事实恢复证据做交叉门控，否则容易把罕见格式、工具参数噪声和真正关键决策混为一谈。

## 核心方法

- 对 sampled-token reverse-KL 的 K2 estimator 做解析梯度分解。
- 统计每个 token 的 student probability、teacher–student log gap 与梯度范数。
- SuRe 根据 student 对已采样 token 的低概率程度生成有界、停止梯度的权重，再乘到原 per-token reverse-KL loss 上；分母仍使用未加权 token 数。

## 关键实验结果

**论文原文结果：**

- Qwen3-1.7B：SuRe 相比 vanilla OPD，在 AMC23 avg@8 从 39.38 提至 43.12，MATH-500 avg@4 从 66.55 提至 67.65。
- Qwen3-4B：AMC23 avg@8 从 56.56 提至 58.44，MATH-500 avg@4 从 79.05 提至 79.15；AIME25 avg@8 从 17.08 降至 14.17，说明并非所有指标均提升。
- MATH-500 第二 seed 上，vanilla OPD 66.40，SuRe 67.50，与主 seed 的 66.55 vs 67.65 相近。
- 实验 teacher 为 Qwen3-8B，student 为 1.7B/4B，训练数据为 DeepMath 57K hard split。

## 证据质量与局限

**证据质量：中等。** 理论分解清楚，包含 OOD 检查和一个第二 seed；但方法增益总体较小且不一致。仅研究 sampled-token reverse-KL，未覆盖 full-vocabulary/JS divergence；任务主要是较短数学推理，未验证长时程 Agent、工具调用或 verifier score 蒸馏。

## 最接近的相关工作

- AED / SMOPD：按 entropy 选择或调整 OPD token。
- CROP：用反事实任务相关性筛选 token。
- GC-OPD：用 verifier–teacher 残差校准长上下文 OPD。
- OPDVR：用终局正确性阻断符号冲突，而 SuRe 只重分配幅度。
- TA-OPD：保留 top-k 外概率质量，关注尾部与熵漂移。

## 如何复用或推进 LLM-as-a-Verifier

- 将 SuRe 的 surprise 权重作为候选重要性，而非最终监督信号。
- 对 Agent step 同时计算：student surprise、Judge disagreement、环境状态变化、反事实贡献；至少两个信号一致才放大梯度。
- 在 score-level verifier 中，可优先蒸馏 student 低置信且 teacher 序数分布明确的样本；student/teacher 都高熵时保留探索而非强行模仿。
- 将 token 权重聚合到工具调用、参数 span、观察解释与恢复动作等语义单元。

## 对现有 Agent verifier × OPD 实验路线的具体影响

### Score-level on-policy verifier distillation

提供“按 student surprise 加权”的简单基线，但要与 teacher score entropy 和环境真值联合使用。

### Pairwise A/B/T 与序数评分分布

可优先抽取 student A/B/T 接近 Tie、而 teacher 分布明显偏向一方的样本；不能用低 token 概率直接替代序数不确定性。

### 程序化/环境真值门控

建议把 SuRe 权重乘在 OPDVR 式真值门控之后：硬真值先决定方向，surprise 只决定幅度。

### Student-generated critique states

可用 surprise 定位 student critique 中最不稳定的错误归因 span，再通过环境重放判断是否值得蒸馏。

### 高熵分叉下保留探索

这是最直接影响。低概率分叉不应一律强化；只在 teacher 低熵且可验证贡献为正时放大，其余分叉保留或置零。

### 独立 sealed eval

必须监控 avg@K、pass@K、分支熵、工具错误率和新路径覆盖，避免数学 avg 指标上升掩盖 Agent 路径收缩。