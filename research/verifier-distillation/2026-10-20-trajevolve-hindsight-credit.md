# TrajEvolve: Trajectory Evolution for Reinforcement Learning with Hindsight Credit Assignment

- **作者**：Yi Wen、Hao Chen、Wanyu Wang、Maolin Wang、Pengyue Jia、Derong Xu、Huize Tan、Yingyi Zhang、Wenlin Zhang、Weihong Luo、Xiku Du、Xiangyu Zhao
- **首次公开日期**：2026-10-20
- **版本日期**：2026-10-20（v1）
- **原始论文**：https://arxiv.org/abs/2610.28060
- **arXiv ID**：2610.28060
- **DOI**：https://doi.org/10.48550/arXiv.2610.28060
- **代码/项目**：未公开

## 一句话结论

通过修复历史轨迹中的低质量步骤生成稀有高质量组合，并用反事实验证把连续信用简化成“该步骤是否完成任务所必需”的二元标签。

## 真正新增的内容

同时扩展成功轨迹支持集与步骤信用：不是只重采样整条轨迹，而是在 base model 支撑范围内进化局部步骤。

## 核心方法

选择低质量历史步骤进行替换或修复得到 evolutionary trajectories；移除/改变步骤后重新验证终局，以 necessity 二分类标签训练步骤级信用。

## 关键实验结果

论文在两个数据集上报告优于既有长时程 RL 方法；公开摘要未给出完整数值，具体收益需以正文表格复核。

## 证据质量与局限

NeurIPS 2026 接收且具有反事实 verifier 设计；但仅两个数据集、摘要缺少效应量，必要性二元化可能忽略冗余但有益的多路径策略。

## 最接近的相关工作

与 BATON、RLDS、RECAP、ToolOPD、ReTRAIL 和 EPIG-Tree 最接近。

## 如何复用或推进 LLM-as-a-Verifier

把必要性标签与 pairwise A/B/T 结合：删除步骤仍成功为 B/冗余，删除后失败为 A/关键，环境无法可靠重放则为 T；序数幅度由多次反事实成功率决定。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】可作为长轨迹步级边际贡献的程序化真值基线，但高熵分叉中不应删除所有非必要步骤，应保留替代成功路径和 lineage coverage。

## 结论边界

除明确标注“分析推断”的段落外，上述方法与实验结论来自论文原文或公开摘要；推断部分是面向现有研究路线的可检验假设，不应视为论文作者已经证明的结论。
