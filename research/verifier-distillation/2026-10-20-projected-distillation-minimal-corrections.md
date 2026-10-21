# Projected Distillation: On Learning to Solve Hard Problems from Close, Correct Targets

- **作者**：Shripad V. Deshmukh、Christian Bock、Kangrui Ruan、Abhijeet Awasthi、Vijay Lingam、Rein Houthooft、Manish Prajapat
- **首次公开日期**：2026-10-20
- **版本日期**：2026-10-20（v1）
- **原始论文**：https://arxiv.org/abs/2610.27467
- **arXiv ID**：2610.27467
- **DOI**：https://doi.org/10.48550/arXiv.2610.27467
- **代码/项目**：未公开

## 一句话结论

把 student 失败轨迹最小编辑成正确目标，在全失败难题上取得接近 on-policy 的监督，同时减少整段 teacher 答案带来的分布外侵蚀。

## 真正新增的内容

论文把 on-policyness 视为连续量，并给出 regret 随编辑距离增长的理论刻画：最小纠正为线性 horizon，整答案替换可能为二次。

## 核心方法

从 student 失败尝试出发生成最小正确修改，用对比更新提升纠正轨迹、压低原失败轨迹，并随 student 演化持续刷新目标。

## 关键实验结果

在 Qwen3-8B 与 OLMo-2-7B、数学/代码/科学/工具使用五域上，specialization–retention AUC 对 GRPO 与 OPD 的九个格中领先八个，对 SPOT 与 SODA 领先七个。

## 证据质量与局限

理论与跨模型、跨域实验相互支持；但“最小正确编辑”仍需可靠 oracle/teacher，编辑器错误可能把近轨迹优势转成局部伪标签。

## 最接近的相关工作

与 Distill Until Divergence、STRIDE、ReDiST、TILDE recovery 及 DAgger 最接近。

## 如何复用或推进 LLM-as-a-Verifier

用环境重放验证每个最小补丁，只蒸馏从首错到恢复点的局部差分；未通过真值校验的修复进入 T，不进入 critique-state 训练。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】应加入 edit-distance 分桶，比较完整 teacher takeover、首错截断、最小修复三者对能力保持与高熵探索的影响；sealed eval 需覆盖未见失败形态。

## 结论边界

除明确标注“分析推断”的段落外，上述方法与实验结论来自论文原文或公开摘要；推断部分是面向现有研究路线的可检验假设，不应视为论文作者已经证明的结论。
