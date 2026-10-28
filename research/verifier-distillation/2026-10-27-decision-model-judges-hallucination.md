# Decision Models as Judges：低成本概率型 Hallucination Verifier

- **论文标题**：Decision Models as Judges for Hallucination Detection
- **作者**：Haozheng Liu, Zhaoqian Xue, Zhongyin Wang, Junting Mu, Zihui Ma, Shuya Feng, Lingyao Li
- **首次公开日期**：2026-10-27
- **版本日期**：2026-10-27（v1）
- **原始论文**：https://arxiv.org/abs/2610.37229
- **代码链接**：未在论文首页给出
- **标识**：arXiv:2610.37229；DOI: 10.48550/arXiv.2610.37229

## 一句话结论

预定义标签概率的 decision model 可在部分错误类型上以 1%–3% 成本接近生成式 Judge，但其过度自信和类型依赖要求按错误类型校准与路由。

## 真正新增的内容

**论文原文结论**：在五类 hallucination、9,852 个样本上，decision model 对上下文不一致可匹配 gpt-6-sol，对事实错误差距小于 3 点，但对逻辑与指令不一致落后 4–8 点；置信级联在三类任务上提升 1.9–3.3 点。

**分析推断**：这提供了低成本 distributional verifier teacher：输出完整标签概率，而非只给单次文本 verdict；但概率必须经类型条件校准后才能参与 OPD。

## 核心方法

构建来自六个数据集的五类二元 hallucination 基准，对比五个 decision model 与生成式 Judge；分析 balanced accuracy、概率校准、正确/错误决策分离能力，并按置信度级联多个 decision model。

## 关键实验结果

最佳 decision model 在上下文不一致上匹配 gpt-6-sol，事实错误上落后不超过 3 点，逻辑和指令不一致落后 4–8 点。级联在三类上提升 1.9–3.3 点，并以 gpt-6-sol 约 1%–3% 的成本匹配或超过它。

## 证据质量与局限

优点是样本量较大、错误类型明确并报告成本。局限是仅测试二元 hallucination，概率仍过度自信且对正确性分离有限；没有在线优化、长轨迹或对抗性策略适应实验。

## 最接近的相关工作

最接近 JEV-as-a-Judge、Our Own Jev、Rethinking Verbalized Confidence、Robust Conformal Consensus 与 UniRRM；不同点是强调预定义 verdict 概率与低成本级联。

## 如何复用或推进 LLM-as-a-Verifier

采用类型路由：轻量 decision model 先输出标签分布，低置信或其弱项（逻辑、指令不一致）再升级到 generative verifier；最终用环境证据校准温度与 abstention 阈值。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：用校准后的概率差控制蒸馏幅度，不让未经校准的高置信度决定梯度方向。
- **A/B/T 与序数分布**：后验重叠或跨模型分歧大时生成 T；可将多错误类型联合成有序风险分布。
- **程序化/环境真值门控**：事实/执行类错误优先由检索、测试或环境结算确认。
- **student-generated critique states**：decision model 负责路由，生成式模型负责解释；解释必须回指证据。
- **高熵分叉与探索**：低置信样本升级或保留多分支，不按单个 overconfident score 剪枝。
- **sealed eval**：按错误类型、模型快照和策略阶段分别校准，隐藏阈值与 holdout，报告 ECE、选择性风险及 downstream utility。