# O²PD: Overlap-Gated On-Policy Distillation on Reliable Prefix

- **作者**：Shuaishuai Zu, Jihao Zhao, Pengfei Li, Guanghuan Fang, Ben Feng, Yuhan Liu, Biao Qin, Baochuan Yang
- **首次公开日期**：2026-11-05
- **版本日期**：2026-11-05（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.07731
- **DOI**：https://doi.org/10.48550/arXiv.2611.07731
- **代码**：论文页面未给出公开代码链接

## 一句话结论

O²PD 只在更可靠的 student 轨迹前 20% 做蒸馏，并用 teacher/student 支持集重叠动态切换支持集与 α-divergence，直接处理 teacher 在 student 后缀上越走越 off-policy 的问题。

## 真正新增的内容

论文同时回答“在哪些 token 对齐”和“如何对齐”。它不把 teacher top-k 当完整目标：提出 Teacher-support Uncovering 与 Dominant-Mode Mismatch 两类失败，并用 reset atom 汇总 top-k 外概率质量或收敛到已对齐交集。

## 核心方法

先量化 teacher 在 student 生成上下文上的可靠性，选择 rollout 前 20% 作为可靠前缀；随后计算两分布重叠度，以 overlap-gated α-divergence 在 mode-covering 与 mode-seeking 间切换，并配合 Reset Support / Support Convergence。

## 关键实验结果

**论文原文**：摘要明确给出可靠前缀为每条 rollout 的前 20%，并以理论分析刻画 top-k OPD 的两类支持集问题；摘要未披露完整 benchmark 数值，需以正文表格为准。

## 证据质量与局限

证据包含可靠性测量与分布支持的理论刻画，强于仅靠经验阈值；但固定 20% 是否能迁移到长时程 Agent、不同语言和不同 teacher 尚未由摘要证明，且“前缀可靠”不等价于环境正确。

## 最接近的相关工作

最接近 top-k reverse-KL OPD、Unified Per-Token OPD Gating、RouteOPD、TV-Regulated OPD、STRIDE 与 SCOPE。

## 如何复用或推进 LLM-as-a-Verifier

将 score-level verifier 的蒸馏区域限制在“teacher/student verdict 分布仍有足够重叠且环境状态可复现”的前缀；top-k 外质量显式保留为 reset/unknown 桶，不把未覆盖概率误当零。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

1. 用 overlap 与 prefix age 联合决定 score-level OPD 强度。
2. A/B/T 中，支持集低重叠的分叉应标 T 或送强 verifier，而非硬排序。
3. critique state 仅在可靠前缀内准入；越过首个环境不一致点后停止蒸馏。
4. 高熵状态保留 mode-covering，重叠高后再转 mode-seeking。
5. sealed eval 应按轨迹深度报告校准与支持覆盖，防止平均指标掩盖后缀失真。