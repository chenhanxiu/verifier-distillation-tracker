# 从 Test-Time Scaling 理解 OPD：Illusory Distillation

## 基本信息

- **标题**：Towards Understanding On-Policy Distillation through the Lens of Test-Time Scaling
- **作者**：Xinmu Ge, Zizhuo Zhang, Yu Huang, Jianing Zhu, Lin Yuan, Wanli Gu, Weichang Wu, Weiran Huang, Xiaolu Zhang, Bo Han, Jun Zhou, Jiangchao Yao
- **首次公开/版本日期**：2026-08-12（v1）
- **arXiv**：https://arxiv.org/abs/2608.11829
- **代码**：截至记录时未发现公开仓库

## 一句话结论

OPD 的小采样预算收益主要来自把概率质量重新集中到 student 原本就能生成的正确路径，而非真正扩大可解问题集合；这要求 verifier × OPD 同时报告效率与能力边界。

## 真正新增的内容

**论文结论：** 作者跨 (K=1) 到 1024 比较 avg@K 与 pass@K，发现 OPD 在小 K 提升明显，但大 K 的 pass@K 不升反降；用 pass@1024 定义可解性时，OPD 遗忘的原可解问题多于新学会的问题。多种改进 OPD 也呈相同趋势。

**分析推断：** 现有 Agent verifier × OPD 若只看 greedy/单 rollout 成功率，可能把概率重排误判为新能力；需要把“更常选对”和“新增可行分支”分开。

## 核心方法

- 三组 student/teacher：Qwen3、Skywork、JustRL。
- 在 AMC2023、AIME2024/25/26 上从 K=1 扩展到 1024。
- avg@K 衡量采样分布的平均质量，pass@K 衡量预算下至少一次成功的可达性。
- 进一步做 problem-level solvability transition 与随机轨迹 perplexity 分析。

## 关键实验结果

**论文报告：** 标准及多个改进 OPD 在小 K 的 avg/pass 指标提升，但大 K pass@K 没有对应扩张；多数题在训练前后均可解，发生变化的题中“可解→不可解”多于“不可解→可解”。off-policy distillation 不呈现同样模式。

## 证据质量与局限

- K 扩展到 1024、三种设置和问题级迁移分析，诊断力度较强。
- 仍集中于数学推理，pass@1024 只是经验能力边界，不是证明不可解。
- 大 K 成本高，采样温度与 verifier 误差会影响结论。
- 未测试长时程 Agent、工具状态或 verifier 蒸馏。

## 最接近的相关工作

OPD、test-time scaling、pass@K/avg@K、off-policy distillation，以及关注探索支持集的 Prune/FiRe/ExOPD。

## 如何复用或推进 LLM-as-a-Verifier

对同一 Agent 状态保存多个动作/短程续跑，分别测 top-1 选择质量与“至少存在一个可验证成功分支”。student verifier 不只拟合均值，还应学习分支价值分布和可达性。

## 对 Agent verifier × OPD 路线的影响

- **Score-level OPD**：同时报告 greedy accuracy、best-of-K、分布熵和成功分支覆盖率。
- **A/B/T**：检查蒸馏后是否只是更常选择既有 A，而不是发现新的有效 B/T 分支。
- **真值门控**：用环境成功定义可达性，不以 teacher likelihood 代替。
- **Critique states**：验证 critique 是否打开原先不可达的成功分支，而不只是重排已有路径。
- **高熵探索**：这是保留探索的直接证据；必须监控原可解分支是否被蒸馏遗忘。
- **Sealed eval**：能力边界应在独立任务和 evaluator 上评估，避免训练 verifier 定义“新能力”。
