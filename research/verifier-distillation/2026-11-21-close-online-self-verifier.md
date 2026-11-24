# CLOSE: A Calibrated Label-free Online Self-Evaluating Verifier for Object Hallucination in Vision-Language Models

- **作者**：Zhaoxi Wang, Jiahao Lai
- **首次公开日期**：2026-11-21
- **版本日期**：2026-11-21（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.28589
- **DOI**：https://doi.org/10.48550/arXiv.2611.28589
- **代码**：未见作者在 arXiv 摘要页给出独立代码链接

## 一句话结论

用在线 rank/quantile memory 代替不可比的绝对概率，再融合 hidden-state pseudo-label scorer，可把无标签自验证器转成可执行的选择性生成门控。

## 真正新增的内容

**论文原文结论**：提出 label-free、online、self-evaluating verifier，以秩而非绝对概率校准跨模型阈值，并在生成中回滚、禁用被拒对象。  
**分析推断**：它为 distributional verifier 提供“相对校准 + abstention + 在线记忆”的工程模板，但不能替代外部真值。

## 核心方法

从无标签图像冷启动 quantile memory；以四种 hidden-state 信号产生伪标签，自训练 scorer，并与 self-asking 按秩融合。拒绝对象后使用 laddered back-off、ban 和 recognition table 阻止同义重现。

## 关键实验结果

模型自问可拒绝 44%–62% 的幻觉，yes probability AUROC 0.90–0.95，但仍有重叠。LLaVA-1.5-7B 拒绝 20%/40% 对象提及时 CHAIRs 降 42%/87%，F1 分别 +1.9/-6.1；Qwen3-VL-8B 拒绝 20%/35% 时可达幻觉降 79%/96%，F1 +0.5/-5.3。

## 证据质量与局限

报告覆盖两模型、多个拒绝率并显式展示质量—覆盖权衡。局限是自生成伪标签可能共适应，后半段高拒绝率以显著 F1 损失换取低幻觉，且未在长轨迹上验证。

## 最接近的相关工作

最接近 JEV-as-a-Judge 的选择性路由、Agent 轨迹可诊断性的 abstention、FARM 的分布式风险读取，以及 verbalized confidence 校准工作。

## 如何复用或推进 LLM-as-a-Verifier

将绝对 reward score 改为滚动分位数与 ordinal bins，输出 `P(A), P(B), P(T)`；不同 teacher/model family 只在 rank space 融合。高拒绝样本进入外部 oracle，而不是直接删除。

## 对 Agent verifier × OPD 实验路线的具体影响

可用 online quantile memory 校准 score-level OPD 门限，解决跨 checkpoint 分数尺度漂移；但 memory 只从训练流更新，sealed eval 必须冻结。student-generated critique 被拒时允许回滚再生成，但保留原分支用于探索与失败审计，避免“拒绝即遗忘”造成选择偏差。