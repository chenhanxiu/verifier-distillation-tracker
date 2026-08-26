# Selective Regenerative Decoding: Trajectory-Level Intervention for Inference-Time Reasoning

## 基本信息

- 作者：Sophia Xiao Pu、Yumo Xu、Sailik Sengupta、Millennium Bismay、Ruixue Lian、James Gung、Yi-an Lai、Arshit Gupta
- 首次公开日期：2026-08-25
- 版本日期：2026-08-25（v1）
- arXiv：2608.24338
- 原始论文：https://arxiv.org/abs/2608.24338
- DOI：https://doi.org/10.48550/arXiv.2608.24338
- 代码：论文公开页未提供

## 一句话结论

SRD 不再整条保留或丢弃推理轨迹，而是把候选分为 discard、keep、局部重生成三类，只重写退化后缀并保留有价值前缀，以更少 token 匹配 Best-of-N。

## 真正新增的内容

**论文原文结论：** 将 generation–reward model 对的判断用于 segment-level intervention；在温和假设下，相对 rejection sampling 获得 1.28–1.36 倍样本效率，并具有更高期望轨迹质量。

**分析推断：** discard/keep/refine 天然对应 A/B/T 或三阶序数 verifier，可用于长 Agent 轨迹的“保留、回滚、局部修复”决策，而不是二元剪枝。

## 核心方法

reward model 识别候选轨迹中仍有价值的 prefix 与退化 suffix；高质量轨迹保留，低质量轨迹丢弃，边界轨迹从退化位置重新生成。该方法不需要更大的 target model。

## 关键实验结果

在 MATH500、GPQA Diamond、HotpotQA、AlpacaEval 和多个 generation–reward model 组合上，SRD 用显著更少生成 token 达到 Best-of-N 准确率，并在低算力区间优于 speculative rejection。理论样本效率增益为 1.28–1.36 倍。

## 证据质量与局限

证据质量中等：含理论结果和四类 benchmark，但仍是推理/文本任务，不是带真实环境状态的 Agent；公开摘要未给出实际 token 节省比例、统计区间或代码。退化点依赖 reward model，若定位错误会破坏可恢复路径。

## 最接近的相关工作

最接近 DART-SD、Wrong but Useful、COTA、SafeBranch 与 process reward-guided decoding。区别是把整轨迹 selection 改为后缀级修复。

## 如何复用或推进 LLM-as-a-Verifier

训练三分类 verifier 输出 discard/keep/refine 的概率，并额外预测最早退化位置；用环境续跑验证“局部重生成是否真正改善终态”，再蒸馏成低成本在线路由器。

## 对 Agent verifier × OPD 实验路线的具体影响

- **Score-level OPD：** 只对被证实退化的 suffix 蒸馏 teacher，保护有效 student prefix。
- **A/B/T 与序数分布：** 三路决策可直接建模为有序或带动作语义的分布。
- **真值门控：** 重生成前后的环境终态差值校准退化定位。
- **Student critique states：** critique 聚焦首次退化点，并作为 refine 条件而非整轨迹总结。
- **高熵探索：** 边界轨迹进入 refine，不应立即 discard。
- **Sealed eval：** 报告误删成功路径率、恢复率和独立 reward model 结果，防止 selection–generator 共适应。
