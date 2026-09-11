# A Unified Per-Token Gating Family for On-Policy Distillation: FKL/RKL Mixing with Multi-Channel and Bias Coefficients

- **作者**：Suwan Wu、Yumeng Lin、Pengcheng Yuan、Xiaolong Jiang
- **首次公开日期**：2026-09-10
- **当前版本日期**：2026-09-10（v1）
- **原始论文**：https://arxiv.org/abs/2609.11768
- **DOI**：https://doi.org/10.48550/arXiv.2609.11768
- **代码**：截至记录时未发现公开代码
- **状态**：EMNLP 2026 Findings 接收

## 一句话结论

论文把逐 token 的 FKL/RKL 选择统一为一个可组合门控族；结果支持“多个不确定性通道共同决定蒸馏方式”，但现有证据主要来自短输出分类，尚不能直接证明其适用于长时程 Agent。

## 真正新增的内容

**论文原文结论**：提出 `λ_t = sigmoid(a h_t + b u(x) + c + d gap_t)`，把 token 熵、输入级不确定性、显式偏置和 teacher–student gap 放入同一坐标系；EOPD 与 ToDi 可视为其中方向对齐的一维限制。  
**分析推断**：其价值不只是“再加一个 gate”，而是提供可消融的统一参数化，可将 verifier 的置信分布、环境门控和策略熵接到同一个逐状态 OPD 控制器。

## 核心方法

在 student 自生成样本上，逐 token 混合 forward KL 与 reverse KL；门控同时接收局部熵、样本级不确定性、固定偏置及 teacher–student 分歧。作者用匹配有效 KL 强度的静态基线，尝试隔离“动态选择”本身的贡献。

## 关键实验结果

Qwen3-32B teacher 蒸馏到 Qwen3-4B，在 TweetEval emotion/hate 上，完整门控族相对匹配幅度的一维限制在 36 个可比单元中赢 33 个；对有效 KL 匹配的静态基线，26 个单元中赢 19 个。九个 headline 比较的三随机种子复验中 8/9 方向为正，但效应小于单种子估计，且 n=3 时单项均未显著。

## 证据质量与局限

作者主动声明共享训练数据、模型与参数结构使 33/36 不能当作独立显著性检验，这是可信的克制。任务仅为短输出分类，teacher/student 仅一个模型族，缺少长轨迹、可执行奖励、跨域校准与 sealed eval；因此不应把结果夸大为通用 Agent OPD 优势。

## 最接近的相关工作

EOPD、ToDi、逐 token 熵门控、teacher–student gap 门控，以及以 reverse/forward KL 调节 mode-seeking 与 coverage 的 OPD 方法。与 TV-Regulated OPD 的“方向优先”观点互补。

## 如何复用或推进 LLM-as-a-Verifier

把 `h_t` 替换或扩展为序数评分分布熵，把 `gap_t` 定义为 generative verifier 与 student critique 的分歧，并让程序化真值对 gate 施加不可覆盖的符号约束。应同时记录 gate 值、评分分布和实际执行结果，以校准软信号。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：优先做“环境真值定方向、分布式 verifier 定幅度、策略熵定是否保留探索”的四通道 gate。
- **A/B/T 与序数分布**：由同前缀分支的序数分布熵和重叠度驱动 `λ_t`，重叠大时输出 T 或减弱蒸馏。
- **critique states**：把 student-generated critique 的证据充分性作为额外通道，而非直接作为标签。
- **高熵探索**：高策略熵且 verifier 不确定时避免强 RKL 收缩；只有硬真值或稳定优势出现后再加强。
- **sealed eval**：冻结 gate 校准集、环境版本和独立 evaluator；否则 gate 与训练 verifier 可能共同适应。