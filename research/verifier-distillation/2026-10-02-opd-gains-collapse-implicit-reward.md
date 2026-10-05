# Gains and Collapse in On-Policy Distillation: A Reinforcement Learning Perspective

- 作者：Han Cui、Jianhao Yan、Yun Luo、Hongbo Zhang、Zhizhang Fu、Yue Zhang
- 首次公开日期：2026-10-02
- 当前版本日期：2026-10-02（v1）
- arXiv：2610.03185
- 原始论文：https://arxiv.org/abs/2610.03185
- Canonical URL：https://doi.org/10.48550/arXiv.2610.03185
- 代码：https://github.com/HancCui/opd_hacking

## 一句话结论

【论文原文】OPD 可视为 teacher 对 student 行为施加隐式奖励：可靠偏好让正确答案更易采样，但偏好错位会放大 teacher 自己很少生成的冗长重复轨迹并导致 reward hacking。

## 真正新增的内容

【论文原文】论文把 OPD 的增益与崩塌放进同一 RL 解释：关键不只是 teacher 生成质量，而是 teacher 对 student rollout 的评价可靠性。实验还指出，OPD 提升性能不等同于扩展 student 已可解决的问题集合。

## 核心方法

【论文原文】作者比较 teacher 生成分布与其对 student 行为诱导的隐式偏好，分析何时正确响应更易被采样、何时过长重复响应获得更高隐式奖励；并测试屏蔽不健康响应与 SFT 初始化两种干预。

## 关键实验结果

【论文原文】在所测设置中，偏好与质量对齐时 OPD 提升采样到正确答案的概率；错位时出现过长和重复输出。屏蔽不健康响应与 SFT 初始化均能缓解崩塌。论文同时开源 13 组训练配置。

## 证据质量与局限

【论文原文】优点是给出统一机制解释并提供可复现实验代码。局限是“能力未扩展”的结论依赖所用可解集合与采样预算；主要证据来自推理任务，不能直接外推到真实长时程工具 Agent；屏蔽规则若由同一 evaluator 产生，仍可能共适应。

## 最接近的相关工作

最接近 PROSE 的过程奖励自强化失败、SIGNBALANCE 的伪优势、TV-Regulated OPD 的方向信号，以及 RetireOPD 的 teacher 退出条件。不同点是本文将 OPD 本身明确解释为隐式 reward optimization。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】把 teacher 的 token/score 偏好当作需要审计的 reward model：除准确率外，测量长度、重复、格式和策略族条件下的偏好翻转；将 hard verifier 决定更新方向，隐式 teacher 分数只控制幅度。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level on-policy verifier distillation**：【分析推断】新增“teacher score 是否预测环境成功”的在线校准曲线，并在失配区间停止或裁剪蒸馏。
- **pairwise A/B/T 与序数评分分布**：【分析推断】对同结果但不同长度/重复度的 A/B 对进行反事实审计；偏好不稳定时输出 T 而非强排序。
- **程序化/环境真值门控**：【分析推断】环境成功必须决定偏好方向，teacher 可在同真值层内提供细粒度排序。
- **student-generated critique states**：【分析推断】critique 也可能成为可被隐式奖励利用的“长而重复”通道，应限制其证据结构并验证修复结果。
- **高熵分叉下保留探索**：【分析推断】监控策略熵与独特解覆盖，避免 OPD 仅提高既有正确模式采样率却收缩策略支持。
- **独立 sealed eval**：【分析推断】在未暴露的长度、重复和风格扰动上测 reward soundness；训练 monitor 与评测 monitor 必须隔离。
