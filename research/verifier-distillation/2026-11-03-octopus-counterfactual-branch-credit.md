# Octopus: One Brain, Many Branches for Latent-KV Multi-Agent Reinforcement Learning

- **作者**：Tianming Sha
- **首次公开日期**：2026-11-03
- **版本日期**：2026-11-03（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.06956
- **DOI**：https://doi.org/10.48550/arXiv.2611.06956
- **代码**：论文页面未给出公开代码链接

## 一句话结论

Octopus 把多 Agent 分支表示为共享 KV 状态 DAG，并用 leave-one-branch-out 边际回报分配反事实分支信用，在降低 KV 成本的同时显著提升研究型 Agent。

## 真正新增的内容

系统不再把并行分支压成文本摘要或独立轨迹，而以 fork/read/wait/rewind/commit 原语保留依赖结构；DAG-GRPO 直接训练整棵分支图。

## 核心方法

Zero-Copy Radix Forking 共享前缀 KV；Attention-Only KV Mounting 读取 sibling 结果并隔离线性递归状态；Packed DAG-GRPO 用 block-sparse attention 一次训练全部分支，以移除某分支后的回报变化估计其边际信用。

## 关键实验结果

- Qwen3.5-4B 在 BrowseComp-Plus 达 **49.6%**，比 143K-context single-agent GRPO 高 **17.5 点**，比文本摘要 multi-agent RL 高 **12.5 点**。
- OpenResearcher 达 **51.2%**。
- 训练吞吐提高 **3.3×**，峰值 KV 内存降低 **2.8×**。
- off-task hijacking 从 **57.9% 降至 2.7%**，保留 92.2% full-text mutual information。

## 证据质量与局限

系统、训练与两个 benchmark 联合验证，数值完整；但 leave-one-branch-out 信用仍依赖终局 reward，可能混入分支交互效应，且目前是单作者预印本、未见代码。

## 最接近的相关工作

最接近 TSBPO、EPIG-Tree、ArenaFlow、DDO 与多 Agent tree search / branch credit。

## 如何复用或推进 LLM-as-a-Verifier

把分支 DAG 作为 verifier 的原生输入：为每条边输出边际贡献分布、证据和依赖；环境 oracle 决定总回报，生成式 verifier 仅细化分支信用。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

1. score-level OPD 可在共享前缀的 sibling 分支间蒸馏边际 score。
2. leave-one-out 分支天然构造 A/B/T，交互效应大时标 T。
3. critique state 应绑定 DAG node 与依赖证据，避免摘要污染。
4. 低成本 KV fork 允许在高熵状态保留更多探索。
5. sealed eval 必须重放完整 DAG，并检查 branch removal 的环境因果效应。