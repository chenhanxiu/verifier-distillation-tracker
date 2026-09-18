# BATON：轨迹内归因与轨迹间质量归一化

## 元数据
- **论文标题**：Dual-Axis Policy Optimization for LLM Agents: Bayesian Feedback Attribution and Trajectory Mass Normalization
- **作者**：Yingxuan Zhuang、Binhe Yu、Jingxiao Yang、Ruopei Sun、Ziting Li、Cheng Tan、Xuhong Zhang、Jianwei Yin、Jintao Chen
- **首次公开日期**：2026-09-17
- **版本日期**：2026-09-17（v1）
- **原始论文**：https://arxiv.org/abs/2609.19830
- **代码链接**：未发现公开代码链接

## 一句话结论
Agent RL 的信用分配应拆成两个独立问题：环境反馈在单条轨迹内如何归因，以及不同长度轨迹在 batch 中应占多少优化质量。

## 真正新增的内容
**论文原文结论**：BATON 将 Intra-Trajectory Feedback Attribution 与 Inter-Trajectory Objective Aggregation 明确分离，分别用 Bayesian Feedback Attribution（BFA）和 Trajectory Mass Normalization（TMN）实现；两轴各自增益独立，组合效果最好。

**分析推断**：长轨迹 verifier 不应把 step score 与 trajectory weighting 混成单一 advantage。score-level OPD 可复用 BFA 生成后验步骤分布，同时用 TMN 防止长轨迹因 token 数更多而支配更新。

## 核心方法
- BFA：根据环境反馈构造已采样动作的后验归因分布。
- TMN：让完整轨迹获得相等优化质量，避免长度导致隐式加权。
- 在 GRPO 与 GiGPO 上分别及联合加入两轴模块。

## 关键实验结果
**论文报告**：在 ALFWorld、WebShop、SearchQA 和多个模型规模上，BFA 与 TMN 均提供独立收益，组合在所有总体比较中表现最强。摘要未给绝对数值，故不推断统一提升幅度。

## 证据质量与局限
覆盖三类 Agent 环境并跨两种优化器，支持模块独立性。局限是归因后验仍依赖环境反馈质量；没有证明后验等价于真实因果贡献；缺少对不完整轨迹与不可逆副作用的专门分析。

## 最接近的相关工作
PGPO、DRACO、γOPD、Key-Step Supervision 与 Legibility is Not Interpretability 都处理步骤信用；BATON 新增轨迹内与轨迹间两轴正交化。

## 如何复用或推进 LLM-as-a-Verifier
训练 verifier 同时输出步骤归因后验和轨迹级质量；前者用于 critique/局部 A/B/T，后者用于 batch weighting。用环境重放校验高后验步骤，无法区分的质量留在 T 分布。

## 对 Agent verifier × OPD 实验路线的具体影响
- **score-level OPD**：步骤后验控制 token/动作权重，TMN 控制轨迹权重。
- **A/B/T**：从高后验决策点构造反事实分支。
- **真值门控**：终局环境反馈决定后验更新方向。
- **critique states**：在后验质量集中的首错或恢复点生成 critique。
- **高熵探索**：区分策略熵与梯度贡献不确定性。
- **sealed eval**：独立测量归因准确性和最终成功率，避免只凭训练 advantage 自证。