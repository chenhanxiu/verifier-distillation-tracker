# Which Successes Make Good References? Action-Sequence Alignment for Multi-Turn On-Policy Distillation

- **作者**：Mufei Li、Nikki Lijing Kuang、Zhuoer Wang、Samson Koelle、Jie Yuan、Manqing Mao、Hong Wang、Yanjun Lin、James Feng、Daniel Edmiston、Pan Li、Wei Niu
- **首次公开日期**：2026-11-11
- **版本日期**：2026-11-11（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.13135
- **代码**：未发现公开代码链接
- **标识符**：arXiv:2611.13135

## 一句话结论

【论文原文】多轮 Agent OPD 不能随便拿同任务成功轨迹作 privileged reference；以动作序列 LCS 选择与失败轨迹状态路径最兼容的成功参考，才在 ALFWorld 与 τ³-bench 上稳定优于 reference-free OPD。

## 真正新增的内容

【论文原文】工作将成功参考选择表述为 free-target optimal transport：目标不是找到全局“最好”的成功轨迹，而是为每条失败轨迹匹配最兼容的成功路径。由于潜在状态不可见，作者用动作序列对齐作为可观测代理。

## 核心方法

- 为当前失败/on-policy 轨迹建立候选成功参考集合。
- 以最长公共子序列（LCS）识别共享且有序的动作骨架，同时容许可恢复的绕路。
- 将 LCS 相容度用于逐轨迹 reference assignment。
- privileged teacher 读取选定成功参考，对 student 自己的多轮轨迹提供 OPD 信号。

## 关键实验结果

【论文原文】在 ALFWorld 与 τ³-bench airline 域中，LCS 是唯一同时改善 ALFWorld 总分和 airline 三项指标的候选选择器；未进一步优化时，从 airline 训练的模型迁移到 retail 域仍改善全部三项指标。摘要未提供绝对数值或置信区间。

## 证据质量与局限

【论文原文】跨两个多轮工具环境并包含跨域迁移，直接支持“轨迹相容性”主张。但 LCS 只看动作符号顺序，可能忽略参数、观察内容和不可逆状态差异；成功参考本身也不保证局部动作适用于失败状态。

## 最接近的相关工作

最接近 STRIDE、AC-OPD、The Tasteful Agent、ReplayRCA 与 DENSE。本文相较于按最终奖励或语义相似度选参考，显式约束动作路径兼容性。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】长轨迹 verifier 可只比较共享状态骨架上的后缀，并把不兼容路径标为 T/不可比，而不是强制产生 A/B。生成式 critique 也应绑定到 LCS 对齐的决策点，避免把成功轨迹中的“正确建议”注入无法执行的状态。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：teacher reference 先经过状态/动作相容门控，再产生逐状态 score。
- **A/B/T 与序数分布**：低相容轨迹进入 T 或 abstain；高相容分叉才做 A/B。
- **程序化/环境真值**：用可执行状态和动作前置条件复核 LCS，弥补纯序列代理。
- **student-generated critique states**：critique 必须引用对齐的 observation 与可执行动作。
- **高熵分叉**：允许多个同样相容的成功参考共同保留，避免单参考模式坍缩。
- **sealed eval**：使用未参与 reference 选择的任务和环境快照，防止 selector 过拟合训练路径。