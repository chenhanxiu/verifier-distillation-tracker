# Our Own Jev: Typed Decisions in One Forward Pass, from an In-House Judge to Open LoRA Models

- **作者**：Yuchuan Weng、Chi Liu、Xin Chen、Srinivasan Manoharan
- **首次公开日期**：2026-10-21
- **版本日期**：2026-10-21（v1）
- **原始论文**：https://arxiv.org/abs/2610.29052
- **arXiv ID**：2610.29052
- **DOI**：https://doi.org/10.48550/arXiv.2610.29052
- **代码/项目**：未发现与论文对应的公开链接

## 一句话结论

把 Judge 变成一次前向计算的 typed probability distribution，可把 Agent 轨迹筛选成本降到约 frontier Judge 的 1%，但小评测与数据版本会造成两位数波动。

## 真正新增的内容

报告一个用于约 14.8 万条 agentic coding session 的内部 typed Judge，以及把同类接口复现到开放 LoRA 模型的实验；输出不是解析文本，而是固定选项的完整概率分布。

## 核心方法

冻结 backbone、训练 rank-16 LoRA，并用 pointer head 或 decoder 输出层读取固定选项概率；三个 typed questions 在一次前向中共同回答，可直接保留分布不确定性。

## 关键实验结果

1,000 个 session 约三分钟 GPU、参考成本约 0.06 美元；历史 frontier 标签在双 Judge 一致子集上仅匹配 26.9%。35B 单 seed 在 111 个 hard items 上为 79.3%，商业参考为 73.0%（未校正 p=0.12）；2B 换新版训练语料后准确率移动 11.7 点。

## 证据质量与局限

大规模生产筛选展示了吞吐价值，但公开 hard set 仅 111 项、部分结果单 seed，且 35B 在测试集可见条件下开发；不能据此声称普遍优于 frontier Judge。

## 最接近的相关工作

最接近 JEV-as-a-Judge、Rethinking Verbalized Confidence、Robust Conformal Consensus 与多 Judge 面板有效规模研究。

## 如何复用或推进 LLM-as-a-Verifier

直接将 typed probability vector 用作序数或 A/B/T 分布，而非先 argmax；用环境真值做温度校准，并只把低熵且通过 routing-lift 对照的样本用于强蒸馏。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】可把三路输出定义为 A/B/T 或“失败/不确定/成功”，作为低成本 score-level teacher；但 11.7 点语料版本漂移要求 sealed eval 锁定 checkpoint、语料版本和选项顺序，并把分布漂移单列报告。

## 结论边界

除明确标注“分析推断”的段落外，上述方法与实验结论来自论文原文或公开摘要；推断部分是面向现有研究路线的可检验假设，不应视为论文作者已经证明的结论。
