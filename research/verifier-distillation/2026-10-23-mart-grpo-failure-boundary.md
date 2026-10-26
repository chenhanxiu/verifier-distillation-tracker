# MART-GRPO：在失败轨迹的恢复边界停止惩罚

- **论文标题**：When to Stop Penalizing Actions? Martingale GRPO for VLA Reinforcement Learning
- **作者**：Zongyao Zhao、Cheng-Jie Zhao、Ruihang Jiang、Bing Zheng、Zhaolin Wang、Yuanwei Liu
- **首次公开日期**：2026-10-23
- **版本日期**：2026-10-23（v1）
- **原始论文**：https://arxiv.org/abs/2610.32431
- **DOI / canonical URL**：https://doi.org/10.48550/arXiv.2610.32431
- **代码**：未发现公开代码链接

## 一句话结论

MART-GRPO 证明失败轨迹不应把负 advantage 均匀传播到恢复尝试之后，并以错误/恢复事件定位停止惩罚的边界，直接推进长轨迹 verifier 的时间信用分配。

## 真正新增的内容

**论文原文结论**：作者用成功概率与 policy-score martingale 描述理想停止条件；在这些条件下，截去的梯度条件期望为零，因此可保持参考 GRPO 估计的期望并降低协方差。实践中由冻结 VLM 在完整视频中定位“最后一个可见且未恢复的错误”。

**分析推断**：这给“只惩罚责任区间”提供了理论边界，而不是依赖逐步 Judge 的直觉打分；尤其适合失败后仍含有效探索和恢复动作的 Agent 轨迹。

## 核心方法

1. 终局失败仍提供响应级负 advantage。
2. VLM 从完整 rollout 定位错误与恢复事件。
3. 只保留到最后一个未恢复错误区间的负反馈，之后动作不再受罚。
4. 成功轨迹损失和原归一化保持不变。
5. 用 martingale 分析理想与回顾式边界的偏差、方差变化。

## 关键实验结果

**论文原文结论**：OpenVLA-OFT 在 RoboTwin 2.0 多任务上均优于 full-trajectory GRPO；在相近负反馈预算下，事件引导截断优于随机/预算匹配消融。

## 证据质量与局限

有理论推导、视频事件标注和反馈预算对照，但只验证 VLA/机器人域；边界检测器由标注数据 LoRA 微调，可能错过不可见状态；回顾式使用未来信息，部署时不能直接在线应用；摘要未报告跨种子置信区间。

## 最接近的相关工作

最接近 Distill Until Divergence、STRIDE、PROSE、BATON、RLDS、γOPD 与 trajectory truncation。区别是用 martingale 条件解释何时截断不改变期望。

## 如何复用或推进 LLM-as-a-Verifier

训练 generative verifier 输出“错误起点—是否恢复—最后未恢复错误—证据指针”，并用程序状态重放核验。只有边界通过硬检查时才把终局负分传播到步骤级。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

- **score-level OPD**：负轨迹只在未恢复责任区间施加 verifier 蒸馏，恢复后的 token 保持或轻量更新。
- **A/B/T**：共享前缀的失败分支与恢复分支组成 A/B；不可观测恢复标 T。
- **真值门控**：环境状态决定“是否恢复”，视觉/语言 Judge 只提议边界。
- **critique states**：critique 必须指向可重放事件，并说明修复是否已生效。
- **探索保留**：避免把失败后的有价值恢复动作一起压低。
- **sealed eval**：用独立事件标注器与环境 oracle 评测边界精度，并单报误伤恢复动作率。
