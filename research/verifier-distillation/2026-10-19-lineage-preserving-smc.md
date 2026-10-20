# Keep the Lineages Alive: Diversity-Preserving SMC for Diffusion LLM Decoding

- **作者**：Minoo Ahmadi、Seyedarmin Azizi、Mehdi Kamal、Massoud Pedram
- **首次公开日期**：2026-10-19
- **版本日期**：2026-10-19（v1）
- **原始论文**：https://arxiv.org/abs/2610.25932
- **arXiv ID**：2610.25932
- **DOI**：https://doi.org/10.48550/arXiv.2610.25932
- **代码/项目**：未公开

## 一句话结论

证明常用 ESS 会掩盖分支谱系坍缩，并用 LP-SMC 在 verifier 引导搜索中保留低权重但可恢复的推理分支。

## 真正新增的内容

将“粒子权重均衡”与“独立谱系存活”分开测量，指出 multinomial resampling 可让 ESS 最大化却已丢失探索多样性。

## 核心方法

以 Chopthin 限制重采样后最大/最小权重比，并设置相对最大权重的输入下限，使早期低分谱系仍有恢复机会；可接内部置信度或外部过程 RM。

## 关键实验结果

两种模型、数学与代码任务中，oracle coverage 全部提升 1.8–25.6 点；同一 RM selector 下 12 个设置有 11 个提升，LLaDA-1.5 最高 +7.9，Dream-7B 最高 +18.3。

## 证据质量与局限

跨模型、跨任务且同时报告 coverage 与最终准确率；但对象是 diffusion LLM 推理时搜索，迁移到自回归 Agent/训练期分叉仍属外推。

## 最接近的相关工作

与 EPIG-Tree、belief-shift branching、DDO 及 verifier-guided beam/SMC 搜索最接近。

## 如何复用或推进 LLM-as-a-Verifier

在高熵 Agent 状态记录 ancestry ID、distinct lineage count 和环境可恢复性，不以权重 ESS 代替行为多样性；过程 verifier 仅重权，不应过早硬删。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】现有高熵分叉实验应新增 lineage survival 与 oracle coverage 指标，并给 A/B/T 中的 T 分支最低存活预算；最终选择仍由环境真值/sealed verifier 决定。

## 结论边界

除明确标注“分析推断”的段落外，上述方法与实验结论均来自论文原文或公开摘要；推断部分是面向现有研究路线的可检验假设，不应视为论文作者已经证明的结论。
