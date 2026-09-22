# FLARE：面向长时程 Coding Agent 的全生命周期生成式奖励模型

- 论文标题：FLARE: A Full-Lifecycle Dense Supervision Paradigm for Long-Horizon Coding Agents via Generative Reward Model
- 作者：Jingxuan Xu；Gang Wu；Yanan Wu；Yutao Mou；Songwei Yu；Tianzhuang He；Zhengshuo Gong；Zhao Liu；Zihang Xu；Wenqiang Zhu；Xinping Lei；Weihao Li；Yuhui Bai；Zhongqiu Wang；Yan Wu；Ariel Deng
- 首次公开日期：2026-09-20
- 当前版本日期：2026-09-20（v1）
- arXiv：https://arxiv.org/abs/2609.23808
- DOI：https://doi.org/10.48550/arXiv.2609.23808
- 代码：截至 v1 未见论文提供独立公开代码仓库

## 一句话结论

FLARE 从带终局执行结果的轨迹反向定位因果错误链，蒸馏轻量生成式奖励模型，再把结构化风险信号同时用于在线断点修复、SFT 数据筛选和 RL 稠密奖励，是当前最贴近“长轨迹 generative verifier × 蒸馏 × 环境真值”的完整闭环。

## 真正新增的内容

- 【论文原文】RADAR 以 causal-chain backtracking 从完整失败轨迹生成 hindsight-free 的前缀监督，避免在线 verifier 偷看未来。
- 【论文原文】将监督蒸馏成轻量 GRM；输出不是单一标量，而是因果分析、错误 taxonomy、严重度和可执行修复建议。
- 【论文原文】同一 GRM 贯穿推理、SFT 与 RL：高风险步触发局部 breakpoint re-execution，轨迹分用于筛选 SFT 数据，步骤风险用于稠密 RL 奖励。

## 核心方法

1. 在可执行 SWE 环境中收集成功与失败轨迹，以最终测试结果为硬锚。
2. RADAR 沿失败因果链回溯关键步骤，并只使用当时可见前缀生成诊断标签。
3. 蒸馏 GRM，使其从当前轨迹状态生成 issue tag、severity、证据化分析和 repair advice。
4. 推理期在风险断点局部重跑；训练期以 GRM 排序选择过程质量高的轨迹，并把逐步风险并入 RL reward。

## 关键实验结果

- 【论文原文】在四个仓库级基准（SWE-bench Verified、Pro、Multilingual、SWE-Compass）上，GRM-DBKR 的失败转成功率为 14.10%（N=1）和 19.59%（N=5），对应比 Global Rollout 提升 80.77% 和 42.78%。
- 【论文原文】单分支 FLARE 超过五分支 Global Rollout，同时把 base-agent 输出 token 降低约 5 倍；但该成本口径未计 GRM 输入输出、延迟和环境执行。
- 【论文原文】用过程分筛选 3,000 条 SFT 轨迹，四基准平均 pass rate 相对随机抽样提升 19.13%。
- 【论文原文】稠密奖励 RL 相对稀疏奖励在四基准分别提升 +2.80、+3.97、+2.67、+4.45 个百分点，平均相对提升 9.19%。

## 证据质量与局限

- 证据较强：覆盖四个真实仓库级基准，将 verifier 分别用于推理、SFT 和 RL，并给出多种对照与专家审计。
- 局限：报告的 token 节省不含 GRM 推理、环境和离线标注成本；固定错误 taxonomy 可能漏掉新型错误；基础 Agent 若缺乏语义修复能力或发生严重目标漂移，定位正确也无法挽救。
- 【分析推断】GRM、数据筛选和 RL 同处一个闭环，存在 evaluator 共适应风险；论文尚未用完全独立的 sealed evaluator 验证长期 soundness。

## 最接近的相关工作

最接近 SWE-TRACE、course-correcting SWE agents with PRMs、AgenTracer、DRACO、BATON、PaperDoctor 和 Key-Step Supervision；相比仅给标量 PRM，FLARE 更强调因果诊断、结构化 critique 和跨生命周期复用。

## 如何复用或推进 LLM-as-a-Verifier

- 将现有工具轨迹映射为“可见前缀—风险标签—证据指针—下一步修复”，蒸馏轻量 verifier，而不是直接复刻强 Judge 的整段解释。
- 以环境成功率、状态断言和工具返回值作为不可覆盖真值；GRM 负责定位与幅度，硬真值负责奖励方向。
- 把 student 自生成 critique 作为候选状态，只有在环境重放证明修复分支优于原分支后才写入 memory 或用于 OPD。

## 对现有 Agent verifier × OPD 路线的具体影响

- 【分析推断】可直接构建 score-level on-policy verifier distillation 基线：每步输出 ordinal risk distribution + issue taxonomy + critique，再以终局真值对方向门控。
- 【分析推断】在高熵状态生成多个局部 repair branch，形成 A/B/T；保留多个执行成功但策略不同的分支，避免 GRM 收缩探索。
- 【分析推断】训练 Judge/GRM 与最终评测器必须分离；sealed eval 应使用未参与 RADAR 标注的仓库、隐藏测试与固定 evaluator，专门监测“GRM 分数上升但真实 pass rate 不升”的共适应。
