# Ask to Distill: Learning to Synthesize Data for On-Policy Distillation

- **作者**：Jiashuo Sun、Hao Zhang、Xueqiang Xu、Heng Wang、Yixuan Xie、Pengcheng Jiang、Zhenrui Yue、Jiajun Fan、Peiran Li、Ge Liu、Shaowen Wang、Jiawei Han
- **首次公开日期**：2026-10-20
- **版本日期**：2026-10-20（v1）
- **原始论文**：https://arxiv.org/abs/2610.27450
- **arXiv ID**：2610.27450
- **DOI**：https://doi.org/10.48550/arXiv.2610.27450
- **代码/项目**：https://github.com/GasolSun36/Ask_to_Distill

## 一句话结论

不依赖答案或 reward，直接优化能在 student rollout 上激发高密度、可学习 teacher 信号的问题，用于构造 OPD prompt bank。

## 真正新增的内容

将训练问题视为“分布监督激发器”，并用 teacher–student 分歧、teacher 对 student 候选支撑集的概率质量以及长度/多样性共同评价问题价值。

## 核心方法

从 student 初始化问题生成器，以冻结 student–teacher 对计算分布式 surrogate reward；筛选、去重得到仅含 prompt 的数据银行，再执行标准 OPD。

## 关键实验结果

在数学、代码和 Agent 任务上，优于未优化 student 自生成问题及 KL 过滤真实问题，并在所测设置中达到或超过真实问题库 OPD；优化问题以更短回答产生更密集和更多总监督信号。

## 证据质量与局限

跨三类任务且代码、数据、模型公开；但无答案 surrogate 可能偏好“分歧大但无真实价值”的题，需用外部能力增益和 sealed task 验证。

## 最接近的相关工作

最接近 One-Shot OPD、Data-free OPD、AutoGym 与 active data selection；区别是优化问题的分布激发价值而非正确率。

## 如何复用或推进 LLM-as-a-Verifier

可让合成器专门寻找 verifier 高熵、teacher 候选仍在 student 支撑集内的 Agent 状态，再用环境真值过滤是否值得形成 A/B/T 分叉。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】现有路线应将 prompt 数量与有效状态覆盖拆开报告，并把 sealed eval 增益作为最终选择信号，避免 surrogate 与同源 teacher 共适应。

## 结论边界

除明确标注“分析推断”的段落外，上述方法与实验结论来自论文原文或公开摘要；推断部分是面向现有研究路线的可检验假设，不应视为论文作者已经证明的结论。
